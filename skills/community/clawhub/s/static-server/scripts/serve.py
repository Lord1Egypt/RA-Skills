#!/usr/bin/env python3
"""
Static HTTP server for previewing HTML files.
Usage: python serve.py <path> [--port PORT]
"""
import sys
import os
import http.server
import socketserver
from pathlib import Path

def serve(path, port=8000):
    """Start HTTP server for the given path."""
    path = Path(path).resolve()
    
    if path.is_file():
        directory = path.parent
        filename = path.name
    else:
        directory = path
        filename = "index.html"
    
    os.chdir(directory)
    
    Handler = http.server.SimpleHTTPRequestHandler
    
    with socketserver.TCPServer(("", port), Handler) as httpd:
        url = f"http://localhost:{port}/{filename}"
        print(f"Serving at {url}")
        print(f"Directory: {directory}")
        print("Press Ctrl+C to stop")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python serve.py <path> [--port PORT]")
        sys.exit(1)
    
    path = sys.argv[1]
    port = 8000
    
    if "--port" in sys.argv:
        port_idx = sys.argv.index("--port") + 1
        port = int(sys.argv[port_idx])
    
    serve(path, port)
