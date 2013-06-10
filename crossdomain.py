'''
    Description:
        This is a middleware class that will allow crossdomain XHR when using HTML5 post 
        methods.  This is to manipulate the headers to append the permission needed.  Without
        this class, you would get a 405 method not allowed error.
        
        Access-Control-Allow-Origin: *
        Access-Control-Allow-Methods: POST, GET, OPTIONS, PUT, DELETE
        
        Referenced from: https://gist.github.com/426829
        
    How to implement:
        1 - Make a folder called "middleware" and create a file called "crossdomain.py" (this file)
        2 - Add "__init__.py" file under middleware so django can understand it is a module.
        3 - Add "[YOUR_PROJECT_PATH_TO_MIDDLEWARE].middleware.crossdomain.XsSharing" in MIDDLEWARE_CLASSES 
            section of settings
'''

from django import http
try:
    from django.conf import settings
    ''' Set headers from settings '''
    XS_SHARING_ALLOWED_ORIGINS = settings.XS_SHARING_ALLOWED_ORIGINS
    XS_SHARING_ALLOWED_METHODS = settings.XS_SHARING_ALLOWED_METHODS
    XS_SHARING_ALLOWED_HEADERS = settings.XS_SHARING_ALLOWED_HEADERS
    XS_SHARING_ALLOWED_CREDENTIALS = settings.XS_SHARING_ALLOWED_CREDENTIALS
except AttributeError:
    ''' Set headers if settings not found '''
    XS_SHARING_ALLOWED_ORIGINS = '*'
    XS_SHARING_ALLOWED_METHODS = ['POST', 'GET', 'OPTIONS', 'PUT', 'DELETE']  
    XS_SHARING_ALLOWED_HEADERS = ['Content-Type', '*']
    XS_SHARING_ALLOWED_CREDENTIALS = 'true'
 
class XsSharing(object):

    def process_request(self, request):
        if 'HTTP_ACCESS_CONTROL_REQUEST_METHOD' in request.META:
            response = http.HttpResponse()
            response['Access-Control-Allow-Origin']  = XS_SHARING_ALLOWED_ORIGINS 
            response['Access-Control-Allow-Methods'] = ",".join( XS_SHARING_ALLOWED_METHODS ) 
            response['Access-Control-Allow-Headers'] = ",".join( XS_SHARING_ALLOWED_HEADERS )
            response['Access-Control-Allow-Credentials'] = XS_SHARING_ALLOWED_CREDENTIALS
            return response
        return None
 
    def process_response(self, request, response):
        response['Access-Control-Allow-Origin']  = XS_SHARING_ALLOWED_ORIGINS 
        response['Access-Control-Allow-Methods'] = ",".join( XS_SHARING_ALLOWED_METHODS )
        response['Access-Control-Allow-Headers'] = ",".join( XS_SHARING_ALLOWED_HEADERS )
        response['Access-Control-Allow-Credentials'] = XS_SHARING_ALLOWED_CREDENTIALS
        return response