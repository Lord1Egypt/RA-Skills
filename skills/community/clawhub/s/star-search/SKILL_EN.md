---
name: star-search-en
description: "Comprehensive web search + LLM-answer engine. Use when asked to search the web, find online information, research topics, get news, look up Chinese content, or check A股/finance/tech news. **v20.7 — Speed/Streaming/Multi-turn/Stable/Academic/Structured/Favorites/Monitoring/Claude Desktop MCP**! star-search is a standard Model Context Protocol server (4 tools: web_search/web_search_news/web_search_finance/get_engines) callable by Claude Desktop / Cursor / Hermes. Public HTTP/SSE: https://search.token-star.cn/mcp/sse . v20 features (实战 35-48): speed optimization 6s→0.2s + SSE streaming (first token <1s) + multi-turn dialogue (history injection) + ultimate stability (killed watchdog) + academic/code 4 engines (Sourcegraph available) + structured output 4 formats (default/table/json/mermaid) + history/favorites localStorage + /metrics Prometheus endpoint + monitoring alert service + Prometheus + Grafana public HTTPS. 16 engines (11 HTTP + 5 RSS) + intelligent routing (finance query auto-finance mode) + starry-sky frontend UI + systemd user daemon + OpenAI API. Goal: free Chinese alternative to Baidu search + LLM agent real-time fact layer (free Chinese version of Tavily/Perplexity)."
version: 20.7.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [Search, Web, Bing, Sogou, Baidu, 360, Weixin, Toutiao, Zhihu, GitHub, China, Hybrid, HTTP, Playwright, Chinese, Cache, API, OpenAI, Cron, Incremental, CSDN, Cnblogs, Eastmoney, CLS, Sina, Sohu, Quality, Explain, Debug, RSS, Ithome, 36kr, Sspai, Oschina, Woshipm, Global, Public, HTTPS, Frontend, SmartRouting, Finance, MCP, JSON-RPC, SSE, LLM-Answer, Perplexity-Mode, Honest-LLM, Honest-Search, v20, Speed-Optimization, Streaming, Multi-Turn, Monitoring, Prometheus, Grafana, Structured-Output, Favorites, Academic-Search, Code-Search, English]
    related_skills: [arxiv, blogwatcher, session_search, commercial-opportunity-research, ai-api-relay-station, building-mcp-servers, native-mcp]
    references:
      - v16-v17-legacy-archive.md
      - v16-finance-mode-and-smart-routing.md
      - v16-public-deployment-and-daemon.md
      - v17-frontend-answer-card.md
      - v17-llm-answer-quality-strategy.md
      - mcp-server-zero-deps.md
      - site-bing-proxy-pattern.md
      - incremental-cache-pattern.md
      - llm-answer-honest-prompt.md
---

# Star Search v20.7.0 — Speed / Streaming / Multi-turn / Stable / Academic / Structured / Favorites / Monitoring — Integrated Chinese Search + LLM Answer

**A single script to replace Baidu Search API + Answer + Monitoring. Free, multi-engine, high quality, serve subagents.**

> This skill has evolved from v8.3 (Camofox) to v20.7.0 (HTTP+Playwright hybrid + intelligent routing + public deployment + LLM answer + SSE streaming + multi-turn + Prometheus monitoring). Complete v16-v17 chapters are archived in `references/v16-v17-legacy-archive.md`. GitHub: https://github.com/muchenhengxin/Star @ commit da860bf (v20.7.0). Public: https://search.token-star.cn (HSTS + LE cert + nginx reverse proxy).

---

## 🔥 v20.7.0 Key Upgrades (P0-1 through P0-5 + P3-21/25/47/48)

