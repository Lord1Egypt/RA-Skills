# stealth-browser

Invisible Chrome automation for web scraping and browser automation. Launches a real Chrome instance that's completely hidden from the user, controlled via Chrome DevTools Protocol (CDP).

> **macOS only.** Stealth mode relies on AppleScript and macOS-specific APIs (`open -g`, `osascript`) to hide Chrome. Standard mode (plain `agent-browser`) works on any OS.

## Why?

Standard browser automation tools (Playwright, Puppeteer, Selenium) use modified Chromium builds that bot detection services can fingerprint. They set `navigator.webdriver`, modify browser APIs, and leave other detectable traces.

stealth-browser takes a different approach:
- Launches **your actual Chrome install** (not a modified Chromium)
- Uses a **real user profile** with browsing history, cookies, and extensions
- Sends commands via **raw CDP** (Chrome DevTools Protocol) which is invisible to page JavaScript
- Keeps Chrome **completely hidden** - no visible window, no dock icon flash

The result: sites see a normal Chrome browser doing normal browsing. No detectable automation.

## Quick Start

```bash
# Check everything is installed
stealth-browser doctor

# Read a page as markdown (simplest use case)
stealth-browser read https://example.com

# Read another page (Chrome stays running - instant, no flash)
stealth-browser read https://another-site.com

# Done
stealth-browser close
```

## Installation

### Dependencies

