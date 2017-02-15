from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, unquote
import threading
#import webbrowser
import requests
import datetime

def _url(path):
    return 'https://login.live.com' + path

class OnedriveClient(object):
    def __init__(self, scope, redirect_uri, client_id, client_secret):
        self.__client_id = client_id
        self.__client_secret = client_secret

        resp = self.__authenticate(self, self.__get_auth_code(scope,
            redirect_uri), redirect_uri)
        # SS: need error checking here

        self.access_token = resp[0]
        self.refresh_token = resp[1]

        self.access_token_expiry = datetime.datetime.now() + datetime.timedelta(seconds=int(resp[2]))

    def __check_access_token(self):
        if self.access_token_expiry <= datetime.datetime.now():
            resp = self.refresh_access_token(self.refresh_token)
            self.access_token = resp[0]
            self.access_token_expiry = datetime.datetime.now() + datetime.timedelta(seconds=int(resp[1]))
            # SS: need error checking here
        return True

    def __refresh_access_token(self, token):
        pass


    def __auth_code_req(self, scope, redirect_uri):
        payload = {'client_id' : self.__client_id, 
                'scope' :'wl.signin wl.offline_access onedrive.readwrite',
                'response_type' : 'code',
                'redirect_uri' : redirect_uri}
        print("Get auth code")
        return requests.get(_url('/oauth20_authorize.srf'),
                params=payload)


    def __get_auth_code(self, scope, redirect_uri):
        url_netloc = urlparse(redirect_uri).netloc
        if ':' not in url_netloc:
            host_address = url_netloc
            port = 80 # default port
        else:
            host_address, port = url_netloc.split(':')
            port = int(port)
        # Set up HTTP server and thread
        code_acquired = threading.Event()
        s = authsrv((host_address, port), code_acquired, code_req_handler)    
        th = threading.Thread(target=s.serve_forever)
        th.start()

    #    webbrowser.open(auth_url)
        # At this point the browser will open and the code
        # will be extracted by the server

        resp = self.__auth_code_req(scope, redirect_uri)
        print(resp)

        code_acquired.wait()  # First wait for the response from the auth server
        code = s.auth_code
        s.shutdown()
        th.join()
        return code

    def __auth_req(self, code, redirect_uri):
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        params = {"client_id": self.__client_id,
                "redirect_uri": redirect_uri,
                "client_secret": self.__client_secret,
                "code": code,
                "response_type": "code",
                "grant_type": "authorization_code" }
        resp = request.post(_url('/oauth20_token.srf'), 
                params=params, headers=headers)
        return resp 

    def __authenticate(self, code, redirect_uri):
        #        url_netloc = urlparse(redirect_uri).netloc
#        if ':' not in url_netloc:
#            host_address = url_netloc
#            port = 80 # default port
#        else:
#            host_address, port = url_netloc.split(':')
#            port = int(port)
        # Set up HTTP server and thread
#        authenticated = threading.Event()
#        s = authsrv((host_address, port), authenticated, req_handler)    
#        th = threading.Thread(target=s.serve_forever)
#        th.start()

    #    webbrowser.open(auth_url)
        # At this point the browser will open and the code
        # will be extracted by the server

        resp = self.__auth_req(self, code, redirect_uri, client_id, client_secret)
        print(resp)

#        authenticated.wait()  # First wait for the response from the auth server
#        s.shutdown()
#        th.join()

        return resp

class authsrv(HTTPServer, object):

    def __init__(self, server_address, stop_event, RequestHandlerClass):
        print("INIT: server addr: %s:%d" % (server_address[0],
            server_address[1]))
        HTTPServer.__init__(self, server_address, RequestHandlerClass)
        print("HTTPServer INIT")
        self.__stop_event = stop_event
        self.__auth_resp = None

    @property
    def auth_resp(self):
        return self.__auth_resp

    @auth_resp.setter
    def auth_resp(self, value):
        self.__auth_resp = value
        print(value)
        if value is not None:
            self.__stop_event.set()


class code_req_handler(BaseHTTPRequestHandler):

    def do_GET(self):
        print("Got one!\n")
        params = parse_qs(urlparse(self.path).query)
        if "code" in params:
            # Extract the code query param
            self.server.auth_resp = params["code"][0]
        if "error" in params:
            error_msg, error_desc = (unquote(params["error"][0]),
                    unquote(params["error_description"][0]))
            raise RuntimeError("The server returned an error: {} - {}"
                    .format(error_msg, error_desc))
            self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(
            '<script type="text/javascript">window.close()</script>'
            .encode("utf-8")))


        #class auth_req_handler(BaseHTTPRequestHandler):
#
#    def do_GET(self):
#        params = parse_qs(urlparse(self.path).query)
#        if "token_type" in params:
#            # Extract the code query param
#            self.server.auth_resp = params["code"][0]
#        if "error" in params:
#            error_msg, error_desc = (unquote(params["error"][0]),
#                    unquote(params["error_description"][0]))
#            raise RuntimeError("The server returned an error: {} - {}"
#                    .format(error_msg, error_desc))
#            self.send_response(200)
#        self.send_header("Content-type", "text/html")
#        self.end_headers()
#        self.wfile.write(bytes(
#            '<script type="text/javascript">window.close()</script>'
#            .encode("utf-8")))
