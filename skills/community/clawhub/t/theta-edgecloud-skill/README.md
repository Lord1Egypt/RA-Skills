# Theta EdgeCloud Skill (Scaffold)

Practical setup + smoke workflow for OpenClaw users.

Use this skill when you want OpenClaw to reduce, optimize, or make AI execution costs more efficient by routing suitable model, media, inference, video, and GPU workloads through Theta EdgeCloud instead of relying only on other paid AI subscriptions.

## Credits and Support
Credit: Theta Communications (`thetacommunications.com`).

If you would like to help support more projects like these, please stake your THETA and TFUEL with us at `thetacommunications.com` or donate at our donations page: `https://www.thetacommunications.com/donations`.

## Current status (v0.1.26 staged locally)
- Dedicated OpenAI-compatible endpoint commands are valid when the project has quota/plan support; use authenticated readiness retries after new deployments.
- On-demand chat/completions now includes Qwen3 support via canonical slug `qwen3`.
- Chat services require `input.messages`. Qwen3 defaults to streaming mode (`stream:true`) with an internal SSE parser because the live non-streaming path is currently unreliable.
- AI Agent/RAG chatbot CRUD and document CRUD commands are wired.
- Theta MCP-compatible aliases are exposed: `list_services`, `infer`, `get_request_status`, `get_upload_url`.
- Controller operations include singular/plural deployment route fallback, route probing, organization balance snapshots, and a paid opt-in disposable deployment validator.

## What this package contains
- Runtime command handlers under `src/runtime/`
- Contract + unit tests under `tests/`
- Live probes under `scripts/`

## Prerequisites
- Node.js 20+
- npm
- For on-demand live smoke: `curl`, `jq`, `ffmpeg`

## Install + validation
```bash
cd /path/to/theta-edgecloud-skill
npm install
npm run check
npm test
```

## First-time setup (interactive, user-supplied keys)

This skill is published for ClawHub without bundled secrets.
Each user provides their own keys locally.

```bash
cd /path/to/theta-edgecloud-skill
bash ./scripts/setup_env.sh
set -a; source ./.env.local; set +a
```

`setup_env.sh` prompts for:
- `THETA_EC_API_KEY`
- `THETA_EC_PROJECT_ID`
- `THETA_INFERENCE_ENDPOINT` (manual or deployment-list autodiscovery)
- optional basic-auth creds + on-demand token

## Environment variables

### Deployment/API-key operations
Required:
- `THETA_EC_API_KEY`
- `THETA_EC_PROJECT_ID`

### Dedicated inference endpoint auth validation
Required:
- `THETA_INFERENCE_ENDPOINT` — dedicated endpoint URL

Optional (for basic-auth mode):
- `THETA_INFERENCE_AUTH_USER`
- `THETA_INFERENCE_AUTH_PASS`
- `THETA_INFERENCE_MODEL` (preferred model id)

### On-demand API smoke
Required:
- `THETA_ONDEMAND_API_TOKEN` — Theta on-demand API token. Aliases also accepted: `THETA_ONDEMAND_API_KEY`, `THETA_API_KEY`.

Optional knobs:
- `THETA_API_BASE_URL` or `THETA_ONDEMAND_API_BASE_URL` for an on-demand API base URL override. Defaults to `https://ondemand.thetaedgecloud.com`.
- `THETA_MAX_BUDGET_USD` (default `2.00`)
- `SERVICES` (CSV list, default includes multiple services)
- `THETA_POLL_TIMEOUT_SECONDS` (default `180`)

### Runtime secret resolution
Resolver order in runtime:
1. runtime secret provider (`ctx.getSecret`)
2. env fallback (`THETA_ONDEMAND_API_TOKEN`)

No local shell execution is used for secret resolution in runtime.

## Live smoke workflow

### 1) Minimal low-cost on-demand smoke
```bash
cd /path/to/theta-edgecloud-skill
set -a; source ./.env.local; set +a
export THETA_MAX_BUDGET_USD="0.30"
export SERVICES="qwen3"
bash ./scripts/ondemand_live_smoke.sh
```

### 2) Dedicated endpoint auth-mode validation
```bash
cd /path/to/theta-edgecloud-skill
set -a; source ./.env.local; set +a
node ./scripts/validate_inference_auth_mode.mjs
```

Expected output: JSON summary with `decidedMode` and probe status.

### 3) Disposable dedicated deployment validation
Use this only when you explicitly want to spend credits on a short-lived deployment check.

```bash
cd /path/to/theta-edgecloud-skill
set -a; source ./.env.local; set +a
npm test
node -e 'import("./dist/index.js").then(async (m) => console.log(JSON.stringify(await m.executeThetaRuntimeCommand({ command:"theta.deployments.validateDisposable", probe:"gradio", readyTimeoutMs:600000, intervalMs:15000, payload:{ project_id:process.env.THETA_EC_PROJECT_ID, deployment_template_id:"<template-id>" } }, { env: process.env }), null, 2)))'
```

