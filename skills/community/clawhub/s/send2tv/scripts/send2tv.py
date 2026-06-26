#!/usr/bin/env python3
"""
send2tv.py - Push text, images, or audio to Huawei Smart Screen via DLNA/UPnP

Usage:
  python3 send2tv.py "text message" [--font-size N]
  python3 send2tv.py --image /path/to/image.jpg
  python3 send2tv.py --audio /path/to/audio.mp3
  python3 send2tv.py --tts "text to speak" [--voice zh-CN-XiaoxiaoNeural]
  python3 send2tv.py --image /path/to/image.jpg --text "overlay text"

Requirements:
  - Pillow (for text rendering)
  - TV must be on same LAN, UPnP enabled
  - WenQuanYi font for Chinese text (installed at /usr/share/fonts/truetype/wqy/)
  - node-edge-tts for --tts option (npm install node-edge-tts)
"""

import subprocess
import socket
import threading
import time
import sys
import os
import re
import shutil
from PIL import Image, ImageDraw, ImageFont
import http.server
import socketserver

# TV configuration
TV_IP = "192.168.3.252"
TV_PORT = 25826
LOCAL_IP = "192.168.3.53"
HTTP_PORT = 8082

FONT_CJK = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
FONT_DEFAULT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def find_font(size, text=None):
    """Find best font for the text."""
    # Check if text contains CJK characters
    if text and re.search(r'[\u4e00-\u9fff]', text):
        if os.path.exists(FONT_CJK):
            return ImageFont.truetype(FONT_CJK, size)
    return ImageFont.truetype(FONT_DEFAULT, size)


