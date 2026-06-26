---
name: openmarlin
description: "Use OpenMarlin from OpenClaw to answer questions, run tasks, and manage OpenMarlin account setup and billing flows."
metadata: {"openclaw":{"skillKey":"openmarlin","requires":{"bins":["python3"]},"primaryEnv":"OPENMARLIN_PLATFORM_API_KEY"}}
---

# OpenMarlin

Use this skill when a user explicitly wants to use OpenMarlin from inside
OpenClaw.

This skill covers four main jobs:

- account registration and API key bootstrap
- native execution requests through `/v1/executions`
- asynchronous long-running jobs through `/v1/tasks`
- billing, balance, and `402 Payment Required` recovery

## When To Activate

Activate this skill for requests such as:

- "use openmarlin to answer this"
- "ask openmarlin to summarize this page"
- "use openmarlin to find today's USD/CNY exchange rate"
- "use openmarlin to execute this task"
- "use openmarlin to generate a video"
- "use openmarlin to submit an async video task"
- "register OpenMarlin"
- "check OpenMarlin balance"

When routing the request:

- treat "use openmarlin ..." as an OpenMarlin intent, not generic chat
- prefer `/v1/executions` for normal tasks such as answering, searching,
  summarizing, extracting, or translating
- prefer `/v1/tasks` for video generation and other artifact-oriented jobs even
  when the user did not explicitly say "async"
- treat requests mentioning video, rendering, long-running generation, or
  background execution as `/v1/tasks` by default unless the user explicitly
  asks for synchronous execution
- do not reject activation just because the user did not provide an exact model
  ref in the first sentence

## Core Constraints

- Keep the flow OpenClaw-first by default.
- Do not collect passwords, magic links, MFA secrets, or raw credentials in
  chat.
- Prefer the `device` auth flow unless the deployment specifically requires
  `workos_callback`.
- Treat browser use as a narrow external step for identity or Stripe checkout,
  not the main control plane.
- After browser handoff begins, keep polling the registration session in
  OpenClaw until it becomes `completed` or `expired`.
- Treat browser callback or landing pages as user-facing only. Machine-readable
  registration state must come from the registration session.
- Treat `OPENMARLIN_SERVER_URL` as the only trusted API origin and keep it as a
  bare origin without `/v1`.
- Do not use `https://openmarlin.ai` as `OPENMARLIN_SERVER_URL`; that is the
  browser-facing website. Use `https://api.openmarlin.ai` unless the user is
  targeting a custom deployment.
- Use server-provided `handoff.authorization_url` directly. Do not reconstruct
  WorkOS or browser URLs locally.
- Store platform API keys in OpenClaw auth-profile storage when available, not
  in ordinary skill config.
- Treat `OPENMARLIN_PLATFORM_API_KEY` as a temporary override for debugging,
  not the preferred steady-state storage path.
- When balance information is incomplete, label local billing state as
  last-known or estimated instead of pretending it is authoritative.

## Installation

This skill is distributed as a directory, not as a standalone Markdown file.
If you install it manually, copy both `SKILL.md` and the sibling `scripts/`
directory.

Required files:

- `SKILL.md`
- `scripts/registration_session.py`
- `scripts/platform_request.py`
- `scripts/billing.py`
- `scripts/openclaw_billing_state.py`
- `scripts/openclaw_platform_auth.py`
- `scripts/openclaw_skill_config.py`

Runtime expectations:

- `python3` is available in `PATH`
- `OPENMARLIN_SERVER_URL` defaults to `https://api.openmarlin.ai`
- `OPENMARLIN_SERVER_URL` must be a bare origin, not a URL ending in `/v1`

## First Run

For a new user, the shortest safe path is:

1. Confirm `OPENMARLIN_SERVER_URL` if you need to override the default.
2. Start registration with `python3 scripts/registration_session.py create`.
3. Complete external auth in the browser if the server returns a handoff URL.
4. Poll the registration session with `watch` until it becomes `completed`.
5. Bootstrap and store the first workspace API key with `bootstrap --store`.
6. Optionally call `python3 scripts/platform_request.py models`.
7. Send the first execution request.

After setup, the most common next actions are:

