#!/usr/bin/env python3
"""Servidor local do SIGAE.

Abre em http://localhost:5173/  (serve o index.html do projeto)

    python3 serve.py            # porta 5173
    PORTA=8080 python3 serve.py # outra porta
"""
import http.server, os, socketserver

PORTA = int(os.environ.get("PORTA", "5173"))


class H(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", ""):
            self.send_response(302)
            self.send_header("Location", "/index.html")
            self.end_headers()
            return
        return super().do_GET()

    def end_headers(self):
        # evita cache durante o desenvolvimento
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, *a):
        pass


socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("0.0.0.0", PORTA), H) as s:
    print(f"SIGAE em http://localhost:{PORTA}/  (Ctrl+C para parar)")
    s.serve_forever()
