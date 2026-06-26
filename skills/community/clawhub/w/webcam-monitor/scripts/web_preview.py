#!/usr/bin/env python3.10
"""
Web-based Live Preview for Webcam
Streams to http://localhost:8080
"""

import cv2
import numpy as np
import time
from datetime import datetime
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import io

SNAPSHOT_DIR = Path.home() / ".openclaw" / "workspace" / "camera" / "snapshots"
DEVICE_ID = 0

class CameraStream:
    def __init__(self):
        self.cap = None
        self.frame = None
        self.running = False
        self.lock = threading.Lock()
        
    def start(self):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting camera stream...")
        self.cap = cv2.VideoCapture(DEVICE_ID)
        if not self.cap.isOpened():
            print("ERROR: Could not open camera!")
            return False
        
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        time.sleep(2)
        
        self.running = True
        threading.Thread(target=self._capture_loop, daemon=True).start()
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Camera started: 1280x720")
        return True
    
    def _capture_loop(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                with self.lock:
                    self.frame = frame
            time.sleep(0.033)
    
    def get_frame(self):
        with self.lock:
            return self.frame.copy() if self.frame is not None else None
    
    def save_snapshot(self, frame):
        SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = SNAPSHOT_DIR / f"snapshot_{timestamp}.jpg"
        cv2.imwrite(str(filename), frame)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Snapshot saved: {filename.name}")
        return filename
    
    def stop(self):
        self.running = False
        if self.cap:
            self.cap.release()
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Camera stopped")

camera = CameraStream()

HTML_PAGE = '''<!DOCTYPE html>
<html>
<head>
    <title>Camera Live Preview</title>
    <style>
        body { font-family: sans-serif; text-align: center; background: #1a1a1a; color: #fff; margin: 0; padding: 20px; }
        h1 { margin-bottom: 10px; }
        .status { color: #4CAF50; margin-bottom: 20px; }
        #stream { max-width: 100%; border: 2px solid #333; border-radius: 8px; }
        .controls { margin-top: 20px; }
        button { padding: 12px 24px; font-size: 16px; cursor: pointer; background: #4CAF50; color: white; border: none; border-radius: 4px; margin: 5px; }
        button:hover { background: #45a049; }
        #message { margin-top: 10px; color: #4CAF50; min-height: 24px; }
    </style>
</head>
<body>
    <h1>Live Camera Preview</h1>
    <div class="status">Live</div>
    <img id="stream" src="/stream" alt="Camera Stream">
    <div class="controls">
        <button onclick="takeSnapshot()">Take Snapshot</button>
        <button onclick="location.reload()">Refresh</button>
    </div>
    <div id="message"></div>
    <script>
        function takeSnapshot() {
            fetch('/snapshot').then(r => r.text()).then(msg => {
                document.getElementById('message').textContent = msg;
                setTimeout(() => document.getElementById('message').textContent = '', 3000);
            });
        }
    </script>
</body>
</html>'''

class StreamHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self._serve_html()
        elif self.path == '/stream':
            self._serve_stream()
        elif self.path == '/snapshot':
            self._take_snapshot()
        else:
            self.send_error(404)
    
    def _serve_html(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(HTML_PAGE.encode())
    
    def _serve_stream(self):
        self.send_response(200)
        self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=frame')
        self.end_headers()
        
        while camera.running:
            frame = camera.get_frame()
            if frame is not None:
                _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
                self.wfile.write(b'--frame\r\n')
                self.send_header('Content-Type', 'image/jpeg')
                self.send_header('Content-Length', len(buffer))
                self.end_headers()
                self.wfile.write(buffer.tobytes())
                self.wfile.write(b'\r\n')
            time.sleep(0.033)
    
    def _take_snapshot(self):
        frame = camera.get_frame()
        if frame is not None:
            filename = camera.save_snapshot(frame)
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(f"Snapshot saved: {filename.name}".encode())
        else:
            self.send_error(503, "No frame available")
    
    def log_message(self, format, *args):
        pass

def main():
    if not camera.start():
        print("Failed to start camera")
        return 1
    
    server = HTTPServer(('0.0.0.0', 8081), StreamHandler)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Server started: http://localhost:8081")
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Press Ctrl+C to stop")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        camera.stop()
        server.shutdown()
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Server stopped")
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())