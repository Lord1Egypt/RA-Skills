---
name: studio-agent
description: Use this for ClickZetta Studio requests such as querying tasks, listing workspaces, checking projects, and creating or running ClickZetta jobs from a single JDBC secret configured in OpenClaw.
metadata:
  {
    "openclaw":
      { "emoji": "🌉", "primaryEnv": "CZ_STUDIO_JDBC_URL", "requires": { "bins": ["node"], "env": ["CZ_STUDIO_JDBC_URL"] } },
  }
---

# ClickZetta Studio

Use this skill when the user wants OpenClaw to work with ClickZetta Studio.

Typical triggers:

- "帮我创建个 lakehouse 任务"
- "用 Studio Agent 帮我 ..."
- "在 ClickZetta 里执行/创建 ..."
- "我当前有哪些 ClickZetta 任务"
- "帮我查 ClickZetta 任务/作业/项目/工作区"
- "列出当前可用 workspace"
- "切换到 workspace 101201"
- "刷新 workspace 列表"

## Default Runtime Path

If the user asks any normal ClickZetta / Studio / Lakehouse business question and
the skill already has `CZ_STUDIO_JDBC_URL`, immediately run:

```bash
node {baseDir}/scripts/cz-agent-oneshot.mjs --input "<user_input>"
```

Rules:

- Do not ask for internal connection fields such as instance id, tenant id, project id, workspace, or password first.
- The runner resolves runtime discovery itself from the stored JDBC secret.
- Only fall back to setup instructions when the runner returns a concrete config/runtime error.
- For queries like "我当前有哪些clickzetta任务", "帮我查任务", "查 workspace/project", "执行 SQL", default to the one-shot runner immediately.
- For workspace management queries like "当前 workspace 是什么", "列出 workspace", "切换到 workspace 101201", also default to the one-shot runner immediately.
- `列出 workspace` / `切换 workspace` 会使用短 TTL 的 workspace 列表缓存；`刷新 workspace 列表` 会强制刷新。
- For SQL execution requests, forward the user's original wording once. Do not rewrite it into follow-up variants such as "创建一个 SQL 任务", "运行刚才创建的任务", or other speculative recovery prompts.

## Install then Configure (Required)

Preferred ClawHub / OpenClaw UI flow:

- Install the skill
- Open the Skills page
- Paste one JDBC URL into the secret field for `CZ_STUDIO_JDBC_URL`

Example JDBC URL:

```text
jdbc:clickzetta://<instance>.<api-host>/<workspace>?username=<username>&password=<password>
```

The skill parses this JDBC URL at runtime and extracts:

- `instanceName` from the hostname prefix
- `apiGateway` from the JDBC host
- `username` and `password` from query params
- `workspace` from the path

Runtime note: if this setup step is skipped, this skill should tell the user to open the Skills page and set `CZ_STUDIO_JDBC_URL`.

## What this skill provides

- One-step ClickZetta access from a single JDBC secret
- Automatic runtime login and identity discovery
- Workspace-aware task, job, project, and SQL operations
- A cached workspace list for faster follow-up requests

## Execution policy

- Do not ask the user for `CZ_*` env vars up front.
- Assume the JDBC secret is already wired via the Skills page unless runtime errors prove otherwise.
- When runtime reports missing/invalid Studio config, tell the user to open the Skills page and set `CZ_STUDIO_JDBC_URL`.
- Default path for normal user requests: run `scripts/cz-agent-oneshot.mjs` once and return its result.
- When describing connection status to the user, refer to the runtime-discovered Studio connection; do not ask the user to manually provide internal `CZ_AGENT_*` values.
- For requests like "帮我创建个 lakehouse 任务", immediately:
  1. run one-shot runner command
  2. read runner JSON output
  3. if `ok=true`, return `content`; if `ok=false`, return concise error and stop
- If the runner returns `ok=false`, do not issue additional paraphrased or workaround requests to the Studio agent in the same turn.
- If runner returns `ok=true`, treat Studio as connected and continue the user workflow; do not claim Studio is down.
- Only ask the user for config details when runtime returns a concrete missing minimal-config error.
- Treat config-missing as a narrow case only:
  - `ok=false`
  - `error.code == "PROTOCOL_ERROR"`
  - and the message explicitly says config is missing, such as missing `CZ_STUDIO_JDBC_URL` or other missing Studio runtime connection info
- If `error.code == "REMOTE_ERROR"`, do not claim JDBC is missing or suggest reconfiguration. Report the remote error directly and keep the original error message.
- For errors like `expected string or bytes-like object, got 'NoneType'`, explain that the request reached the remote ClickZetta agent but failed during remote processing.
- For SQL requests that return `REMOTE_ERROR`, do not suggest retrying with paraphrased prompts such as `执行 SQL: ...`, `创建一个 SQL 任务 ...`, or `运行刚才创建的任务`.
- Do not invent alternative SQL execution workflows unless the remote agent explicitly asks for additional fields.
- Preferred response shape for these failures:
  1. state the original remote error
  2. say the request reached the remote ClickZetta agent
  3. stop
- If remote asks follow-up fields (task type, SQL details, etc.), relay those follow-up questions to the user as normal.

Mandatory one-shot command for normal requests:

```bash
node {baseDir}/scripts/cz-agent-oneshot.mjs --input "<user_input>"
```

Runner output is one JSON object:

- success: `{"ok":true,"content":"...","conversation_id":"...","request_id":"..."}`
- failure: `{"ok":false,"error":{"code":"...","message":"..."}, ...}`

## Runtime Discovery

Minimal required input field for ClawHub users:

- `CZ_STUDIO_JDBC_URL`

Auto-discovery behavior:

- parse `jdbc:clickzetta://...` from `CZ_STUDIO_JDBC_URL`
- derive the Studio instance from the JDBC host
- sign in to ClickZetta at runtime
- resolve the current user and tenant identity
- load the accessible workspace list and enrich project/workspace metadata
- initialize the Studio session connection automatically
- workspace 选择状态单独保存在本地缓存中，不污染 `~/.openclaw/clawdbot.json`
- workspace 列表和 token 分开缓存：token 跟随登录过期时间，workspace 列表默认 5 分钟 TTL
- if `workspace` / `workspaceId` / `projectId` is configured, runtime uses that workspace first and ignores local switch state
- if the configured workspace selector matches zero or multiple workspaces, validation/runtime now fails fast instead of falling back to the default workspace

Notes:

- In ClawHub / OpenClaw UI mode, the only user-facing field is `CZ_STUDIO_JDBC_URL`.
- Runtime-derived connection data are internal and must not be requested from the user during normal use.
- The one-shot runner also supports local workspace commands:
  - `当前 workspace 是什么`
  - `列出 workspace`
  - `刷新 workspace 列表`
  - `切换到 workspace <name|workspaceId|projectId>`
  - `恢复默认 workspace`
- If a workspace is explicitly configured, that configured workspace takes precedence over runtime switching.
- `--replace` keeps config minimal and removes stale extra keys from previous setups.
- `CZ_PROJECT_ID` / `CZ_WORKSPACE` are now best-effort enrichments, not hard requirements.
