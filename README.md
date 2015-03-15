_[ResolveRef](https://github.com/pansapiens/resolveref)_ uses human-readable URLs which resemble minimal journal citations to redirect users to the requested full text journal article. It is written using the Google App Engine framework, and there is a version of running at http://resolveref.appspot.com .

Behind the scenes, _ResolveRef_ does a [PubMed](http://www.ncbi.nlm.nih.gov/pubmed/) search, extracts the [DOI](http://en.wikipedia.org/wiki/Digital_object_identifier), and (hopefully) uses this to forward the user to the requested document. 

eg, the URL:

http://resolveref.appspot.com/ref/BMC%20Bioinformatics/2007/8/487

redirects to the journal article:

    EL Willighagen, NM O'Boyle, H Gopalakrishnan, D Jiao, R Guha, C Steinbeck and D J Wild, Userscripts for the Life Sciences, BMC Bioinformatics, 2007, 8, 487.

The general form of _ResolveRef_ URLs is:

    http://resolveref.appspot.com/ref/_journal_/_year_/_volume_/_page_

or in the case where there is no volume identifier,

    http://resolveref.appspot.com/ref/_journal_/_year_/_page_
    
----
_Resolveref_ was inspried by [the proposal by Noel O'Boyle](http://baoilleach.blogspot.com/2008/01/doi-or-doh-proposal-for-restful-unique.html) for a new unique identifier for journal articles. I wrote a short blog post about the [development here](http://blog.pansapiens.com/2008/04/23/announcing-resolveref-on-google-app-engine/).