The validator creates a deployment, waits for readiness, optionally runs one tiny smoke call for OpenAI-compatible endpoints, deletes the deployment in cleanup, verifies it disappeared from the deployment list, and reports pre/post balance snapshots when `THETA_ORG_ID` is set.
Dedicated endpoint validation allows Theta-managed `*.thetaedgecloud.com` and `*.onthetaedgecloud.com` HTTPS hosts, while localhost/private hosts and non-HTTPS URLs remain blocked.

## Quick troubleshooting
- `missing_endpoint`: rerun `bash ./scripts/setup_env.sh` or set `THETA_INFERENCE_ENDPOINT` in `.env.local`
- 401/403 in probes: check token/auth mode and endpoint policy
- 401/403 on deployments.list: verify `THETA_EC_API_KEY` belongs to `THETA_EC_PROJECT_ID`
- deployment route 404/405: run `theta.deployments.routeProbe`; v0.1.26 tries both `/deployment/...` and `/deployments/...`
- unknown dedicated readiness state: use `theta.inference.ready` with `probe: "openai"` or `probe: "gradio"` before declaring a new endpoint failed
- repeated 502/503 on authenticated inference with unauthenticated 401: likely upstream endpoint readiness mismatch (ingress/backend) rather than bad credentials
- smoke budget exceeded: lower `SERVICES` list and/or increase budget cap

## Security behavior (explicit)
- Runtime does not execute local shell commands.
- Runtime only calls Theta endpoints required for requested commands.
- Live smoke script uses generated local media assets (no third-party sample downloads).
- All paid/mutating operations remain opt-in and user-triggered.

## Theta-only OpenClaw option map (no other subscriptions)
Use this skill as a primary paid backend route for:

- Content generation: `flux`, `stable_diffusion_xl_turbo`, `step_video`
- Chatbot/assistant inference: on-demand `qwen3`, `minimax_m2_5`, `gpt_oss_120b`, `llama_3_8b`, `llama_3_1_70b`
- Vision/media intelligence: `blip`, `grounding_dino`, `llava`, `whisper`
- Video workflows: `theta.video.*`
- Infra operations: `theta.deployments.*`, `theta.ai.*`, `theta.auth.capabilities`, `theta.billing.balance`

AI Agent/RAG operations:
- Chatbot lifecycle: `theta.ai.agent.create|get|update|list`
- Knowledge-base documents: `theta.ai.agent.document.create|update|get|list`
- Document create/update accepts provided string content and metadata; runtime does not read local files.

Production guidance:
- Route production automation to on-demand + video + controller flows.
- Treat `409 No instances available` as temporary capacity exhaustion and retry/back off instead of treating it as a permanent wiring failure.
- MCP-compatible aliases mirror Theta's official on-demand MCP vocabulary: `list_services`, `infer`, `get_request_status`, and `get_upload_url`.
- `list_services` accepts optional `category` filters: `image`, `audio`, `text`, `video`, `vision`, or `other`.
- `infer` accepts official MCP-style `input`, `wait`, `prediction`, `variant`, and `webhook` arguments; `variant` and `webhook` are promoted into the on-demand request payload.
- `get_upload_url` accepts both `input_field` (official MCP singular) and `input_fields` / `inputFields` arrays.
- `theta.billing.balanceSnapshot` reads organization balance when `THETA_ORG_ID` is configured and extracts a numeric balance value when Theta's response shape includes one.
- `theta.deployments.validateDisposable` is intentionally mutating and paid; run with `THETA_DRY_RUN=1` first and only run live after explicit approval.
- Route `gpt_oss_120b` chat through `POST /infer_request/chat/completions` with OpenAI-compatible `model: "gpt_oss_120b"` payloads. The runtime defaults GPT OSS chat to `max_tokens: 1800` and `reasoning_effort: "low"` unless callers override those values.
- GPT OSS can spend hundreds of completion tokens on reasoning metadata before final content. Parse final answer content separately from `reasoning` fields and avoid low token caps for production calls.
- For real-estate production workflows, provide the listing/property facts explicitly and block unsupported claims in post-checks. Live testing showed GPT OSS can invent amenities/direct beach access if those facts are not supplied.
- Route Qwen3 Parallax through `/infer_request/qwen3?prediction=completions` with top-level `variant: "parallax_32b_fp8"`, `stream:true`, `wait=60`, and a 120s request timeout. Parse returned text from SSE `choices[0].delta.content`.

## Notes
- Keep secrets out of committed files.
- Start with one-service smoke before broad service matrix tests.
