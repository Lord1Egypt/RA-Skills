---
name: zhihu-publish-attach
description: Auto-publish Zhihu column articles on Linux (Chrome attach/VNC). Agent writes title+body then exec zhihu_publish.sh with --publish --submit. Triggers 知乎发帖, 发知乎, 知乎文章, 写一篇发知乎, 帮我发帖, zhihu publish, 发布到知乎, 自动发知乎.
metadata: {"openclaw":{"os":["linux"],"requires":{"bins":["python3","curl","unzip"]}}}
---

# Zhihu publish (Chrome attach / Linux VNC)

This skill is **self-contained**: everything runs from `{baseDir}/scripts/`. No other repository files are required.

Publish **column articles** (专栏) by attaching to Chrome on `127.0.0.1:9222` after the user logged in via VNC.

Uses **`exec`** + `bash {baseDir}/scripts/zhihu_publish.sh` — not Browser Relay (see ClawHub `zhihu-post` for Windows).

## First-time setup (after ClawHub install)

Run **once** on the Linux server:

```bash
bash {baseDir}/scripts/setup.sh
bash {baseDir}/scripts/install_chromedriver.sh
bash {baseDir}/scripts/start_chrome_debug.sh
```

In VNC: log in to Zhihu in that Chrome window.

Verify:

```bash
bash {baseDir}/scripts/zhihu_publish.sh --check --json
```

Expect: `"ok": true, "logged_in": true`.

Details: `{baseDir}/references/linux-vnc-setup.md`

## When to use

- Linux server + VNC, Chrome started with debug port **9222**
- Zhihu already logged in (or user can log in after `start_chrome_debug.sh`)
- User wants to publish with **title** + **body**

## Scripts in `{baseDir}/scripts/`

| Script | Purpose |
|--------|---------|
| `setup.sh` | `pip install --user` selenium + chmod (no sudo) |
| `install_chromedriver.sh` | Install chromedriver (once) |
| `start_chrome_debug.sh` | Start Chrome (VNC window) |
| `ensure_chrome_debug.sh` | Restart Chrome if closed (keeps login profile) |
| `zhihu_publish.sh` | **Agent entry** — always use this |
| `zhihu_attach_standalone.py` | Called by zhihu_publish.sh |

## Title and body (parameters)

| Parameter | How |
|-----------|-----|
| `--title "..."` | Required |
| `--body-file /path` | **Preferred** for long text — write file first, then pass path |
| `--body "..."` | Short text only |
| `--publish` | Open editor and fill |
| `--submit` | Click 发布 (real post; omit for dry-run) |
| `--json` | JSON result for the agent |
| `--no-ensure-chrome` | Skip auto-start (only if Chrome is already running) |

**Auto-start:** Every `zhihu_publish.sh` run **automatically** calls `ensure_chrome_debug.sh` first. If the user closed the browser, Chrome restarts in the background with the same profile (`~/.chrome-zhihu-automation`) — login usually persists. No need to pass a separate flag unless debugging.

**Never** put user content inside one shell string. Use separate exec args or `--body-file`.

## Where title and body come from (important)

This skill **does not** generate articles by itself. **You (the OpenClaw agent / LLM) supply them:**

| Field | Source |
|-------|--------|
| **Title** | User gives it explicitly, OR you draft a short headline from the topic (≤ 100 chars, no clickbait unless asked). |
| **Body** | User pastes it, OR you **write the full article** (Markdown/plain text) based on the user’s topic, then save to a file. |

Typical flow when the user says *「帮我写一篇关于 XX 发知乎」*:

1. Clarify topic, tone, length only if truly ambiguous (one short question max).
2. **Compose** title + article text yourself.
3. **Write file** e.g. `/tmp/zhihu_post_body.txt` (use your file/write tool — not inline in bash).
4. **Exec** `zhihu_publish.sh` with `--title`, `--body-file`, `--publish`, **`--submit`**, `--json`.

