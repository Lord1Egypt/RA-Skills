---
name: superlog-onboard
description: "Onboard a project to Superlog by installing OpenTelemetry traces, logs, and metrics across every app and service in the repo. Triggers on requests like 'install Superlog', 'set up Superlog', 'add Superlog telemetry', 'onboard this repo to Superlog', 'instrument with OpenTelemetry for Superlog'."
---

# Superlog onboarding

Wire OpenTelemetry traces, logs, and metrics into the user's project so telemetry streams to Superlog. Cover **every app and service in the repo** — not just the one the user is currently sitting in.

Prefer native OpenTelemetry APIs and the framework's documented bootstrap over custom helper layers. If a specific stack stumps you, search the OTel docs for that language; don't guess.

Before editing, read the applicable companion skills:

- `otel-onboarding-style` for general OTel taste.
- `otel-python-style` for Python services.
- `otel-fastapi-style` for FastAPI services.
- `otel-livekit-style` for LiveKit agents.
- `otel-nextjs-style` for Next.js/Vercel apps.
- `otel-expo-style` for Expo / React Native apps.
- `otel-supabase-edge-style` for Supabase Edge Functions.
- `otel-generic-style` for any other language (Go, Java/Kotlin, Ruby, Rust, .NET/C#, PHP, Elixir, plain Node, …) — use this as the fallback when none of the above match.

## Step 0 — Endpoint and public token handling

The **OTLP endpoint** is always `https://intake.superlog.sh` and goes directly
in the bootstrap source.

The **Superlog public ingest token** starts with `sl_public_`. It is
project-scoped, write-only, and intentionally safe to include in application
source, including browser and mobile bundles. Treat it like a PostHog project
token, Sentry DSN, or Datadog RUM client token: it can send telemetry to one
project, but cannot read data, change settings, or access the Superlog account.

Inline the public token as a constant next to the endpoint. Do not put it in
`.env` files, deploy settings, or generated shell commands; source-level config
is the intended onboarding path and avoids broken deploys from missing env vars.

When an OTLP exporter requires headers, pass the public token through the
exporter constructor as the **`x-api-key`** header. This is the single most
common onboarding failure: the token is valid, but the exporter sends it under
the wrong header name (or no header), so ingest returns 401 on every request and
the install looks broken when the key is fine. Ingest reads the token from
exactly two places — `x-api-key: <token>`, or `Authorization: Bearer <token>`
(the literal `Bearer ` prefix is required). Use `x-api-key`; it avoids the
`Bearer `-prefix footgun and survives proxies/SDKs that strip `Authorization`.
Do **not** invent other header names (`api-key`, `x-superlog-token`,
`Authorization: <token>` without `Bearer `) — all of them 401.

Wrap it in a one-line helper so the header name lives in exactly one place, and
**define the helper** — never call an undefined `superlogHeaders`:

```ts
function superlogHeaders(token: string): Record<string, string> {
  return { "x-api-key": token };
}
```
```python
def superlog_headers(token: str) -> dict[str, str]:
    return {"x-api-key": token}
```

Two paths, no questions asked:

### Public token in the prompt

If the invoking prompt contains an `sl_public_...` token, validate the prefix and
inline it in every telemetry bootstrap file you write. Do not print the full
token in chat; it will be visible in the code diff like any other public client
token.

### No public token

Generate a public token locally, register a signup intent immediately, then
keep working in parallel — don't block install on signup.

1. Generate a random plaintext public ingest token with the shape
   `sl_public_<base64url-ish random bytes>`. Use at least 32 bytes of entropy
   after the prefix. Keep the plaintext in memory so you can inline it in
   bootstrap files, but never print the full token back to chat.
2. Compute `keyHash = sha256(plaintextToken)` as lowercase hex and
   `keyPrefix = the token prefix plus the first 6 token characters after the
   prefix`.
3. `POST https://api.superlog.sh/api/signup-intents` with
   `Content-Type: application/json` and body:

   ```json
   {
     "keyHash": "<sha256 hex>",
     "keyPrefix": "<short public token prefix>",
     "returnTo": null
   }
   ```

   If the agent runtime exposes a safe return/deep link back to the current
   conversation, pass it as `returnTo`; otherwise use `null`. Never put the
   plaintext token in this request.
4. The response includes `id`, `signupUrl`, and `expiresAt`. Open `signupUrl`
   in the user's default browser (`open "$signupUrl"` / `xdg-open "$signupUrl"`
   / `start "" "%signupUrl%"`) and print the URL in chat. Mention briefly that
   the signup tab is open (GitHub/Slack integrations happen there) and that the
   install will check ingest at the end — no need to interrupt their current
   flow.
