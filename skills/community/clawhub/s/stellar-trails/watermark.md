# Custom Popup Preview — How to Change

> **Watermark**: This document records findings from extensive investigation
> into the ZAI sandbox popup preview mechanism (v6.3.0 → v7.3.0, Jun 2026).
> Preserved for future maintainers and users who want to customize their
> popup preview landing page.

## How ZAI Popup Preview Works

### Architecture

```
Browser (user) → ZAI CDN/proxy → sandbox:81 (Caddy) → :3000 (dev.sh → python3)
```

1. **ZAI platform** renders popup iframe pointing to `https://preview-<bot-id>.space-z.ai/`
2. **ZAI CDN** proxies request to sandbox port `:81`
3. **Caddy** (PID 2, root daemon) on `:81` reverse-proxies to `:3000`
4. **dev.sh** (launched by `/start.sh`) runs Python HTTP server on `:3000`
5. **Python server** serves files from `/home/z/my-project/.zscripts/`
6. **index.html** in `.zscripts/` is the landing page users see

### File Locations

```
/home/z/my-project/
├── .zscripts/
│   ├── index.html    ← Landing page (what users see in popup)
│   ├── dev.sh        ← HTTP server script (serves .zscripts/ on :3000)
│   └── chibi.svg     ← Mascot image (SVG format, referenced by index.html)
└── skills/
    └── stellar-trails/
        ├── index.html ← Source copy (in skill zip, distributed via ClawHub)
        └── dev.sh     ← Source copy (in skill zip)
```

## How to Change the Popup Preview

### Method 1: Edit index.html directly (quick, session-only)

```bash
# Edit the landing page
nano /home/z/my-project/.zscripts/index.html

# Trigger crash recovery to pick up new file
kill $(ss -tlnp 2>/dev/null | grep :3000 | grep -oP 'pid=\K[0-9]+' | head -1)

# Or if :3000 not running, start dev.sh with double-fork
( setsid bash /home/z/my-project/.zscripts/dev.sh </dev/null >/dev/null 2>&1 & ) &
```

Changes are session-only. Next sandbox session will use whatever is in the
skill zip (from ClawHub or `/home/user_skills/`).

### Method 2: Update skill source + publish (permanent)

```bash
# 1. Edit source file in stellar-trails repo
cd ~/.stellar-trails-repo
nano skill/stellar-trails/index.html

# 2. Bump version in SKILL.md
sed -i 's/version": X.Y.Z/version": X.Y.W/' skill/stellar-trails/SKILL.md

# 3. Commit + push + tag
git add -A && git commit -m "feat: new popup preview"
git tag -a vX.Y.W -m "vX.Y.W"
git push origin main refs/tags/vX.Y.W

# 4. Publish to ClawHub
clawhub skill publish skill/stellar-trails \
  --slug stellar-trails --version X.Y.W \
  --source-repo https://github.com/hoshiyomiX/stellar-trails \
  --source-commit $(git rev-parse HEAD)

# 5. Update local .zscripts/
cp skill/stellar-trails/index.html /home/z/my-project/.zscripts/index.html
cp skill/stellar-trails/dev.sh /home/z/my-project/.zscripts/dev.sh
chmod +x /home/z/my-project/.zscripts/dev.sh

# 6. Restart popup server
kill $(ss -tlnp 2>/dev/null | grep :3000 | grep -oP 'pid=\K[0-9]+' | head -1)
```

### Method 3: clawhub install (for fresh sandbox)

```bash
clawhub install stellar-trails
# Then copy index.html + dev.sh to .zscripts/
cp /home/z/my-project/skills/stellar-trails/index.html /home/z/my-project/.zscripts/
cp /home/z/my-project/skills/stellar-trails/dev.sh /home/z/my-project/.zscripts/
chmod +x /home/z/my-project/.zscripts/dev.sh
```

## dev.sh — Custom No-Cache HTTP Server

### Key Features

1. **Cache-Control: no-store** — HTTP response header that prevents browser
   from caching old versions. Without this, Python's `http.server` default
   has no cache headers → browser uses heuristic caching → popup stuck on
   old version.

2. **Crash recovery loop** (`while true`) — If python3 process dies (OOM,
   signal, etc), dev.sh auto-restarts after 1 second. Without this, single
   python crash = popup down forever until session restart.