| Dependency | Install | Required for |
|------------|---------|-------------|
| macOS | - | Stealth mode (AppleScript, `open -g`) |
| Google Chrome | [google.com/chrome](https://google.com/chrome) | Everything |
| agent-browser | `npm install -g agent-browser` | Everything |
| python3 | `brew install python3` (usually pre-installed) | Everything |
| d2m | `npm install -g d2m` | `read` command only |
| curl | Pre-installed on macOS | Everything |

Run `stealth-browser doctor` to check what's installed and what's missing.

### Bundled Profile

stealth-browser ships with a clean Chrome profile that includes two extensions pre-installed:

- **uBlock Origin Lite** - blocks ads and trackers (makes pages cleaner for scraping)
- **I still don't care about cookies** - auto-dismisses cookie consent banners

These extensions make the browser look more like a real user and improve scraping results (no cookie banners or ads in the extracted content).

The profile contains **no cookies, no history, no saved passwords, no autofill data** - just the extensions and clean preferences. Chrome regenerates its runtime caches on first launch.

To add more extensions or customize the profile:

```bash
# Open Chrome with the stealth profile (visible, for manual setup)
stealth-browser open https://chromewebstore.google.com --visible

# Install extensions, change settings, etc.

# Close when done
stealth-browser close
```

## Commands

### `read <url>`
Fetch a page and return clean markdown. The main command for scraping content.

```bash
stealth-browser read https://example.com
```

- Launches Chrome hidden (if not already running)
- Navigates to the URL
- Extracts HTML and converts to markdown via d2m
- Strips images (not useful as text)
- Chrome stays running for instant re-use

### `open <url> [--hidden]`
Launch Chrome with CDP enabled. Use this when you need full browser automation (clicking, form filling, etc.) rather than just reading content.

```bash
# Hidden (invisible to user)
stealth-browser open https://example.com --hidden

# Visible (for debugging or manual interaction)
stealth-browser open https://example.com
```

After opening, use `agent-browser --cdp 9222` for any browser command:

```bash
agent-browser --cdp 9222 snapshot -i          # See page elements
agent-browser --cdp 9222 click @e3            # Click a button
agent-browser --cdp 9222 fill @e1 "hello"     # Fill an input
agent-browser --cdp 9222 screenshot page.png  # Take screenshot
agent-browser --cdp 9222 eval "document.title" # Run JavaScript
```

### `close`
Stop Chrome. Run this when you're done.

```bash
stealth-browser close
```

### `status`
Check if Chrome is running, what URL it's on, and whether it's visible.

```bash
stealth-browser status
```

### `screenshot [path]`
Take a CDP screenshot. If Chrome is hidden, it briefly unhides (behind other windows), takes the screenshot, and re-hides.

```bash
stealth-browser screenshot /tmp/page.png
```

### `hide` / `unhide`
Toggle Chrome visibility. Useful for debugging.

```bash
stealth-browser unhide   # Make Chrome visible (for debugging)
stealth-browser hide     # Hide it again
```

### `setup`
Delete and re-create the Chrome profile. Use if the profile gets corrupted.

```bash
stealth-browser setup
```

### `doctor`
Check all dependencies and show their status.

```bash
stealth-browser doctor
```

## How the Hiding Works

On macOS, there's no clean way to launch Chrome completely invisibly. Chrome actively fights being hidden during startup. stealth-browser uses a multi-layered approach:

1. **`open -g`** - macOS flag that launches Chrome without making it the frontmost app
2. **Small window (500x375)** - minimum Chrome window size, less visible if it flashes
3. **Top-left positioning** - Chrome prefs place the window in the corner of the leftmost display
4. **Off-screen move** - background loop moves the window to (-32000, -32000) every 50ms
5. **`set visible to false`** - AppleScript hides Chrome after startup completes
6. **Re-activate user's app** - whatever app was in front stays in front

The first launch has a brief flash (fraction of a second). All subsequent operations with the already-running Chrome are completely invisible.

## Architecture

```
stealth-browser (bash)          Chrome (real install)
    |                               |
    |-- open -g ------------------>| Launch hidden
    |                               |
    |-- osascript ---------------->| Move off-screen + hide
    |                               |
    |   agent-browser --cdp 9222    |
    |       |                       |
    |       |-- CDP websocket ----->| Send commands
    |       |<-- CDP response ------| Get results
    |       |                       |
    |-- kill ---------------------->| Stop
```

- **stealth-browser**: Bash script that manages Chrome lifecycle (launch, hide, stop)
- **agent-browser**: Node.js CLI that sends CDP commands (navigate, click, snapshot, etc.)
- **Chrome**: Your real Chrome install with a dedicated profile at `~/.claude/skills/stealth-browser/profile/`
- **CDP**: Chrome DevTools Protocol on port 9222 - invisible to page JavaScript

## Claude Code Integration

stealth-browser works best when Claude Code automatically falls back to it whenever `WebFetch` gets blocked. It also **learns** which domains block WebFetch and skips straight to stealth-browser on future requests.

### Domain Blocklist (learning)

stealth-browser maintains a blocklist of domains that have blocked WebFetch before:

```
~/.claude/skills/stealth-browser/data/blocked-domains.txt
```

One domain per line. When a domain is in this list, a PreToolUse hook blocks the WebFetch call before it even fires and tells Claude to use stealth-browser directly. Domains get added to the list automatically (soft blocks) or by Claude following the CLAUDE.md rule (hard blocks).

To manually add/remove domains:
```bash
# Add a domain
echo "www.glassdoor.com" >> ~/.claude/skills/stealth-browser/data/blocked-domains.txt

# View the blocklist
cat ~/.claude/skills/stealth-browser/data/blocked-domains.txt

# Remove a domain (edit the file and delete the line)
```

### Integration Layers

Three hooks and a rule work together to make this seamless:

#### 1. PreToolUse Hook (blocks known-bad domains)

Checks every WebFetch URL against the blocklist. If the domain was blocked before, rejects the WebFetch call and tells Claude to use stealth-browser. Saves time and avoids wasted requests.

Add to `~/.claude/settings.json` inside `"hooks"`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "WebFetch",
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/.claude/hooks/webfetch-preflight.sh"
          }
        ]
      }
    ]
  }
}
```

Then create `~/.claude/hooks/webfetch-preflight.sh`:

```bash
#!/bin/bash
# PreToolUse hook for WebFetch - skip known-blocked domains

BLOCKLIST="$HOME/.claude/skills/stealth-browser/data/blocked-domains.txt"

if [ ! -f "$BLOCKLIST" ]; then
  exit 0
fi

input=$(cat)
url=$(echo "$input" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('url',''))" 2>/dev/null)
domain=$(echo "$url" | python3 -c "import sys; from urllib.parse import urlparse; print(urlparse(sys.stdin.read().strip()).netloc)" 2>/dev/null)

if [ -n "$domain" ] && grep -qiF "$domain" "$BLOCKLIST" 2>/dev/null; then
  echo "DOMAIN PREVIOUSLY BLOCKED ($domain) - Skip WebFetch. Use stealth-browser directly:"
  echo "  ~/.claude/skills/stealth-browser/scripts/stealth-browser read $url"
  exit 2
fi

exit 0
```

#### 2. PostToolUse Hook (learns from soft blocks)

When WebFetch returns HTTP 200 but the content is a Cloudflare challenge page, this hook adds the domain to the blocklist and tells Claude to retry.

Add to `~/.claude/settings.json` inside `"hooks"`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "WebFetch",
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/.claude/hooks/webfetch-fallback.sh"
          }
        ]
      }
    ]
  }
}
```

Then create `~/.claude/hooks/webfetch-fallback.sh`:

