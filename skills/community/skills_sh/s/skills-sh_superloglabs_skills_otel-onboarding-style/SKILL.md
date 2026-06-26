---
name: otel-onboarding-style
description: "General OpenTelemetry onboarding style for Superlog managed agents: native APIs, signal quality, env vars, LLM metrics, and smoke checks."
---

# OTel Onboarding Style

Use native OpenTelemetry APIs. Do not invent helper APIs.

In TypeScript/JavaScript, use the published `@superlog/otel-helpers` `withSpan`
helper for bounded business spans and add `@superlog/otel-helpers` to
`package.json` when it is not already present. This is required when the package
can be installed. `withSpan` is the intended replacement for expanding a whole
function into `tracer.startActiveSpan(...)` plus `try` / `catch` / `finally`. Do
not use helpers to wrap provider SDK calls that OpenInference/provider
instrumentation can observe directly.

Do:

```ts
const tracer = trace.getTracer("mugline.api");
const meter = metrics.getMeter("mugline.api");
const ordersSubmitted = meter.createCounter("orders.submitted");

await withSpan("order.submit", async (span) => {
  span.setAttributes({
    "tenant.id": tenantId,
    "order.id": orderId,
    outcome: "success",
  });
  ordersSubmitted.add(1, { "tenant.id": tenantId, outcome: "success" });
}, { tracer });
```

Do not:

```ts
await sendSuperlogSpan(...);
recordCounter(...);
withTelemetry(...);
```

## Naming

- Files/functions are provider-neutral: `telemetry.ts`, `observability.ts`,
  `initTelemetry()`, `initObservability()`.
- The word Superlog belongs only in endpoint/key setup comments or PR
  instructions.
- Span names are conventional and low-cardinality: `checkout.process`,
  `voice.session`, `llm.generate_copy`.
- Prefer semantic product-operation span names over provider transport names.
  `llm.generate_copy` or `llm.voice_response` is usually more useful than
  `llm.anthropic.messages.create`.

## Endpoint and public token

Inline the endpoint and the Superlog public ingest token directly in the
bootstrap source. The token starts with `sl_public_`, is project-scoped and
write-only, and is intended to be safe in browser/mobile/server source code
like a PostHog project token or Sentry DSN.

```text
SUPERLOG_ENDPOINT = "https://intake.superlog.sh"
SUPERLOG_PUBLIC_TOKEN = "sl_public_…"
```

Do not invent legacy names such as `SUPERLOG_API_KEY` or `SUPERLOG_INTAKE_URL`,
even as placeholder text in docs or comments. While pairing is in flight, use
the generated `sl_public_` token in source; ingest may reject it until the
signup intent flow claims it for the user's project.

Pass the inline values to the SDK explicitly via the exporter constructor's
`endpoint` / `headers` options. Do not configure Superlog through implicit
OTEL env-var reads; missing env vars are the main onboarding failure mode this
skill avoids.

The token goes in the **`x-api-key`** header. Ingest accepts only
`x-api-key: <token>` or `Authorization: Bearer <token>` (literal `Bearer `
prefix required) — prefer `x-api-key`. Any other header name returns 401 on
every request even though the token is valid, which is the second most common
onboarding failure after missing env vars. Define a one-line helper so the
header name lives in one place:

```ts
function superlogHeaders(token: string): Record<string, string> {
  return { "x-api-key": token };
}
```
```python
def superlog_headers(token: str) -> dict[str, str]:
    return {"x-api-key": token}
```

If the repo can call telemetry init from multiple paths, guard provider/exporter
setup so repeated imports, tests, reloads, or framework callbacks do not install
duplicate processors or log handlers. For a single-entrypoint app that starts
cleanly, keep this simple.

Include standard resource attributes when values are available:
`service.name`, `service.version`, `deployment.environment.name`, and the VCS
attributes below.

## Environment tagging

Tag every signal with the runtime environment when possible. Prefer setting
`deployment.environment.name` once on the OTel resource so it propagates to
traces, logs, and metrics. Infer it from existing platform env vars such as
`NODE_ENV`, `VERCEL_ENV`, `RAILWAY_ENVIRONMENT_NAME`, `FLY_APP_NAME`/release
metadata, `ENVIRONMENT`, `APP_ENV`, or `PYTHON_ENV`; normalize obvious values
to low-cardinality names like `local`, `development`, `preview`, `staging`, and
`production`.

If a runtime/exporter path cannot attach resource attributes to all observables,
add the same low-cardinality environment value to custom span attributes, log
records, and metric data points manually. Do not create separate attribute names
such as `env`, `environment`, or `app.environment` unless the repo already has a
standard; use `deployment.environment.name` wherever the SDK allows it.

## VCS resource attributes

Set `vcs.repository.url.full` on the OTel resource for every instrumented
service. The value is the canonical https URL of the repo (e.g.
`https://github.com/acme/api`) — the same URL the user would paste in a
browser, not an SSH URL, not a local working-tree path. This is the important
one: it lets Superlog link telemetry back to the source of truth. It is fine
to hardcode this string alongside `service.name` in the SDK init; if a build
env already exposes the slug (e.g. `VERCEL_GIT_REPO_OWNER` +
`VERCEL_GIT_REPO_SLUG`, `RAILWAY_GIT_REPO_OWNER` + `RAILWAY_GIT_REPO_NAME`),
prefer reading from env so a fork or rename doesn't drift.

