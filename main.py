import os
from http.server import HTTPServer, SimpleHTTPRequestHandler, BaseHTTPRequestHandler
import cgi

UPLOAD_DIR = os.path.abspath("shared")  # Directory to store uploads

class FileServerHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/upload':
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )
            fileitem = form['file']
            if fileitem.filename:
                filepath = os.path.join(UPLOAD_DIR, os.path.basename(fileitem.filename))
                with open(filepath, 'wb') as f:
                    f.write(fileitem.file.read())
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'File uploaded successfully.')
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'No file uploaded.')
        else:
            self.send_response(404)
            self.end_headers()

    def list_directory(self, path):
        # Show upload form at the top
        html = '''
        <html><body>
        <h2>Upload File</h2>
        <form enctype="multipart/form-data" method="post" action="/upload">
        <input name="file" type="file"/>
        <input type="submit" value="Upload"/>
        </form>
        <hr>
        '''
        html += super().list_directory(path).decode()
        return html.encode()

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

os.chdir(UPLOAD_DIR)
server_address = ('', 8000)  # '' means all interfaces
httpd = HTTPServer(server_address, FileServerHandler)
print("Serving on port 8000...")
httpd.serve_forever()