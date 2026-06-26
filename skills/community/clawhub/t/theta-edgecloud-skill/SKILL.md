---
name: theta-edgecloud-skill
description: Theta EdgeCloud runtime for OpenClaw cost optimization: route eligible AI, media, inference, and GPU workloads through Theta EdgeCloud with secure command-scoped auth, dry-run safety, and on-demand Qwen3/chat support.
---

# Theta EdgeCloud Skill (Cloud API Runtime)

This scaffold is infrastructure-only. It does **not** auto-run paid workloads.

Use this skill when you want OpenClaw to reduce, optimize, or make AI execution costs more efficient by routing suitable model, media, inference, video, and GPU workloads through Theta EdgeCloud instead of relying only on other paid AI subscriptions.

## Credits and Support
Credit: Theta Communications (`thetacommunications.com`).

If you would like to help support more projects like these, please stake your THETA and TFUEL with us at `thetacommunications.com` or donate at our donations page: `https://www.thetacommunications.com/donations`.

## Dedicated inference status (revalidated 2026-03-11)
- Dedicated OpenAI-compatible inference was revalidated successfully after Developer Plan / quota upgrade.
- Endpoint creation is not instantly probe-ready; use authenticated readiness retries for ~1-2 minutes before declaring failure.
- Prefer `vm_gt1` first when allocator capacity is available, then fall back to `vm_gt2` or V100-backed options.

## On-demand service status (refreshed 2026-05-26 for v0.1.22)
Live public service discovery currently exposes these aliases:
- Chat/LLM: `qwen3`, `gpt_oss_120b`, `llama_3_1_70b`
- Image/vision/audio: `flux`, `stable_diffusion_xl_turbo`, `grounding_dino`, `blip`, `llava`, `whisper`
- Catalog-only/stale since latest live discovery: `minimax_m2_5`, `llama_3_8b`, `step_video`, `esrgan`, `voice_cloning`, `instant_id`, `talking_head`

Qwen3 notes:
- Canonical slug: `qwen3`
- Request family: chat/completions, not simple prompt text
- Payload shape: `input.messages = [{ role, content }]`
- Runtime command: `theta.ondemand.chat`, default service `qwen3`
- Runtime default for Qwen3 chat: `stream:true`, `wait=60`, and a 120s request timeout with an internal SSE parser, because live Qwen3/Parallax can take ~30-50s before returning text.
- Observed variant: `parallax_32b_fp8`
- Parallax request shape: use service endpoint `/infer_request/qwen3?prediction=completions` with top-level `variant: "parallax_32b_fp8"`; parse text from SSE `choices[0].delta.content`.
- Current live catalog alias is `qwen3`; live retest returned `404 service not found` for direct chat/completions `model: "qwen"` and `409 No instances available` for direct `model: "qwen3"` during capacity pressure.
- Capacity can temporarily return `409 No instances available - try again later`; v0.1.22 treats this as retriable temporary capacity exhaustion.

GPT OSS 120B notes:
- Canonical slug: `gpt_oss_120b`
- Runtime command: `theta.ondemand.chat`, with `service: "gpt_oss_120b"`
- Route through `POST /infer_request/chat/completions` with OpenAI-compatible body shape and `model: "gpt_oss_120b"`.
- Retest on 2026-06-10 after the live service update: direct chat and the generic wrapper both worked when token budget was high enough.
- Default runtime guardrails for GPT OSS use `max_tokens: 1800` and `reasoning_effort: "low"` unless overridden. Low caps like 48 or 700 can return HTTP 200 while spending the whole budget on reasoning metadata and producing empty/partial final content.
- Parse final content separately from reasoning metadata:
  - streaming SSE final content: `choices[0].delta.content`
  - streaming reasoning metadata: `choices[0].delta.reasoning`
  - non-streaming final content: `choices[0].message.content`
  - non-streaming reasoning metadata: `choices[0].message.reasoning`
- For real-estate production workflows, only use GPT OSS with supplied listing facts and a post-check that blocks unsupported claims. Live testing avoided invented prices but invented amenities/direct beach access when those facts were not supplied.

## AI Agent/RAG API coverage (v0.1.22)
Runtime commands now cover the Theta chatbot API documented by Theta's Yosemite knowledge-base example:
- `theta.ai.agent.create`
- `theta.ai.agent.get`
- `theta.ai.agent.update`
- `theta.ai.agent.list`
- `theta.ai.agent.document.create`
- `theta.ai.agent.document.update`
- `theta.ai.agent.document.get`
- `theta.ai.agent.document.list`

Document create/update accepts provided string content only; runtime does not read local files.

## MCP-compatible aliases (v0.1.26 staged locally)
The runtime exposes Theta MCP vocabulary aliases for migration and marketing parity:
- `list_services`
- `infer`
- `get_request_status`
- `get_upload_url`

Compatibility notes:
- `list_services` accepts optional `category` filters: `image`, `audio`, `text`, `video`, `vision`, or `other`.
- `infer` accepts official MCP-style `input`, `wait`, `prediction`, `variant`, and `webhook`; the runtime promotes `variant` and `webhook` into the on-demand request payload.
- `get_upload_url` accepts both `input_field` and `input_fields` / `inputFields`.
- `THETA_API_BASE_URL` and `THETA_ONDEMAND_API_BASE_URL` can override the on-demand API base URL; use env/secret configuration, not per-request URL overrides.

