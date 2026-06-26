# Agent Log Format

## File naming

One file per agent per day:

- `reports/main-ai-log-YYYY-MM-DD.jsonl`
- `reports/cortex-ai-log-YYYY-MM-DD.jsonl`
- `reports/trading-ai-log-YYYY-MM-DD.jsonl`

## One-line schema

```json
{"ts":"2026-04-05T14:10:00+08:00","agent":"main","task":"完成量化交易系统回测模块初版","tokens":12000}
```

## Rules

- Use UTF-8
- One JSON object per line
- `task` must be one line
- `tokens` must be integer total tokens for that work unit
- Append only
- Write immediately after a completed work unit

## Good examples

```json
{"ts":"2026-04-05T14:10:00+08:00","agent":"main","task":"完成量化交易系统回测模块初版","tokens":12000}
{"ts":"2026-04-05T14:28:00+08:00","agent":"cortex","task":"产出一期视频脚本初稿","tokens":9500}
{"ts":"2026-04-05T15:05:00+08:00","agent":"trading","task":"整理两个候选市场的赔率与催化因素","tokens":6400}
```

## Bad examples

Bad: multiline task content

```json
{"ts":"2026-04-05T14:10:00+08:00","agent":"main","task":"先做A\n再做B","tokens":12000}
```

Bad: missing token field

```json
{"ts":"2026-04-05T14:10:00+08:00","agent":"main","task":"完成模块A"}
```

Bad: writing directly into dashboard instead of log

Do not do that.
