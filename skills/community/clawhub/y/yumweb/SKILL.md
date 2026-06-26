---
name: yumweb
description: "Use an already-logged-in Edge/Chrome/Chromium browser as the agent's hands. A persistent logged-in browser bridge for OpenClaw, Copilot CLI, Claude Code, Hermes, and other local AI agents. Use when: open browser, reuse logged-in websites, check X/Gmail/Outlook/Amazon/LinkedIn/Facebook/Instagram/WeChat Web, read webpages, switch tabs, click, type, fetch pages, browser automation."
argument-hint: "Command: start | stop | status | goto <url> | read [--mode text|md|html] [--selector CSS] | click <selector> | type <selector> <text> [--enter] | screenshot <path> | eval <js> | tabs | tab-new [url] | tab-switch <idx> | tab-close <idx> | fetch <url> | x-read [--user <h>] [--n 20] | x-post <text>"
---

# yumweb — logged-in browser bridge for AI agents

> **Platform: Windows / macOS / Linux**, with any Chromium-based browser
> (Microsoft Edge preferred; Chrome / Chromium also auto-detected).
> **Python: 64-bit only** — Playwright's `greenlet` dependency has no 32-bit
> Windows wheel.

A dedicated Chromium-based browser instance with Chrome DevTools Protocol (CDP)
enabled, running on **port 9333** with its own user-data directory — separate
from your everyday browser by default. Cookies persist across runs, so you log
in once (e.g. to `x.com`, Gmail, Outlook, Amazon, LinkedIn, Facebook,
Instagram, or WeChat Web) and stay logged in for later agent sessions.

When multiple tabs are open, yumweb persists the last explicitly activated tab
(`tab-switch`, `tab-new`, `goto`, `x-read`, etc.) so follow-up commands like
`read`, `click`, and `type` target the intended page more reliably.

This skill exposes a single Python script (`scripts/yumweb.py`, Playwright
backend) that any AI agent (OpenClaw, Copilot CLI, Claude Code, Hermes, etc.)
can shell out to in order to: open URLs, read page contents as text or
markdown, click & type, take screenshots, run JavaScript, and operate inside
real logged-in websites.

## Why this skill exists

Most browser tools focus on controlling a browser.

yumweb focuses on preserving a **persistent, logged-in browser world** that an
agent can come back to later.

That makes it useful for personal-assistant style tasks like:
- checking X / LinkedIn / Facebook feeds
- reading Gmail / Outlook inboxes
- opening Amazon product pages or carts
- revisiting WeChat Web / other already-authenticated sites

## Why a separate browser?

- **No collision** with whatever browser instance your day-to-day work uses.
- **Persistent profile** in `./profile/` next to this skill — log in once, keep
  cookies across runs (treat that directory like credentials; the bundled
  `.gitignore` excludes it from git).
- **Headed by default** so you can see what's happening and log in manually.
- **One-shot CLI** — every command attaches, does its job, exits.
- **Multi-agent / cross-browser** — works well with OpenClaw, Copilot CLI,
  Claude Code, Hermes, and Chromium-based browsers like Edge and Chrome.

## Setup

See [README.md](README.md) for full installation. Quick version:

```cmd
python -m pip install playwright html2text requests
python scripts\yumweb.py start
# Manually log in to x.com (or any site you want cached cookies for).
```

`start` is idempotent — running it again is a no-op if Edge is already up.

## Commands

| Command | Description |
|---|---|
| `start` | Launch Edge with `--remote-debugging-port=9333` + dedicated profile. Detached. |
| `stop` | Kill the Edge instance (only the one on port 9333) |
| `status` | Show whether Edge is up, current URL, list of tabs |
| `goto <url>` | Navigate active tab to URL (waits for load) |
| `read [--mode text\|md\|html] [--selector CSS] [--max N]` | Get page text/markdown/HTML. Default: text, body, max 8000 chars |
| `fetch <url>` | Shortcut: `goto <url> && read --mode md` |
| `click <selector>` | Click first element matching CSS |
| `type <selector> <text> [--enter]` | Focus selector, type text (optionally press Enter) |
| `screenshot <path>` | Save PNG screenshot of viewport |
| `eval <js>` | Run JS in active tab, print JSON result |
| `tabs` | List all open tabs (idx, title, url) |
| `tab-new <url>` | Open new tab |
| `tab-switch <idx>` | Switch active tab |
| `tab-close <idx>` | Close tab |
| `x-read [--user <handle>] [--n 20]` | Read tweets from home timeline or user profile |
| `x-post <text>` | Post a new tweet (requires prior login) |

All commands print to stdout. Errors go to stderr with non-zero exit.

## Examples

```cmd
:: Quick read of any URL (markdown form, good for LLMs)
python scripts\yumweb.py fetch https://example.com

:: Read your home timeline
python scripts\yumweb.py x-read --n 10

:: Read someone's tweets
python scripts\yumweb.py x-read --user satyanadella --n 5

:: Post a tweet
python scripts\yumweb.py x-post "Hello from CLI"

:: Click a button by CSS
python scripts\yumweb.py click "button[data-testid='login']"

:: Search box: type and press enter
python scripts\yumweb.py type "input[name=q]" "GB200 firmware" --enter
```

## How AI tools should use this skill

When the user asks to "check what's on X about XYZ", "go look at this URL",
"post a tweet about Y", or anything web-browsing related:

1. Run `./scripts/run.sh status` (or `python scripts\yumweb.py status` on Windows) — `start` if not running.
2. Use `fetch <url>` for quick reads (LLM-friendly markdown output).
3. Use `x-read` / `x-post` for X.
4. Use `tab-switch <idx>` before `read` / `click` / `type` when multiple tabs are open.
5. Use `eval` for anything custom (return must be JSON-serializable).
6. Output is plain text, ready to summarize back to the user.

## Files

- `scripts/yumweb.py` — main script (Playwright backend)
- `scripts/config.json` — port, profile dir, edge.exe path (paths blank → auto-resolve next to this skill)
- `profile/` — Edge user-data dir (created on first `start`, **gitignored**)
- `logs/yumweb.log` — stderr from launched Edge (gitignored)
- `logs/active_tab.json` — last active tab metadata used to make follow-up commands target the intended page

## Dependencies

- 64-bit Python 3.10+
- `playwright` (>= 1.40) — attaches to existing browser via CDP; **no bundled browser needed**
- `psutil` (>= 5.9) — cross-platform process management for `stop`
- `requests`
- `html2text` (auto-installed on first `read --mode md` if missing)

## Security notes

- Cookies live in `profile/` — treat that directory like a credential. The
  bundled `.gitignore` excludes it. Don't commit it.
- `eval` runs arbitrary JS — only invoke with trusted strings.
- Default port 9333 is **localhost-only**. Do not expose externally.
