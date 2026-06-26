import urllib.request
import xml.etree.ElementTree as ET
import random
import os
import json

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE = os.path.join(SKILL_DIR, "config.json")
OUTPUT_FILE = os.path.join(SKILL_DIR, "data", "prepared_quotes.md")

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {"subreddits": ["r/technology"], "language": "zh-CN"}

def fetch_titles():
    config = load_config()
    sources = [f"https://www.reddit.com/{sub}/.rss" for sub in config.get("subreddits", [])]
    items = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    
    for url in sources:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                root = ET.fromstring(response.read())
                for item in root.findall('.//item'):
                    t = item.find('title').text
                    l = item.find('link').text
                    if t and l: items.append((t, l))
                for entry in root.findall('.//{http://www.w3.org/2005/Atom}entry'):
                    t = entry.find('{http://www.w3.org/2005/Atom}title').text
                    link_elem = entry.find('{http://www.w3.org/2005/Atom}link')
                    l = link_elem.get('href') if link_elem is not None else None
                    if t and l: items.append((t, l))
        except Exception:
            continue
    return items

def update_prepared_quotes():
    items = fetch_titles()
    if not items:
        return
    
    random.shuffle(items)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for title, link in items[:20]:
            f.write(f"{title}|{link}\n")

if __name__ == "__main__":
    update_prepared_quotes()
