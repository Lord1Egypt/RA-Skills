# Usage Tracker Skill

Track AI model usage and generate cost reports across all providers.

## Overview

This skill tracks AI API calls and generates cost reports. It supports:
- Multiple providers: MiniMax, Anthropic, OpenAI, Google, xAI, Voyage, Mistral
- Cost calculation based on current pricing
- Daily, weekly, and monthly reports
- Filtering by model and task type

## Tools

### log_usage

Log an AI API call for tracking.

**Parameters:**
- `provider` (required): Provider name (minimax-portal, anthropic, openai, google, xai, voyage, mistral)
- `model` (required): Model identifier (e.g., MiniMax-M2.5, gpt-4o, claude-3-opus)
- `input_tokens` (required): Number of input tokens
- `output_tokens` (required): Number of output tokens  
- `task_type` (optional): Type of task (coding, reasoning, general, writing, analysis, chat)

### usage_report

Generate a usage and cost report.

**Parameters:**
- `period` (required): Time period (daily, weekly, monthly)
- `model_filter` (optional): Filter by model name
- `task_filter` (optional): Filter by task type

### realtime_report

Get real-time usage report for the last 24 hours. No parameters required.

## Usage Examples

```
Log a usage call:
log_usage(provider="minimax-portal", model="MiniMax-M2.5", input_tokens=1500, output_tokens=800, task_type="general")

Get daily report:
usage_report(period="daily")

Get weekly report:
usage_report(period="weekly", model_filter="gpt")

Get real-time report:
realtime_report()
```

## Pricing (USD per 1M tokens)

| Provider | Model | Input | Output |
|----------|-------|-------|--------|
| MiniMax Portal | M2.5 | Free | Free |
| Anthropic | Claude Opus 4 | $15 | $75 |
| Anthropic | Claude Sonnet 4 | $3 | $15 |
| Anthropic | Claude Haiku 4 | $0.80 | $4 |
| OpenAI | GPT-4.5 | $75 | $300 |
| OpenAI | GPT-4o | $2.50 | $10 |
| OpenAI | GPT-4o Mini | $0.15 | $0.60 |
| Google | Gemini 2.5 Pro | $1.25 | $10 |
| Google | Gemini 1.5 Flash | $0.075 | $0.30 |
| xAI | Grok 2 | $2 | $10 |

## Telegram Commands

- `/usage` - Get real-time usage report (last 24 hours)
- `/cost` - Get real-time usage report (last 24 hours)

## Storage

Logs are stored in: `usage-logs/api-cells.jsonl`
Reports can be generated on-demand using the tools above.
