# DeepSeek compatibility protocols

The current official revision is DeepSeek-V4.1-Flash-1017, updated on
2026-10-17. V4.1 Flash first launched on 2026-09-10. Use `deepseek-flash`;
`deepseek-v4-flash` and `deepseek-v4-flash-vision-exp` remain compatibility
names. The official upgrade does not establish the revision of every RunAPI
service option. Third-party versions remain unconfirmed unless separately
verified. See the [current model reference](https://runapi.ai/models/deepseek/v4.1-flash.md).

Load this reference only for an existing Anthropic Messages or Gemini contents client.

For Messages, use base URL `https://runapi.ai`, a RunAPI key, a supported exact
model ID, `max_tokens`, and text messages. `deepseek-v4-flash-vision-exp` is a retired
compatibility alias. Prefer `deepseek-flash` for supported image requests and
check the current model contract before using an `image_url` content part. Verify final content, `stop_reason`, and `usage`;
streaming ends at `message_stop`.

For Gemini contents, set `RUNAPI_MODEL` to a supported exact model ID and use
`https://runapi.ai/v1beta/models/$RUNAPI_MODEL:generateContent`
or `streamGenerateContent` with `x-goog-api-key`. Verify candidates,
`finishReason`, and `usageMetadata`.

Apply one evidence-backed shape correction, at most one safe pre-response
transport retry, and no automatic model or protocol hopping.