- send a routed execution request
- submit a long-running task and poll for completion
- inspect available models
- recover from a `402 Payment Required` response
- inspect balance or recent billing activity
- fetch the caller's referral code and invite link

## Request Model

### Registration

Registration flows are built on:

- `POST /v1/registration/sessions`
- `GET /v1/registration/sessions/:sessionId`
- `POST /v1/registration/sessions/:sessionId/api-keys`

Registration session states:

- `pending_external_auth`
- `completed`
- `expired`

When a session completes, OpenClaw should continue from the machine-readable
registration session state, not from browser callback output.

### Executions

Native execution uses:

- `POST /v1/executions`

Execution requests may include:

- `instruction`
- `kind = agent_run`
- `stream`
- `provider_id`
- `labels`
- `agent_id`
- `session_key`
- `timeout_ms`
- `model`
- `metadata`

Execution routing rules:

- with neither `model` nor `provider_id`, let the server choose both
- with only `model`, use an exact full ref and let the server choose a provider
- with only `provider_id`, let the server choose an eligible model on that
  provider
- with both `model` and `provider_id`, the server enforces both constraints

If `model` is provided, it must be an exact full ref such as
`openai-codex/gpt-5.4`.

If you provide both `provider_id` and `model`, first confirm from
`python3 scripts/platform_request.py models` that the provider advertises that
same exact model ref.

### Tasks

Long-running jobs use:

- `POST /v1/tasks`
- `GET /v1/tasks/:taskId`

Task requests do not use the same routing shape as `/v1/executions`.

Task requests use:

- `kind = video`
- `input.prompt` required
- `input.media_urls` optional
- `input.media_ids` optional
- `input.duration_ms` optional
- `input.aspect_ratio` optional
- `metadata` optional

Task requests do not accept:

- `instruction`
- `provider_id`
- `labels`
- `model`
- `stream`

Prefer `/v1/tasks` when:

- generation may take many minutes
- stream output is absent or not useful
- the real result is expected to arrive later as artifact metadata such as an
  `artifact_url`
- the request is for video generation, unless the user explicitly insists on a
  synchronous execution path
- when using `/v1/tasks` from inside OpenClaw, default to submitting with
  watch-and-wait behavior instead of stopping after returning a `task_id`

Task states:

- `queued`
- `running`
- `succeeded`
- `failed`

### Billing

Billing and recovery flows use:

- `GET /v1/balance`
- `GET /v1/usage-events`
- `GET /v1/ledger`
- `POST /v1/topup/sessions`
- `GET /v1/topup/sessions/:sessionId`

Structured balance failures may return:

- `error_code = insufficient_balance`
- `message`
- `workspace_id`
- `current_balance.amount / unit`
- `required_balance.amount / unit`

Treat that `402` shape as workflow input, not a generic transport failure.

## Common Commands

### Registration

Create a registration session:

```bash
python3 scripts/registration_session.py create
```

Create a callback-style session when the deployment requires it:

```bash
python3 scripts/registration_session.py create --auth-flow workos_callback
```

Check or poll a registration session:

```bash
python3 scripts/registration_session.py status --session-id <session-id>
python3 scripts/registration_session.py watch --session-id <session-id>
```

Bootstrap and store the first API key:

```bash
python3 scripts/registration_session.py bootstrap \
  --session-id <session-id> \
  --store
```

### Executions

List currently available exact models:

```bash
python3 scripts/platform_request.py models
```

Let the server choose model and provider automatically:

```bash
python3 scripts/platform_request.py executions \
  --body-json '{"instruction":"say hello"}'
```

Use an exact model ref with automatic provider routing:

```bash
python3 scripts/platform_request.py executions \
  --body-json '{"instruction":"say hello","model":"openai-codex/gpt-5.4"}'
```

Use an explicit provider override:

```bash
python3 scripts/platform_request.py executions \
  --provider node-a \
  --body-json '{"instruction":"say hello"}'
```

Send a dry run:

```bash
python3 scripts/platform_request.py executions \
  --dry-run \
  --server-url https://your-server.example.com \
  --api-key claw_wsk_placeholder \
  --body-json '{"instruction":"say hello"}'
```

Use streaming execution:

```bash
python3 scripts/platform_request.py executions \
  --body-json '{"instruction":"say hello","stream":true}'
```

### Tasks

