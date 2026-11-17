# Grok compatibility protocols

Load this reference only for an existing Anthropic Messages or Gemini contents client.

For Messages, use base URL `https://runapi.ai`, a RunAPI key, a supported exact
model ID, `max_tokens`, and messages. Verify final content, `stop_reason`, and
`usage`; streaming ends at `message_stop`.

For Gemini contents, set `RUNAPI_MODEL` to a supported exact model ID and use
`https://runapi.ai/v1beta/models/$RUNAPI_MODEL:generateContent`
or `streamGenerateContent` with `x-goog-api-key`. Verify candidates,
`finishReason`, and `usageMetadata`.

Apply one evidence-backed shape correction, at most one safe pre-response
transport retry, and no automatic model or protocol hopping.
