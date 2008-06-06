# NOTES:
# * Modified Bio/EUtils/ThinClient to work with urlfetch

import cgi, os, re
import wsgiref.handlers

# Django templating
from google.appengine.ext.webapp import template

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.api import urlfetch

from Bio import EUtils
from Bio.EUtils import DBIdsClient, ThinClient

from xml.dom import minidom

import urllib
from urllib import unquote, unquote_plus

from journal_titles import title_list

base_url = "http://resolveref.appspot.com"

## TODO: see if it's smarter to just subclass urllib2.OpenDirector
##       and override some methods
## TODO: use StringIO.StringIO
class UrlFetch:
    """
    Instances behave like urllib2.OpenDirector objects,
    but use google.appengine.api.fetch to retrieve content.
    """
    def __init__(self):
        self.content = None

    def open(self, url):
        result = urlfetch.fetch(url)
        self.content = result.content
        return self

    def read(self, *args):
        #if args:
        #    size = args[0]
        #    out = self.content[size] 
        #    content = self.content[size:]
        #    return out

        return self.content
    
    def readline(self):
        pass


class PubRef(webapp.RequestHandler):
    
    def resolve(self, *req_path):
        """
        Takes variable number of arguments that constitute
        the request path (eg /ref/someoldjournal/1896/2/3 is
        ('ref','someoldjournal','1986','2','3') ) and queries
        PubMed to retrieve the DOI URL to forward to.

        Returns a tuple of (HTTP status code, DOI URL, ResolveRef path)
        """
        # request path is processed 'manually' here
        # req_path isn't used at all.
        # it's ugly, and I'll change it when I see the better way
        args = self.request.path.split('/')
        for a in args:
            if a == '':
                args.remove(a)
            if a == 'undefined':
                args.remove(a)
        args = args[1:] # remove the 'ref' from the start of the path
 
        kw = self.request.GET

        # deals with openref://Journal/Year/Page
        # (no volume argument)
        if len(args) == 3:
            journal, year, page = args
            query = '"%s"[TA] AND "%s"[DP] AND "%s"[PG]' % \
              (journal, year, page)
            pubref_path = "%s/%s/%s" % (journal, year, page)

        # deal with openref://Journal/Year/Volume/Page
        # (including volume number)
        elif len(args) == 4:
            journal, year, volume, page = args
            query = '"%s"[TA] AND "%s"[DP] AND "%s"[VI] AND "%s"[PG]' % \
              (journal, year, volume, page)

            pubref_path = "%s/%s/%s/%s" % (journal, year, volume, page)
        # not a valid "openref" identifier
        else:
            pubref_path = "/".join(args)
            return (pubref_path, "", 400)
        
        # TODO: figure out why the query needs to be double-unquoted
        query = unquote(unquote_plus(query))
        pubref_path = unquote(unquote_plus(pubref_path))

        #urlfetcher = UrlFetch()

        # search NCBI PubMed with EUtils
        # do-the-right-thing and specify the tool and an email for NCBI
        thinclient = ThinClient.ThinClient(tool="resolveref.appspot.com", \
                                           email="ajperry@pansapiens.com", \
                                           opener=None)
        client = DBIdsClient.DBIdsClient(eutils=thinclient)
        try:
            result = client.search(query, retmax = 1)
        except DownloadError:
            return (pubref_path, "", 503)
        try:
            res = result[0].efetch(retmode = "xml", rettype = "xml").read()
        except:
            return (pubref_path, "", 404)
        
        # get doi link from eutils XML result, example:
        #<ArticleIdList>
        #    <ArticleId IdType="pii">S0022-2836(07)01626-9</ArticleId>
        #    <ArticleId IdType="doi">10.1016/j.jmb.2007.12.021</ArticleId>
        #    <ArticleId IdType="pubmed">18187149</ArticleId>
        #</ArticleIdList>
        xml_doc = minidom.parseString(res)
        doi = None
        pmid = None
        for tag in xml_doc.getElementsByTagName("ArticleId"):
            if tag.getAttribute("IdType") == "doi":
                doi = tag.childNodes[0].data
            if tag.getAttribute("IdType") == "pubmed":
                pmid = tag.childNodes[0].data

        # make the Entrez Pubmed resolution URL
        pubmed_url =  "http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=%s&dopt=Abstract" % (pmid)
        # and lets not forget a URL to HubMed
        hubmed_url = "http://www.hubmed.org/display.cgi?uids=%s" % (pmid)

        # make the DOI resolution URL
        if doi:
            doi_url = urllib.basejoin("http://dx.doi.org/", doi)
        else:
            doi_url = hubmed_url
        
        # decide where to redirect to based on "?redirect=xxx" argument
        if kw.has_key("redirect"):
            if kw['redirect'] == "doi":
                url = doi_url
            elif kw['redirect'] == "pubmed":
                url = pubmed_url
            elif kw['redirect'] == "hubmed":
                url = hubmed_url
        else:
                url = doi_url
        
        return (pubref_path, url, 200)

    def get(self, *req_path):
        pubref_path, url, status = self.resolve(req_path)
        if status == 400:
            self.response.out.write('"%s" is not a valid ResolveRef identifier.\n' % (pubref_path) )
            self.response.set_status(status)
        elif status == 404:
            self.response.out.write('No article matching "%s" was found.\n' % (pubref_path) )
            self.response.set_status(status)
        elif status == 503:
            self.response.out.write('PubMed was temporarily unavailable when fetching "%s". Try again later\n' % (pubref_path) )
            self.response.set_status(status)
        else:
            self.redirect(url)

