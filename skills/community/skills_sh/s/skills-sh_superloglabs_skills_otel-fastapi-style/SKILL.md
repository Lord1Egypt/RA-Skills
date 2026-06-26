---
name: otel-fastapi-style
description: "FastAPI OpenTelemetry style: native FastAPIInstrumentor, centralized observability init, Python decorators, OTLP logs, and LLM cost metrics."
---

# OTel FastAPI Style

Use native FastAPI instrumentation. Do not replace request handling with manual
middleware just to create spans.

```python
from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

def init_observability(app: FastAPI) -> bool:
    ...
    FastAPIInstrumentor.instrument_app(app)
    return True
```

Keep `FastAPIInstrumentor.instrument_app(app)` with the rest of the
observability setup so the bootstrap is easy to reason about. If the generated
token is not claimed yet because signup is still in progress, it is still okay
to initialize providers; ingest may reject exports until the browser flow
finishes.

## Entrypoint

Initialize before serving user traffic.

```python
app = FastAPI(title="Mugline API")
init_observability(app)
```

## Bounded Work

Use module-scope OTel objects and decorators for helpers that auto-instrumented
HTTP spans cannot see.

```python
tracer = trace.get_tracer("mugline.api")
meter = metrics.get_meter("mugline.api")

@tracer.start_as_current_span("mug.recommend")
async def recommend_mug(*, tenant_id: str, preference: str) -> dict[str, str]:
    span = trace.get_current_span()
    span.set_attribute("tenant.id", tenant_id)
    ...
```

## Logs

For OTLP-forwarded stdlib logs, configure all of these:

- `LoggerProvider`
- `set_logger_provider(logger_provider)`
- `OTLPLogExporter`
- `LoggingHandler`
- `LoggingInstrumentor().instrument(...)`

## LLM Calls

LLM routes need token coverage:

- `llm.tokens.input`
- `llm.tokens.output`

Tag explicit token counters with tenant, provider, model, use case, call site,
and outcome only when provider instrumentation cannot capture token usage.
Do not add app-side LLM cost metrics or pricing tables; Superlog estimates cost
centrally from provider/model/token data.
