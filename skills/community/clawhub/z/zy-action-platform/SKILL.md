---
name: zy-action-platform-en
display_name: ZY Action Platform Assistant
display_name_en: ZY Action Platform Assistant
description: "Connect and operate ZY Action Platform (AI Business Action System): guide verified install & DeepSeek key config, then health-check/login and, across the five products AIP/Foundry/Gotham/Apollo/Swift, run natural-language data queries, list/run automation workflows, query datasets/ontology, search intel, inspect deployments and more. Enforces HTTPS-only remote transport, origin-bound tokens and write confirmations."
description_zh: "连接并操作 ZY Action Platform（AI 商业行动系统）：引导本机下载安装与 DeepSeek Key 配置；支持账号登录（令牌与源严格绑定），并跨五个产品完成健康检查、自然语言查数、工作流、数据集与本体查询、情报搜索、部署查看等常用操作。"
description_en: "Connect ZY Action Platform. Guide verified install & API key setup, then log in and operate all five products: NLQ data query and workflow automation on AIP, datasets/ontology on Foundry, intel search/graph on Gotham, deployments on Apollo, health on Swift. Remote access is HTTPS-only with origin-bound tokens and explicit write confirmation."
category: analytics
version: 1.1.0
author: ZY Tech (zyinfo.pro)
allowed-tools: Bash, Read, Grep, Glob
---

# ZY Action Platform Data & Automation Assistant

## 1. Skill Overview & Trigger Words

This skill helps you operate the in-house enterprise data intelligence platform **ZY Action Platform (AI Business Action System)**: from "download & install (with integrity verification) and API-key configuration" to "connect & log in, query data, run automations, inspect deployments/intel". Activate this skill when the user mentions "ZY Action", "AI Business Action System", "Action Platform", or expresses intents like **query data/analytics, run workflows/automations, list datasets/ontology/metrics, search intel/entities, check deployment status**, in the context of a locally installed (or to-be-installed) platform. Politely decline unrelated requests.

The platform ships five independently runnable backend products (all started together by the one-click launcher; default ports below):

| Product | Code | Port | One-line capability |
| --- | --- | --- | --- |
| LightAIP | aip | 18080 | NLQ data query, automation workflows, datasources |
| LightFoundry | foundry | 18081 | Data integration, datasets, ontology/metrics, semantic search |
| LightApollo | apollo | 18082 | Deployment platform: desired state / deployments / drift / bundles / Spoke |
| LightGotham | gotham | 18083 | Intelligence analysis: search / knowledge graph / resolved entities / geo-temporal / reports |
| LightSwift | swift | 18084 | Onboard settlement (health check only in this skill) |

## 2. Runtime & Ground Rules

- All platform calls go through the script `scripts/zy_platform.py` (pure Python standard library). Invocation: `python3 scripts/zy_platform.py <command> --product <product> [args]`; use `python` on Windows when `python3` is missing. If the script cannot run, tell the user Python 3 is missing or the path is wrong.
- Run the script and read its JSON output first, then summarize for the user in their language; never fabricate API results.
- `--product` defaults to `aip`; the product port is the default `--base-url` (`http://127.0.0.1:<port>`), so you usually don't pass it. For cross-machine/gateway access pass `--base-url`, and **remote addresses must be https** (see sections 7 and 8).
- The script prints JSON to stdout only; errors go to stderr prefixed with `[zy_platform]`. Exit codes: 0 success / 1 argument error or local/security-policy refusal / 2 network unreachable or timeout (including certificate failure) / 3 HTTP error / 4 auth failure (401) / 5 business failure (envelope code≠0). Check the exit code and message before acting.
- **A security-policy refusal (exit 1, stderr starting with "security policy") is not a malfunction**: follow section 8, restate to the user, obtain consent, then retry.

## 3. Install & Configuration Guidance (platform missing / not running)

1. **Download (versioned artifact)**: open the official download page `https://zyinfo.pro/action/` and pick the **versioned release artifact** (e.g. `ZY-Action-Platform_v2026.09.rar`, several hundred MB, containing all five backends + frontend + one-click launcher).   for that version.
2. **Confirm before running (never auto-execute downloaded packages)**: restate the artifact name, version and both verification results to the user, and only **after explicit consent** extract and run.
3. **Extract**: unzip the rar to any directory (Windows, no installer, no Python/Node/DB needed). The root contains `Run ZY Action System.exe` (localized name), `Stop All Services.bat`, `config.yaml.example`, `.env.example`, `bin/`, `docs/`, etc. If a trusted package-manager channel (e.g. an official winget source) is available, prefer channels with signed metadata and rollback protection.
4. **Fill in the API key (required for NLQ/search)**: copy `config.yaml.example` to `config.yaml`, open it, and under `llm:` → `api_keys:` fill the DeepSeek key at `deepseek: "sk-..."`; add `dashscope` for RAG/vector search. If the user is just demoing without PostgreSQL, change `database.type` from `"PostgreSQL"` to `"SQLite"` (SQLite is the default when config.yaml is absent). Equivalent: copy `.env.example` to `.env` and set `DEEPSEEK_API_KEY=sk-...`.
4. **Start**: double-click the launcher exe (or the same-named `.bat`). It starts the five backends plus the gateway and opens `http://127.0.0.1/`. After ~2–5 seconds verify readiness with the `health` command for each product.
5. **Login account**: a fresh install seeds `admin / admin1` (change the password after first login); users can also self-register in the UI. The user provides their own credentials for login in conversation. **Recommend creating a dedicated read-only account for the AI assistant** for query/list operations (see section 8).
6. **Stop**: double-click `Stop All Services.bat` in the root directory.