3. **SO_REUSEADDR** (`allow_reuse_address = True`) — Allows binding to :3000
   even if previous socket is in TIME_WAIT state (prevents "Address already
   in use" error after rapid restart).

4. **Port guard** — Checks if :3000 already in use before starting. Idempotent:
   running dev.sh multiple times won't create duplicate processes.

5. **Signal traps** — SIGTERM/SIGINT handled gracefully (clean exit instead
   of SIGKILL).

### dev.sh Source Location

- **Source** (in skill zip): `skill/stellar-trails/dev.sh`
- **Runtime** (served by /start.sh): `/home/z/my-project/.zscripts/dev.sh`
- `/start.sh` copies dev.sh from skill to `.zscripts/` at session start
  (if .zscripts/dev.sh doesn't exist, it stays as-is from previous session)

### How /start.sh Launches dev.sh

```bash
# /start.sh (runs as ROOT at session start, uptime ~8.9s)
if [ -f "/home/z/my-project/.zscripts/dev.sh" ]; then
  (
    sudo -u z bash /home/z/my-project/.zscripts/dev.sh
  ) &
  BUN_PID=$!
fi
```

- Parent process = root daemon (caddy PID 2) → **persistent** sepanjang session
- `/start.sh` only runs ONCE at session start — does NOT monitor or re-launch

## Double-Fork Technique (Persistent Without Restart)

### Problem

When user (z) starts dev.sh via bash tool, process is killed when bash tool
exits (sandbox cleanup kills child processes of temporary shell).

### Solution: Double-Fork

```bash
( setsid bash /home/z/my-project/.zscripts/dev.sh </dev/null >/dev/null 2>&1 & ) &
```

### How It Works

1. `( ... )` — subshell, backgrounded with `&`
2. `setsid` — creates a new session, detaches from the controlling terminal
3. `bash dev.sh` — runs in new session
4. Subshell exits immediately
5. dev.sh becomes **orphan** → parent = PID 1 (tini/init) → **survives shell exit**

### Verification

```bash
# Check parent PID — should be 1 (orphan)
DEV_PID=$(pgrep -f "dev\.sh" | head -1)
cat /proc/$DEV_PID/status | grep PPid
# Expected: PPid: 1
```

### Used in SKILL.md Step 3

```bash
DEV_SH="/home/z/my-project/.zscripts/dev.sh"
if [ -f "$DEV_SH" ] && ! ss -tlnp 2>/dev/null | grep -q ':3000 '; then
  ( setsid bash "$DEV_SH" </dev/null >/dev/null 2>&1 & ) &
fi
```

Step 3 runs on every `Skill(command="stellar-trails")` invoke. If :3000
is not listening, it auto-launches dev.sh with double-fork → popup preview
auto-starts without manual intervention or sandbox restart.

## Caching Layers (Debug Guide)

If popup shows old version after update, check these layers:

### Layer 1: File on Disk

```bash
grep "title>" /home/z/my-project/.zscripts/index.html
```

If wrong version → update file: `cp skill/stellar-trails/index.html .zscripts/`

### Layer 2: Python HTTP Server

```bash
curl -s http://localhost:3000/ | grep "title>"
```

If wrong version → restart python3 (crash recovery):
```bash
kill $(ss -tlnp 2>/dev/null | grep :3000 | grep -oP 'pid=\K[0-9]+' | head -1)
```

### Layer 3: Caddy Proxy (:81)

```bash
curl -s http://localhost:81/ | grep "title>"
```

If wrong version → Caddy is transparent proxy, should match :3000.
If mismatch → check Caddy is running: `ps -ef | grep caddy`

### Layer 4: Browser Cache

- Hard refresh: `Ctrl+Shift+R` or `Cmd+Shift+R`
- Or: F12 → Network → "Disable cache" → refresh
- Cache-Control: no-store header should prevent this (v7.2.2+)

### Layer 5: ZAI Platform CDN

If all above correct but popup still shows old version:
- ZAI CDN may cache response between browser and sandbox
- **Cannot purge from sandbox** — wait for TTL expire (5-60 min)
- Or try cache-buster URL: `?cb=<timestamp>`

## index.html Design Guidelines

### Minimalist (v7.3.0, current)

- **6 KB** — lightweight, fast render
- Single gradient orb (breathe animation, GPU-friendly)
- Text-based phase flow (no cards)
- No backdrop-filter, no starfield, no feature grid
- Animations: fadeIn, float, breathe, pulse — all CSS, no JS

### Cosmic (v7.1.4, previous)

- **19 KB** — richer, more visual
- Starfield + 3 radial gradients + drift animation
- 6 glassmorphism cards for phase flow
- 6 feature cards with icons
- backdrop-filter: blur(10px) on cards
- Heavier render (but still fast on modern browsers)

### Recommendations

- Keep index.html under 10 KB for fast popup load
- Avoid `backdrop-filter` (performance cost on low-end devices)
- Use CSS animations only (no JS animation libraries)
- Always include `<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">`
- Use `chibi.svg` via `<img src="chibi.svg" onerror="this.style.display='none'">` for graceful fallback
- Test with `agent-browser screenshot` + VLM analysis before publishing

## Version History of Popup Preview

| Version | Design | Size | Key Change |
|---------|--------|------|------------|
| v6.3.0 | Basic dark (Stellar Frameworks) | 2 KB | Original inline heredoc in boot.sh |
| v7.1.4 | Cosmic glassmorphism | 19 KB | New design, cp from skill source |
| v7.2.2 | Cosmic + no-cache headers | 19 KB | dev.sh with Cache-Control: no-store |
| v7.2.6 | Cosmic + double-fork | 19 KB | Persistent process without restart |
| **v7.3.0** | **Minimalist** | **6 KB** | **Lightweight, well-animated, -68% size** |
