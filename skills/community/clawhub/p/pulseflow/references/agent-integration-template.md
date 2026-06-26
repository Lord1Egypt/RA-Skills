# Agent Integration Template

Add this rule into each execution agent's AGENTS.md.

## Completed work must append AI work log

After each completed work unit, append one JSON line to today's per-agent log file:

Path:
- `.../reports/<agent>-ai-log-YYYY-MM-DD.jsonl`

Format:
```json
{"ts":"ISO8601","agent":"<agent>","task":"一句话描述本次完成的工作","tokens":12345}
```

Rules:
- append-only
- one line per completed work unit
- `task` must be one line
- `tokens` is optional; if written, use an integer total or `0`
- do not write to `todo/NOW.md` directly

Example:
```json
{"ts":"2026-04-05T16:00:00+08:00","agent":"main","task":"完成回测模块初版","tokens":12000}
```
