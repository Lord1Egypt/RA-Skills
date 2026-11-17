---
name: theta-edgecloud-skill
description: "Theta EdgeCloud on-demand AI, GPU nodes, RAG agents, video and game-character workflows: discover live services, run inference, manage approved resources with confirmation gates, and verify costs."
license: MIT-0
metadata: {"openclaw": {"primaryEnv": "THETA_EC_API_KEY", "homepage": "https://www.thetaedgecloud.com"}}
---

# Theta EdgeCloud

## Permissions and data flow

- Network: HTTPS only. Credentials go only to Theta hosts:
  `ondemand.thetaedgecloud.com`, `controller.thetaedgecloud.com` (REST and
  hosted MCP), `api.thetaedgecloud.com`, `api.thetavideoapi.com`,
  `ai-chars-api.thetaedgecloud.com`, and your configured Theta-managed dedicated
  endpoint. Redirects are refused. `*.onthetaedgecloud.com` also hosts other
  customers' deployments, so configure only your own endpoint.
- Two non-Theta destinations, both opt-in:
  - Uploads: `get_upload_url` returns a Theta-issued presigned cloud-storage URL.
    The agent, not this runtime, PUTs a file the user approved to that URL.
    The runtime itself never reads local files.
  - Webhooks: if you pass `webhook` to on-demand inference, Theta POSTs results
    to that URL. It must be `https` and requires `confirm:true`; the runtime
    cannot verify ownership, so pass only your own URL. Dedicated-endpoint chat
    rejects webhook fields.
- Credentials: read from the host secret store or environment, sent only as auth
  headers to the matching Theta host, and not logged. Results redact values under
  secret-looking names (password, token, API key and similar); only numeric usage
  counts such as `prompt_tokens` are kept. `theta()` reports
  only which credential families are configured.
- Data sent: prompts, messages, uploaded files, RAG document contents and
  character messages, GPU container image identifiers and SSH public keys go to Theta for processing. Treat inputs and outputs as
  private.
- Approval (enforced inside the bundled network clients): outside dry-run,
  `confirm:true` is required for:
  - every remote create/update/start/stop/delete: deployments, GPU nodes, RAG
    agents and documents, video, and all Characters writes including messages;
  - inference on any service not on the low-cost allowlist (video such as
    `seedance_2_5`, unknown or future services);
  - any webhook.
- Ungated by design: chat on listed models and inference on the listed low-cost
  image/audio/vision services, with `max_tokens` clamped to 1..5000 per call and
  fan-out fields removed; dedicated-endpoint chat (same clamp); upload-URL
  creation; read-only queries.
- `confirm:true` is supplied by the calling agent. It records, but cannot verify,
  user approval. Also use least-privilege keys and provider-side quotas.
- Packaging: one unminified bundle, `dist/index.js`, built from the included
  `src/` (shipped for review). It exports only the runtime command API and the
  read-only `theta()`, and is the only supported entry point.
- No shell execution, local file reads, wallet or chain signing, or install
  hooks.

## 1. Discover and select the route

Read `references/capabilities.md` for command families and coverage limits.
Resolve every relative command from this skill directory. Import `./dist/index.js`
and use `listThetaRuntimeCommands()` / `thetaRuntimeCommandSchemas` as the
executable capability inventory; documentation alone does not prove support.

Run `executeThetaRuntimeCommand({command:"list_services"}, {env:process.env})`
before selecting an on-demand service. Require `source:"live"`; a catalog
fallback is historical metadata, not availability. Inspect the service's
`predictions`, `inputSchema`, variants, workers and pricing. A listed model
can still lack capacity. Do not substitute a removed slug silently.

Choose on-demand for small inference/media jobs, `theta.gpu.*` (hosted MCP)
for GPU capacity, pricing, deployments, events and logs, controller APIs for
templates and older deployment routes, dedicated endpoints for existing serving workloads, Video API
for video hosting/streams, and AI Characters for game NPCs/sessions.
Finish selection with a verified service/endpoint, input contract and auth family.

## 2. Resolve credentials and authority

Use existing protected credentials; never request or display keys in chat.
Runtime on-demand resolution checks `ctx.getSecret` then environment aliases
`THETA_ONDEMAND_API_TOKEN`, `THETA_ONDEMAND_API_KEY`, `THETA_API_KEY`.
Supply other credential families through protected runtime environment:
- Controller and hosted MCP (GPU/billing): `THETA_EC_API_KEY`, `THETA_EC_PROJECT_ID`;
  the raw org-balance fallback also uses `THETA_ORG_ID`.
- Dedicated: `THETA_INFERENCE_ENDPOINT`, optionally
  `THETA_INFERENCE_AUTH_USER` / `THETA_INFERENCE_AUTH_PASS`.
- Video: `THETA_VIDEO_SA_ID` / `THETA_VIDEO_SA_SECRET`.
- Characters: `THETA_CHARACTERS_API_KEY`, a separate game-scoped Bearer key.

No keys belong in source, test fixtures, archives intended for publication, or reports.

Set `THETA_DRY_RUN=1` for lifecycle rehearsal. Dry-run blocks every write and
inference but still performs authenticated read requests (HTTP GETs and
read-only hosted-MCP `tools/call` POSTs). It is not an offline mode. A caller can
turn dry-run on, but cannot turn off an operator-enabled dry-run.
Before passing `confirm:true`, state the exact action and price to the user and
get their approval. Read-only billing does not authorize account changes.

## 3. Execute bounded inference

