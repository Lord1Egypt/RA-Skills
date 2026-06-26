---
name: token-optimizer-pro
description: "Agent token usage optimizer. Input usage logs, transcript excerpts, model bills, or runtime traces; output token/cost breakdown, waste patterns, context compaction opportunities, caching suggestions, and before/after optimization actions. Privacy boundary: redact secrets and do not upload sensitive logs unless the user explicitly chooses an external tool."
---

# Token Optimizer Pro

Use this skill when the user wants to understand where token usage and model cost are going, then reduce waste without hurting task quality.

## Inputs

- Token usage exports
- Model billing summaries
- Agent runtime logs
- Conversation transcripts or excerpts
- Prompt templates and tool traces

## Outputs

- Cost and token breakdown by task, model, phase, or tool
- High-waste patterns: repeated context, oversized prompts, unused files, verbose tool output, weak summarization
- Optimization checklist: compaction, caching, retrieval boundaries, shorter outputs, batching, cheaper model routing
- Before/after estimate with caveats

## Safety

- Redact API keys, credentials, private customer data, and personal identifiers.
- Do not upload logs or transcripts to an external service unless the user explicitly chooses that route.
- Treat cost estimates as approximate unless the user provides official billing exports.

## Example Prompts

1. `Analyze this agent run log and tell me where token usage was wasted.`
2. `Given these model bills, identify the top 5 cost drivers and how to reduce them.`
3. `Review this prompt template and make it cheaper without losing task quality.`
4. `Compare before/after token usage for these two runs.`
5. `Design a token budget and compaction strategy for a long-running coding agent.`