| Practice | Upgrade | Value | Performance Change |
|---|---|---|---|
| **35** | Speed optimization (search layer) | playwright skip + 4s top-level timeout + cache hit | **6s → 0.2-1s** |
| **36** | SSE streaming output | `POST /v1/search/stream` + 5 events + first token < 1s | **First byte 11s → < 1s** |
| **37** | Answer layer acceleration | `max_tokens=300` + `LLM_TIMEOUT=25s` | **7-8s complete** |
| **38-39** | Multi-turn dialogue | `session_id` + `history` + localStorage | **6 turns context** |
| **40** | Ultimate stability | killed `/tmp/watchdog.sh` (6/3 deployment leftover) | **NRestarts=0** |
| **41-43** | Academic/code + structured + favorites | 4 engines + 4 formats + ⭐ button | **3 major features** |
| **44-46** | Monitoring + Prometheus + Grafana | `/metrics` + 8 alerts + 11 panel dashboard | **Public HTTPS** |
| **47** | Sourcegraph 4 bug fix + Semantic Scholar | text=True/returncode/POST→GET/SSE parser + x-api-key header | **1/4 engines recovered** |
| **48** | Claude Desktop MCP integration | stdio + SSE dual transport, 4 tools tested 301ms | **Public tutorial** |

---

## 🏗️ Architecture (v20.7)

```
[Browser] → https://search.token-star.cn:443
    ↓ (nginx + LE cert)
[/var/www/star-search/index.html]    ← 49KB frontend (streaming/favorites/history/format switch)
    ↓ (location /v1/ / /mcp/ / /v1/search/stream SSE)
[FastAPI 127.0.0.1:<api-port>]     ← api_server.py (systemd user)
    ├─ 16 engines (9 HTTP enabled + 4 PW skipped + 3 cache)
    ├─ answer.py (GLM-4-Flash summarization, honest-first)
    ├─ metrics.py (Prometheus metrics, 14 indicators)
    ├─ academic_code.py (4 engines)
    ↓
[LLM API: https://api.token-star.cn/v1]   ← GLM-4-Flash (permanently free)
[Prometheus + Grafana + node-exporter]     ← 9090/3000/9100 (public HTTPS)
[star-search-monitor.service]             ← Monitoring alerts (user systemd)
```

---

## 6 Major Capability Modules (v20.7)

### 1. Speed & Streaming (P0-1, 实战 35-37)

- **Search layer 0.2-1s**: playwright 4 engines skip + 4s top-level timeout + cache hit 0ms
- **Answer layer 7-8s**: `max_tokens=300` + `LLM_TIMEOUT=25s` + 30min cache
- **SSE streaming**: `POST /v1/search/stream` returns 5 events (`search_start` / `search_done` / `answer_chunk×N` / `answer_done` / `done`)
- **First token < 1s**: frontend fetch + ReadableStream SSE parsing, character-by-character display

### 2. Multi-turn Dialogue (实战 38-39)

- **API fields**: `session_id` + `history: [{q, a}, ...]`
- **Backend**: `generate_answer(history)` splices into prompt (`=== Previous conversation ===\nUser: ...\nAssistant: ...\n---`)
- **Frontend**: localStorage stores `chat:{session_id}:history` (last 20 turns) + left session list

### 3. Ultimate Stability (实战 40)

- **systemd daemon**: `stardust-svc.service` (user systemd + linger) + `Restart=always`
- **Killed 6/3 leftover watchdog**: `/tmp/watchdog.sh` ran 11 days, miskilled 39 times → `kill -9` + `rm` fix
- **uvicorn logging force=True**: avoid root logger override causing detail.log 0 bytes
- **Tested**: 7 queries run, NRestarts=0 stable

### 4. Academic / Code / Structured / Favorites (实战 41-43)

- **Academic/code 4 engines**: `google_scholar` / `semantic_scholar` / `grep_app` / `sourcegraph` (independent module `academic_code.py`)
  - Actual: 1/4 available (Sourcegraph; other 3 limited by GFW / rate limiting / anti-scraping)
- **Structured output 4 formats**: `default` / `table` / `json` / `mermaid` (LLM fully complies)
  - Pydantic avoid reserved name `format` → rename to `fmt`
  - cache key includes `fmt` (4 formats independent cache)
- **History/favorites UI**: top bar 📚 history + ⭐ favorites 2 buttons + per-result ⭐ button + overlay + localStorage

### 5. Monitoring Alerts (实战 44-45)

- **`/metrics` endpoint**: pure Python 14 indicators (QPS / P99 / cache hit rate / error count / LLM latency)
- **`star-search-monitor.service`**: user systemd + linger + 3 alert rules + 5min summary
- **Alert rules**: error rate > 20% / cache hit rate < 10% / fetch failed 3 times

### 6. Prometheus + Grafana (实战 46)

