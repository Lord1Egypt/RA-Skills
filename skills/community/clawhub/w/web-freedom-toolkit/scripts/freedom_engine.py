import json
import os
import sys
import time
from curl_cffi import requests as requests_cffi
from DrissionPage import ChromiumPage, ChromiumOptions
from scrapling import Fetcher

# v8.0.0 GENERAL FREEDOM ENGINE
# Harmonizing S-Mode, D-Mode, and Scrapling for total web freedom.

class FreedomEngine:
    def __init__(self):
        self.home = os.path.expanduser("~")
        self.browser_path = self._find_chrome()

    def _find_chrome(self):
        import shutil
        return shutil.which('google-chrome-stable') or os.path.join(self.home, ".pixi/bin/google-chrome-stable")

    def quick_fetch(self, url):
        """Ultra-fast stealth fetch using Scrapling (SOTA 2026)."""
        print(f"[Freedom] Executing Scrapling Stealth Fetch: {url}")
        try:
            fetcher = Fetcher(auto_match=True)
            response = fetcher.get(url)
            return {
                "status": "success",
                "mode": "scrapling",
                "title": response.title,
                "text": response.text[:2000]
            }
        except Exception as e:
            print(f"[Freedom] Scrapling failed, falling back to CFFI: {e}")
            return self.impersonate_fetch(url)

    def impersonate_fetch(self, url):
        """Kernel-level TLS impersonation using curl_cffi."""
        print(f"[Freedom] Executing CFFI Impersonation: {url}")
        try:
            r = requests_cffi.get(url, impersonate="chrome124", timeout=20)
            return {
                "status": "success",
                "mode": "cffi",
                "status_code": r.status_code,
                "text": r.text[:2000]
            }
        except Exception as e:
            return {"status": "error", "msg": str(e)}

    def deep_interact(self, url):
        """Full browser interaction (D-Mode) for complex JS/WAF."""
        print(f"[Freedom] Launching Full Browser (D-Mode): {url}")
        co = ChromiumOptions().set_argument('--no-sandbox').set_argument('--headless=new')
        if self.browser_path: co.set_browser_path(self.browser_path)
        
        try:
            page = ChromiumPage(co)
            page.get(url)
            page.wait.load_start()
            # Visual AI logic placeholder
            time.sleep(2) 
            res = {"status": "success", "mode": "browser", "title": page.title}
            page.quit()
            return res
        except Exception as e:
            return {"status": "error", "msg": str(e)}

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
    engine = FreedomEngine()
    print(json.dumps(engine.quick_fetch(target), indent=2, ensure_ascii=False))