## 4. Connect & Log In (show the destination; get consent before sending credentials)

1. Run a health check first:
   `python3 scripts/zy_platform.py health --product aip` (repeat for foundry/apollo/gotham/swift as needed).
2. **Login (two steps; always dry-run first)**:
   - Step 1: `python3 scripts/zy_platform.py login --product <product> --username <user> --password <pass> --dry-run`. The script returns the normalized destination (JSON `destination`, e.g. `http://127.0.0.1:18080/api/v1/auth/login`) without sending anything. **Show this address to the user verbatim and get explicit consent.**
   - Step 2: after consent, run again without `--dry-run` (the script also prints the destination to stderr). On success the token is cached under `~/.workbuddy/` (OS credential store preferred; otherwise a 0600 hardened fallback file, local machine only, never uploaded with the skill); later commands attach it automatically.
3. **First contact with a remote origin requires confirmation**: when `--base-url` points to a non-loopback address the script refuses and asks for `--trust-host`. Restate the normalized address to the user, get informed consent, then add the flag; the origin is remembered locally afterwards (`logout --forget-host` revokes).
4. **Tokens are strictly origin-bound**: a token is bound to the tuple scheme|host|port|product|api-root. Changing origin/port/scheme/gateway form makes the script refuse to attach the old token (stderr notice); re-login for that origin or pass an explicit `--token`.
5. **Logout**: `logout --product <product>` removes the current origin's token; `logout --all` clears everything; `logout --all --forget-host` also revokes all trusted origins. Offer logout when the session ends or the user asks.
6. On exit code 4 / "auth failure (401)" the token has expired (expired entries are purged automatically) — run login again before continuing.

## 5. Common Operations Quick Reference (confirm intent with the user, then pick commands)

- **NLQ query (AIP)**: `chat --product aip --query "<user's words>"`. NLQ turns natural language into SQL; the result contains `sql_query/query_result/confidence`. Summarize in the user's language; show the table only when asked. On LLM-related business errors, suggest checking the `deepseek` key in config.yaml and platform licensing.
- **Workflows (AIP)**: `workflow-list --product aip` to get workflow ids and confirm with the user; `workflow-run --product aip --workflow-id <id>` (optional `--params '{"region":"east"}'`); with the `execution_id`, poll `workflow-status --product aip --execution-id <eid>` (interval adapts to status, max ~60s) and report the conclusion and outputs; `workflow-cancel` when needed.
- **Datasources & audit**: `datasource-list --product aip|foundry`; `audit-list --product aip`.
- **Foundry data/ontology**: `dataset-list`, `dataset-preview --dataset-id <id>`, `ontology-objects`, `ontology-search --query "<business semantics>"` (recommended), `metric-list`, `dashboard-list`, `report-list`.
- **Gotham intel**: `search --query "<keyword>" --limit 5` (unified search across graph/entities/timeline/map), `graph-nodes`, `graph-stats`, `entity-list`, `timeline-events`, `map-features`, `report-list`.
- **Apollo deployments**: `apollo-docs` (introspects all endpoints & permissions), `desired-state-list`, `deployment-list`, `deployment-status --deployment-id <id>`, `drift-list`, `bundle-list`, `agent-list`.
- **Swift**: `health --product swift` only.

All commands accept `--pretty`; list commands accept `--page/--page-size/--limit`.

## 6. When an Endpoint Isn't Built In: Generic Pass-through + Official Docs

The platform API evolves. Two extension paths:

