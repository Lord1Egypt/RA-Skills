---
name: scrapfly-cli
description: >-
  Use the Scrapfly CLI (`scrapfly`) to scrape web pages, capture screenshots,
  extract structured data with AI, crawl entire sites, and drive a cloud
  browser over CDP from a shell. JSON envelope on stdout for every command.
  Use when the user asks to "scrape a URL", "screenshot a page", "extract
  data from HTML", "crawl a site", "drive a browser with Playwright/CDP",
  "bypass anti-bot", or any task involving the `scrapfly` command.
---

# Scrapfly: Web Scraping, Rendering, and Browser Automation

Scrapfly gives AI agents and applications access to the web through five
products: scraping, screenshots, AI extraction, recursive crawling, and a
remote browser that you can drive directly over CDP, through a
persistent session daemon, or hand to an LLM agent.

This CLI, `scrapfly`, is the single surface over all five products plus a
Playwright-MCP-style agent mode. It speaks JSON by default so LLM callers
can pipe it directly.

## Installation

Pre-built binaries (macOS universal, Linux amd64/arm64, Windows amd64) on
the [Releases page](https://github.com/scrapfly/scrapfly-cli/releases). Or
from source:

```bash
go install github.com/scrapfly/scrapfly-cli/cmd/scrapfly@latest
```

## Six Usage Paths

**Path A (Fetch content):** `scrapfly scrape <url>` - the default. Covers
every `ScrapeConfig` field from the SDK:

- Render & navigate: `--render-js`, `--wait-for-selector`, `--rendering-wait`,
  `--rendering-stage`, `--auto-scroll`, `--js-file FILE`, `--js-scenario-file FILE`
- Anti-bot: `--asp`, `--cost-budget N`, `--proxy-pool`, `--country`, `--geolocation`
- Format & extraction: `--format markdown|clean_html|text|raw` + `--format-option`;
  `--extraction-prompt`, `--extraction-model`, `--extraction-template`,
  `--extraction-template-file FILE` (ephemeral inline template)
- Request shape: `--method`, `--header k=v`, `--cookie n=v`, `--body`,
  `--body-file`, `--data-file FILE` (structured body as JSON map), `--lang`,
  `--os`, `--browser-brand`
- Sessions & caching: `--session`, `--session-sticky-proxy`, `--cache`,
  `--cache-ttl N`, `--cache-clear`, `--retry=true|false`
- Screenshots on scrape: `--screenshot` (fullpage shortcut),
  `--screenshot-named name=selector` (repeatable), `--screenshot-flag FLAG`
- Observability: `--debug`, `--ssl`, `--dns`, `--correlation-id`, `--tag`,
  `--webhook NAME`, `--timing`
- Batch: multiple positional URLs or `--from-file PATH|-` + `--concurrency`
  (ndjson on stdout)
- Pipe-friendly: `--proxified` streams the raw upstream body with no JSON
  envelope

**Path B (Binary / structured outputs):** dedicated commands for focused
products.

- `scrapfly screenshot <url>` - PNG/JPG/WebP of the page or a selector.
  Full `ScreenshotConfig` surface: `--format`, `--capture`, `--resolution`,
  `--country`, `--option`, `--wait-for-selector`, `--rendering-wait`,
  `--auto-scroll`, `--js-file`, `--cache`, `--cache-ttl`, `--cache-clear`,
  `--webhook`, `--vision-deficiency`.
- `scrapfly extract --file page.html --prompt "..."` - run AI/template
  extraction on a document you already fetched. Full `ExtractionConfig`:
  body via `--file` or stdin; `--content-type`, `--url`, `--charset`,
  `--prompt | --model | --template | --template-file` (one of four
  extraction modes), `--compression`, `--webhook`, `--request-timeout`.
- `scrapfly crawl run <url> --max-pages N` - recursive crawls with status
  polling, content streaming, WARC/HAR artifacts. Post-download:
  `crawl parse har-list|har-get|warc-list|warc-get` reads the artifact
  directly (no separate tooling). See the Crawler section below.

**Path C (Interactive browser - one-shot):** mint a CDP WebSocket URL to
hand to Playwright, Puppeteer, or `browser-use`:

```bash
# plain session
scrapfly browser --pretty

# pre-navigate through /unblock so the target's anti-bot is bypassed
scrapfly browser https://target.example.com --unblock --country us --pretty
```

**Path D (Interactive browser - persistent daemon):** keep one CDP session
open across many CLI calls. Cookies, tabs, and AXTree refs all persist for
the daemon's lifetime. `--session` is needed only on `start`; subsequent
calls auto-resolve via `~/.scrapfly/sessions/.current`.

```bash
scrapfly browser --session demo --session-timeout 1800 start &
scrapfly browser navigate https://web-scraping.dev/login
scrapfly browser wait 'input[name=username]' --visible
scrapfly browser fill 'input[name=username]' user123
scrapfly browser fill 'input[name=password]' password
scrapfly browser click 'button[type=submit]'
scrapfly browser content --raw > page.html         # fully rendered HTML
scrapfly browser eval 'document.body.innerText'
scrapfly browser close                             # daemon + remote release
```

When running against Scrapfly's custom browser, `fill` / `click` /
`wait` / `slide` automatically use the **Antibot** CDP domain for
human-like timing; `content` uses **Page.getRenderedContent** which
inlines iframe content. Against a non-Scrapfly browser, the CLI falls
back to raw `Input.*` events.

**Path E (LLM agent):** `scrapfly agent "<task>" --url <target>` runs an
autonomous loop. The model picks tool calls (open, snapshot, click, fill,
scroll, screenshot, eval, unblock, done), the CLI executes them against
the Browser, and the result feeds back until the model calls `done`.
Providers are pluggable: Anthropic (default), OpenAI, Gemini, or local
(Ollama / OpenAI-compatible). AXTree-based observations keep the token
budget small.

**Path F (REST API only):** skip the CLI, call
`https://api.scrapfly.io/{scrape,screenshot,extraction,crawl}` directly
with `?key=<API_KEY>`. Official SDKs: Python, TypeScript, Go, Rust. See
[docs.scrapfly.io](https://scrapfly.io/docs).

**Path G (Alerting on account metrics):** `scrapfly alert ...` defines
threshold rules on Scrapfly's monitoring metrics (success rate, block
rate, error count, cost, latency, ...) and routes notifications via
email, webhook, or in-app. Enterprise plan; GATED behind the ALERTING
feature flag on customer accounts.

```bash
# Discover legal metrics
scrapfly alert metric-families

# Tune the threshold against the last 24h
scrapfly alert preview \
  --metric scrape.success_rate --comparator lt --threshold 95 \
  --sustained-minutes 10 --range-minutes 1440

# Create
scrapfly alert create \
  --name "Scrape Success Rate Low" \
  --metric scrape.success_rate --comparator lt --threshold 95 \
  --sustained-minutes 10 \
  --channel email:ops@example.com \
  --channel webhook:https://hooks.example.com/scrapfly
```

`alert list / get / update / snooze / unsnooze / test / delete / series
/ count-active` cover the rest of the lifecycle. Per-alert HMAC signing
keys are generated server-side and exposed via `alert get` for webhook
verification. Detailed reference: the
[scrapfly-alerting](../scrapfly-alerting/) skill.

**Path H (Scheduling recurring jobs):** `scrapfly schedule` plus the
per-product subgroups (`scrapfly scrape schedule`,
`scrapfly screenshot schedule`, `scrapfly crawl schedule`) define cron- or
interval-based recurring fires whose results are delivered to a webhook.

```bash
# Daily scrape schedule (config payload from a file, '-' for stdin)
scrapfly scrape schedule create --cron "0 6 * * *" \
  --webhook my-hook --config ./scrape.json

# Interval schedule with an inline payload
scrapfly crawl schedule create --interval 6 --unit hour \
  --webhook my-hook --config-inline '{"url":"https://example.com"}'

# Cross-product lifecycle (top-level group)
scrapfly schedule list [--status ACTIVE|PAUSED|CANCELLED]
scrapfly schedule get <id>
scrapfly schedule update <id> --set-recurrence --cron "0 */2 * * *"
scrapfly schedule pause <id>     # / resume <id>
scrapfly schedule execute <id>   # fire now, ignoring next_scheduled_date
scrapfly schedule delete <id>    # terminal, cannot be resumed
```

`--webhook` is required (it's where each fire's result lands).
`--cron` wins over `--interval`/`--unit`. `--retry-on-failure
--max-retries N` (0..3) and `--allow-concurrency` tune fire behavior.

**Path I (BYOP Exit Peer):** `scrapfly exit-peer` installs and runs the
Bring-Your-Own-Proxy connector that routes Scrapfly traffic through your
own network egress over an mTLS tunnel.

```bash
scrapfly exit-peer install            # download binary + per-customer cert bundle
scrapfly exit-peer run --name lab-01  # run the connector in the foreground
scrapfly exit-peer status             # local install state + cert lifetime
```

Install dir defaults to `$SCRAPFLY_BYOP_DIR` or `$HOME/.scrapfly/byop`.

## Authentication

Set once:

```bash
export SCRAPFLY_API_KEY=scp-live-...
# or, persisted:
scrapfly config set-key scp-live-...
# interactive (opens a browser to mint a key):
scrapfly auth login        # / logout / whoami
```

Resolution order: `--api-key` flag > `SCRAPFLY_API_KEY` env >
`~/.scrapfly/config.json`. Dev / self-hosted stacks: `--host` and
`--browser-host`, or `SCRAPFLY_API_HOST` / `SCRAPFLY_BROWSER_HOST`.

`scrapfly status` prints CLI version + auth state + account usage in one
call; `scrapfly account` shows plan, quota and subscription usage.

LLM providers for `agent` mode use their own env vars:
`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GEMINI_API_KEY`, or `OLLAMA_HOST`.
The CLI auto-detects the first one set.

## Output contract (for LLMs)

All commands emit a stable JSON envelope on stdout:

```json
{"success": true,  "product": "scrape", "data": { ... }}
{"success": false, "product": "scrape", "error": {"code": "...", "message": "...", "http_status": 422}}
```

Exit code is `0` on success, `1` on any error. `--pretty` swaps JSON for a
one-line human summary. Binary products (screenshots, crawl artifacts,
session recordings) require `-o <file>` or `-O <dir>` for the path; without
either, JSON mode returns base64. `browser content --raw` prints the HTML
body directly to stdout with no envelope (handy for pipes).

## Browser session reference

### Lifecycle
| Command | Purpose |
|---|---|
| `browser --session <id> start [--url <target> --unblock]` | Start daemon; foreground, background it with `&` |
| `browser status` | Print pid, ws_url, alive |
| `browser stop` | Shut down daemon only (remote session lives until timeout) |
| `browser close` | Shut down daemon **and** release Scrapfly's remote browser immediately |

### Actions (sent to the daemon; `--session` optional once `start` has run)
| Command | Notes |
|---|---|
| `browser navigate <url>` | Page.navigate + wait for load |
| `browser snapshot` | AXTree with refs (`e1`, `e2`, …) + `ax_node_id` + `backend_node_id` |
| `browser click <locator>` | Antibot.clickOn on CSS/XPath/axNodeId; raw click for refs |
| `browser fill <locator> <value> [--clear --wpm N]` | Antibot.fill on CSS/XPath/axNodeId; Input.insertText for refs |
| `browser click-ai <description>` | Resolve the target from a natural-language description via the LLM, then click |
| `browser fill-ai <description> <value>` | Resolve the target via the LLM, then fill |
| `browser wait <selector> [--visible --timeout-ms N]` | Antibot.waitForElement (native, no JS poll) |
| `browser slide <source> --target <sel> \| --distance <px>` | Antibot.clickAndSlide (slider captchas) |
| `browser scroll <direction> [--amount px --ref e3]` | Input wheel event |
| `browser screenshot [--fullpage]` | PNG via Page.captureScreenshot; use `-o/-O` for the file |
| `browser content [--raw] [--skip-iframes]` | Page.getRenderedContent - HTML with iframes inlined |
| `browser eval <js>` | Runtime.evaluate with awaitPromise |

### Locators

`click` / `fill` accept any of:
- **AXTree ref** - `e3`, taken from the last `snapshot`. Uses raw `Input.*` path.
- **CSS selector** (default) - `input[name=username]`
- **XPath** - `//button[text()="Submit"]` with `--selector-type xpath`
- **AX node id** - `42` from snapshot's `ax_node_id` field with `--selector-type axNodeId`
- **AI description** - `ai:<plain English>` (or the `click-ai` / `fill-ai`
  shortcuts) lets an LLM resolve the ref from the live snapshot.

For CSS/XPath/axNodeId the CLI goes through Antibot on Scrapfly's browser.

### Recordings, extensions

| Command | Purpose |
|---|---|
| `browser list` | List active Browser sessions on the account |
| `browser video <run-id>` | Download the session recording (webm); needs `-o`/`-O` |
| `browser playback <run-id>` | Fetch playback metadata for a debug run |
| `browser extensions list \| get <id> \| upload <path> \| delete <id>` | Manage account browser extensions (`.zip`/`.crx`) |

## Crawler reference

### Submit + poll
| Command | Purpose |
|---|---|
| `crawl start <url>` | Submit a crawl; print the UUID immediately |
| `crawl run <url>` | Submit + poll until DONE / FAILED / CANCELLED |
| `crawl watch <uuid>` | Live stats panel (visited/extracted/failed/skipped/queue/credits) until terminal |
| `crawl status <uuid>` | Fetch status; envelope exposes a top-level `terminal` field (`running\|done\|failed\|cancelled`) for shell scripting |
| `crawl urls <uuid> --status visited\|pending\|failed\|skipped` | Stream discovered URLs (paginated) |
| `crawl contents <uuid> --format markdown [--url URL --plain]` | Bulk JSON or single-URL plain body |
| `crawl contents-batch <uuid> <url...> [--from-file F] --format markdown` | One round-trip for up to 100 URLs |
| `crawl cancel <uuid>` | Stop a running crawl |
| `crawl artifact <uuid> --type warc\|har -o file` | Download the recording |

### Flags on `crawl start` / `crawl run`
Every documented `CrawlerConfig` field is exposed:

| Flag | Maps to |
|---|---|
| `--max-pages N` | `page_limit` |
| `--max-depth N` | `max_depth` |
| `--max-duration N` | `max_duration` (seconds, 15-10800) |
| `--max-api-credit N` | `max_api_credit` |
| `--exclude PATH` / `--include PATH` | `exclude_paths` / `include_only_paths` (repeatable, mutually exclusive) |
| `--ignore-base-path` | `ignore_base_path_restriction` |
| `--follow-external` / `--allowed-external-domain D` | `follow_external_links` / `allowed_external_domains` |
| `--follow-internal-subdomains true\|false` (tri-state) / `--allowed-internal-subdomain D` | matching fields |
| `--header k=v` (repeatable) | `headers` |
| `--delay MS` / `--user-agent UA` / `--max-concurrency N` / `--rendering-delay MS` | request shape |
| `--use-sitemaps` / `--ignore-no-follow` / `--respect-robots-txt true\|false` | strategy |
| `--cache` / `--cache-ttl S` / `--cache-clear` | caching |
| `--content-format F` (repeatable) / `--extraction-rules-file PATH` | content + extraction |
| `--asp` / `--proxy-pool P` / `--country CC` | scraping options |
| `--webhook NAME` / `--webhook-event E` (repeatable) | webhooks |

### Read from a WARC / HAR artifact

```bash
scrapfly crawl artifact <uuid> --type warc -o crawl.warc
scrapfly crawl parse warc-list crawl.warc --pretty             # URLs + statuses
scrapfly crawl parse warc-get crawl.warc https://example.com \
  --raw > page.html                                             # body straight to stdout

scrapfly crawl artifact <uuid> --type har -o crawl.har
scrapfly crawl parse har-list crawl.har --pretty               # request table
scrapfly crawl parse har-get crawl.har https://example.com/api \
  --raw | jq .                                                  # extract one response
```

`-` as the file path reads from stdin, so you can pipe straight from
`crawl artifact -o -`.

## Core API Endpoints

| Product | Endpoint | CLI |
|---|---|---|
| Web Scraping | `GET/POST /scrape` | `scrapfly scrape <url>` |
| Screenshot | `POST /screenshot` | `scrapfly screenshot <url>` |
| Extraction | `POST /extraction` | `scrapfly extract` |
| Crawler | `POST /crawl` + `/crawl/{uuid}/{status,urls,contents,artifact}` | `scrapfly crawl {start,run,status,urls,contents,cancel,artifact}` |
| Browser (CDP) | `wss://browser.scrapfly.io?api_key=...` | `scrapfly browser` |
| Browser Unblock | `POST /unblock` | `scrapfly browser <url> --unblock` |
| Browser Session Stop | `POST /session/{id}/stop` | `scrapfly browser close` |
| Session Recording | `GET /run/{id}/video` | `scrapfly browser video <run-id>` |

## Quick examples

```bash
# Scrape a JS-heavy page with anti-bot and markdown output
scrapfly scrape https://web-scraping.dev/products --render-js --asp --format markdown

# Scrape many URLs in parallel (ndjson on stdout, one envelope per line)
scrapfly scrape https://web-scraping.dev/products \
               https://web-scraping.dev/product/1 \
               https://web-scraping.dev/product/2 \
               --format markdown --concurrency 5

# Or feed URLs from a file
scrapfly scrape --from-file urls.txt --format markdown | jq -c '.data.result.url'

# Pipe scrape body straight into AI extraction
scrapfly scrape https://web-scraping.dev/product/1 --render-js --proxified \
  | scrapfly extract --content-type text/html --prompt "name, price, sku"

# Screenshot into an auto-named file in a directory
scrapfly -O ./shots screenshot https://example.com --resolution 1920x1080

# Crawl synchronously with markdown content streaming
scrapfly crawl run https://example.com --max-pages 20 --content-format markdown

# Multi-call browser session: log in, dump rendered HTML, clean up
scrapfly browser --session demo --session-timeout 1800 start &
scrapfly browser navigate https://web-scraping.dev/login
scrapfly browser wait 'input[name=username]' --visible
scrapfly browser fill 'input[name=username]' user123 --wpm 280
scrapfly browser fill 'input[name=password]' password
scrapfly browser click 'button[type=submit]'
scrapfly browser content --raw > after-login.html
scrapfly browser close

# Hand a Scrapfly-unblocked CDP URL to browser-use
WS=$(scrapfly browser https://target.example.com --unblock --country us --pretty | jq -r .ws_url)
python examples/browser-use-with-scrapfly.py   # reads WS from scrapfly CLI

# LLM agent with structured output
ANTHROPIC_API_KEY=... scrapfly agent "Name and price of the first product" \
  --url https://web-scraping.dev/products \
  --schema '{"type":"object","properties":{"name":{"type":"string"},"price":{"type":"string"}},"required":["name","price"]}'
```

## Shell completion

Cobra ships completion scripts for bash, zsh, fish, and PowerShell. Install once:

```bash
# zsh
scrapfly completion zsh > "${fpath[1]}/_scrapfly"
# bash
scrapfly completion bash > /etc/bash_completion.d/scrapfly  # or ~/.bash_completion.d/
# fish
scrapfly completion fish > ~/.config/fish/completions/scrapfly.fish
```

## MCP server

`scrapfly mcp serve` exposes `scrape`, `screenshot`, `extract`, `crawl_run`,
and `selector` as MCP tools over stdio. Add the binary to a compatible
client (Claude Desktop, Cursor, Claude Code):

```jsonc
{
  "mcpServers": {
    "scrapfly": {
      "command": "scrapfly",
      "args": ["mcp", "serve"],
      "env": { "SCRAPFLY_API_KEY": "scp-live-..." }
    }
  }
}
```

Selector discovery also works from inside the agent loop via the
`find_selector` tool - useful when the model wants to produce a durable
CSS selector instead of relying on per-snapshot refs.

## Reference

- Docs: https://scrapfly.io/docs
- SDKs: https://scrapfly.io/docs/sdk
- CLI source + examples: https://github.com/scrapfly/scrapfly-cli
