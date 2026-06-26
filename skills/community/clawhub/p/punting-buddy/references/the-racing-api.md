# The Racing API

## Role in this skill

Use The Racing API free plan as the default source for v1.
It is the backbone for:
- what races are next
- what is on today or tomorrow
- course and region discovery
- today's results

## Auth and transport

Current setup supports:
- MCP access via `mcporter`
- direct REST access via HTTP Basic Auth

REST base URL:
- `https://api.theracingapi.com`

Public OpenAPI spec:
- `https://api.theracingapi.com/openapi.json`

## Free-plan endpoints

Use these endpoints first:
- `GET /v1/courses/regions`
- `GET /v1/courses`
- `GET /v1/racecards/free`
- `GET /v1/results/today/free`

Useful params:
- racecards free:
  - `day=today|tomorrow`
  - `region_codes`
  - `course_ids`
  - `limit`
  - `skip`
- results today free:
  - `region`
  - `limit`
  - `skip`

## What the free plan is good for

Good enough for:
- listing upcoming races
- pulling a racecard
- runner-by-runner conversational discussion
- checking today's results
- supporting a punting-buddy style workflow

## What the free plan is not good for

Do not overclaim these on v1:
- deep historical research
- advanced horse, jockey, or trainer metrics
- rich odds/value modelling
- robust quantitative probability modelling

## Rate limiting

Be conservative.
The project notes a free-tier constraint of about `1 request per second`.
Even if docs elsewhere mention higher defaults, do not burst.

Practical rules:
- serialize requests
- avoid needless polling
- prefer fewer larger fetches
- reuse fetched cards within the same conversation
- on `429`, back off and retry later rather than hammering the API

## Time handling

Convert race times into the user's local timezone when replying.
Do not just leave them in UTC unless the user explicitly asks.

## Recommended v1 usage pattern

- broad discovery question -> fetch racecards free once
- specific race question -> reuse cached card if available
- results question -> use results today free
- course filtering -> use courses and regions only if needed