5. **Do not block on signup.** Keep going with Steps 1–4 using the generated
   plaintext token in the bootstrap source. Step 4 is the gate: it sends real
   telemetry and uses the response code to decide whether the user still needs
   to finish signup.

## Step 1 — Map every app/service in the repo

Before instrumenting anything, enumerate what's here. Check workspace manifests (`pnpm-workspace.yaml`, root `package.json` `workspaces`, `go.work`, Cargo workspace, Python `pyproject.toml` workspace setups, `apps/*` and `services/*` conventions). Identify each service: web frontend, API, workers, background jobs, CLIs, sample/demo apps, mobile apps, Supabase and/or server functions. Mobile and serverless/edge functions are in scope; do not skip them merely because they are client-side or short-lived. Skip pure type/config packages with no runtime entry point. Do not skip any runnable services or leave them "out of scope": instrument absolutely everything in this run; there may be no follow-up.

Show the user the list before you start, so they can correct it.

## Step 2 — For each service, install native OTel and bootstrap

**Use the language's native OpenTelemetry SDK.** Don't reach for vendor wrappers or hand-rolled helpers when an official package exists. Examples of what "native" means here: `@opentelemetry/sdk-node` for Node servers, `@vercel/otel` for normal Next.js/Vercel apps (sdk-node breaks Next's webpack and misses the framework bootstrap), `@opentelemetry/sdk-trace-web` + browser/mobile-compatible exporters for Vite/SPA/Expo, `opentelemetry-instrumentation-*` + `opentelemetry-sdk` for Python, `go.opentelemetry.io/otel` for Go.

No broad wrapper APIs. Avoid reusable helpers like `sendSuperlogSpan`, `recordCounter`, `recordLog`, `startTelemetrySpan`, or `withTelemetry`. Acquire native tracers/meters/loggers at module scope and use the SDK's own APIs directly. In TypeScript/JavaScript, use the published `@superlog/otel-helpers` `withSpan` helper for bounded business spans and add `@superlog/otel-helpers` to `package.json`; this is required when the package can be installed because it avoids expanding a whole function into `startActiveSpan` plus `try` / `catch` / `finally`. Do not use helpers around provider SDK calls that OpenInference/provider instrumentation can observe directly. If an edge runtime genuinely cannot load an upstream OTel SDK, keep the shim tiny, provider-neutral, and OTel-shaped: `tracer.startActiveSpan`, `span.setAttributes`, `SpanStatusCode`, `meter.createCounter`, `histogram.record`.

Wire all three signals — traces, logs, metrics. **Logs go through OTLP, not just stdout** — set up the OTel log bridge for the language so app logs (with their existing log levels and structured fields) carry the active `trace_id` / `span_id` automatically. The user's existing logger keeps working; you're just adding an OTLP handler/processor underneath.

The log bridge is not optional and is not "covered" by the SDK init alone — most language SDKs and framework wrappers wire traces (and sometimes metrics) by default but require an **explicit** `LoggerProvider` + OTLP log exporter + log-record processor + a bridge to the existing logger. Examples: Python stdlib needs `LoggerProvider` + `OTLPLogExporter` + `LoggingHandler` attached to the root logger (and `LoggingInstrumentor` for trace correlation on existing records); Node needs `@opentelemetry/sdk-logs` + an instrumentation for the project's logger (`pino`/`winston`/`bunyan`); `@vercel/otel` requires the `logRecordProcessor(s)` option — without it, no logs leave the process. The companion style skills spell out the exact pieces per stack — read them.

Common log-bridge mistakes to actively check for:
- Handler attached to a named logger when the app uses the root logger (or vice versa) — nothing flows.
- Default level filter (e.g. WARNING) swallowing the INFO/DEBUG lines the user actually wants in Superlog.
- `BatchLogRecordProcessor` not flushed on shutdown → short-lived CLIs, serverless, and edge functions drop the last batch. Wire `shutdown()` / `forceFlush()` into the runtime's exit hook.
- An existing vendor transport (Pino → Logtail, Winston → Datadog, etc.) left in place is fine and expected — but make sure you're bridging from the *logger*, not adding a second transport that double-emits the same line through a different formatter.
- Logs emitted outside any span will arrive without `trace_id` / `span_id`. That is correct and expected; do not "fix" it by starting throwaway spans around log calls.

Bootstrap rules:
- The bootstrap file must run before any framework imports. Use the language/framework's documented hook (`--import` flag, `instrumentation.ts`, top-of-`main.py` import, etc.).
- Inline the endpoint (`https://intake.superlog.sh`) and public ingest token directly in the bootstrap source. Do not read from `process.env.OTEL_EXPORTER_OTLP_*` or write any `.env` files. (See the framework-specific style skills for the exact shape per stack.)
- Use HTTP OTLP exporters, not gRPC. gRPC pulls in native bindings that break bundlers and complicate containers.
- Use the project's existing package manager (detect via lockfile).
- Prefer idempotent edits. If a config file already exists, edit don't overwrite.
- Set resource attributes on the OTel resource for every service: `service.name`, `service.version`, `deployment.environment.name`, and **`vcs.repository.url.full`** — the canonical https URL of the repo (e.g. `https://github.com/acme/api`). The repo URL is the important one and is fine to hardcode alongside `service.name` in the SDK init; if the build platform exposes the slug (Vercel `VERCEL_GIT_REPO_OWNER`/`VERCEL_GIT_REPO_SLUG`, Railway `RAILWAY_GIT_REPO_OWNER`/`RAILWAY_GIT_REPO_NAME`), prefer reading from env. Also set **`vcs.ref.head.revision`** (commit SHA) on a best-effort basis from whatever env the runtime already injects (`VERCEL_GIT_COMMIT_SHA`, `RAILWAY_GIT_COMMIT_SHA`, `GITHUB_SHA`, `SOURCE_COMMIT`, `GIT_COMMIT`, `HEROKU_SLUG_COMMIT`, …). Do not shell out to `git` from the running process. Skipping the SHA is fine, skipping the URL is not. Use the OTel semantic-convention keys exactly — do not invent `git.repo` / `app.repo_url`.

Framework rules:
- **Next.js/Vercel:** use `instrumentation.ts` with `@vercel/otel` `registerOTel(...)` as the bootstrap. Do not substitute a raw `@opentelemetry/sdk-node` / `NodeSDK` bootstrap unless the repo already uses that architecture and you are extending it. Use `@opentelemetry/api` tracers/meters inside route handlers only where auto-instrumentation is blind. **`registerOTel` does not export logs by default** — pass `logRecordProcessor` (v1) / `logRecordProcessors` (v2) with an `OTLPLogExporter` from `@opentelemetry/exporter-logs-otlp-http`, or no logs will leave the process. Match the option name to the installed `@vercel/otel` major version.
- **Expo/React Native:** preserve existing Expo Go / unsupported-runtime guards. In supported builds, call `initObservability()` before Sentry and before app registration/user code. Inline the endpoint + `sl_public_` token in the observability module; do not use `EXPO_PUBLIC_*` env vars for Superlog.
- **Supabase Edge Functions:** native Deno OpenTelemetry does not work in hosted Supabase Edge today. Use the tiny OTel-shaped shim pattern above; keep exporter endpoint/headers in one setup area and avoid Superlog-specific function/file names.
- **Python/FastAPI:** use native instrumentation such as `FastAPIInstrumentor.instrument_app(app)` rather than replacing request handling with manual middleware.
- **Python/LiveKit:** lifecycle spans that cross shutdown callbacks may use `start_span` + `trace.use_span(..., end_on_exit=False)` and end in the shutdown callback. Bounded work should still use decorators or context managers.

**Coexist with existing observability vendors. Don't remove Sentry, Datadog, New Relic, Honeycomb, Logtail, Pino transports, etc.** OTel sits alongside them. The user explicitly wants both signals flowing during migration; ripping out the incumbent is not your call.

## Step 3 — Add custom spans, metrics, and logs around business operations

Auto-instrumentation gets you HTTP in/out, DB queries, framework lifecycle. That's the floor, not the ceiling. Read the project to find the operations a human operator would actually want to see when something looks wrong.

### Traces

Wrap **every critical business operation** with an active span. Auto-instrumented spans are fine where they exist — but if an operation isn't already getting a span, add one.

- Naming: `domain.verb` (`order.process`, `payment.charge`, `email.send`, `agent.run`, `interview.create`, `job.<type>`).
- Attributes: entity IDs (order.id, user.id, workspace.id, tenant.id), counts, key boolean branch outcomes, model name / provider for LLM calls.
- Record exceptions: `span.recordException(err)` + `span.setStatus({ code: ERROR })` on failure paths.
- For Python functions with clear boundaries, prefer `@tracer.start_as_current_span("operation.name")` — the same call works as a decorator and as a context manager, and the decorator form is usually what you want for a whole function:

  ```python
  @tracer.start_as_current_span("do_work")
  def do_work():
      print("doing some work...")
  ```

  Use a context manager when a decorator does not fit (partial scope, dynamic span name, etc.). Do not use detached `start_span()` + manual `end()` for bounded work.
- Skip trivial getters, pure transforms, internal helpers — anything with no real latency or failure mode.
- **Never put PII in attributes** (emails, passwords, tokens, full request bodies).

### Logs

Make sure logs are **structured and carry operation context**. Concretely: every log line emitted inside a span should arrive at Superlog with `trace_id` / `span_id` populated and any structured fields (orderId, userId, etc.) preserved as attributes. Trace/span context may be added natively by the log bridge or integration, or may require additional work.

Use logs for narrative ("starting batch reconcile", "retrying after 3xx") and exceptional events. An error log must only be emitted if the operation cannot recover and manual intervention is required.

### Metrics

Cover **business + performance + cost**. Three categories to look for:

- **Business logic counters.** Every meaningful state transition: created, started, completed, failed, retried. Per-tenant, per-channel, per-status — low-cardinality dimensions only (never user/order IDs).
- **Performance histograms.** Latency of operations the user cares about, queue depth, batch sizes, payload sizes. Reuse existing timing instrumentation if the project already has any (`time.perf_counter` blocks, custom `LatencyTracker`s, "[TIMING]" log lines) — emit a histogram from those measurements rather than measuring twice.
- **Costs — especially LLM costs.** If the project calls OpenAI / Anthropic / Google / any LLM provider, prefer provider instrumentation such as OpenInference where available so native SDK calls stay readable. Do not add pricing constants or LLM cost math in product handlers; Superlog computes estimated cost centrally in the UI/query layer from captured provider/model/token attributes. Avoid duplicating token counters already captured by provider instrumentation.

Get the meter once at module level, create instruments at module level, increment in the hot path. Don't create a fresh meter per call.

## Step 4 — Verify the app still works

Per service:

1. **Run the project's own dev or build command** (whatever its `package.json` / `pyproject` / `Makefile` already wires up). Confirm it starts cleanly with no errors that trace back to your OTel install. Also run a telemetry bootstrap smoke that imports or starts the app, so provider setup, exporter construction, log bridging, and framework instrumentation all initialize. For a Python server this can be an import/startup command such as `uv run python -c 'from app.main import app; print(app.title)'`; for Node/Next use the repo's build/start path. For a server, hit at least one route with curl so traffic flows through the instrumentation; choose a route that exercises an instrumented operation when practical, not only a static health route. For a CLI, invoke a real command. **Don't ship if the app's own startup is now broken** — that's a regression.
2. **Push real telemetry through prod and read the response code — for all three signals.** This is a hard gate. Drive the running app so it actually emits at least one span, one log, and one metric, then watch the OTLP exporter's HTTP responses for `/v1/traces`, `/v1/logs`, and `/v1/metrics`. To force the logs path specifically, hit a route (or invoke a CLI command) that calls the project's logger inside an instrumented operation. The response status from ingest is the signal:

   - **All three return 2xx → done.** Signup is already claimed; move on to Step 5. Do not nudge the user back to the signup tab.
   - **Any return 401/403 → token isn't claimed yet.** Tell the user to finish signup at the URL from Step 0 (the tab is already open). Wait for them to confirm, then re-run the smoke and re-check until you see 2xx on all three. Don't declare success on a 401/403.
   - **Any return 5xx, time out, or never POST → real bug.** Debug it before moving on. If only `/v1/traces` shows up, the log bridge isn't wired (most common causes: `LoggerProvider` never set, handler attached to the wrong logger, level filter too strict, `@vercel/otel` missing `logRecordProcessor(s)`, or shutdown not flushing the batch processor). If `/v1/metrics` is missing, the meter provider or periodic reader isn't wired.

A bootstrap that loads but never POSTs — or POSTs traces but no logs/metrics — is not a partial success. Fix it before moving on.

## Step 5 — Hand-off (final message to the user)

You only reach this step if Step 4 saw 2xx from `/v1/traces`, `/v1/logs`, and `/v1/metrics`. The token is already inlined in the bootstrap source — do not print it back to chat. Telemetry is flowing into the user's project; the next thing they need is a deploy.

### What changed

3–7 short factual bullets covering: packages installed, files created/modified, business spans/metrics added. Per service if changes differed, grouped if uniform. Mention any existing observability vendor (Sentry, Datadog, Logtail, Pino transports, etc.) you intentionally left in place so the coexistence is explicit.

### Deploy

Drive the user into deployment now; don't stop at "deploy as you normally would." Infer the most likely deploy path from the repo and give one concrete next action.

- If the repo has a direct deploy tool/config (`vercel.json`, `netlify.toml`, `fly.toml`, `wrangler.*`, `railway.json`, `render.yaml`, `Dockerfile`, deploy scripts in `package.json`, etc.), name the target and ask for confirmation before running any production/public deploy command: "I can deploy this now with `<command>` to `<target>`. Want me to run it?" If they say yes, run it and watch the result.
- If deployment is CI-on-push/merge, say that clearly and give the exact next step the user needs: commit/push/merge the branch, or open the existing hosting dashboard. Respect the hard rule below: do not commit, push, or open PRs from this skill unless the user explicitly switches you into that task outside the skill run.
- If you can't identify a production path, offer the best local substitute: start the dev server, hit an instrumented route, and tell the user the exact command you used plus what production deploy info you could not find.
- After a deploy or local run, hit at least one instrumented route so traces/logs/metrics flow from the deployed environment too.

There are no Superlog env vars to wire: the endpoint and public token are in the
bootstrap source.

## Step 6 — MCP suggestion

Do not manually drive GitHub or Slack from the agent anymore. The signup intent page handles both integrations after auth; if the user signed in with GitHub, it still verifies the app has the right repo permissions.

Suggest installing the Superlog MCP server so the agent (Claude Code, Codex, Cursor, etc.) can query telemetry directly next time they're debugging — search logs, pull traces, check error rates from inside the chat without context-switching to the dashboard.

For **Claude Code** (most common — that's where this skill is running), offer to run it for them:

```
claude mcp add --transport http superlog https://api.superlog.sh/mcp
```

This edits the user's Claude Code config. **Confirm before running** (the user may have a custom MCP scope or want to install elsewhere). If they decline, print the command so they can run it themselves later.

For other agents the user might also use, mention but do *not* run:

- Codex: `codex mcp add superlog --url https://api.superlog.sh/mcp && codex mcp login superlog`
- Cursor / others: copy the `mcpServers` snippet from https://superlog.sh/ → Connect.

Close out with a single line directing the user to deploy their app — they're ready to ship.

## Hard rules

- Never modify files outside the project root.
- Never commit, push, or open PRs.
- Never run a production/public deploy command without explicit user confirmation after showing the exact command and target.
- Inline only `sl_public_` public ingest tokens. Never inline account/session/admin tokens, private keys, or provider API keys. Do not print full tokens in chat.
- Never remove an existing observability vendor unless the user asks for it.
- Use the project's existing package manager and existing logger.
- Prefer native OTel packages for the language; don't reinvent telemetry plumbing the SDK already provides.
- If the dev/build command errors out *because of* your instrumentation, that's a failure — fix it or report it, don't paper over it.
