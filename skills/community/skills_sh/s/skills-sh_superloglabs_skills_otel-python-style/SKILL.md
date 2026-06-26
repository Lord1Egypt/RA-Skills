---
name: otel-python-style
description: "Python OpenTelemetry style: module-scope tracers/meters, decorators for bounded work, error spans, logs, and no wrappers."
---

# OTel Python Style

Acquire OTel objects at module scope.

```python
from opentelemetry import metrics, trace
from opentelemetry.trace import Status, StatusCode

tracer = trace.get_tracer("mugline.voice")
meter = metrics.get_meter("mugline.voice")

greetings = meter.create_counter("voice.greetings.delivered", unit="1")
```

## Bounded Work

`tracer.start_as_current_span(...)` works as both a decorator and a context
manager — the same call. For a whole function, the decorator form is usually
what you want:

```python
@tracer.start_as_current_span("do_work")
def do_work():
    print("doing some work...")
```

It works the same way on async functions and on methods, and you can grab the
active span inside the body with `trace.get_current_span()` to set attributes:

```python
@tracer.start_as_current_span("voice.deliver_initial_greeting")
async def _deliver_initial_greeting(*, tenant_id: str, user_id: str) -> None:
    span = trace.get_current_span()
    span.set_attributes({
        "tenant.id": tenant_id,
        "user.id": user_id,
        "voice.use_case": "initial_greeting",
    })
```

Use a context manager when a decorator does not fit (partial scope, dynamic
span name, etc.).

```python
with tracer.start_as_current_span("order.validate") as span:
    span.set_attribute("tenant.id", tenant_id)
    validate_order(order)
```

Do not use detached `tracer.start_span(...); span.end()` for bounded work.

## Error Paths

Record exceptions on the active span.

```python
try:
    result = await client.messages.create(...)
except Exception as exc:
    span = trace.get_current_span()
    span.record_exception(exc)
    span.set_status(Status(StatusCode.ERROR))
    logger.exception("llm mug copy failed", extra={"tenant_id": tenant_id})
    raise
```

## Logs

If logs are claimed as OTLP-forwarded, configure both:

- an OTel LoggerProvider + OTLPLogExporter + LoggingHandler
- `set_logger_provider(logger_provider)` from `opentelemetry._logs`
- log correlation for existing records, e.g. `LoggingInstrumentor().instrument(...)`

Preserve existing `logging.basicConfig`, console/file handlers, and log levels.

## Init Behavior

Use the source-level public Superlog configuration pattern from
`otel-onboarding-style` in the init module. The public project token is
write-only and belongs with the endpoint in the setup block, like a PostHog
project token or Sentry DSN.

```python
SUPERLOG_ENDPOINT = "https://intake.superlog.sh"
SUPERLOG_PUBLIC_TOKEN = "sl_public_..."


# The token MUST be sent as the `x-api-key` header. Ingest only reads
# `x-api-key` or `Authorization: Bearer <token>`; any other header name 401s.
def superlog_headers(token: str) -> dict[str, str]:
    return {"x-api-key": token}


def init_observability() -> None:
    exporter = OTLPSpanExporter(
        endpoint=f"{SUPERLOG_ENDPOINT}/v1/traces",
        headers=superlog_headers(SUPERLOG_PUBLIC_TOKEN),
    )
    ...
```

Add a small `_INITIALIZED` guard only when the app can realistically call this
function more than once.

## Metrics

Counters:

- `llm.tokens.input`
- `llm.tokens.output`
- requests/events/jobs/errors

Use semantic units when the SDK supports them: token counters use
`unit="tokens"`. Do not add app-side `llm.cost_usd` pricing metrics for normal
LLM calls; Superlog estimates cost centrally from provider/model/token data.

Histograms:

- duration
- latency
- payload size

Avoid raw high-cardinality values in metric attributes. Prefer
tenant/org/project, operation/use case, provider/model, and outcome dimensions
over user-level metric tags.