class Main(webapp.RequestHandler):
    def get(self):
        if users.get_current_user():
            loginout_url = users.create_logout_url(self.request.uri)
            loginout_linktext = 'Logout'
        else:
            loginout_url = users.create_login_url(self.request.uri)
            loginout_linktext = 'Login'
        
        template_values = {
         'loginout_url': loginout_url,
         'loginout_linktext': loginout_linktext,
        }

        # Django templating ...
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))


class ResolveForm(webapp.RequestHandler):
    def post(self):

        if users.get_current_user():
            user = users.get_current_user()

        journal = self.request.get('journal')
        year = self.request.get('year')
        volume = self.request.get('volume')
        page = self.request.get('page')

        if volume == '':
            self.redirect('/ref/%s/%s/%s' % (journal, year, page) )
        
        self.redirect('/ref/%s/%s/%s/%s' % (journal, year, volume, page) )

class Verify(PubRef):
    def get(self, *req_path):
        pubref_path, url, status = self.resolve(req_path)
        if status == 200:
            self.response.out.write("Valid ResolveRef URL:<br/><a href='/ref/%s'>%s/ref/%s</a><br/><br/>Redirects to:<br/><a href='%s'>%s</a>" % (pubref_path, base_url, pubref_path, url, url))
        elif status == 400:
            self.response.out.write('<em>%s</em> is not a valid ResolveRef identifier.\n' % (pubref_path) )
        elif status == 404:
            self.response.out.write('No article matching <em>%s</em> was found.\n' % (pubref_path) )


class JournalTitle(db.Model):
    title = db.StringProperty(required=True)
    first_two_letters = db.StringProperty(required=True)


class SuggestJournal(webapp.RequestHandler):
    def get(self, q=""):
        # the query string
        q = self.request.get('q')
        # example journal title list
        # in reality we use the big one in journal_titles.py
        #title_list = ["BMC Bioinformatics","Current Biology","Science","Cell","Nature", "Journal of Molecular Biology"]
        #title_list.sort()

        suggestions = []
        qregex = re.compile(q.lower())
        # Search all titles to see if they match the query
        #
        # This is probably really in efficient, since we
        # don't cache anything between calls
        #
        # Could be smarter to use title_list as a dictionary
        # keyed by two letter stubs ?
        for t in title_list:
            if qregex.match(t.lower()):
                # truncate title to 40 chars for suggestion
                #suggestions.append(t[:40])
                suggestions.append(t)
                if len(suggestions) > 19:
                    break
         
        self.response.out.write("\n".join(suggestions))

def main():
    application = webapp.WSGIApplication(
                                       [('/', Main),
                                        ('/ref/(.*)/(.*)', PubRef),
                                        ('/ref/(.*)', PubRef),
                                        ('/search', ResolveForm),
                                        ('/suggestjournal', SuggestJournal),
                                        ('/verify/(.*)', Verify),
                                        ('/verify/(.*)/(.*)', Verify)],
                                       debug=True)
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
    main()
