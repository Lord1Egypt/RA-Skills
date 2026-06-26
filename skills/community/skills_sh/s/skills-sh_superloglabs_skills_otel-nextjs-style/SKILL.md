---
name: otel-nextjs-style
description: "Next.js/Vercel OpenTelemetry style: instrumentation.ts, @vercel/otel bootstrap, native @opentelemetry/api call sites, inline public ingest token, and no raw NodeSDK replacement."
---

# OTel Next.js Style

For Next.js apps, prefer the framework entrypoint.

```ts
// instrumentation.ts
import { registerOTel } from "@vercel/otel";

export function register() {
  registerOTel({
    serviceName: "mugline-web",
  });
}
```

Do not replace this with a custom `NodeSDK` bootstrap unless the repo is not a
normal Next/Vercel app or already has a custom provider that must be extended.

For JavaScript/TypeScript LLM providers, prefer provider instrumentation over
manual child spans. For Anthropic, add OpenInference in the same bootstrap and
keep call sites native. This example uses `@vercel/otel@2.x`; if the installed
types are v1, use `logRecordProcessor` singular instead.

```ts
import Anthropic from "@anthropic-ai/sdk";
import { AnthropicInstrumentation } from "@arizeai/openinference-instrumentation-anthropic";
import { OTLPLogExporter } from "@opentelemetry/exporter-logs-otlp-http";
import { BatchLogRecordProcessor } from "@opentelemetry/sdk-logs";
import { registerOTel } from "@vercel/otel";

const anthropicInstrumentation = new AnthropicInstrumentation({
  traceConfig: {
    hideInputs: true,
    hideOutputs: true,
  },
});

anthropicInstrumentation.manuallyInstrument(Anthropic);

export function register() {
  registerOTel({
    serviceName: "mugline-web",
    instrumentations: [anthropicInstrumentation],
    logRecordProcessors: [new BatchLogRecordProcessor(new OTLPLogExporter())],
  });
}
```

## Route Handlers

Use native OTel APIs where auto-instrumentation is blind.

```ts
import { withSpan } from "@superlog/otel-helpers";

const tracer = trace.getTracer("mugline.web");
const meter = metrics.getMeter("mugline.web");
const requests = meter.createCounter("mug.copy.generated");

export async function POST(request: Request) {
  const tenantId = request.headers.get("x-tenant-id") ?? "tenant_demo";
  return await withSpan("mug.copy.generate", async (span) => {
    span.setAttribute("tenant.id", tenantId);
    requests.add(1, { "tenant.id": tenantId, outcome: "success" });
    return Response.json({ ok: true });
  }, { tracer });
}
```

For TypeScript route handlers, use `@superlog/otel-helpers` `withSpan` for
bounded business spans and add `@superlog/otel-helpers` to `package.json` when it
is not already present. This is required when the package can be installed. It
keeps span lifecycle/error handling out of the handler body and avoids a large
indentation diff. Do not expand the whole route into
`tracer.startActiveSpan(...)` plus `try` / `catch` / `finally` unless the helper
cannot be added or the span has a true cross-callback lifecycle.

If a route has an LLM call and OpenInference/provider instrumentation supports
that SDK, do not wrap the provider call. Leave `client.messages.create(...)` /
equivalent in place and put business context on the active product span or
structured log. Do not duplicate provider/model/token attributes in route-level
spans, logs, or metrics when OpenInference already reports them. Do not calculate
LLM cost in route handlers; Superlog derives estimated cost in the UI/query layer
from OpenInference provider/model/token attributes.
For Anthropic in Next.js/ESM, keep the instrumentation instance and
`manuallyInstrument(Anthropic)` call at module scope so it runs once and before
route code.

Match the `@vercel/otel` logs option to the installed package/types:
`@vercel/otel@1.x` uses `logRecordProcessor` singular, while
`@vercel/otel@2.x` uses `logRecordProcessors` plural. For normal
Next.js/Vercel apps, do not guard
`registerOTel(...)` behind `NEXT_RUNTIME`; Next calls `instrumentation.ts` in
the appropriate runtime and `@vercel/otel` handles its own runtime differences.

`console.info` is not OTLP log export. If there is no existing logger bridge,
use `@opentelemetry/api-logs` for production log records. Remove pre-existing
`console.*` calls that duplicate the same structured OTel log event:

```ts
logger.emit({
  severityNumber: SeverityNumber.INFO,
  severityText: "INFO",
  body: "generated mug copy",
  attributes: {
    "tenant.id": tenantId,
    "gen_ai.provider.name": "anthropic",
    "gen_ai.request.model": model,
    "app.gen_ai.use_case": "web.mug_copy",
    outcome: "success",
  },
});
```

## Configuration And Smoke

Use the source-level public Superlog configuration pattern from
`otel-onboarding-style` inside `instrumentation.ts`, then pass those constants
explicitly to `registerOTel`. The public project token is write-only and belongs
with the endpoint in the setup block, like a PostHog project token or Sentry
DSN.

```ts
const SUPERLOG_ENDPOINT = "https://intake.superlog.sh";
const SUPERLOG_PUBLIC_TOKEN = "sl_public_...";

// The token MUST be sent as the `x-api-key` header. Ingest only reads
// `x-api-key` or `Authorization: Bearer <token>`; any other header name 401s.
function superlogHeaders(token: string): Record<string, string> {
  return { "x-api-key": token };
}

registerOTel({
  serviceName: "mugline-web",
  traceExporter: new OTLPTraceExporter({
    url: `${SUPERLOG_ENDPOINT}/v1/traces`,
    headers: superlogHeaders(SUPERLOG_PUBLIC_TOKEN),
  }),
  // …same shape for log + metric exporters
});
```

Smoke checks should use tools already in the repo, e.g. `npm run typecheck` or
`npm run build`, plus a real app request where practical. Do not invent fragile
inline Node scripts that import TypeScript source files directly, and do not
assume `ts-node` exists unless it is already installed.
