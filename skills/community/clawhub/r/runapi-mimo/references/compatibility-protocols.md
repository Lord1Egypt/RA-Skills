# MiMo compatibility protocols

Load this reference only when an existing client already requires OpenAI
Responses or Anthropic Messages. New MiMo integrations use Chat Completions
from the main skill.

## OpenAI Responses

Authenticate with `OPENAI_API_KEY`, set the base URL to
`https://runapi.ai/v1`, and call `client.responses.create` with a supported
exact model ID and text `input`. Verify `output_text`, terminal `usage`, and a
completed response. Streaming must include `response.completed` and `[DONE]`.

## Anthropic Messages

Set the Anthropic client base URL to `https://runapi.ai`, use the RunAPI key as
`api_key`, and call `client.messages.create` with a supported exact model ID,
`max_tokens`, and text messages. Verify final text, `stop_reason`, and `usage`;
a stream is complete only after `message_stop`.

Apply the same stop boundary as the primary recipe: one evidence-backed shape
correction, at most one safe pre-response transport retry, and no automatic
model or protocol change after a terminal failure.

## Claude Code with mimo-v2.5

Set `ANTHROPIC_BASE_URL=https://runapi.ai` and `ANTHROPIC_API_KEY` to your
RunAPI key for the command, then run `claude --model mimo-v2.5`. Remove any
conflicting `ANTHROPIC_AUTH_TOKEN` from that command's environment.

The base model supports custom `tools` with `input_schema`, `tool_use` and
`tool_result` messages, string-valued `metadata`, text `cache_control`, and
`thinking` (including Claude Code's adaptive mode). Preserve tool IDs and the
returned thinking blocks in subsequent turns. Consume streaming responses
through `message_stop`, including the terminal usage and stop reason.

Claude Code's `output_config.effort` and
`context_management.edits: [{type: "clear_thinking_20251015", keep: "all"}]`
are accepted. Hosted tools, structured output formats, and other context edits
are not enabled. These capabilities apply to `mimo-v2.5`; Pro and Responses
retain their basic text scope.
