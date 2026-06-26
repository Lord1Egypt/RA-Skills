---
name: recall-local
description: Local memory search for OpenClaw agents. Runs a lightweight Node.js server that indexes all files in ~/clawd/memory/ plus MEMORY.md and WORKING.md, then exposes keyword search over them. Use when you need to find something from past sessions, daily logs, decisions made, things learned, bugs fixed, or anything in the agent's history. Also use to set up, check, or restart the server.
---

# Recall Local

Indexes your entire `~/clawd/memory/` archive and serves it as a searchable web UI + API at `http://localhost:3456`. No external services, no API keys, nothing leaves your machine.

## Setup (first time)

```bash
# Copy the server to your tools directory
mkdir -p ~/clawd/tools/recall-local
cp "$(dirname "$0")/scripts/server.js" ~/clawd/tools/recall-local/server.js

# Create a LaunchAgent so it starts on login
cat > ~/Library/LaunchAgents/ai.wren.recall-local.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>ai.wren.recall-local</string>
  <key>ProgramArguments</key>
  <array>
    <string>/opt/homebrew/bin/node</string>
    <string>/Users/YOUR_USERNAME/clawd/tools/recall-local/server.js</string>
  </array>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><true/>
  <key>StandardOutPath</key><string>/Users/YOUR_USERNAME/clawd/tools/recall-local/recall.log</string>
  <key>StandardErrorPath</key><string>/Users/YOUR_USERNAME/clawd/tools/recall-local/recall.log</string>
</dict>
</plist>
EOF

# Replace YOUR_USERNAME, then load it
launchctl load ~/Library/LaunchAgents/ai.wren.recall-local.plist
```

Or just run it manually: `node ~/clawd/tools/recall-local/server.js &`

## Search (agent use)

```bash
curl -s "http://localhost:3456/search?q=YOUR+QUERY" | python3 -c "
import json,sys
d = json.load(sys.stdin)
print(f'{d[\"total\"]} chunks indexed')
for r in d['results'][:5]:
    print(f'[{r[\"source\"]}] {r[\"text\"][:300]}')
    print()
"
```

## Check if running / start if down

```bash
curl -s http://localhost:3456/search?q=test > /dev/null 2>&1 && echo "UP" || (echo "Starting..."; launchctl start ai.wren.recall-local; sleep 2)
```

## Human UI

Open `http://localhost:3456` in a browser. Search box, results below. Works on mobile too if on same local network.

## Tips

- Reloads all files on every search — always reflects the latest memory
- Source filenames are dates (`2026-03-01.md`) — useful for spotting when something happened
- Multi-word queries score better than single words
- For broad questions use general terms; for specific lookups use exact terms