def create_text_image(text, size=(1920, 1080), font_size=200, bg_color=(0, 0, 0), text_color=(255, 255, 255)):
    """Render text to an image, auto-sizing to fit."""
    img = Image.new('RGB', size, color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Try to find best fit font size
    font = find_font(font_size, text)
    
    # Get text bounding box
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    
    # Scale down if text too wide or tall
    scale = 1.0
    if tw > size[0] * 0.9:
        scale = size[0] * 0.9 / tw
    if th * scale > size[1] * 0.8:
        scale = min(scale, size[1] * 0.8 / th)
    
    if scale < 1.0:
        font_size = int(font_size * scale)
        font = find_font(font_size, text)
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
    
    # Center text
    x = (size[0] - tw) // 2
    y = (size[1] - th) // 2 - bbox[1]
    draw.text((x, y), text, font=font, fill=text_color)
    return img


def prepare_image(image_path, output_path="/tmp/dlna_push.jpg", max_size=(1920, 1080)):
    """Prepare image for DLNA push - convert to JPEG."""
    img = Image.open(image_path)
    
    # Convert to RGB if needed
    if img.mode not in ('RGB', 'L'):
        img = img.convert('RGB')
    
    # Resize if too large
    if img.width > max_size[0] or img.height > max_size[1]:
        img.thumbnail(max_size, Image.LANCZOS)
    
    img.save(output_path, "JPEG", quality=85)
    return output_path


class DLNAHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP handler that serves the DLNA content (image or audio)."""
    
    # Class variables to track what to serve
    serve_type = 'image'  # 'image' or 'audio'
    
    def log_message(self, format, *args): pass
    
    def do_GET(self):
        paths = {
            'image': ['/dlna_push.jpg', '/image.jpg', '/'],
            'audio': ['/dlna_push.mp3', '/audio.mp3', '/']
        }
        
        if self.serve_type == 'audio':
            # Serve audio file
            if self.path in paths['audio']:
                try:
                    audio_path = "/tmp/dlna_push.mp3"
                    with open(audio_path, 'rb') as f:
                        data = f.read()
                    self.send_response(200)
                    self.send_header('Content-Type', 'audio/mpeg')
                    self.send_header('Content-Length', str(len(data)))
                    self.send_header('Accept-Ranges', 'bytes')
                    self.end_headers()
                    self.wfile.write(data)
                    print(f"Served {len(data)} audio bytes to {self.client_address}")
                except Exception as e:
                    print(f"Error: {e}")
                    self.send_error(500)
            else:
                self.send_error(404)
        else:
            # Serve image file (original behavior)
            if self.path in paths['image']:
                try:
                    with open("/tmp/dlna_push.jpg", 'rb') as f:
                        data = f.read()
                    self.send_response(200)
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', str(len(data)))
                    self.end_headers()
                    self.wfile.write(data)
                    print(f"Served {len(data)} image bytes to {self.client_address}")
                except Exception as e:
                    print(f"Error: {e}")
                    self.send_error(500)
            else:
                self.send_error(404)

class ReuseAddrTCPServer(socketserver.TCPServer):
    allow_reuse_address = True
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        super().server_bind()

def start_server(port=HTTP_PORT):
    """Start HTTP server for DLNA push."""
    subprocess.run(["fuser", "-k", f"{port}/tcp"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(0.5)
    httpd = ReuseAddrTCPServer(("0.0.0.0", port), DLNAHandler)
    t = threading.Thread(target=httpd.serve_forever, daemon=False)
    t.daemon = False
    t.start()
    return httpd


def send_soap(action, body):
    """Send SOAP request to TV AVTransport service."""
    soap = '<?xml version="1.0" encoding="utf-8"?><s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body>' + body + '</s:Body></s:Envelope>'
    req = f"POST /upnp/service/AVTransport/Control HTTP/1.1\r\n"
    req += f"HOST: {TV_IP}:{TV_PORT}\r\n"
    req += 'Content-Type: text/xml; charset="utf-8"\r\n'
    req += f'SOAPACTION: "urn:schemas-upnp-org:service:AVTransport:1#{action}"\r\n'
    req += f"Content-Length: {len(soap)}\r\n"
    req += "Connection: close\r\n\r\n"
    req += soap
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    sock.connect((TV_IP, TV_PORT))
    sock.sendall(req.encode())
    resp = b""
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            break
        resp += chunk
    sock.close()
    return resp.decode('utf-8', errors='replace')


def stop():
    send_soap("Stop", '<u:Stop xmlns:u="urn:schemas-upnp-org:service:AVTransport:1"><InstanceID>0</InstanceID></u:Stop>')


def set_uri(url):
    body = f'<u:SetAVTransportURI xmlns:u="urn:schemas-upnp-org:service:AVTransport:1"><InstanceID>0</InstanceID><CurrentURI>{url}</CurrentURI><CurrentURIMetadata></CurrentURIMetadata></u:SetAVTransportURI>'
    return send_soap("SetAVTransportURI", body)


def play():
    body = '<u:Play xmlns:u="urn:schemas-upnp-org:service:AVTransport:1"><InstanceID>0</InstanceID><Speed>1</Speed></u:Play>'
    return send_soap("Play", body)


def push(url):
    """Push image URL to TV."""
    stop()
    time.sleep(0.3)
    r = set_uri(url)
    ok = "200 OK" in r
    if not ok:
        print(f"SetAVTransportURI failed: {r[:300]}")
    time.sleep(0.3)
    r = play()
    if not ok or "200 OK" not in r:
        print(f"Play failed: {r[:300]}")
        return False
    return True


def prepare_audio(audio_path, output_path="/tmp/dlna_push.mp3"):
    """Prepare audio file for DLNA push - convert to MP3 if needed."""
    # If already the target path, nothing to do
    if os.path.abspath(audio_path) == os.path.abspath(output_path):
        return output_path
    
    # Check if file is already mp3
    if audio_path.lower().endswith('.mp3'):
        shutil.copy(audio_path, output_path)
        return output_path
    
    # Convert to mp3 using ffmpeg if available
    if shutil.which('ffmpeg'):
        subprocess.run([
            'ffmpeg', '-y', '-i', audio_path,
            '-codec:a', 'libmp3lame', '-qscale:a', '2',
            output_path
        ], check=True, capture_output=True)
        return output_path
    
    # If no ffmpeg and not mp3, just copy and hope TV supports it
    shutil.copy(audio_path, output_path)
    return output_path


def text_to_speech(text, voice='zh-CN-XiaoxiaoNeural', rate='default', output_path='/tmp/dlna_push.mp3'):
    """Convert text to speech using edge-tts.
    
    Args:
        text: Text to convert
        voice: Voice name (default: zh-CN-XiaoxiaoNeural for Chinese)
        rate: Speech rate (e.g., '+10%', '-20%', 'default')
        output_path: Output file path
    
    Returns:
        Path to generated audio file
    """
    # Find tts-converter.js
    converter_paths = [
        '/root/.claude/skills/edge-tts/scripts/tts-converter.js',
        os.path.expanduser('~/.claude/skills/edge-tts/scripts/tts-converter.js'),
        os.path.expanduser('~/.openclaw/workspace/skills/edge-tts/scripts/tts-converter.js'),
    ]
    
    converter = None
    for p in converter_paths:
        if os.path.exists(p):
            converter = p
            break
    
    if not converter:
        raise FileNotFoundError("edge-tts skill not found. Install with: skillhub install openclaw/skills/edge-tts")
    
    cmd = ['node', converter, text, '--voice', voice, '--output', output_path]
    if rate != 'default':
        cmd.extend(['--rate', rate])
    
    print(f"Running TTS: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"TTS stderr: {result.stderr}")
        raise RuntimeError(f"TTS conversion failed: {result.stderr}")
    
    print(f"TTS stdout: {result.stdout}")
    return output_path


def main():
    text = None
    image_path = None
    audio_path = None
    tts_text = None
    tts_voice = 'zh-CN-XiaoxiaoNeural'
    tts_rate = 'default'
    font_size = 200
    
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == '--image' and i + 1 < len(args):
            image_path = args[i + 1]
            i += 2
        elif args[i] == '--audio' and i + 1 < len(args):
            audio_path = args[i + 1]
            i += 2
        elif args[i] == '--tts' and i + 1 < len(args):
            tts_text = args[i + 1]
            i += 2
        elif args[i] == '--voice' and i + 1 < len(args):
            tts_voice = args[i + 1]
            i += 2
        elif args[i] == '--rate' and i + 1 < len(args):
            tts_rate = args[i + 1]
            i += 2
        elif args[i] == '--text' and i + 1 < len(args):
            text = args[i + 1]
            i += 2
        elif args[i] == '--font-size' and i + 1 < len(args):
            font_size = int(args[i + 1])
            i += 2
        elif args[i] == '--size' and i + 1 < len(args):
            w, h = map(int, args[i + 1].split('x'))
            i += 2
        elif not args[i].startswith('--'):
            text = args[i]
            i += 1
        else:
            i += 1
    
    if not text and not image_path and not audio_path and not tts_text:
        print("Usage: send2tv.py [options]")
        print("")
        print("Image/Text mode:")
        print("  send2tv.py \"text message\" [--font-size N]")
        print("  send2tv.py --image /path/to/img.jpg [--text \"overlay\"]")
        print("")
        print("Audio mode:")
        print("  send2tv.py --audio /path/to/audio.mp3")
        print("")
        print("TTS mode (text-to-speech to TV):")
        print("  send2tv.py --tts \"要朗读的文字\" [--voice VOICE] [--rate RATE]")
        print("")
        print("Options:")
        print("  --voice VOICE    TTS voice (default: zh-CN-XiaoxiaoNeural)")
        print("  --rate RATE      TTS speed (e.g., +10%, -20%, default)")
        print("")
        print("Available Chinese voices:")
        print("  zh-CN-XiaoxiaoNeural   (female, natural, recommended)")
        print("  zh-CN-YunyangNeural    (male, natural)")
        print("  zh-CN-XiaoyiNeural     (female, sweet)")
        print("  zh-CN-YunjianNeural    (male, mature)")
        sys.exit(1)
    
    # Handle TTS mode
    if tts_text:
        print(f"Converting text to speech: {tts_text[:50]}...")
        audio_path = text_to_speech(tts_text, voice=tts_voice, rate=tts_rate)
        print(f"Audio generated: {audio_path}")
    
    # Handle audio mode
    if audio_path:
        prepare_audio(audio_path)
        print(f"Audio prepared: {os.path.getsize('/tmp/dlna_push.mp3')} bytes")
        
        # Set handler type
        DLNAHandler.serve_type = 'audio'
        
        # Start HTTP server
        httpd = start_server(HTTP_PORT)
        print(f"HTTP server on port {HTTP_PORT}")
        time.sleep(0.5)
        
        # Push to TV
        url = f"http://{LOCAL_IP}:{HTTP_PORT}/dlna_push.mp3"
        print(f"Pushing audio to TV: {url}")
        
        if push(url):
            print("Audio push successful!")
        else:
            print("Audio push failed!")
            sys.exit(1)
        
        # Keep server alive for TV to download
        print("Keeping server alive for 60s...")
        time.sleep(60)
        return
    
    # Handle image mode (original behavior)
    if image_path:
        prepare_image(image_path)
        print(f"Image prepared: {os.path.getsize('/tmp/dlna_push.jpg')} bytes")
    else:
        img = create_text_image(text, font_size=font_size)
        img.save("/tmp/dlna_push.jpg", "JPEG", quality=90)
        print(f"Text image rendered: {os.path.getsize('/tmp/dlna_push.jpg')} bytes")
    
    # Set handler type
    DLNAHandler.serve_type = 'image'
    
    # Start HTTP server
    httpd = start_server(HTTP_PORT)
    print(f"HTTP server on port {HTTP_PORT}")
    time.sleep(0.5)
    
    # Push to TV
    url = f"http://{LOCAL_IP}:{HTTP_PORT}/dlna_push.jpg"
    print(f"Pushing to TV: {url}")
    
    if push(url):
        print("Push successful!")
    else:
        print("Push failed!")
        sys.exit(1)
    
    # Keep server alive for TV to download
    print("Keeping server alive for 30s...")
    time.sleep(30)


if __name__ == "__main__":
    main()
