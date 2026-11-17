# Claude compatibility protocols

Load this reference only for an existing OpenAI or Gemini client. New Claude integrations use Anthropic Messages from the main skill.

`claude-sonnet-5-5` and `claude-haiku-5-5` are served through Anthropic Messages
only; they are not supported model IDs for the OpenAI or Gemini protocols below.

For OpenAI clients, set the base URL to `https://runapi.ai/v1`, use a RunAPI
key, and call Chat Completions or Responses with a supported exact Claude model
ID. Verify `finish_reason` plus `usage` for Chat, or `response.completed` plus
`usage` for Responses. SSE ends at `[DONE]`.

For Gemini contents, set `RUNAPI_MODEL` to a supported exact model ID and use
`https://runapi.ai/v1beta/models/$RUNAPI_MODEL:generateContent`
or `streamGenerateContent` with `x-goog-api-key`. Verify candidates,
`finishReason`, and `usageMetadata`.

Apply one evidence-backed shape correction, at most one safe pre-response
transport retry, and no automatic model or protocol hopping.
