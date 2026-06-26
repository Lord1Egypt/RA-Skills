# yumweb

> **Use your already-logged-in browser as the agent’s hands.**
>
> For **OpenClaw, Copilot CLI, Claude Code, Hermes, and other local AI
> agents** — on **Edge, Chrome, and other Chromium-based browsers**.
>
> yumweb is a cross-platform, AI-friendly **logged-in browser bridge**. It
> keeps a persistent browser session alive so an agent can operate inside the
> websites you already use: read pages, switch tabs, click, type, screenshot,
> run JS, and work inside real logged-in products like X, Gmail, Outlook,
> Amazon, LinkedIn, Facebook, Instagram, or WeChat Web.

Designed to be dropped into agent frameworks (OpenClaw, Claude Code, GitHub
Copilot, custom RPA scripts, etc.) as a **skill**: every command is one-shot,
prints to stdout, and exits with a sensible code.

**At a glance**
- **Multi-agent:** OpenClaw, Copilot CLI, Claude Code, Hermes, and other local agents
- **Cross-browser:** Edge preferred, Chrome / Chromium supported
- **Logged-in by default:** log in once, let the agent continue later
- **Local-first:** browser session stays on your machine

Under the hood: [Playwright](https://playwright.dev/python/) attaches over
Chrome DevTools Protocol to an Edge instance launched with a private user-data
directory and `--remote-debugging-port=9333`. No bundled browser is
downloaded — we use the Edge you already have installed.

---

## Why yumweb?

- **Multi-agent:** built for OpenClaw, Copilot CLI, Claude Code, Hermes, and any agent that can call local CLI tools
- **Cross-browser:** Microsoft Edge preferred, with Chrome, Chromium, and other Chromium-based browsers supported
- **Logged-in by default:** log in once, let the agent come back later and continue
- **Local-first:** your browser session stays on your machine

## What makes yumweb different?

Most browser automation tools focus on **controlling a browser**.

yumweb focuses on something slightly different:

- **keeping a persistent, logged-in browser session alive**
- **letting an agent come back later and continue using it**
- **making already-authenticated websites part of the agent’s working world**

That makes yumweb less like a test runner and more like a **personal web
operator bridge**.

If OpenClaw browser tooling and Playwright MCP are the browser infrastructure,
yumweb is the lightweight layer that says:

> *the user already logged in — now let the agent help from there.*

## Why not just use a sandbox browser?

Sandboxed browser sessions are great for public web tasks, testing, and clean
reproducible automation.

But for many real assistant jobs, a sandbox browser is not enough:

- it usually starts **logged out**
- it does not already live inside your real inbox, feed, cart, or social graph
- it cannot reliably continue from the state you built up over days or weeks
- it is good for "open a webpage" tasks, but often useless for "help me inside
  *my* web life" tasks

yumweb exists for the cases where the agent needs to work inside the websites
you already authenticated and already care about.

## Requirements

- **Windows, macOS, or Linux**
- **A Chromium-based browser** installed locally — Microsoft Edge preferred,
  but Google Chrome and Chromium also work (yumweb auto-detects). On Linux
  this means any of `microsoft-edge`, `google-chrome`, `chromium`, or
  `chromium-browser` on `PATH`.
- **64-bit Python 3.10+**
  - 32-bit Python will **not** work: Playwright depends on `greenlet`, which
    ships no 32-bit Windows wheels. Verify with `python -c "import platform;
    print(platform.architecture())"` — must report `('64bit', ...)`.

## Install

```cmd
git clone https://github.com/yumyumtum/yumweb.git
cd yumweb
python -m pip install -r requirements.txt
```

(or `python -m pip install playwright html2text requests`)

You do **not** need `playwright install` — yumweb never launches a bundled
browser. It only attaches to your real Edge.

### Recommended wrapper (macOS / Linux)

For agent environments, prefer the included wrapper so the local `.venv` is
bootstrapped automatically:

```bash
./scripts/run.sh status
./scripts/run.sh start
./scripts/run.sh fetch https://example.com
```

## First run

```cmd
python scripts\yumweb.py start
```

(On macOS / Linux: `python scripts/yumweb.py start`.)

This launches your browser with a dedicated profile directory (`./profile/`)
and remote-debugging enabled on `127.0.0.1:9333`. The browser window stays
open in the background; subsequent commands attach to it.

**Log into any sites you want yumweb to access** (e.g. `x.com`, Gmail,
Outlook, LinkedIn, Amazon, WeChat Web). Cookies are stored in `./profile/`
and survive across runs, so you log in once and the agent can keep working in
that same browser world later.

To stop the dedicated Edge:

```cmd
python scripts\yumweb.py stop
```

## Quick tour

```cmd
:: Read any page as markdown (great for feeding to an LLM)
python scripts\yumweb.py fetch https://example.com

:: Plain-text body of the currently active tab
python scripts\yumweb.py read --mode text --max 2000

:: Take a screenshot
python scripts\yumweb.py screenshot shot.png

:: Run arbitrary JavaScript and print the JSON result
python scripts\yumweb.py eval "document.title"

:: Click and type
python scripts\yumweb.py click "button.signup"
python scripts\yumweb.py type "input[name=q]" "hello world" --enter

:: List tabs
python scripts\yumweb.py tabs

:: X (Twitter) — read home timeline (requires prior login in the Edge window)
python scripts\yumweb.py x-read --n 10

:: X — read another user's tweets
python scripts\yumweb.py x-read --user satyanadella --n 5

:: X — post (also requires login)
python scripts\yumweb.py x-post "hello from yumweb"
```

Full command reference: [SKILL.md](SKILL.md).

## Configuration

`scripts/config.json` controls the port, profile location, log location, and
optional explicit browser paths. By default:

- `profile_dir` / `log_path` are blank → auto-resolved to `./profile/` and
  `./logs/yumweb.log` next to the skill root.
- `edge_exe_candidates` is empty → yumweb auto-discovers the browser by
  searching `PATH` (`msedge`, `microsoft-edge`, `google-chrome`, `chromium`,
  …) and standard install locations on the current OS.

Override any of them with explicit paths if needed:

```json
{
  "remote_debugging_port": 9333,
  "profile_dir": "",
  "log_path": "",
  "edge_exe_candidates": [],
  "default_read_max_chars": 8000
}
```

Example override for a non-standard Edge install:

```json
{
  "edge_exe_candidates": ["/opt/edge/microsoft-edge"]
}
```

## Use as an agent skill

This is where yumweb is strongest:

- open a persistent browser once
- let the user log into real services
- come back later and continue from that logged-in state
- treat the browser like the agent’s local pair of hands

That makes it especially good for personal-assistant style tasks such as:

- checking X / LinkedIn / Facebook feeds
- reading Gmail / Outlook inboxes
- checking Amazon product pages or carts
- opening WeChat Web / social tabs the user already authenticated
- navigating real logged-in sites without rebuilding auth every run

The repo's [SKILL.md](SKILL.md) has YAML front-matter
(`name`/`description`/`argument-hint`) compatible with skill-loading agents
such as OpenClaw and GitHub Copilot. Point your agent at this directory and
it can discover the commands automatically.

A typical pattern an agent should follow:

1. Call `python scripts\yumweb.py status` (or `./scripts/run.sh status` on macOS/Linux) — if not running, call `start`.
2. For reading a URL, call `fetch <url>` and pipe the markdown to the LLM.
3. For X timeline / posting, use `x-read` / `x-post`.
4. For custom DOM extraction, write JS and call `eval` (it must return
   JSON-serializable data).
5. Prefer explicit `tab-switch <idx>` before `read` / `click` / `type` when multiple tabs are open; yumweb now persists the active tab between commands.

## Architecture

```
User / Agent
     |
     | (shell)
     v
scripts/yumweb.py  --[Playwright sync API]--> CDP @ 127.0.0.1:9333
                                                    |
                                                    v
                                        msedge.exe (--user-data-dir=./profile)
```

- `yumweb.py start` `Popen`s Edge detached with a unique profile dir.
- Every other command opens a fresh Playwright session, `connect_over_cdp()`s
  to port 9333, performs the action on the first non-`devtools://`/`edge://`
  page, prints the result, and exits.
- `browser.close()` after a CDP attach **only disconnects the client**; it
  does **not** kill the Edge instance.

## Security

- `profile/` contains live cookies and session data. The bundled `.gitignore`
  excludes it. Never commit, share, or upload that directory.
- The default single-profile setup means multiple sites may share one browser session. For higher isolation, run separate yumweb copies with different `profile_dir` values.
- `eval` executes arbitrary JavaScript in the active tab. Only call it with
  trusted input.
- The CDP port is bound to `127.0.0.1` only. Do not expose `9333` externally.

## License

MIT — see [LICENSE](LICENSE).
