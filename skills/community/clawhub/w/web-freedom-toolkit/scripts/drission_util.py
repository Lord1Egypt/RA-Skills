import os
import shutil
from DrissionPage import ChromiumPage, ChromiumOptions

def get_browser_path():
    """SOTA dynamic browser detection."""
    # 1. Check system path
    path = shutil.which('google-chrome-stable') or shutil.which('google-chrome')
    if path: return path
    
    # 2. Check common user sandbox paths
    home = os.path.expanduser("~")
    user_paths = [
        os.path.join(home, ".pixi/bin/google-chrome-stable"),
        "/usr/bin/google-chrome-stable"
    ]
    for p in user_paths:
        if os.path.exists(p): return p
    return None

def get_drission_page(headless=True):
    co = ChromiumOptions()
    co.set_argument('--no-sandbox')
    if headless: co.set_argument('--headless=new')
    
    path = get_browser_path()
    if path: co.set_browser_path(path)
    
    # Force IPv4 to avoid handshake 404 ghost
    co.set_address('127.0.0.1:9222')
    return ChromiumPage(co)
