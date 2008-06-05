// ==UserScript==
// @name           ResolveRef URL for PubMed
// @namespace      com.pansapiens
// @description    Inserts ResolveRef URLs in to a PubMed abstract page
// @include        *.
// ==/UserScript==


// This part thanks to: http://www.joanpiedra.com/jquery/greasemonkey/
// and: http://colinharrington.net/blog/index.php/2008/02/15/jquery-greasemonkey-♥/
// Add jQuery
var GM_JQ = document.createElement('script');
//GM_JQ.src = 'http://jquery.com/src/jquery-latest.min.js';
GM_JQ.src = 'http://resolveref.appspot.com/js/jquery.js';
GM_JQ.type = 'text/javascript';
document.getElementsByTagName('head')[0].appendChild(GM_JQ);

// Check if jQuery's loaded
function GM_wait() {
    if(typeof unsafeWindow.jQuery == 'undefined') { window.setTimeout(GM_wait,100); }
else { $ = unsafeWindow.jQuery; letsJQuery(); }
}
GM_wait();

// All your GM code must be inside this function
function letsJQuery() {
//make sure there is no conflict between jQuery and other libraries
$.noConflict()
// First, find the PMID on the page, or via the URL
//

//var PMID = 16461275;
var PMID = location.pathname.split('/')[2];
var eutils_url = 'http://www.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id='+PMID;

//alert(eutils_url);

// based on: http://blog.reindel.com/2007/09/24/jquery-and-xml-revisited/

$.get(eutils_url, function(xml){
  //alert(xml);
  //alert( $("*").text() );
  alert( $("PubmedArticleSet > PubmedArticle > MedlineCitation > PMID", xml).text() );
});

/*
$.ajax({
type: 'GET',
url: eutils_url,
dataType: 'xml',
success: function(xml) {
//process XML in here
//
alert(xml);
},
error: function (XMLHttpRequest, textStatus, errorThrown) {
  // typically only one of textStatus or errorThrown 
  // will have info
  this; // the options for this ajax request
  alert("ajax error");
}

});//close ajax
*/

}//close letsJQuery