Use `theta.ondemand.chat` with `messages` and explicit `max_tokens`. These run
on `/infer_request/chat/completions`:
- `glm_5_3` / `glm_5_3_flash` (`reasoning_effort` low|high|max): the only live
  models that return structured tool calls.
- `qwen3_8_max` / `qwen3_8_flash` (`enable_thinking`): Flash is the cheapest
  live chat model.
- `ling_3_0_flash_fin`: finance model; reasoning appears in content, so allow
  at least 1024 tokens.
Tools sent to Qwen3.8 or Ling are rejected, because Theta drops them silently,
unless `allowUnverifiedTools` is exactly `true`.
Pass `tools`, `tool_choice`, `parallel_tool_calls`, and `stream` at the
command's top level. Preserve assistant `tool_calls` and tool-message
`tool_call_id` for continuation.

Read `body.infer_requests[0].output.message` separately from
`output.tool_calls` and `metadata.reasoning`. JSON and streamed responses
retain structured calls, including fragmented parallel arguments and
`reasoning_content`. Check finish reason, response model and tool arguments;
a successful HTTP response or reasoning-only result is not completion.

Qwen3 retains the service-specific streaming route and optional
`variant:"parallax_32b_fp8"`; capacity 409 is not an authentication failure.
Retired services (GPT-OSS, GLM-5.2, FLUX, step_video) are historical catalog entries only.
Do not change an OpenClaw primary/fallback model as part of an inference test.

For media, use `infer` with live prediction-specific `input`, optional
`prediction`, `variant`, `wait` (0–60), and an optional user-owned `https`
`webhook` (needs `confirm:true`).
Live media 2026-10-03: `stable_diffusion_xl_turbo` (text-to-image, 512px),
`image_to_image` (`stylize` | `upscale` | `background_removal`, the last two
with `style_image_filename:""`), `esrgan`, and `seedance_2_5` (video:
high-cost, so it needs `confirm:true`, and is often unavailable). OpenClaw's native `image_generate`/`video_generate` can reach
these only through a separately installed media-provider plugin. This skill
does not ship or install one.
`get_upload_url` accepts `input_field` or `input_fields` and returns
`uploads[field].{upload_url,filename}`. PUT only authorized files with
`Content-Type: application/octet-stream`, then pass the filename to inference.
Runtime handlers do not execute shell commands or upload arbitrary local files.

Poll asynchronous jobs with `theta.ondemand.pollUntilDone` and
`options:{timeoutMs,intervalMs,maxAttempts}`. Verify terminal success and the
actual output (download/decode an image or inspect the requested media), not
just submission. Presigned URLs are sensitive; omit them from public reports.
Prompts, uploaded files, character messages and outputs go to Theta services.
Treat them as private, send only data the user authorized, and avoid logging full
responses.

For paid smoke tests, use one explicit service/request at a time, synthetic
input and small token/frame limits. Only GET reads are retried
(`THETA_HTTP_MAX_RETRIES`); writes and inference are never resent to the same URL. After ambiguous
timeouts, reconcile the remote job/resource before any manual retry.
Post-call accounting cannot enforce a provider-side hard spend cap. Unknown price units/cost fields
are unknown costs, never zero. Report tokens/units and only assert currency
when Theta's current billing data establishes it.

## 4. Manage GPU, RAG, Video or Characters

Follow the matching section in `references/capabilities.md`.
For GPU work, run `theta.gpu.resources.list` (USD/h, availability, region) and
`theta.gpu.templates.list`, then dry-run `theta.gpu.deployments.create`. State
the hourly price, get approval, then create with `maxPricePerHourUsd` and
`confirm:true`. The cap is sent to Theta, and creation is refused when the
resource's listed price is unknown or above it. Diagnose nodes with
`theta.gpu.deployments.get|events|logs`. Report spend from
`theta.billing.balance|usage` (USD), not from raw credits.
Use base IDs to restart stopped GPU nodes. Preserve remote resource IDs and
cleanup ownership before creating anything.

Dedicated endpoints must be HTTPS Theta-managed hosts
(`*.thetaedgecloud.com` or `*.onthetaedgecloud.com`); private/localhost and
request-level endpoint overrides are rejected. Use bounded authenticated
`theta.inference.ready` with `probe:"openai"` or `"gradio"` after deployment.
Transient 404/502 during warm-up does not alone prove bad credentials.

`theta.deployments.validateDisposable` is PAID: dry-run first, approve
template/VM/time/cost, then pass `confirm:true` and a `smokeMessage`. With the
default `openai` probe, `ok` is true only when readiness, the smoke inference,
deletion and absence from the deployment list all succeed (`gradio` probes check
readiness and cleanup only); `smokeTested` shows whether inference ran. A failed
cleanup is BLOCKED, not success.

For RAG, provide content strings and approved settings to existing chatbot and
document commands; do not claim Custom Tool CRUD without an API contract.
For Characters, use only game-key runtime commands. Every Characters write,
including session messages and context, needs `confirm:true`. Dashboard login, game
creation and key renewal are deliberately not implemented with project tokens.

## 5. Verify and hand off

For release verification, run `npm run check` and `npm test` from the source or complete local package. Test changed handlers with mocked request/response contracts,
then bounded live calls where credentials and authorization permit.
Use the same built artifact for source tests and installed-runtime verification.

Report separately: implemented, contract-tested, live-tested, unavailable
credentials, missing public API contract, and paid tests not performed.
Do not equate ClawHub latest with complete Theta feature parity.
Do not claim “all latest features” from a news announcement alone.


## Credits

Theta Communications: https://www.thetacommunications.com
