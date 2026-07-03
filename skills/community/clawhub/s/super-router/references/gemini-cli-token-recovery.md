# Recovering Gemini CLI token usage when super-router ledger is unavailable

Use this when any super-router process stops before the final token ledger is printed, but one or more underlying Gemini CLI calls completed. This includes planning-capture harness termination, manual kill, timeout, crash, interrupted executor fanout, metadata extraction failure, or finalizer failure. The recovery is phase-agnostic: recover every completed Gemini CLI call in the router process time window, then attribute calls to phases where possible.

## Symptom

A super-router run stops before emitting its normal token ledger / `Token Usage Summary`, for example:

- planning-capture harness terminates after the streamed plan
- user/manual kill
- timeout
- process crash
- executor fanout interruption
- metadata extractor/finalizer failure
- any other incomplete router run

The router artifact may show token fields as `null` / unavailable, often with:

```json
"usage_source": "unavailable: router terminated after streamed plan before final token ledger"
```

The router log may also contain no `Token Usage Summary` lines.

## Recovery source

Gemini CLI persists session JSONL files under:

```text
~/.gemini/tmp/<user>/chats/session-*.jsonl
```

For a run, filter by the router capture time window. Each relevant JSONL often contains a `tokens` object like:

```json
"tokens": {
  "input": 16338,
  "output": 306,
  "cached": 0,
  "thoughts": 3348,
  "tool": 0,
  "total": 19992
},
"model": "gemini-3-flash-preview"
```

## Procedure

1. Determine the router process start/stop window from available evidence: wrapper JSON, terminal/process timestamps, router logs, output artifact mtimes, or shell history.
2. Normalize the time window carefully. Gemini CLI `session-*.jsonl` filenames may align with UTC-like timestamps while terminal `date` output or user-facing run logs may be local time. If an initial local-time search finds zero token records, retry using the UTC timestamp from the run artifact.
3. Read router artifacts for phase/model context: planner, judge, pro, flash, metadata extractor, and finalizer models when available.
4. List Gemini CLI session files around that time:

```bash
ls -lt ~/.gemini/tmp/$USER/chats/session-YYYY-MM-DDTHH-*.jsonl
```

4. Parse candidate files and extract nested objects containing `tokens.total`, `model`, and timestamps/snippets if present.
5. Deduplicate by `(file, model, token-object)`.
6. Attribute records whose timestamps overlap the router run window and whose models/prompts/snippets match expected router phases.
7. Sum `input`, `output`, `cached`, `thoughts`, `tool`, and `total`; optionally group by model and inferred phase.
8. Patch telemetry as recovered provider telemetry, not an estimate. If phase attribution is uncertain, label it `super_router_recovered_unattributed` rather than guessing.

## Python snippet

```python
import json, pathlib
chatdir = pathlib.Path('~/.gemini/tmp').expanduser() / pathlib.Path.home().name / 'chats'
files = sorted(chatdir.glob('session-YYYY-MM-DDTHH-*.jsonl'))
records = []
for p in files:
    for line in p.read_text(errors='ignore').splitlines():
        try:
            obj = json.loads(line)
        except Exception:
            continue
        def visit(x):
            if isinstance(x, dict):
                if isinstance(x.get('tokens'), dict) and 'total' in x['tokens']:
                    records.append({'file': p.name, 'model': x.get('model'), 'tokens': x['tokens']})
                for v in x.values():
                    visit(v)
            elif isinstance(x, list):
                for v in x:
                    visit(v)
        visit(obj)
seen, uniq = set(), []
for r in records:
    key = (r['file'], r.get('model'), json.dumps(r['tokens'], sort_keys=True))
    if key not in seen:
        seen.add(key)
        uniq.append(r)
sums = {k: sum(int(r['tokens'].get(k, 0) or 0) for r in uniq)
        for k in ['input', 'output', 'cached', 'thoughts', 'tool', 'total']}
print(sums)
```

## Interpretation

- `input`: prompt/context tokens.
- `cached`: subset of input/context served from provider cache; do not add it again to input.
- `thoughts`: provider-reported internal reasoning tokens.
- `output`: visible response tokens.
- `total`: provider-reported total accounting field.

## Caveats

- This recovers token usage, not dollar cost. Dollar cost depends on current provider pricing and cached-token billing rules.
- Only use files in the matching time window; other Gemini/Codex jobs may create nearby sessions.
- If multiple concurrent Gemini jobs used the same models in the same minute, inspect prompts/text snippets before attributing records.
