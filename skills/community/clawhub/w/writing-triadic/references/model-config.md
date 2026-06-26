# Model Configuration Reference — v2.9.1

## Default Models (Recommended)

| Role | Model | Context | Rationale |
|---|---|---|---|
| Creator (main AI) | `deepseek/deepseek-v4-pro` | 1M | Reasoning model for deep intent mining & quality oversight |
| Executor (sub-agent) | `deepseek/deepseek-v4-flash` | 1M | Fast generation, cost-effective for producing multiple drafts |
| Reader (sub-agent) | `deepseek/deepseek-v4-pro` | 1M | Reasoning model needed for critical evaluation & comparison |
| Evolution Analyst (sub-agent) | `deepseek/deepseek-v4-pro` | 1M | Precise judgment on preference vs one-off, conflict resolution |

## Rationale for Executor using Flash (not Pro)

The Executor's job is to follow rules and templates — it doesn't need deep reasoning. What it needs:
- Speed (fast multi-draft generation)
- Cost efficiency (writing often requires multiple iterations)

The Creator, Reader, and Evolution Analyst do the heavy intellectual work. The Executor executes.

## Alternative Configurations

### Maximum Quality (all Pro)
All three roles use `deepseek/deepseek-v4-pro`. Highest quality, highest cost.
Use for critical pieces (thesis chapters, important publications, client deliverables).

### Budget Mode (all Flash)
All three roles use `deepseek/deepseek-v4-flash`. Fastest and cheapest.
Use for quick drafts, internal notes, or when iterating rapidly.

### Local Privacy Mode (Ollama)
For sensitive/private content that should not leave the machine:

| Role | Model |
|---|---|
| Creator | `gemma4:e4b` (8K) or `qwen3.5:9b` (8K) |
| Executor | `qwen3.5:9b` |
| Reader | `qwen3.5:9b` |
| Evolution Analyst | `qwen3.5:9b` |

Note: 8K context limits mean long-form writing may need chunking. Evolution analysis may be less precise with local models.

## For Users of Other AI Providers

Users with access to different AI providers can substitute:
- `deepseek/deepseek-v4-pro` → `openai/gpt-5` or `anthropic/claude-sonnet-4-20250514`
- `deepseek/deepseek-v4-flash` → `openai/gpt-5-mini` or `anthropic/claude-haiku-4-5-20251001`

Select based on model capability, not geography. Any provider with comparable reasoning + generation capabilities works.

## How to Change Models

Edit the `model` parameter in `sessions_spawn` calls within SKILL.md Phase 3, Phase 4, Phase 5.1, and Phase 5.5.