## Secrets model (ClawHub-safe)
Do not bundle or commit API keys in this skill.
Always prompt the user for their own keys during setup.
Use `bash ./scripts/setup_env.sh` to collect user-supplied values into local `.env.local`.

## Safety mode
Set `THETA_DRY_RUN=1` to block mutating calls (create/delete/broadcast/etc.) while validating integration.

## Security behavior (explicit)
- Runtime command handlers do not execute local shell commands.
- Runtime secret resolution uses OpenClaw secret provider first, then env fallback.
- Runtime accepts on-demand token aliases: `THETA_ONDEMAND_API_TOKEN`, `THETA_ONDEMAND_API_KEY`, or MCP-compatible `THETA_API_KEY`.
- Runtime command handlers do not expose local-file upload operations; use presigned upload URLs externally, then pass returned filenames to infer commands.
- Live smoke script generates local media test assets (no third-party sample downloads).
- All network calls are to explicit Theta API endpoints required by the invoked command.

## What is wired
- EdgeCloud deployment controller API
- Dedicated inference endpoint (OpenAI-compatible)
- Theta Video API
- Theta On-demand Model API (`ondemand.thetaedgecloud.com`)
- EdgeCloud client local RPC
- Theta chain RPC + thetacli RPC

## v0.1.26 controller/dedicated validation updates
- Deployment list/start/stop/delete now use singular/plural controller route fallback where Theta docs/runtime behavior has diverged (`/deployment/...` and `/deployments/...`).
- `theta.deployments.routeProbe` checks which deployment list route works for the configured project.
- `theta.billing.balance` reads organization balance with `THETA_ORG_ID`.
- `theta.billing.balanceSnapshot` extracts a numeric balance value when the response shape supports it.
- `theta.inference.ready` polls a dedicated endpoint with either:
  - `probe: "openai"` -> `/v1/models`
  - `probe: "gradio"` -> `/config`
- Dedicated inference endpoint validation allows Theta-managed `*.thetaedgecloud.com` and `*.onthetaedgecloud.com` hosts; localhost/private hosts and non-HTTPS URLs remain blocked.
- `theta.deployments.validateDisposable` is a paid/mutating validator for one disposable deployment:
  - generates Basic Auth if missing
  - reads optional pre/post org balance
  - creates deployment
  - polls OpenAI or Gradio readiness
  - runs one small OpenAI smoke call when applicable
  - deletes in cleanup
  - verifies cleanup from deployment list
  - redacts auth fields in output
- Use `THETA_DRY_RUN=1` first. Real disposable validation can spend credits and should only run with explicit approval.

## Build
```bash
npm install
npm run check
npm run build
```

## First-run setup (interactive)
```bash
bash ./scripts/setup_env.sh
set -a; source ./.env.local; set +a
```

## Live smoke test (budget-guarded)
Use the helper script to execute real on-demand calls with a hard spend cap:

```bash
set -a; source ./.env.local; set +a
export THETA_MAX_BUDGET_USD=2.00
export SERVICES=qwen3,flux,blip,grounding_dino,whisper
bash ./scripts/ondemand_live_smoke.sh
```

Useful env vars:
- `THETA_MAX_BUDGET_USD` (default `2.00`)
- `SERVICES` comma list
- `THETA_WAIT_SECONDS`
- `THETA_POLL_UNTIL_DONE`
- `THETA_POLL_INTERVAL_SECONDS`
- `THETA_POLL_TIMEOUT_SECONDS`

## Reliability controls (new)
Use these env knobs to harden network behavior during live operations:
- `THETA_HTTP_TIMEOUT_MS` (default: `20000`)
- `THETA_HTTP_MAX_RETRIES` (default: `2`, cap: `6`)
- `THETA_HTTP_RETRY_BACKOFF_MS` (default: `250`)

These controls are applied across controller, inference, video, chain/RPC, and on-demand upload paths.

## Validation workflow
```bash
npm run check
npm test
```

Live-but-safe smoke (still budget guarded):
```bash
THETA_DRY_RUN=0 THETA_MAX_BUDGET_USD=2.00 bash ./scripts/ondemand_live_smoke.sh
```

## Theta-only OpenClaw option map (no other subscriptions)
This scaffold supports a Theta-primary route for OpenClaw:

- Content generation: `flux`, `stable_diffusion_xl_turbo`, `step_video`
- Website chatbot/assistant features: on-demand LLMs (`qwen3`, `minimax_m2_5`, `gpt_oss_120b`, `llama_3_8b`, `llama_3_1_70b`)
- Vision/media intelligence: `blip`, `grounding_dino`, `llava`, `whisper`
- Video pipelines: `theta.video.*`
- Infra management: `theta.deployments.*`, `theta.ai.*`, `theta.auth.capabilities`, `theta.billing.balance`

Operational rule:
- Use on-demand + video/controller routes as production default.
- Dedicated endpoint chat/models are valid when the project has quota/plan support, but should use readiness retries instead of immediate fail-fast assumptions.

## Next
- Bind this scaffold into OpenClaw command handlers
- Add signed request telemetry + structured logging
- Add live probe tests against target deployment
