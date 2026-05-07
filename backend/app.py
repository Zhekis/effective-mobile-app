#!/usr/bin/env python3
"""
Простой HTTP сервер для Effective Mobile
Поддерживает GET и HEAD методы для healthcheck
"""

from http.server import HTTPServer, BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        """Обработка GET запросов"""
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.send_header('X-Health-Status', 'healthy')
            self.end_headers()
            self.wfile.write(b'Hello from Effective Mobile!')
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_HEAD(self):
        """Обработка HEAD запросов для healthcheck"""
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.send_header('X-Health-Status', 'healthy')
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        """Кастомное логирование"""
        print(f"[Backend] {self.address_string()} - {format % args}")

def run(server_class=HTTPServer, handler_class=Handler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting HTTP server on port {port}...')
    print(f'Health check endpoint: http://localhost:{port}/')
    print('Supported methods: GET, HEAD')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
