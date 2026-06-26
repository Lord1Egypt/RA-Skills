---
name: websearch-ddgs
description: Use a local DDGS MCP server (SSE) via mcporter to access fast web search tools (text/news/images/videos/books) without API keys. Use when user requests general web search, especially in automated/cron runs, images search, news search, videos search, books search.
metadata: {"clawdbot":{"emoji":"🔍","requires":{"bins":["mcporter", "python3"]},"install":[{"id":"brew","kind":"brew","formula":"steipete/tap/mcporter","bins":["mcporter"],"label":"Install mcporter (brew)"}]}}
---

# DDGS web search

## Setup: install `ddgs`, run MCP server (SSE), optionally keep it as a daemon
It is recommended to enable built-in `mcporter` skill.

### Install the Python package
```bash
python3 -m pip install -U ddgs
```

### Run the DDGS MCP server (SSE)
Foreground (good for debugging):
```bash
ddgs api --host 127.0.0.1 --port 8000
```
Detached/background mode (convenient on a dev machine):
```bash
ddgs api -d --host 127.0.0.1 --port 8000
```
Stop the detached server:
```bash
ddgs api -s
```

### Optional: systemd user service (always available)
Create `~/.config/systemd/user/ddgs.service`:
```ini
[Unit]
Description=DDGS MCP SSE server
After=network-online.target

[Service]
Type=simple
ExecStart=%h/.local/bin/ddgs api --host 127.0.0.1 --port 8000
Restart=on-failure
RestartSec=2

[Install]
WantedBy=default.target
```
Then:
```bash
systemctl --user daemon-reload
systemctl --user enable --now ddgs
systemctl --user status ddgs --no-pager
```

### Add the MCP server to mcporter
Add a named server pointing at the DDGS SSE endpoint:
```bash
mcporter config add ddgs http://127.0.0.1:8000/sse --allow-http
```
Verify it shows up:
```bash
mcporter config list ddgs
```
Then you can call tools as `ddgs.<tool>` (examples below).

Key idea:
- **DDGS runs an MCP SSE endpoint** at `http://127.0.0.1:8000/sse`
- **mcporter** connects to that endpoint and exposes tools like `ddgs.search_text_search_text_post`

## Defaults (use unless user says otherwise)
- `backend="duckduckgo"` (most reliable)
- `max_results=10` (“SERP page 1”)
- `region="us-en"`, `safesearch="moderate"`

## Workflow

### 0) Preconditions / sanity
1) Confirm DDGS server is up:
   - `curl -s http://127.0.0.1:8000/health`
2) Confirm mcporter can see the server:
   - `mcporter config list ddgs`

If the server is down, either:
- start/restore it (if you have permission), or
- use fallback (`web_search`).

### 1) Execution examples
Use mcporter to call DDGS tools and parse JSON.

Text search:
```bash
mcporter call ddgs.search_text_search_text_post \
  query="<query>" max_results=10 backend="duckduckgo" region="us-en" safesearch="moderate" --json
```

News search:
```bash
mcporter call ddgs.search_news_search_news_post \
  query="<query>" max_results=10 backend="bing" timelimit="w" --json
```

Images:
```bash
mcporter call ddgs.search_images_search_images_post \
  query="<query>" max_results=10 backend="duckduckgo" region="us-en" safesearch="moderate" --json
```

Videos:
```bash
mcporter call ddgs.search_videos_search_videos_post \
  query="<query>" max_results=10 backend="duckduckgo" region="us-en" safesearch="moderate" --json
```

Books:
```bash
mcporter call ddgs.search_books_search_books_post \
  query="<query>" max_results=10 backend="annasarchive" --json
```

## Available tools (via mcporter)
- `ddgs.search_text_search_text_post`
- `ddgs.search_images_search_images_post`
- `ddgs.search_news_search_news_post`
- `ddgs.search_videos_search_videos_post`
- `ddgs.search_books_search_books_post`

## Tool parameters
Common parameters (most endpoints):
- `query` — the search string.
- `max_results` — cap results; default 10 (fast, “page 1”).
- `backend` — engine selector. Prefer `duckduckgo` for reliability; `bing` as second choice; avoid `google` on servers (403/captcha risk)
- `region` — locale for results (e.g. `us-en`, `uk-uk`).
- `safesearch` — content filtering (`off|moderate|strict`); default `moderate`.

News-specific:
- `timelimit` — recency filter (commonly `d`, `w`, `m`, `y`).

Books-specific:
- recommended `backend` is `annasarchive`.

Tip: when you need reproducibility, explicitly pass `backend`, `region`, `safesearch`, `max_results` even if they match defaults.

## Troubleshooting
- `mcporter` says server not found → you’re using a different config file; if you use a non-default config, pass `--config` path from your system (default is `~/.openclaw/workspace/config/mcporter.json`).

- `backend="google"` often returns HTTP 403 in server environments → use another backend, e.g. `duckduckgo`/`bing`.
- Full API docs available locally at `http://localhost:8000/docs`.
