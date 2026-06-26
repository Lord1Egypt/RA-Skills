# Model Reference

Detailed model information for sub-agent routing decisions.

## Available Models

### Anthropic

| Model | Alias | Input/MTok | Output/MTok | Context | Best For |
|-------|-------|------------|-------------|---------|----------|
| claude-opus-4-5 | `opus` | $5 | $25 | 200K | Complex reasoning, architecture |
| claude-sonnet-4-5 | `sonnet` | $3 | $15 | 1M | Research, synthesis, long docs |
| claude-haiku-4-5 | `haiku` | $1 | $5 | 200K | Quick tasks, simple transforms |

### OpenAI (via Codex subscription)

| Model | Alias | Pricing | Context | Best For |
|-------|-------|---------|---------|----------|
| gpt-5.2-codex | `codex` | Subscription | 128K | Code generation, implementation |
| gpt-5.2 | `gpt5` | Subscription | 128K | General tasks |

## Thinking Levels

Control reasoning depth with the `thinking` parameter:

| Level | Behavior | Use When |
|-------|----------|----------|
| `off` | No extended thinking | Simple, fast tasks |
| `low` | Light reasoning | Most routine work |
| `medium` | Moderate reasoning | Complex but bounded problems |
| `high` | Deep reasoning | Architecture, complex debugging |

Higher thinking = more tokens = more cost/time. Match to task complexity.

## Model Characteristics

### Codex (gpt-5.2-codex)
- **Strengths:** Code generation, refactoring, test writing, debugging
- **Weaknesses:** May over-engineer simple tasks
- **Tips:** Give clear file paths, existing patterns to follow

### Sonnet (claude-sonnet-4-5)
- **Strengths:** Research synthesis, long document analysis, balanced cost/capability
- **Weaknesses:** Not as strong at code as Codex
- **Tips:** Great for GitHub issues, documentation, data analysis

### Haiku (claude-haiku-4-5)
- **Strengths:** Speed, cost efficiency, simple transformations
- **Weaknesses:** May miss nuance on complex tasks
- **Tips:** Use for formatting, simple lookups, quick validations

### Opus (claude-opus-4-5)
- **Strengths:** Deepest reasoning, complex multi-step problems
- **Weaknesses:** Expensive, slower
- **Tips:** Reserve for truly complex coordination, not routine work

## Cost Awareness

Rough token estimates for common tasks:
- Simple code task: ~2K input, ~1K output
- Research task: ~5K input, ~3K output  
- Complex implementation: ~10K input, ~5K output

**Cost formula:** `(input_tokens × input_rate + output_tokens × output_rate) / 1,000,000`

Example: Sonnet research task
- Input: 5K × $3 = $0.015
- Output: 3K × $15 = $0.045
- Total: ~$0.06 per task

## Rate Limits

Rate limits vary by provider and tier. Common patterns:
- Anthropic: Requests/min and tokens/min limits
- OpenAI Codex: Daily usage caps on subscription tier

When you hit a limit:
1. Check error message for reset timing
2. Switch to fallback model
3. Or wait for reset (usually 30-90 min)
