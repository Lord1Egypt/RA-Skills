# Gemini compatibility protocol

Load this reference only when an existing application already requires an
OpenAI-compatible Chat Completions client. New Gemini integrations use Gemini
contents from the main skill.

Set `OPENAI_API_KEY` to a RunAPI key and the OpenAI client base URL to
`https://runapi.ai/v1`. Call `client.chat.completions.create` with a supported
exact Gemini model ID and messages. For streaming, set `stream=True` and request
terminal Usage with `stream_options.include_usage`.

Verify final assistant content, `finish_reason`, terminal `usage`, and `[DONE]`
for SSE. Apply one evidence-backed shape correction, at most one safe
pre-response transport retry, and no automatic model or protocol hopping.