```bash
#!/bin/bash
# PostToolUse hook for WebFetch - catch soft blocks and learn blocked domains
#
# Only fires on successful WebFetch calls (HTTP 200).
# Hard failures (403, 429) skip PostToolUse - handled by CLAUDE.md rule.

BLOCKLIST="$HOME/.claude/skills/stealth-browser/data/blocked-domains.txt"
input=$(cat)

response=$(echo "$input" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_response',{}).get('result',''))" 2>/dev/null)
url=$(echo "$input" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('url',''))" 2>/dev/null)

if echo "$response" | grep -qiE 'cloudflare|just.a.moment|challenge-platform|captcha|bot.protection|verify.you.are.human|checking.your.browser|ray.id'; then
  domain=$(echo "$url" | python3 -c "import sys; from urllib.parse import urlparse; print(urlparse(sys.stdin.read().strip()).netloc)" 2>/dev/null)
  if [ -n "$domain" ]; then
    mkdir -p "$(dirname "$BLOCKLIST")"
    grep -qxF "$domain" "$BLOCKLIST" 2>/dev/null || echo "$domain" >> "$BLOCKLIST"
  fi
  echo "WEBFETCH GOT A CHALLENGE PAGE - Domain '$domain' added to blocklist. Retry with stealth-browser:"
  echo "  ~/.claude/skills/stealth-browser/scripts/stealth-browser read $url"
fi

exit 0
```

Make both executable: `chmod +x ~/.claude/hooks/webfetch-preflight.sh ~/.claude/hooks/webfetch-fallback.sh`

#### 3. CLAUDE.md Rule (handles hard failures + teaches learning)

When WebFetch throws a hard error (403, 429, timeout), PostToolUse hooks don't fire. The CLAUDE.md rule tells Claude to add the domain to the blocklist AND retry with stealth-browser.

Add to `~/.claude/CLAUDE.md`:

```markdown
## WebFetch Fallback

When WebFetch fails with 403, 429, blocked, timeout, forbidden, access denied, or returns a
Cloudflare/bot challenge page:

1. **Add the domain to the blocklist** so future calls skip WebFetch entirely:
\`\`\`bash
echo "the-domain.com" >> ~/.claude/skills/stealth-browser/data/blocked-domains.txt
\`\`\`

2. **Retry with stealth-browser** immediately - do not ask the user:
\`\`\`bash
~/.claude/skills/stealth-browser/scripts/stealth-browser read <url>
\`\`\`
```

#### 4. SKILL.md Triggers (explicit invocation)

The skill's YAML frontmatter includes triggers like `403 error`, `cloudflare blocked`, `browser blocked`. These match when the user explicitly mentions these terms.

### How the learning works

```
First request to blocked domain:
  WebFetch → 403 error
  Claude sees error + CLAUDE.md rule
  → Adds domain to blocklist
  → Retries with stealth-browser

Soft block (200 + challenge page):
  WebFetch → 200 OK (but challenge content)
  PostToolUse hook detects challenge
  → Adds domain to blocklist automatically
  → Tells Claude to retry with stealth-browser

Every request after that:
  WebFetch → PreToolUse hook checks blocklist
  → Blocks the call immediately
  → Claude uses stealth-browser directly (no wasted request)
```

| Layer | When it fires | What it does |
|-------|--------------|--------------|
| PreToolUse hook | Before every WebFetch | Blocks calls to known-blocked domains |
| PostToolUse hook | After successful WebFetch | Detects challenge pages, learns the domain |
| CLAUDE.md rule | When WebFetch throws an error | Teaches Claude to learn the domain + retry |
| SKILL.md triggers | User says "403", "blocked" | Suggests the skill for explicit use |

### PATH setup (optional)

To use `stealth-browser` without the full path, add to your `~/.zshrc`:

```bash
export PATH="$HOME/.claude/skills/stealth-browser/scripts:$PATH"
```

Then you can just run `stealth-browser read <url>` from anywhere.

## Troubleshooting

**Chrome won't start**: Check if another Chrome is using port 9222. `stealth-browser close` then try again.

**CDP not responding**: Chrome might still be starting up. Wait a few seconds and retry.

**Page shows bot challenge**: Some sites detect automation even with real Chrome. Try adding a longer wait, or interact with the page manually via `stealth-browser unhide`.

**Screenshots fail while hidden**: This is expected - Chrome's compositor pauses when hidden. Use `stealth-browser screenshot` which handles the unhide/re-hide cycle automatically.

**Extensions not working**: Open Chrome visibly (`stealth-browser open url`) and install extensions manually from the Chrome Web Store.