1. **Generic request pass-through (read-only by default)**: `python3 scripts/zy_platform.py request --product <product> --method GET --path=<path relative to API root> [--query-str 'k=v&k2=v2'] [--data '{"..."}']`
   - `--path` is relative to the product API root (`/api/v1`) and **must not start with `/`**: e.g. `--path=metrics/catalog?limit=5` requests `<base>/api/v1/metrics/catalog?limit=5`; `--path=health` hits the server root `/health`. Pass JSON bodies via `--data`.
   - **Method restriction**: only the fixed set GET/HEAD/POST/PUT/PATCH/DELETE is accepted; **only GET/HEAD are allowed by default**.
   - **Double confirmation for writes**: POST/PUT/PATCH/DELETE require explicit `--allow-write`, and you must first run `--dry-run` and show the user the method/normalized URL/body (sensitive fields masked) before executing for real.
   - **Path allowlist**: only data/analytics read-only families are allowed (datasets/metrics/ontology/dashboards/reports/search/graph/timeline/map/entities/workflows/executions/datasources/deployments/drift/bundles/agents/desired-states/docs/audit etc.); sensitive admin families (`auth/users/admin/rbac/config/license/system/database` etc.) are always rejected; writes are allowed only in the `chat` and `ontology/semantic-search` families — use built-in commands otherwise.
   - **Tokens are never attached automatically**: pass-through does not attach the cached token by default; after explaining and getting consent add `--with-token` (origin binding still enforced) or pass `--token` explicitly.
   - **Local audit**: every approved write request is appended to `~/.workbuddy/zy_action_audit.log` (no credentials, no tokens); login/logout are recorded too.
2. **Read the bundled official docs from the install directory (prefer this first)**: when the user tells you the install/extract directory (e.g. "installed at D:\zyaction"), use Read/Grep on the authoritative bundled material before acting:
   - root `README.md` (products/ports/startup), `API 接入及测试方法参考.txt` (cross-product API spec S01–S12, auth, curl examples);
   - `docs/manuals/**` (analyst/admin/ops/FDE guides), `docs/ai-action-demo-full.md`, `docs/story/**` (per-product demo narratives);
   - `api-demo/sence/*.py` (official HTTP call examples, `common.py` has a login wrapper);
   - `config.yaml.example`/`.env.example` (account/port/key config reference).
   After reading real endpoint details, prefer built-in commands; only fall back to pass-through (subject to the item-1 allowlist) when truly needed. Never write or run destructive operations unless the user explicitly asks.

## 7. Gateway / Remote Addresses (fallback)

Direct localhost ports are enough by default. For remote access `--base-url` accepts gateway forms such as AIP `http://127.0.0.1/aip-api/v1`, Foundry `http://127.0.0.1/api/v1`, Apollo `/apollo-api/v1`, Gotham `/gotham-api/v1`, Swift `/swift-api/v1` (equivalent to direct paths), or a cloud/remote instance via **`https://domain/...`**. Rules:
- **Remote (non-127.0.0.1/::1/localhost) must be https**; the script rejects remote plaintext http outright (sending tokens/passwords in cleartext is unacceptable); provide TLS via a reverse proxy/gateway.
- First contact with a remote origin requires `--trust-host` confirmation (see 4.3).
- With `--base-url`, `health` hits the server root `/health`; on some gateway shapes health may be unavailable — verify connectivity via `login`/list commands instead.

## 8. Security & Boundaries

- **Transport**: non-loopback destinations are forced to https; remote plaintext http is always rejected. Destinations are parsed with `urllib.parse.urlsplit`; base-urls carrying userinfo (`user:pass@host`), fragments (`#`) or query strings are refused. Authenticated requests only accept same-origin redirects; cross-origin redirects are blocked and never carry authorization.
- **Credential display**: before sending login credentials, run `login --dry-run`, show the normalized destination, and get consent; never display the user's password in the conversation, never write tokens/passwords into skill files.
- **Token storage (minimal)**: tokens prefer the OS credential store (enabled automatically when the python `keyring` module is installed); otherwise the fallback file `~/.workbuddy/zy_action_session.json` is used (dir 0700, file 0600, atomic replacement via temp file, symlinks rejected, ownership verified on POSIX, permissions tightened before read/write). Only the token and binding metadata are stored — **no usernames/passwords/terminal info**; expired tokens are purged automatically on read/write.
- **Pass-through discipline**: read-only GET/HEAD by default; writes need `--allow-write` plus a prior `--dry-run` confirmation of method/URL/body with the user; sensitive admin route segments are rejected and paths are gated by a family allowlist; cached tokens are never auto-attached to pass-through requests (require `--with-token` with consent).
- **Least-privilege account**: recommend a dedicated **read-only platform account** for the AI assistant's query/list/search operations; switch to a suitable account only with user consent when writes are needed — don't run daily queries with an admin account.
- **High-risk actions**: deletions, bulk writes and publish operations always require restating and confirming with the user first; never execute without authorization.
- **Download integrity**: use versioned artifacts only; before execution require both `verify-artifact` hash verification and a digital-signature check (expected publisher: ZY Tech / zyinfo.pro), restated and confirmed by the user.
- **Error handling**: on network errors (exit 2) suggest "confirm the platform is running (double-click the launcher) and that --product/--base-url are correct"; if stderr mentions certificate verification failure, the remote https certificate is invalid and ops must fix it; on business errors (exit 5) relay the message; on security-policy refusals (exit 1) follow this section; when unsure, say so honestly — never fabricate.
