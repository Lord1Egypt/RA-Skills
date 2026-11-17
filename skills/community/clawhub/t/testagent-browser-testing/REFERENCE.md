# Browser Testing Reference

## Tool selection

### Comparison table

| | OpenClaw built-in browser | Playwright MCP | browser-use CLI |
|---|---|---|---|
| **Invocation** | `browser` tool (snapshot/act/screenshot) | `playwright__browser_*` family | `exec` calling the `browser-use` command |
| **State retrieval** | accessibility snapshot (text tree) | snapshot (text tree) | `state` (indexed element list) |
| **Element targeting** | ref (e.g. e36) | ref + selector | numeric index (e.g. click 5) |
| **Screenshot output** | AI analysis text (❌ not shareable) | PNG file (✅ shareable) | saved path (✅ shareable) |
| **JS execution** | ✅ evaluate | ✅ evaluate | ✅ eval |
| **Keyboard events** | ⚠️ doesn't work on React controlled components | ✅ works well | ✅ `keys "Enter"` |
| **Cloud browser** | ❌ | ❌ | ✅ `cloud connect` |
| **Reuse login session** | ❌ | ❌ | ✅ `--profile "Default"` |
| **Anti-bot/CAPTCHA** | ❌ | ❌ | ✅ built into the cloud browser |
| **Residential proxy** | ❌ | ❌ | ✅ 195+ countries |
| **Internal network tunnel** | ❌ | ❌ | ✅ `tunnel <port>` |
| **Parallel multi-session** | limited | limited | ✅ `--session NAME` |
| **Command chaining** | not supported | not supported | ✅ chainable with `&&` |

### When to use which

**→ Use the OpenClaw built-in browser (default choice)**
- Routine functional testing and page interaction
- Actions within an already-logged-in session
- When screenshots don't need to be shared with the user
- **Advantage**: tightly integrated tooling, gets things done in one step

**→ Use Playwright MCP**
- Need to share a screenshot with the user (bug screenshots, state confirmation)
- Precise interaction with React/Vue controlled components (good keyboard event support)
- Need precise selector-based element targeting
- **Advantage**: most precise element targeting, screenshots are usable

**→ Use browser-use CLI**
- Need a cloud browser (anti-bot, CAPTCHA, residential proxy)
- Need to reuse the user's local Chrome login session
- Internal services need to be reached via a tunnel (`tunnel <port>`)
- Fast exploration of a new product (efficient with `&&` command chains)
- Parallel testing across multiple products (`--session` multi-session)
- **Advantage**: strongest browser capabilities, full coverage across cloud + local + tunnel

### Decision tree

**Default to the OpenClaw built-in browser**, and switch only in these cases:

```
Need to share a screenshot with the user?
  → Try Playwright MCP first (take_screenshot saved to a file)
    → Does playwright__browser_navigate actually work? → Use Playwright MCP
    → Doesn't work (missing system deps / no root)? → Use the built-in browser + direct CDP for screenshots (see below)

React/Vue controlled component interaction fails (keyboard events don't register)?
  → Switch to Playwright MCP

Target site has anti-bot/CAPTCHA, and both the built-in browser and Playwright are blocked?
  → Switch to browser-use CLI (cloud connect)

Need to reuse the user's local Chrome login session?
  → Switch to browser-use CLI --profile "Default"

Need an internal network tunnel or parallel multi-session?
  → Switch to browser-use CLI
```

---

## Correct screenshot workflow

### Path 1: Playwright MCP (preferred)

```
1. playwright__browser_navigate → target URL (only counts as usable once it actually works)
2. playwright__browser_take_screenshot → filename="~/.openclaw/workspace/bug_<number>_<description>.png"
3. Attach in the reply: MEDIA:~/.openclaw/workspace/bug_<number>_<description>.png
```

### Path 2: Direct Chrome CDP connection (the main fallback when Playwright MCP is unavailable)

setup.sh creates a `~/.local/bin/chrome-cdp` launcher script that wraps the correct LD_LIBRARY_PATH and startup flags.

```bash
# 1. Start Chrome (running in background)
chrome-cdp &
sleep 2  # wait for it to start

# 2. Navigate to the target page
curl -s http://localhost:9223/json/new?about:blank  # create a new tab

TARGET_ID=$(curl -s "http://localhost:9223/json" | python3 -c \
  "import json,sys; t=[x for x in json.load(sys.stdin) if x.get('type')=='page']; print(t[0]['id'])")

# 3. Navigate via the CDP WebSocket
node -e "
const ws = new (require('ws').WebSocket)('ws://localhost:9223/devtools/page/$TARGET_ID');
ws.on('open', () => {
  ws.send(JSON.stringify({id:1, method:'Page.navigate', params:{url:'https://your-target.com'}}));
});
ws.on('message', d => { const r=JSON.parse(d); if(r.id===1){ws.close();} });
"

# 4. Take a screenshot
SCREENSHOT="$HOME/.openclaw/workspace/screenshot_$(date +%s).png"
node -e "
const ws = new (require('ws').WebSocket)('ws://localhost:9223/devtools/page/$TARGET_ID');
ws.on('open', () => ws.send(JSON.stringify({id:1,method:'Page.captureScreenshot',params:{format:'png'}})));
ws.on('message', d => {
  const r = JSON.parse(d.toString());
  if (r.id === 1) {
    require('fs').writeFileSync('$SCREENSHOT', Buffer.from(r.result.data,'base64'));
    ws.close(); process.exit(0);
  }
});
"
echo "MEDIA:$SCREENSHOT"
```