Submit a long-running job:

```bash
python3 scripts/platform_request.py tasks-submit \
  --watch \
  --body-json '{"kind":"video","input":{"prompt":"Generate a short plane video."}}'
```

Fetch the current task state:

```bash
python3 scripts/platform_request.py tasks-status --task-id <task-id>
```

Poll until the task succeeds or fails:

```bash
python3 scripts/platform_request.py tasks-watch --task-id <task-id>
```

### Billing

Explain a structured `402` response:

```bash
python3 scripts/billing.py explain-402 \
  --response-json '{"error_code":"insufficient_balance","message":"Workspace balance is insufficient for this request.","workspace_id":"ws_123","current_balance":{"amount":0,"unit":"credits"},"required_balance":{"amount":1,"unit":"credits"}}'
```

Create a top-up session from the `402` shortfall:

```bash
python3 scripts/billing.py create-topup \
  --response-json '{"error_code":"insufficient_balance","message":"Workspace balance is insufficient for this request.","workspace_id":"ws_123","current_balance":{"amount":0,"unit":"credits"},"required_balance":{"amount":1,"unit":"credits"}}'
```

Check top-up progress:

```bash
python3 scripts/billing.py status --session-id <topup-session-id>
python3 scripts/billing.py watch --session-id <topup-session-id>
```

Show current balance:

```bash
python3 scripts/billing.py balance --workspace-id <workspace-id>
```

Show recent billing activity:

```bash
python3 scripts/billing.py activity
```

Fetch the caller's referral code, invite link, and attribution summary:

```bash
python3 scripts/billing.py referral-link
```

## Operational Guidance

### Routing Failures

Translate common routing errors into plain language:

- `provider_unavailable`: the selected provider is not currently connected
- `provider_label_mismatch`: the selected provider does not satisfy the
  requested routing hints
- `execution_provider_not_found`: no eligible execution provider matched the
  current request
- `execution_provider_ambiguous`: more than one execution provider matched and
  the server needs narrower labels or an explicit provider override
- `execution_kind_not_available`: the selected provider does not support the
  requested execution kind
- `task_executor_not_found`: no configured task executor matched the current
  long-running task request
- `invalid_routing_labels`: labels were malformed

When these happen:

- restate the provider and labels you actually sent
- suggest retrying with different labels, a different provider, or automatic
  routing
- do not invent hidden labels or undocumented routing fields

For `/v1/tasks` specifically:

- do not suggest provider overrides, labels, or model routing as a recovery
  path
- suggest validating `kind = video` and the `input` payload shape instead

For long-running jobs:

- prefer `tasks-submit --watch` over asking the user to manually follow up with
  `tasks-watch`
- for video-generation requests, treat `tasks-submit --watch` as the default
  completion path unless the user explicitly asks for fire-and-forget behavior
- acknowledge acceptance as soon as a `task_id` is returned
- keep polling until the task reaches a terminal state or times out; do not
  require the user to ask again just to continue watching the same task
- surface final `output` and `metadata` when the task reaches `succeeded`

### Balance And Recovery

When the server returns a structured `402 insufficient_balance` response:

- show the current balance, required balance, and shortfall explicitly
- explain that this is a recoverable billing state
- keep the recovery flow inside OpenClaw until the required Stripe checkout
  step
- prefer authoritative `GET /v1/balance` reads when available
- keep local billing snapshots only as supporting context

When guiding a top-up flow:

- create the top-up session inside OpenClaw
- show the difference between `pending_payment`, `credit_applied`, and
  `payment_failed`
- tell the user that opening the Stripe `checkout_url` is the only required
  external billing step
- refresh balance after credit lands

## Credential Handling

The returned `secret` from API key bootstrap is the steady-state platform
credential for OpenClaw.

- prefer OpenClaw auth profiles over plain repo files or ordinary config
- store the key in the default OpenClaw auth profile when `--store` is used
- avoid echoing raw secrets unless the active command explicitly returns them
- when reporting success, show where the key was stored or loaded from
- never ask the user to paste a platform API key into chat as the normal
  registration path
- if `openmarlin.ai` appears blocked by browser or Cloudflare protection,
  verify that helpers are targeting `https://api.openmarlin.ai` before
  suggesting manual browser actions
