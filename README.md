PURLclient
==========

purlclient is a REST client library that allows users to programmatically create persistent URLs (PURLs) with
OCLCs service at purl.org (and any other install of the PURLZ software). 

purlclient will try to read a configuration file at ~/.purlrc in the following format: 

 [purl]
 uid=username
 password=password 
 location=purl server url 

At this time, only the resource /admin/purl is covered by this client. This means that you cannot create users
or groups from the client software. Adding such functionality should be trivial and will be done upon request. 

Links 
-----

 * [PURL REST docs](http://purlz.org/project/purl/documentation/requirements/URLs.html) 
 * [purl REST client](http://www.purlz.org/project/purl/source/src/test/org/purl/test/simplePurlClient.java?view=log&sortby=log&pathrev=251)
 