**JS interaction (filling forms, clicking buttons) works the same way** — replace the screenshot command with `Runtime.evaluate`:
```javascript
{id:2, method:'Runtime.evaluate', params:{expression:'document.querySelector("button").click()'}}
```

### Path 3: browser-use CLI (when even CDP won't work)

```bash
browser-use screenshot --output ~/.openclaw/workspace/screenshot.png
```

**General notes**:
- The built-in browser's `browser screenshot` only returns AI analysis text — none of the three paths above include it
- `MEDIA:` only renders inside chat replies; writing it into a `.md` file will not display the image
- `mcp doctor --probe` returning ok is a false positive — it doesn't mean Playwright is actually usable

---

## Report format

```
## Test Report: [Feature name] @ [URL]
Test date: YYYY-MM-DD
Test tool: Playwright MCP / browser-use CLI / built-in browser

### Summary
- Total test points: 5
- Passed: 3
- Bugs found: 2

### Passed test points
- ✅ Normal login flow
- ✅ Required-field validation
- ✅ Core feature X happy path

### Bug list

**Bug #1: [Title]**
- Test point: [corresponding test point]
- Symptom: [one-sentence description]
- Steps to reproduce:
  1. ...
  2. ...
  3. ...
- Expected result: ...
- Actual result: ...
- Screenshot: MEDIA:/root/.openclaw/workspace/bug_1_xxx.png
- Suggested priority: High (core feature unusable)
- Suggested assignee: [per the assignment rules in AGENTS.md]
- Suggested fix timeline: 2 days
```

---

## Priority rules

| Situation | Suggested priority | coding-net value |
|------|-----------|--------------|
| Core feature completely unusable, blocking the user | Highest / High | 0 or 1 |
| Feature is broken but a workaround exists | Medium | 2 |
| UI/UX issue, doesn't affect core usage | Low / Lowest | 3 or 4 |

If AGENTS.md defines more specific priority criteria, defer to AGENTS.md.

---

## Pitfalls

### Built-in browser fails to start / times out (container environments)
**Symptom**: `browser start` reports `Timeout waiting for browser`, `browser doctor` hangs at `launching...`

**Root cause**: the container runs as root, Chromium needs a sandbox, but the container lacks `USER_NAMESPACE` permission

**Fix**: edit `~/.openclaw/openclaw.json` directly (can't use `config.patch` — the browser path is protected):
```json
{
  "browser": {
    "noSandbox": true
  }
}
```
Then run the full restart sequence (order matters):
```bash
browser stop
openclaw gateway restart
# wait about 15 seconds
browser start
```

### Built-in browser navigation fails with blocked by policy (SSRF block)
**Symptom**: `browser navigate` to the target URL reports `blocked by policy`

**Root cause**: the built-in browser enables SSRF protection by default, allowing only allowlisted domains

**Fix**: add the target domain to `browser.ssrfPolicy.allowedHostnames` in `~/.openclaw/openclaw.json`, along with the login page's Auth0/SSO domain (otherwise the login redirect will also be blocked):
```json
{
  "browser": {
    "noSandbox": true,
    "ssrfPolicy": {
      "allowedHostnames": [
        "app.example.com",
        "xxx.us.auth0.com"
      ]
    }
  }
}
```
After editing, run the full restart sequence again: `browser stop` → `gateway restart` → wait 15 seconds → `browser start`

### Ctrl+Enter shortcut doesn't work
Keyboard shortcuts on React controlled components may not trigger through automation tools.

Fix: find the actual send/submit button on the page and click it directly via JS:
```javascript
document.querySelector('[aria-label="Send"]').click()
// or use playwright evaluate / browser evaluate
```

### Mojibake (□□□) in screenshots for Chinese text
Indicates the fonts weren't installed correctly — re-run the browser-setup skill.

Verification command:
```bash
fc-match ":lang=zh"
# Expected output includes "Noto Sans CJK SC", not "DejaVu Sans"
```

### Playwright MCP reports Missing system dependencies

**Symptom**: `playwright__browser_navigate` errors with `Missing system dependencies`, yet `mcp doctor --probe` returns ok

**Root cause**: `mcp doctor` only checks that the MCP server process started — it doesn't verify Chromium can actually run. Without root, 20+ system `.so` files are missing and Chromium crashes on launch.

**Fix**: don't try `sudo`/`apt`/`install-deps` — switch paths directly:
- For screenshots → built-in browser + direct CDP (see Path 2 above)
- For page interaction → keep using the built-in browser (snapshot/act)

### Stuck on an action
If the same method fails 2-3 times, switch strategy immediately:
- Built-in browser fails → switch to Playwright MCP
- Playwright MCP fails (missing deps) → use direct CDP for screenshots, built-in browser for interaction
- Both fail → switch to browser-use CLI
- Don't keep grinding on one path