Also set `vcs.ref.head.revision` (the commit SHA) on a best-effort basis. Read
it from whatever env var the runtime/build platform already injects:
`VERCEL_GIT_COMMIT_SHA`, `RAILWAY_GIT_COMMIT_SHA`, `GITHUB_SHA`,
`SOURCE_COMMIT`, `GIT_COMMIT`, `HEROKU_SLUG_COMMIT`, etc. Do not shell out to
`git` from the running process — many production images do not have git or a
working tree. If no env source is available, omit the attribute; skipping the
SHA is fine, skipping the URL is not.

Use `vcs.repository.url.full` and `vcs.ref.head.revision` exactly as named —
these are the OTel semantic-convention keys. Do not invent parallel attributes
like `git.repo` or `app.repo_url`.

## Signals

The baseline goal for every instrumented service is RED per software component:
operation count, error count, and operation duration. Two things must hold:

- `service.name` is set on every signal, so RED can be rolled up per service.
- Each distinct unit of work produces its own span/metric series with a
  low-cardinality operation identifier — an HTTP route template, a queue
  handler name, a scheduled job name, an RPC method, etc. RED must be
  answerable per operation, not just per service.

If a service ships without something that produces those three numbers per
operation for its main work (inbound HTTP requests, queue handlers, scheduled
jobs, background loops, etc.), the onboarding is incomplete.

- Traces: all critical operations have spans with relevant attributes. Every
  service has at least one span per inbound unit of work — usually from HTTP /
  framework auto-instrumentation, otherwise a manually wired `withSpan` (or
  language equivalent) around the request/handler entry point.
- Logs: structured, concise, OTLP-forwarded, and trace/span-correlated.
- Metrics: critical operations have low-cardinality counters/histograms.
- Tenant/org/project information is included where available.
- Do not put raw user ids or request ids in metric tags unless the repo already
  treats them as bounded tenant-like ids.

## HTTP and framework instrumentation

For each service, install the standard OpenTelemetry HTTP/server
instrumentation for its language and framework (e.g.
`@opentelemetry/instrumentation-http` plus the framework package in Node,
`opentelemetry-instrumentation-fastapi` / `-django` / `-flask` in Python, etc.)
and add it to `package.json` / `pyproject.toml` if missing. This is what
populates `http.server.request.duration`, `http.request.method`, and
`http.response.status_code` and makes RED work without per-route code.

If the service's framework or runtime has no auto-instrumentation available
(custom server, exotic runtime, RPC over a non-HTTP transport, background
worker loop), wire spans manually at the entry point so every unit of work
produces one span with `http.*` or operation-appropriate attributes and a
status. Do not skip this step on the grounds that the service "only has
business spans" — those don't give you per-service RED.

## Errors

Every span that represents a unit of work must signal failure consistently so
error counts are derivable:

- On a caught exception, call `span.recordException(err)` and
  `span.setStatus({ code: SpanStatusCode.ERROR, message })` (or the language
  equivalent). Auto-instrumentation usually does this for HTTP 5xx; you still
  need it for handled errors and for manually wired spans.
- Set an `outcome` attribute of `"success"` or `"error"` on business spans
  and matching metric data points, so a single low-cardinality dimension
  splits RED into success vs. error without joining on status code.
- For known error classes, also set `error.type` to a short, low-cardinality
  string (e.g. `"timeout"`, `"validation"`, `"upstream_5xx"`). Do not use the
  exception message — it's unbounded.
- Do not swallow exceptions silently inside a `withSpan` callback; rethrow
  after recording so the surrounding span and caller see the failure.

## LLM Metrics

If the app uses LLMs, first look for provider instrumentation that already
captures model/provider/token/error spans. In JavaScript/TypeScript, prefer
OpenInference packages such as
`@arizeai/openinference-instrumentation-anthropic` for supported SDKs. Keep the
real provider call native and readable.

```ts
const response = await client.messages.create({
  model,
  max_tokens: 100,
  messages,
});
```

Every provider/call site still needs enough telemetry to answer usage questions.
Let provider instrumentation own model/provider/token spans where it supports
them. Do not duplicate those attributes at every application call site, and do
not put provider pricing tables or cost math in product handlers. Superlog
computes estimated LLM cost centrally in the UI/query layer from captured
provider/model/token data.

```ts
llmInputTokens.add(inputTokens, {
  "tenant.id": tenantId,
  "gen_ai.provider.name": "anthropic",
  "gen_ai.request.model": model,
  "app.gen_ai.use_case": "voice.initial_greeting",
  "app.gen_ai.call_site": "_callMugCopyLlm",
  outcome: "success",
});
```

Use counters for additive totals only when provider instrumentation cannot
capture token usage:

- `llm.tokens.input`
- `llm.tokens.output`

Token counters use `unit="tokens"` or the SDK equivalent. If
OpenInference/provider instrumentation already captures token usage, do not
duplicate token counters just to mirror it. Do not add `llm.cost_usd` or
equivalent app-side cost metrics for normal LLM calls; cost belongs in Superlog's
central pricing layer.

Use histograms for latency/duration distributions.

Prefer current `gen_ai.*` semantic-convention-style attribute names for LLM
provider/model/token attributes, plus `app.gen_ai.*` for bounded application
dimensions such as use case and call site. Avoid inventing parallel `llm.*`
attributes unless the repo already standardizes on them.

If the app has OpenAI, Anthropic, and Google callers, instrument all three.

## Smoke Checks

Add a durable smoke path when the repo has a natural place for it: README,
TESTING guide, script, npm command, pytest, or checked-in command note.

The smoke should explicitly prove startup/import with OTel env vars present so
provider setup, exporter construction, log bridging, and framework
instrumentation initialize without errors. Then, where practical, exercise an
actual instrumented span/log/metric or OTLP export attempt. A generic health
route only proves the server responds; prefer an operation that crosses the
instrumentation you added.
