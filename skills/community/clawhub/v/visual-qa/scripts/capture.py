#!/usr/bin/env python3
"""
Capture screenshots using Playwright (headless Chromium).
"""

import argparse
import json
import os
import sys
import time
import subprocess
import signal
from pathlib import Path
from urllib.parse import urlparse

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("❌ Playwright not installed")
        print("\nInstall with:")
        print("  pip install playwright")
        print("  python3 -m playwright install chromium")
        sys.exit(1)

def slugify(text):
    """Convert text to URL-safe slug."""
    return text.strip('/').replace('/', '_').replace(':', '').replace('?', '').replace('&', '_').replace('=', '_') or 'index'

def capture_screenshot(page, url, viewport_name, output_dir):
    """Capture a screenshot of a URL at a specific viewport size."""
    from playwright.sync_api import sync_playwright
    
    viewports = {
        'desktop': {'width': 1280, 'height': 800},
        'tablet': {'width': 768, 'height': 1024},
        'mobile': {'width': 375, 'height': 812}
    }
    
    if viewport_name not in viewports:
        print(f"⚠️  Unknown viewport: {viewport_name}")
        return None
    
    viewport = viewports[viewport_name]
    page.set_viewport_size(viewport)
    
    try:
        # Navigate and wait for network idle
        page.goto(url, wait_until='networkidle', timeout=30000)
        
        # Additional wait for any animations/transitions
        time.sleep(0.5)
        
        # Generate filename
        parsed = urlparse(url)
        path_slug = slugify(parsed.path)
        filename = f"{path_slug}_{viewport_name}.png"
        filepath = os.path.join(output_dir, filename)
        
        # Capture screenshot
        page.screenshot(path=filepath, full_page=True)
        
        print(f"✓ {filename}")
        return filepath
    except Exception as e:
        print(f"✗ {url} ({viewport_name}): {e}")
        return None

def start_server(command, port, cwd=None):
    """Start a local development server."""
    print(f"🚀 Starting server: {command}")
    
    env = os.environ.copy()
    env['PORT'] = str(port)
    
    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=cwd,
        env=env,
        preexec_fn=os.setsid if os.name != 'nt' else None
    )
    
    # Wait for server to start
    print(f"⏳ Waiting for server on port {port}...")
    max_wait = 30
    waited = 0
    
    while waited < max_wait:
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('localhost', port))
            sock.close()
            
            if result == 0:
                print(f"✓ Server ready on port {port}")
                return process
        except:
            pass
        
        time.sleep(1)
        waited += 1
        
        # Check if process died
        if process.poll() is not None:
            stdout, stderr = process.communicate()
            print(f"❌ Server failed to start")
            print(f"stdout: {stdout.decode()}")
            print(f"stderr: {stderr.decode()}")
            return None
    
    print(f"❌ Server did not start within {max_wait}s")
    stop_server(process)
    return None

def stop_server(process):
    """Stop a server process."""
    if process is None:
        return
    
    print("🛑 Stopping server...")
    
    try:
        if os.name != 'nt':
            # Kill process group on Unix
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        else:
            # Kill process on Windows
            process.terminate()
        
        process.wait(timeout=5)
        print("✓ Server stopped")
    except:
        # Force kill if graceful shutdown failed
        try:
            if os.name != 'nt':
                os.killpg(os.getpgid(process.pid), signal.SIGKILL)
            else:
                process.kill()
        except:
            pass

def main():
    parser = argparse.ArgumentParser(
        description='Capture screenshots using Playwright',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Capture single URL
  %(prog)s http://localhost:3000 --output screenshots/

  # Capture with multiple viewports
  %(prog)s http://localhost:3000 --viewports desktop mobile tablet --output screenshots/

  # Start local server first
  %(prog)s http://localhost:3000 --server "npm run dev" --port 3000 --output screenshots/

  # Use config file
  %(prog)s --config .visual-qa.json --output screenshots/

Config file format (.visual-qa.json):
  {
    "urls": ["/", "/about", "/pricing"],
    "baseUrl": "http://localhost:3000",
    "viewports": ["desktop", "mobile"],
    "server": "npm run dev",
    "port": 3000
  }
        """
    )
    
    parser.add_argument('url', nargs='?', help='URL to capture (or use --config)')
    parser.add_argument('--config', help='Path to config JSON file')
    parser.add_argument('--output', '-o', default='screenshots', help='Output directory (default: screenshots)')
    parser.add_argument('--viewports', '-v', nargs='+', default=['desktop'], 
                       choices=['desktop', 'tablet', 'mobile'],
                       help='Viewport sizes to capture (default: desktop)')
    parser.add_argument('--server', help='Command to start local dev server')
    parser.add_argument('--port', type=int, default=3000, help='Server port (default: 3000)')
    parser.add_argument('--wait', type=int, default=5, help='Seconds to wait for server startup (default: 5)')
    
    args = parser.parse_args()
    
    # Check dependencies
    check_dependencies()
    from playwright.sync_api import sync_playwright
    
    # Load config if provided
    config = {}
    if args.config:
        try:
            with open(args.config) as f:
                config = json.load(f)
        except Exception as e:
            print(f"❌ Failed to load config: {e}")
            sys.exit(1)
    
    # Determine URLs to capture
    urls = []
    base_url = config.get('baseUrl', f'http://localhost:{args.port}')
    
    if config.get('urls'):
        # URLs from config (relative paths)
        for path in config['urls']:
            if path.startswith('http'):
                urls.append(path)
            else:
                urls.append(f"{base_url}{path if path.startswith('/') else '/' + path}")
    elif args.url:
        urls = [args.url]
    else:
        print("❌ No URL provided. Use positional argument or --config")
        parser.print_help()
        sys.exit(1)
    
    # Determine viewports
    viewports = config.get('viewports', args.viewports)
    
    # Determine output directory
    output_dir = config.get('baselineDir', args.output)
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Start server if needed
    server_process = None
    server_command = config.get('server', args.server)
    server_port = config.get('port', args.port)
    
    if server_command:
        server_process = start_server(server_command, server_port)
        if server_process is None:
            sys.exit(1)
    
    try:
        # Launch browser
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            
            print(f"\n📸 Capturing screenshots...")
            print(f"   URLs: {len(urls)}")
            print(f"   Viewports: {', '.join(viewports)}")
            print(f"   Output: {output_dir}\n")
            
            captured = 0
            failed = 0
            
            for url in urls:
                for viewport in viewports:
                    result = capture_screenshot(page, url, viewport, output_dir)
                    if result:
                        captured += 1
                    else:
                        failed += 1
            
            browser.close()
            
            print(f"\n✓ Captured {captured} screenshots")
            if failed > 0:
                print(f"✗ Failed {failed} screenshots")
    
    finally:
        # Stop server if we started it
        if server_process:
            stop_server(server_process)
    
    sys.exit(0 if failed == 0 else 1)

if __name__ == '__main__':
    main()
