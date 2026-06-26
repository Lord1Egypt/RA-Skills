# Qwen Tool-Calling and Structured Output

## Default Stance

Assume tool-calling is fragile until proven stable on the exact combination of:
- model family
- backend server
- chat template
- parser mode
- client SDK

## Safe Pattern

1. Start with one tool and one tiny payload.
2. Validate the raw response before executing anything.
3. Add multiple tools only after single-tool behavior is stable.
4. Add a fallback mode that asks Qwen for strict JSON only if native tool-calling drifts.

## Strict Execution Guardrails

- Use low temperature for automation paths.
- Require exact fields and reject missing or extra keys.
- If parsing fails, stop execution and show the invalid payload.
- Keep a degraded path that returns a human-review task instead of forcing a bad tool call through.

## Backend Notes

### Hosted OpenAI-Compatible Qwen

- Good starting point when the team wants fewer moving pieces.
- Still verify live models and exact tool behavior before assuming parity with another OpenAI-compatible provider.

### vLLM

- Good for team serving and OpenAI-compatible access.
- Keep one backend-specific tool-calling test because parser behavior can differ from hosted routes.
- If using Qwen-Agent, align the parser expectations with the framework instead of layering conflicting parser logic.

### Qwen-Agent

- Qwen-Agent supports function calling and parallel tool calls.
- For QwQ and Qwen3, the official guidance says Qwen-Agent can parse tool outputs from vLLM itself, so avoid adding redundant auto-tool-choice or Hermes parsing just because another stack needed it.
- For Qwen3-Coder, validate whether you want backend-native parsing or raw API handling before scaling up the tool graph.

## Two-Stage Automation

Use this if native tool-calling is unstable:

1. Ask Qwen to produce strict JSON arguments only.
2. Validate with `jq`, schema checks, or application code.
3. Execute the tool outside the model.

This loses some elegance but increases production safety.

## Repro Payload

Keep one tiny regression test like:

```json
{
  "goal": "call exactly one tool with a city argument",
  "tools": ["get_weather"],
  "expected_shape": {"name":"get_weather","arguments":{"city":"Madrid"}}
}
```

If this fails, stop changing business prompts and fix the route first.