- **3 docker containers**: `star-prometheus` v2.54.1 (9090) / `star-grafana` v11.2.0 (3000) / `star-node-exporter` v1.8.2 (9100)
- **8 alert rules**: error rate / cache / service down / P99 / CPU / memory / disk
- **Grafana 11 panel dashboard**: QPS / cache rate / latency / CPU / memory / disk
- **Public HTTPS**: `prom.token-star.cn` + `grafana.token-star.cn` (certbot + nginx 80/443 reverse proxy)

---

## 🚀 Quick Start

### 1. Web UI (recommended, browser direct)

```
https://search.token-star.cn
```

- Single query / multi-turn dialogue / SSE streaming / 4 format switching
- Top 📚 history + ⭐ favorites
- Per-result ⭐ favorite
- Embedded answer AI card + source chips + citation chip

### 2. API Endpoints

| Endpoint | Purpose | Latency | Cache |
|---|---|---|---|
| `POST /v1/search` | Normal search | 0.2-8s | 30min |
| `POST /v1/search/stream` | **SSE streaming** | First token < 1s | 30min |
| `POST /v1/answer` | Answer only (custom results) | 7s | 30min |
| `POST /v1/scholar` | Academic search | 4s | - |
| `POST /v1/code` | Code search | 4s | - |
| `POST /v1/academic_mode` | Mode detection | < 100ms | - |
| `GET /v1/health` | Health check | < 10ms | - |
| `GET /v1/modes` | List modes | < 10ms | - |
| `GET /v1/engines` | List engines | < 10ms | - |
| `GET /metrics` | Prometheus metrics | < 100ms | - |
| `SSE /mcp/sse` | MCP server (4 tools) | - | - |
| `POST /mcp/messages` | MCP client | - | - |

### 3. CLI Mode

```bash
# Normal search
python3 search.py "AI large models"                              # English→global
python3 search.py "asyncio vs threading"                          # English→global
python3 search.py "today stock market"                           # v20 intelligent routing auto finance
python3 search.py "Huawei HarmonyOS" --mode deep --recency=week # deep + recency

# Structured output
python3 search.py "A-share Top10" --format table
python3 search.py "MCP servers" --format json | jq .
python3 search.py "deployment process" --format mermaid

# Multi-turn
python3 search.py "BYD stock price" --session mysession
python3 search.py "compare with Tesla" --session mysession

# Favorites
python3 search.py "BYD stock price" --star
```

### 4. MCP Integration (Claude Desktop / Cursor / Hermes / Cline / Continue)

#### 4.1 stdio mode (local, simplest)

**Claude Desktop config**:

```json
// macOS: ~/Library/Application Support/Claude/claude_desktop_config.json
// Windows: %APPDATA%/Claude/claude_desktop_config.json
{
  "mcpServers": {
    "star-search": {
      "command": "/usr/bin/python3",
      "args": ["/home/ubuntu/star-search/mcp/mcp_server.py"],
      "env": {
        "STAR_SEARCH_API": "http://127.0.0.1:5000/v1/search",
        "PYTHONPATH": "/home/ubuntu/.local/lib/python3.10/site-packages"
      }
    }
  }
}
```

**Hermes agent / Cursor / Cline**:

```json
{
  "mcpServers": {
    "star-search": {
      "command": "python3",
      "args": ["/path/to/mcp_server.py"],
      "env": {
        "STAR_SEARCH_API": "http://127.0.0.1:5000/v1/search"
      }
    }
  }
}
```

**Key**:
- `PYTHONPATH` must include aiohttp venv path (local dev needs `pip install aiohttp`)
- `STAR_SEARCH_API` points to your star-search API server (default `http://127.0.0.1:5000/v1/search`)
- Restart Claude Desktop to take effect

#### 4.2 SSE public mode (remote, cross-device)

**Public endpoints**:
```
Health: https://search.token-star.cn/mcp/health
SSE:    https://search.token-star.cn/mcp/sse
POST:   https://search.token-star.cn/mcp/messages?session_id=<get from SSE-pushed endpoint URL>
```

**Python client example**:

