# Queue Format

Use a compact, structured markdown queue in `QUESTIONS.md`.

## Canonical layout

```md
# QUESTIONS

Purpose: capture unresolved questions worth deliberate investigation.

Status values: `open`, `investigating`, `blocked`, `done`, `wontfix`

## Active Questions

### Q0001 - Why does OpenClaw sometimes show the wrong context window for gpt-5.4?
- status: open
- kind: debug
- priority: high
- createdAt: 2026-04-06T18:00:00+08:00
- startedAt:
- completedAt:
- source: runtime observation
- allowedTools: read, exec, web_search, web_fetch
- successCriteria: identify the cause or confirm it is an upstream bug/regression
- memoryNote:
- links:
  - ~/.openclaw/openclaw.json
- notes:
  - Previously showed 200k instead of 272k.
- evidence:
- conclusion:

## Completed Questions

### Q0000 - Example completed question
- status: done
- kind: research
- priority: low
- createdAt: 2026-04-05T10:00:00+08:00
- startedAt: 2026-04-05T10:10:00+08:00
- completedAt: 2026-04-05T10:28:00+08:00
- source: example
- allowedTools: web_search, web_fetch
- successCriteria: produce a short comparison
- memoryNote: memory/2026-04-05.md
- links:
  - https://example.com
- notes:
  - Keep this as a style reference or delete it after the first real use.
- evidence:
  - Fetched vendor docs and compared capabilities.
- conclusion:
  - Example only.
```

## Field rules

- `Q0001` style ids are stable; never reuse ids.
- `priority`: `low`, `medium`, `high`, `critical`
- `kind`: short category such as `research`, `debug`, `math`, `algorithm`, `design`, `benchmark`
- `allowedTools`: comma-separated first-class tool names that are acceptable for this question
- `startedAt` is set when investigation begins
- `completedAt` is set only for `done` or `wontfix`
- `completedAt` must not be in the future relative to the current run
- `memoryNote` points to `memory/YYYY-MM-DD.md` when durable findings were written
- `evidence` should summarize the basis of the answer, not dump raw logs
- `conclusion` should be short and final-sounding when status is `done`

## Editing rules

- Move finished items from `Active Questions` to `Completed Questions` in the same update where final status is set.
- Keep blocked items in `Active Questions`.
- Preserve old completed entries unless the user explicitly asks to archive them elsewhere.
- Append evidence/conclusion cleanly instead of duplicating the whole question.
- Do not leave `done` or `wontfix` items in `Active Questions`.
