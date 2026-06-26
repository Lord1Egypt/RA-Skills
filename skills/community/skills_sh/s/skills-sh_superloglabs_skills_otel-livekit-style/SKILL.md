---
name: otel-livekit-style
description: "LiveKit Agents OpenTelemetry style: entrypoint/session lifecycle spans, shutdown callbacks, session metrics, and LLM turn token counters."
---

# OTel LiveKit Style

LiveKit session lifecycle begins in `entrypoint(ctx)` and cleanup ends in
`ctx.add_shutdown_callback(on_shutdown)`.

## Whole-Session Span

It is okay for a `voice.session` span to end in `on_shutdown`, because the
operation crosses a framework callback boundary. Make it active while child
work is registered and started.

```python
async def entrypoint(ctx: agents.JobContext) -> None:
    await ctx.connect()
    started_at = asyncio.get_running_loop().time()
    session_span = tracer.start_span(
        "voice.session",
        attributes={
            "tenant.id": tenant_id,
            "user.id": user_id,
            "voice.room_name": room_name,
        },
    )

    with trace.use_span(session_span, end_on_exit=False):
        voice_sessions_started.add(1, {
            "tenant.id": tenant_id,
            "voice.room_name.present": room_name != "unknown",
        })

        async def on_shutdown() -> None:
            duration_ms = int((asyncio.get_running_loop().time() - started_at) * 1000)
            session_span.set_attribute("voice.duration_ms", duration_ms)
            voice_session_duration.record(duration_ms, {
                "tenant.id": tenant_id,
                "voice.disconnect_reason": disconnect_reason,
                "outcome": "success",
            })
            session_span.end()

        ctx.add_shutdown_callback(on_shutdown)
        await _deliver_initial_greeting(...)
```

Do not replace this with a short `voice.session.end` span inside shutdown.

## Bounded Session Work

Bounded operations still get their own decorators.

```python
@tracer.start_as_current_span("voice.deliver_initial_greeting")
async def _deliver_initial_greeting(...):
    ...
```

## Session Metrics

Use both:

- `voice.sessions.started` counter at entrypoint start
- `voice.session.duration_ms` histogram in shutdown

Add product metrics for important voice events, e.g.
`voice.greetings.delivered`.

## Smoke Checks

For a minimal LiveKit fixture, a good smoke path imports the agent and executes
one tiny instrumented function or starts a span/log record with a local OTLP
endpoint. Checking that tracer/meter objects are non-None is not enough.

## LLM Turns

Every LLM provider/call site in the voice agent needs:

- span around the call
- token counters (`llm.tokens.input`, `llm.tokens.output`)
- tenant/provider/model/use case/call site/outcome attributes

Do not add `llm.cost_usd` metrics; Superlog estimates cost centrally from
provider/model/token data.

Name the span for the product operation, not the provider transport call.
For example, prefer `llm.voice_response` or `llm.generate_copy` over
`llm.anthropic.messages.create`.

```python
attrs = {
    "tenant.id": tenant_id,
    "llm.provider": "anthropic",
    "llm.model": model,
    "llm.use_case": "voice.initial_greeting",
    "llm.call_site": "_call_mug_copy_llm",
    "outcome": "success",
}
llm_tokens_input.add(input_tokens, attrs)
llm_tokens_output.add(output_tokens, attrs)
```
