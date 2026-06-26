#!/usr/bin/env python3
import requests, json, os, subprocess

REPORT_SITE = "https://thu-nmrc.github.io/THU-ZeeLin-Reports/"
STATE_FILE = os.path.expanduser("~/.openclaw/memory/zeelin_last_report.json")
TWEET_SCRIPT = os.path.expanduser("~/.openclaw/workspace/skills/zeelin-twitter-web-autopost/scripts/tweet.sh")

os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)

# Load state
posted = set()
if os.path.exists(STATE_FILE):
    with open(STATE_FILE) as f:
        posted = set(json.load(f).get("posted", []))

html = requests.get(REPORT_SITE, timeout=20).text

# crude extraction of report titles
import re
titles = re.findall(r'heading "([^"]+)"', html)

if not titles:
    print("No reports found")
    exit(0)

latest = titles[0]

if latest in posted:
    print("Report already posted")
    exit(0)

# Try to extract the first meaningful paragraph as summary
summary = None
m = re.search(r'<p[^>]*>([^<]{80,500})</p>', html)
if m:
    summary = m.group(1).strip()

# Try to extract a couple of bullet-style insights
bullets = []
for p in re.findall(r'<p[^>]*>([^<]{40,200})</p>', html):
    text = p.strip()
    if len(text) > 60 and len(bullets) < 2:
        bullets.append(text)

if bullets:
    summary = "\n".join(["• " + b[:120] for b in bullets])

if not summary:
    summary = "A new AI research report analyzing recent developments in AI systems and governance."

tweet = f"New AI research report released.\n\n{latest}\n\n{summary}\n\nReport:\n{REPORT_SITE}\n\n#AI #TechTwitter"

subprocess.run(["bash", TWEET_SCRIPT, tweet, "https://x.com"], check=False)

posted.add(latest)
with open(STATE_FILE, "w") as f:
    json.dump({"posted": list(posted)}, f)

print("Posted report:", latest)