```python
import aiohttp, json

async with aiohttp.ClientSession() as s:
    # 1. SSE handshake - server pushes "event: endpoint\ndata: <URL>?session_id=XXX"
    async with s.get("https://search.token-star.cn/mcp/sse") as r:
        line = await r.content.readline()  # event: endpoint
        line = await r.content.readline()  # data: <URL>?session_id=XXX
        endpoint = line.decode().replace("data: ", "").strip()

    # 2. initialize
    req = {
        "jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {"protocolVersion": "2025-06-18"}
    }
    await s.post(endpoint, json=req)

    # 3. Read SSE response to get session_id
    # ...

    # 4. tools/call
    req = {
        "jsonrpc": "2.0", "id": 2, "method": "tools/call",
        "params": {"name": "web_search", "arguments": {"query": "BYD stock price"}}
    }
    await s.post(messages_url, json=req)
```

**Key pitfall** — Client must NOT hard-code session_id:
- **Must use server-pushed session_id** (extract `?session_id=XXX` from SSE endpoint URL)
- **Don't** generate UUID yourself
- Hard-code → will 400 `Invalid session_id`

#### 4.3 Tested Performance

| Tool | query | Latency | Result |
|---|---|---|---|
| `web_search` | "BYD stock price" | 301ms | 8 results (Sina/EastMoney/Zhihu/investing/Xueqiu/10jqka/9fzt) |
| `web_search_finance` | "Shanghai Index today close" | 870ms | 8 results (4074.74 etc.) |
| `web_search_news` | "AI startups" | 280ms | 8 results from IT之家 tech news |
| `get_engines` | - | <10ms | 16 engine list |

#### 4.4 4 MCP Tools

| Tool | Purpose | Engines |
|---|---|---|
| `web_search` | General search (intelligent recognition of finance/English/Chinese) | Default deep + finance auto-finance |
| `web_search_news` | Tech/AI/product news | csdn/cnblogs + 5 RSS (ithome/36kr/sspai/oschina/woshipm) |
| `web_search_finance` | Finance/stock/A股 dedicated | eastmoney/cls/sina_finance/sohu/baidu/weixin/bing_cn |
| `get_engines` | List 16 engines + 5 modes (for agent decision-making) | - |

**LLM agent call examples** (Claude Desktop / Cursor):
```
"Help me search for BYD stock price, use web_search tool"
"Use web_search_finance to find Shanghai Index"
"Use web_search_news to find today's AI startup news"
"List all engines with get_engines"
```

---

## ⚙️ Key Parameters

### Search Layer

| Parameter | Default | Description |
|---|---|---|
| `--mode` | `auto` | deep / quick / news / dev / global / finance / auto |
| `--engine` | auto | Single engine specification (sogou / baidu / weixin / ...) |
| `--top` | 10 | Number of results (max 30) |
| `--recency` | none | day / week / month / year |
| `--exact` | False | Exact match |
| `--sources` | none | Restricted sources (weixin,baidu,...) |
| `--format` | `default` | `default` / `table` / `json` / `mermaid` |
| `--star` | False | Add to localStorage favorites |
| `--session` | auto-generated | Multi-turn session_id |

### Answer Layer

| Parameter | Default | Description |
|---|---|---|
| `--answer` | True | Whether to generate LLM answer |
| `LLM_MODEL` | `glm-4-flash` | LLM model (GLM-4-Flash permanently free) |
| `LLM_TIMEOUT` | 25 | Answer timeout (seconds) |
| `max_tokens` | 300 | Answer length (GLM-4 not strict) |
| `ANSWER_CACHE_TTL` | 1800 | Answer cache TTL (seconds) |

### Monitoring Layer

| Metric | Type | Description |
|---|---|---|
| `star_search_requests_total` | counter | Request count (by endpoint) |
| `star_search_request_errors_total` | counter | Error count |
| `star_search_search_total` | counter | Search count |
| `star_search_cache_hit_rate` | gauge | Cache hit rate (0-1) |
| `star_search_search_latency_ms` | histogram | Search P50/P95/P99 |
| `star_search_answer_latency_ms` | histogram | Answer P50/P95/P99 |
| `star_search_llm_latency_ms` | histogram | LLM P50/P95/P99 |

---

## 📦 Deployment

### 1. systemd user (recommended)

```ini
# ~/.config/systemd/user/stardust-svc.service
[Unit]
Description=star-search API + monitor
After=network.target

[Service]
Type=simple
WorkingDirectory=/home/ubuntu/star-search
ExecStart=/usr/bin/python3 scripts/api_server.py --host 127.0.0.1 --port 5000
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
```

