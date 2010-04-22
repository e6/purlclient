__version__ = '0.1'
__description__ = 'Client software for PURL.'
__long_description__ = \
'''

'''

__license__ = 'BSD'

import os, urllib, urllib2, cookielib
import logging
import ConfigParser, os


logger = logging.getLogger('purl')

class PURL(object):
    
    INI_PATH = '~/.purlrc'
    INI_SECTION = 'purl'
    INI_LOCATION = 'location'
    INI_UID = 'uid'
    INI_PASSWORD = 'password'
    INI_DOMAIN = 'domain'
    
    def __init__(self, location=None, uid=None, password=None):
        config = ConfigParser.ConfigParser({self.INI_LOCATION: 'http://purl.org/admin/'})
        config.read([os.path.expanduser(self.INI_PATH)])
        
        if location is None:
            location = config.get(self.INI_SECTION, self.INI_LOCATION)
        self.base_location = location
        if uid is None:
            uid = config.get(self.INI_SECTION, self.INI_UID)
        if password is None:
            password = config.get(self.INI_SECTION, self.INI_PASSWORD)
        self.uid = uid
        
        if uid and password:
            self.cj = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
            urllib2.install_opener(opener)
            self._login(uid, password)
    
    
    def reset(self):
        self.last_status = None
        self.last_body = None
        self.last_headers = None
        self.last_http_error = None
        self.last_url_error = None

    def open_url(self, location, data=None, headers={}, method=None):
        try:
            if data != None:
                data = urllib.urlencode(data) 
            req = Request(location, data, headers, method=method)
            print req.headers
            self.url_response = urllib2.urlopen(req)
        except urllib2.HTTPError, inst:
            print "purl: Received HTTP error code from PURL."
            print "purl: location: %s" % location
            print "purl: response code: %s" % inst.fp.code
            print "purl: response: %s" % inst.fp.read()
            print "purl: request data: %s" % data
            self.last_http_error = inst
            self.last_status = inst.code
        except urllib2.URLError, inst:
            self.last_url_error = inst
            self.last_status,self.last_body = inst.reason
        else:
            print "purl: OK opening PURL: %s" % location
            self.last_status = self.url_response.code
            self.last_body = self.url_response.read()
            self.last_headers = self.url_response.headers
    
    def get_location(self, resource_name="purl/", domain=None, path=None):
        loc = self.base_location
        loc += resource_name
        if domain is not None:
            loc += domain + "/"
        if path is not None:
            loc += path
        return loc
        
    def _login(self, uid, password):
        url = self.get_location(resource_name='login/', path='login-submit.bsh')
        self.open_url(url, data={'id': uid, 'passwd': password}, method='POST')
        

    def create(self, path, target, _type=302, maintainers=None, domain=None, seealso=None):
        self.reset()
        url = self.get_location(domain=domain, path=path)
        if maintainers is None:
            maintainers = self.uid
        data={'target': target, 'type': _type, 'maintainers': maintainers}
        if seealso is not None:
            data['seealso'] = seealso
        self.open_url(url, data=data, method='POST')

    def read(self, path, domain=None):
        self.reset()
        url = self.get_location(domain=domain, path=path)
        self.open_url(url)
        return self.last_body

    def update(self, path, target=None, _type=302, maintainers=None, domain=None, seealso=None):
        self.reset()
        url = self.get_location(domain=domain, path=path)
        data={}
        if target is not None: 
            data['target'] = target
        if _type is not None:
            data['type'] = _type
        if maintainers is not None:
            data['maintainers'] = maintainers
        if seealso is not None:
            data['seealso'] = seealso
        self.open_url(url, data=data, method='PUT')

    def delete(self, path, domain=None):
        self.reset()
        url = self.get_location(domain=domain, path=path)
        self.open_url(url, method='DELETE')


class Request(urllib2.Request):
    def __init__(self, url, data=None, headers={}, method=None):
        urllib2.Request.__init__(self, url, data, headers)
        self._method = method
        
    def get_method(self):
        if self.has_data():
            if not self._method:
                return 'POST'
            assert self._method in ('POST', 'PUT'), 'Invalid method "%s" for request with data.' % self._method
            return self._method
        else:
            if not self._method:
                return 'GET'
            assert self._method in ('GET', 'DELETE'), 'Invalid method "%s" for request without data.' % self._method
            return self._method
            
                