Do **not** ask the user to run bash commands. Do **not** put the article body in exec args.

## Agent workflow (default — auto publish)

**Default for normal user requests** (*发知乎 / 发帖 / 发布到知乎*): **skip `--check`**, go straight to publish with **`--submit`**.

Chrome is auto-started by `zhihu_publish.sh` if port 9222 is down.

### Step A — Prepare content (you do this)

1. Set `TITLE` (string).
2. Save full article to `/tmp/zhihu_post_body.txt` (UTF-8).

### Step B — One exec (publish + submit)

```bash
bash {baseDir}/scripts/zhihu_publish.sh \
  --publish \
  --title "TITLE" \
  --body-file /tmp/zhihu_post_body.txt \
  --submit \
  --json
```

### Step C — Read JSON and reply to user

- Success: `"ok": true`, `"published": true`, share `url` (should be `zhuanlan.zhihu.com/p/...` **without** `/edit`).
- Failure: explain `error` field; if login/session issue, tell user to log in via VNC once, then **retry Step B** (still no routine `--check`).

### Optional: dry-run only when user asks

Use **no** `--submit` only if the user says *预览 / 先填草稿 / 不要发布 / 我确认后再发*.

### Optional: `--check` only on failure

Run `--check --json` **only** when Step B returns login/API errors — not before every post.

## Exec example (default)

```
command: bash
args: [
  "{baseDir}/scripts/zhihu_publish.sh",
  "--publish",
  "--title", "今天我挺开心的",
  "--body-file", "/tmp/zhihu_post_body.txt",
  "--submit",
  "--json"
]
```

Write `/tmp/zhihu_post_body.txt` in a **separate** step before this exec.

## Chromedriver (version must match Chrome)

Selenium attach **requires** `chromedriver` even when Chrome is already running.  
Default install: **`~/.local/bin/chromedriver`** (no sudo). System-wide: `sudo env CHROMEDRIVER_INSTALL_DIR=/usr/local/bin bash .../install_chromedriver.sh`

```bash
bash {baseDir}/scripts/install_chromedriver.sh
bash {baseDir}/scripts/verify_chrome_stack.sh
```

If you installed Chrome via `dnf` RPM (e.g. 148.0.7778.215), chromedriver must be the **same** build from Chrome for Testing — see `{baseDir}/references/linux-vnc-setup.md`.

## Troubleshooting

| Symptom | Action |
|---------|--------|
| `chromedriver` not in PATH | `install_chromedriver.sh` (writes `scripts/chromedriver.env`) |
| `Permission denied` installing driver | Re-run `install_chromedriver.sh` (uses `~/.local/bin`); or `sudo` for `/usr/local/bin` |
| Version mismatch | `verify_chrome_stack.sh`; re-download driver for your `google-chrome-stable --version` |
| Cannot connect to 9222 | Usually auto-fixed on next `zhihu_publish.sh` run; or `ensure_chrome_debug.sh` |
| Browser closed | Auto-restart on publish; re-login in VNC only if `--check` returns 401 |
| Chrome starts but no window on VNC | Set `DISPLAY` for the OpenClaw/exec user (e.g. `export DISPLAY=:1`) |
| No selenium module | `bash {baseDir}/scripts/setup.sh` |
| `Permission denied` on pip install | Use `setup.sh` (installs to `~/.local`); do not run bare `pip install` as non-root |
| Python 3.6 | setup installs selenium 3.141.x automatically; attach script supports it |
| API 401 | Re-login in VNC |
| `--submit` but no publish | JSON `error`: `form_not_filled` / `publish_button_not_found` / `publish_not_confirmed`; check VNC + `scripts/screenshots/` |

## Safety

- Default **`--submit`** when the user wants a real post (normal 发知乎 / 发布 requests).
- Omit **`--submit`** only for explicit preview/draft requests.
- Do not publish unrelated or harmful content; follow the user’s topic.
- Wait ≥ 3 minutes between posts if publishing repeatedly.