```bash
systemctl --user daemon-reload
loginctl enable-linger ubuntu  # Boot auto-start + logout auto-start
systemctl --user enable --now stardust-svc.service
```

### 2. Prometheus + Grafana

```bash
cd /home/ubuntu/docker
docker compose -f prometheus-grafana-stack.yml up -d
```

### 3. Public HTTPS

```bash
# DNSPod A record
prom.token-star.cn   → <server IP>
grafana.token-star.cn → <server IP>

# certbot SSL
certbot --nginx -d prom.token-star.cn -d grafana.token-star.cn \
  --non-interactive --agree-tos -m <your-email>
```

---

## 🔌 Dependencies

```bash
pip install aiohttp beautifulsoup4 lxml playwright fastapi uvicorn 'pydantic>=2' httpx requests
playwright install chromium  # Optional (v20 实战 35 skipped)
```

No API Key, no login, no payment required (GLM-4-Flash via `api.token-star.cn/v1` permanently free).

---

## ⚠️ Known Pitfalls (v20 实战 35-48 Summary)

### v20.1 Speed Optimization (实战 35)

- **playwright drags 15-20s** → skip 4 engines
- **aiohttp single engine 4s timeout** + top-level 4s forced cutoff
- **try/except degrade** to cache hit

### v20.2 SSE Streaming (实战 36)

- **f-string pitfall**: `"event: done\ndata: {}\n\n"` empty `{}` reports SyntaxError
- **nginx required**: `proxy_buffering off` + `proxy_read_timeout 60s` + `proxy_http_version 1.1`

### v20.3 Answer Layer Acceleration (实战 37)

- **max_tokens 600 → 300**: GLM-4-Flash 46 tok/s × 300 = 6.5s actual (set 600 actual 947 tokens)
- **LLM_TIMEOUT 8 → 12 → 25**: complex formats (json/mermaid) need 25s buffer

### v20.4-5 Multi-turn + Stability (实战 38-40)

- **NRestarts up must find real culprit**: 实战 40 watchdog.sh 6/3 leftover 11 days miskilled 39 times
- **uvicorn logging must force=True**: avoid root logger override causing detail.log 0 bytes
- **cache key excludes history**: hit rate 30-50% (vs 80% with history)

### v20.6 Academic/Structured/Favorites (实战 41-43)

- **Pydantic avoid reserved name**: `format` is reserved → rename to `fmt`
- **New parameter full-chain grep**: 实战 42 `/v1/search` add fmt but `/v1/search/stream` not → 6 debug rounds
- **cache key must include all change factors**: cache key missing fmt → 4 formats hit same cache
- **GFW environment external APIs limited is norm**: 实战 41 4 engines only 1 available

### v20.7 Monitoring Alerts (实战 44-46)

- **docker container mount data dir**: `user:"0"` + `chmod 777` solve mmap permissions
- **docker image acceleration**: Docker Hub direct timeout → `daemon.json` add `daemonocloud.io`
- **Tencent Cloud firewall**: only 22/80/443 open (direct 9090/3000 not, use nginx reverse proxy)
- **DNSPod A record required**: not added won't take effect

### v20.7.1 Sourcegraph Fix (实战 47)

- **text=True SSE parsing error**: SSE chunked stream occasionally decodes wrong, use bytes + decode utf-8
- **curl returncode=28 timeout but stdout has data**: don't check returncode, just check stdout non-empty
- **POST → GET**: `sourcegraph.com/.api/search/stream` POST returns 404, GET returns SSE
- **SSE parser logic**: actual event type is `content` (not `match`), need `data: ` prefix strip + check `repository` field

### v20.7.2 MCP Integration (实战 48)

- **aiohttp not in /usr/bin/python3 default path**: must set `PYTHONPATH=/home/ubuntu/.local/lib/python3.10/site-packages`
- **Hard-code session_id → 400 Invalid session_id**: SSE mode must use server-pushed session_id from endpoint URL

---

## 📁 File Structure (v20.7)

