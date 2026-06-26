
---

**File 2: Inside `soul-md`, create a folder called `scripts`, then create `fetch_latest.py` with this content:**

```python
#!/usr/bin/env python3
import sys, json, urllib.request, xml.etree.ElementTree as ET, re
from datetime import datetime
from pathlib import Path

RSS_URL = "https://buttondown.com/soulmd/rss"
SUBSCRIBE_URL = "https://buttondown.com/soulmd"
STATE_FILE = Path.home() / ".openclaw" / "soul-md-state.json"

def fetch_rss():
    req = urllib.request.Request(RSS_URL, headers={"User-Agent": "soul-md-skill/1.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.read()

def parse_latest(xml_bytes):
    root = ET.fromstring(xml_bytes)
    item = root.find("channel/item")
    if item is None:
        return None
    plain = re.sub(r"<[^>]+>", "", item.findtext("description", ""))[:600].strip()
    return {"title": item.findtext("title","").strip(), "link": item.findtext("link","").strip(), "date": item.findtext("pubDate","").strip(), "excerpt": plain}

def load_state():
    return json.loads(STATE_FILE.read_text()) if STATE_FILE.exists() else {}

def save_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state))

def main():
    check_new = "--check-new" in sys.argv
    try:
        latest = parse_latest(fetch_rss())
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr); sys.exit(1)
    if not latest:
        print("No editions found."); sys.exit(0)
    if check_new:
        state = load_state()
        if latest["link"] == state.get("last_seen_link",""):
            print("NO_NEW_EDITION"); sys.exit(0)
        save_state({"last_seen_link": latest["link"], "last_checked": datetime.utcnow().isoformat()})
    print(f"TITLE: {latest['title']}