---
name: otel-supabase-edge-style
description: "Supabase Edge Function observability style: tiny provider-neutral OTel-shaped shim, OTLP export config, traces/logs/metrics, and LLM cost metrics."
---

# OTel Supabase Edge Style

Hosted Supabase Edge Functions do not support the normal native OTel SDK
lifecycle today. Use a tiny provider-neutral shim that looks like OTel and can
be deleted later if native support lands.

Good reusable API names:

```ts
tracer.startActiveSpan("edge.chat", async (span) => { ... });
span.setAttributes({ "tenant.id": tenantId });
span.setStatus({ code: SpanStatusCode.ERROR });
meter.createCounter("llm.tokens.input").add(tokens, attrs);
histogram.record(durationMs, attrs);
```

Bad reusable API names:

```ts
sendSuperlogSpan(...);
recordCounter(...);
trackSuperlogEvent(...);
```

Keep endpoint/header configuration in one setup area near the top of the
function. Use the source-level public Superlog configuration pattern from
`otel-onboarding-style`; the public project token is write-only and belongs with
the endpoint in the setup block.

```ts
const SUPERLOG_ENDPOINT = "https://intake.superlog.sh";
const SUPERLOG_PUBLIC_TOKEN = "sl_public_...";

// The token MUST be sent as the `x-api-key` header. Ingest only reads
// `x-api-key` or `Authorization: Bearer <token>`; any other header name 401s.
function superlogHeaders(token: string): Record<string, string> {
  return { "x-api-key": token };
}

const OTEL_HEADERS = superlogHeaders(SUPERLOG_PUBLIC_TOKEN);
```

## Signals

- Traces: span around the function operation and each critical provider call.
- Logs: concise structured OTLP log records for critical outcomes.
- Metrics: tenant-tagged counters/histograms for critical operations.
- LLM calls: capture `llm.tokens.input` / `llm.tokens.output` only when provider
  instrumentation is unavailable; tag explicit token counters with tenant,
  provider, model, use case, call site, and outcome. Do not calculate LLM cost in
  edge function code; Superlog estimates it centrally from provider/model/token
  data.

Use `EdgeRuntime.waitUntil(...)` or the runtime's equivalent when available so
OTLP fetches can finish after the response is returned.
