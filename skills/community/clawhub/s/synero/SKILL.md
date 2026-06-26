---
name: synero
description: Ask Synero’s AI Council questions from the terminal and get one synthesized answer from four contrasting AI advisors. Use when a user wants a higher-confidence take on strategy, research, architecture, hiring, positioning, or other judgment-heavy questions where multiple perspectives beat a single-model reply.
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["python3"] },
        "env": ["SYNERO_API_KEY"],
        "optionalEnv":
          [
            "SYNERO_API_URL",
            "SYNERO_TIMEOUT",
            "SYNERO_MODEL_ARCHITECT",
            "SYNERO_MODEL_PHILOSOPHER",
            "SYNERO_MODEL_EXPLORER",
            "SYNERO_MODEL_MAVERICK",
            "SYNERO_MODEL_SYNTHESIZER"
          ]
      }
  }
---

# Synero Skill

Use this skill to query Synero from the terminal when one AI answer is not enough. Synero is positioned as a collective AI intelligence product: one prompt goes to four advisors with different reasoning styles, then Synero synthesizes them into a single response.

This is most useful for ambiguous or high-leverage questions where you want disagreement, tradeoffs, blind-spot checking, and a clearer final recommendation.

## What this skill helps with

Use it for prompts like:
- product or roadmap decisions with meaningful tradeoffs
- technical architecture reviews and go/no-go questions
- research questions where cross-checking perspectives improves trust
- hiring, org, or leadership choices with second-order effects
- messaging, positioning, or content strategy that benefits from competing angles

Prefer simpler tools for basic factual lookups or one-shot chores. This skill shines when the question is judgment-heavy.

## What it does

- Sends a prompt to Synero’s council endpoint
- Supports 4 advisor roles: `architect`, `philosopher`, `explorer`, `maverick`
- Returns either:
  - a synthesized final answer for normal use, or
  - raw SSE stream output for debugging and live visibility
- Supports optional thread continuity and per-slot model overrides

## Prerequisites

Get your API key from `https://synero.ai`, then export it before running the script:

```bash
export SYNERO_API_KEY="sk_live_..."
```

If you are not sure where to get the key, sign in at `https://synero.ai` and use the API/settings area there.

Optional environment variables:

```bash
export SYNERO_API_URL="https://synero.ai/api/query"
export SYNERO_TIMEOUT="120"
export SYNERO_MODEL_ARCHITECT="gpt-5.2"
export SYNERO_MODEL_PHILOSOPHER="claude-opus-4-6"
export SYNERO_MODEL_EXPLORER="gemini-3.1-pro-preview"
export SYNERO_MODEL_MAVERICK="grok-4"
export SYNERO_MODEL_SYNTHESIZER="gpt-4.1"
```

## Quick command

```bash
python3 ~/.openclaw/skills/synero/scripts/synero-council.py "Should we ship this feature in the next 30 days?"
```

That command uses `SYNERO_API_KEY` from your environment and sends the request to Synero at `https://synero.ai/api/query` unless you override `SYNERO_API_URL`.

## Quiet final-output mode

Use `--quiet` when you want only the synthesized answer with no extra status lines:

```bash
python3 ~/.openclaw/skills/synero/scripts/synero-council.py --quiet "Evaluate this architecture plan and recommend a prototype path."
```

## Streaming and debugging mode

Use `--raw` when you want the raw event stream for troubleshooting or to inspect council behavior live:

```bash
python3 ~/.openclaw/skills/synero/scripts/synero-council.py --raw "What are the strongest arguments for and against this pricing change?"
```

## Advanced configuration

Use model overrides when you want to pin specific advisors or a specific synthesizer:

```bash
python3 ~/.openclaw/skills/synero/scripts/synero-council.py \
  --thread-id "your-thread-id" \
  --advisor-model architect=gpt-5.2 \
  --advisor-model philosopher=claude-opus-4-6 \
  --advisor-model explorer=gemini-3.1-pro-preview \
  --advisor-model maverick=grok-4 \
  --synthesizer-model gpt-4.1 \
  "Your question"
```

## Output behavior

Default mode prints:
- HTTP status line
- final synthesized answer

`--quiet` prints:
- final synthesized answer only

`--raw` prints:
- raw SSE events from the API

## Prompting guidance

Write prompts that invite useful disagreement, not generic brainstorming.

- Ask for tradeoffs, risks, assumptions, and a recommendation
- Include operating constraints such as timeline, budget, team size, and risk tolerance
- Use `--thread-id` when continuing the same topic across multiple rounds
- Use `--quiet` when another tool or script needs clean final text only
- Use `--raw` when debugging streaming behavior or inspecting advisor outputs

For reusable prompt templates, read:
- `references/prompt-patterns.md`

## Error handling

- Missing key → exits with clear guidance to set `SYNERO_API_KEY`
- HTTP failure → prints status and response body
- Network failure → prints a clear network error
- Empty synthesis → exits non-zero instead of pretending things are fine
