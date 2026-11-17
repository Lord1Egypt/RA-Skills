# Usage-evidence optimization workflow

Capability revision: `2.3.0`.

## Inputs and invocation conditions

Use this workflow when the user asks to improve a feature from real usage, requests an evidence-led iteration, or says “利用用户数据优化功能效果”. The preferred input is an Agent-ready optimization pack containing a time window, aggregate metrics, bounded dimensions, funnels, ranked opportunities, experiment suggestions, and privacy notes. An event stream may be used only to build that pack; do not hand raw personal content to an Agent.

Minimum safe event input:

```json
{
  "feature": "video-poster",
  "event": "poster_generation_completed",
  "outcome": "success | failure | fallback",
  "durationMs": 4200,
  "properties": {
    "engine": "provider-family",
    "provider": "provider-family",
    "referenceMode": "none | uploaded | library",
    "failureCode": "bounded-code"
  }
}
```

Never include prompts, captions, transcripts, video URLs, source paths, image pixels, titles, free-form feedback, names, emails, IP addresses, API keys, or arbitrary request bodies. Hash a random anonymous session ID with a deployment-local salt before storage. Normalize operation paths so job IDs and UUIDs do not become dimensions.

## Outputs

Produce both:

- a machine-readable current pack (`current.json`) with schema version, window, counts, rates, latency percentiles, bounded dimensions, funnel steps, ranked opportunities, experiments, and warnings;
- a concise Agent-readable current pack (`current.md`) containing the exact command context, top opportunities, evidence, safe next actions, and data limitations.

Daily raw events and aggregates may be retained separately, but the default Agent input is the current pack. Keep actual providers and fallback outcomes visible; never merge a fallback into success merely because a file exists.

## Optimization loop

1. Build the pack for a declared window, normally 30 days.
2. Check sample size and instrumentation coverage. Treat small or missing samples as discovery evidence, not proof.
3. Pick one ranked opportunity. Write the target metric, guardrail, expected mechanism, and failure reproduction before editing.
4. Implement the smallest change that can affect that opportunity. Preserve event names and property semantics across the comparison window.
5. Run deterministic/adversarial regression tests plus a forward test on different input.
6. Compare the same success, fallback, failure, latency, completion, and correction signals. Record result as supported, inconclusive, or rejected.
7. Feed only new bounded event types or dimensions back into the schema; reject arbitrary analytics payloads.

## Failure handling

| Failure | Safe behavior |
| --- | --- |
| No events in the window | return an empty pack with an instrumentation warning; do not invent priorities |
| Event file is malformed | skip and count malformed lines; preserve valid data and report the count |
| Sample is too small | label opportunities exploratory and prefer qualitative/adversarial reproduction |
| Admin authorization missing | deny remote pack access; local generation may continue |
| Storage is unavailable | product workflows continue; telemetry failure must not block user output |
| Schema changes | bump the schema version and provide an additive migration; never reinterpret old fields silently |

## Reuse value

The pack is deliberately stack-independent: another Agent, dashboard, experiment service, or analyst can consume it without reading application logs or personal content. Stable event names and bounded dimensions make before/after comparisons reusable across poster generation, element redraw, journal creation, recall, and provider failover.

## Version evolution

- `2.3.0`: introduces privacy-safe usage events, daily aggregation, an Agent-ready optimization pack, evidence thresholds, and a metric-preserving optimization loop.
- Patch releases may clarify thresholds or add safe failure messages without changing field meaning.
- Minor releases may add optional bounded dimensions, funnels, or experiment fields.
- Major releases are required when event meanings, privacy boundaries, or required pack fields change.
