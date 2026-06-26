from __future__ import annotations
import argparse, os, re, sys, requests
from html import unescape
try:
    from dotenv import load_dotenv; load_dotenv()
except ImportError:
    pass
try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False

def clean(text):
    text = unescape(text or "")
    text = re.sub(r"<script\b[^>]*>.*?</script>", " ", text, flags=re.I|re.S)
    text = re.sub(r"<style\b[^>]*>.*?</style>",  " ", text, flags=re.I|re.S)
    return re.sub(r"\s+", " ", text).strip()

def main():
    p = argparse.ArgumentParser()
    p.add_argument("url")
    p.add_argument("--searxng-url", default=None)  # accepted for consistency
    p.add_argument("--max-chars", type=int, default=5000)
    args = p.parse_args()

    timeout = int(os.environ.get("SEARXNG_TIMEOUT", "20"))
    r = requests.get(args.url, timeout=timeout,
                     headers={"User-Agent": "wsearch-fetch/1.0"})
    r.raise_for_status()
    ct = (r.headers.get("content-type") or "").lower()
    if HAS_BS4 and ("text/html" in ct or "<html" in r.text[:500].lower()):
        text = clean(BeautifulSoup(r.text, "lxml").get_text("\n"))
    else:
        text = r.text.strip()
    print(text[:args.max_chars])

if __name__ == "__main__":
    main()