```
star-search/
├── SKILL.md                      # Main file (v20.7.0, Chinese)
├── SKILL_EN.md                   # English version (v20.7.0)
├── index.html                    # v20.7 frontend (49KB, multi-turn/favorites/format switch)
├── README.md                     # GitHub README
├── search.py                     # v20.7 main search (16 engines + speed optimization)
├── answer.py                     # v20.7 answer layer (GLM-4 + 4 formats + citations + multi-turn)
├── api_server.py                 # v20.7 API server (SSE + multi-endpoint)
├── academic_code.py              # v20.7 academic/code 4 engines
├── metrics.py                    # v20.7 Prometheus metrics (14 indicators)
├── mcp_server.py                 # v20.7 MCP server (4 tools)
├── mcp_*.py                      # v20.7 MCP client
├── scripts/
│   ├── cron_refresh.py           # Scheduled incremental client
│   ├── deploy_web.sh             # nginx deployment
│   ├── star_search_monitor.py    # v20.7 monitoring alert service
│   └── ...
├── references/
│   ├── v16-v17-legacy-archive.md       # v16-v17 complete chapter archive
│   ├── v16-finance-mode-and-smart-routing.md
│   ├── v16-public-deployment-and-daemon.md
│   ├── v17-frontend-answer-card.md
│   ├── v17-llm-answer-quality-strategy.md
│   ├── mcp-server-zero-deps.md
│   ├── site-bing-proxy-pattern.md
│   ├── incremental-cache-pattern.md
│   └── llm-answer-honest-prompt.md
├── /etc/systemd/user/stardust-svc.service   # systemd unit
├── /etc/nginx/sites-enabled/search-token-star.conf
├── /var/www/star-search/index.html
├── /home/ubuntu/docker/prometheus-grafana-stack.yml
└── /home/ubuntu/star-search/.env
    LLM_BASE_URL=https://api.token-star.cn/v1
    LLM_MODEL=glm-4-flash
    LLM_TIMEOUT=25
    ANSWER_CACHE_TTL=1800
    SEMANTIC_SCHOLAR_API_KEY=<your-token>  # Apply at https://www.semanticscholar.org/product/api
```

---

## 🔄 Version History

| Version | Date | Major Changes |
|---|---|---|
| **v20.7.0** | 2026-06-15 | **实战 47-48**: Sourcegraph 4 bug fix + Claude Desktop MCP integration tutorial + 1M token API rate limit |
| v20.6.0 | 2026-06-15 | 实战 35-46: speed optimization + SSE streaming + multi-turn + ultimate stability + academic/code + structured output 4 formats + history/favorites + monitoring + Prometheus + Grafana |
| v17.7.0 | 2026-06-04 | Answer cache (236x speedup) + inline citations (Perplexity Mode complete) |
| v17.5.0 | 2026-06-04 | 4 prompt templates (finance/tech/news/general) |
| v17.4.0 | 2026-06-04 | Multi-turn followup (3 followup chips) |
| v17.3.0 | 2026-06-04 | Frontend AI answer card (Perplexity Mode UI) |
| v17.2.0 | 2026-06-03 | LLM answer layer (GLM-4-Flash permanently free) |
| v17.0.0 | 2026-06-03 | **MCP integration**: 4 tools (web_search / web_search_news / web_search_finance / get_engines) |
| v16.2.5 | 2026-06-03 | finance engine fix Chinese financial search results |
| v16.2.2 | 2026-06-03 | Public frontend + finance intelligent recognition + Playwright graceful degradation |
| v16.2.1 | 2026-06-03 | Public HTTPS + frontend cultural style + daemon process |
| v16.1 | 2026-06-02 | +5 RSS engines + global English-Chinese dual source + finance mode |
| v15.0 | 2026-06-01 | 10 engines direct search + scheduled incremental: toutiao/zhihu/weixin |
| v14.0 | 2026-06-01 | OpenAI API + incremental append |
| v13.0 | 2026-06-01 | Smart cache layer (bucketed TTL + query normalization) |
| v12.2 | 2026-06-01 | Smart deduplication + ⭐ cross-source marking |
| v8.3 | 2026-05-10 | Flagship version (Camofox era, deprecated) |

Complete v16-v17 chapters see `references/v16-v17-legacy-archive.md`.

---

## 📚 Practice Notes (v20 实战 35-48)

以下是实战过程的详细笔记，对应每个升级的 troubleshooting 路径。

