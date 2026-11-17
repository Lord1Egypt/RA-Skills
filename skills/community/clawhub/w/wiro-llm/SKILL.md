---
name: wiro-llm
description: Call LLMs through the Wiro LLM gateway at llm.wiro.ai with OpenAI- or Anthropic-compatible clients (curl, the OpenAI SDK, the Anthropic SDK, or the Vercel AI SDK with the @wiro-ai/wiro-llm provider) and one Wiro API key, including picking a model, streaming, tool calls, structured output, reasoning settings and reading what each call cost. Use when the user wants chat or LLM calls through Wiro, mentions llm.wiro.ai, a Wiro API key or @wiro-ai/wiro-llm, or asks which Wiro model to use or what a call costs.
---

# Wiro LLM gateway

The gateway serves language models from OpenAI, Anthropic, Google, xAI, DeepSeek, Qwen and others through OpenAI Chat Completions, OpenAI Responses and Anthropic Messages, with one Wiro project key.
Calls are paid from your Wiro wallet, and each reply carries the billed amount.
For images, video and audio from the AI SDK, see the provider section below. For Wiro's task API in other languages or the Wiro MCP server, use the wiro-ai skill.
To point a coding agent (Cursor, Claude Code, VS Code, Cline in Windsurf, OpenClaw or Hermes) at the gateway, follow the "Connect an agent" section of https://wiro.ai/docs/completions-api.

## Endpoints and credentials

- OpenAI-compatible clients use the base URL `https://llm.wiro.ai/v1`: `POST /v1/chat/completions` and `POST /v1/responses`. Anthropic SDKs add `/v1` themselves, so they take the origin `https://llm.wiro.ai`: `POST /v1/messages`.
- `GET /v1/models` and `GET /v1/models/{owner}/{model}` describe the models. `GET /v1/generation?id=...` describes a finished call.
- The credential is the API key for an API Key Only project, or `API_KEY:API_SECRET` (joined with a colon) for a Signature project. Send it as `Authorization: Bearer ...`. Anthropic SDKs send it as `x-api-key`, which Messages also takes. If both headers are sent, they must carry the same credential. The Run API's nonce and signature headers are not used here.
- Keep it in `WIRO_API_KEY`. Never print, log or echo it, and never hard-code or commit it. Call the gateway from server code only, never from browser or mobile app code.
- If `WIRO_API_KEY` is not set, ask the user to create a project at https://wiro.ai/panel/project/new and set the variable themselves. Do not ask them to paste the key into the chat.

## Pick a model

```bash
curl -s "https://llm.wiro.ai/v1/models?search=nano&limit=5" \
  -H "Authorization: Bearer ${WIRO_API_KEY}"
curl -s "https://llm.wiro.ai/v1/models/openai/gpt-5-4-nano" \
  -H "Authorization: Bearer ${WIRO_API_KEY}"
```

- Ids are lowercase `owner/model`, such as `openai/gpt-5-4-nano`, `claude/sonnet-5` or `deepseek/v4-flash`. Send the exact id, not a provider's own model name. The list also takes `order` and `after`/`before` cursors, and people can browse the same models at https://wiro.ai/models?categories=llm-tool-call.
- Before you rely on a feature, read `capabilities.endpoints` (`chat`, `responses`, `anthropic`), `supported_parameters` (optional fields such as `tools`, `response_format`, `reasoning_effort` or `temperature`), `capabilities.function_tools`, `capabilities.structured_output_modes`, `capabilities.strict_json_schema` and `capabilities.input_modalities` (`text`, `image`, `document`).
- Sizes are in `context_length`, `max_input_tokens` and `max_tokens` (the longest answer). When set, `pricing.prompt` and `pricing.completion` are USD per token, as strings, and tiered rates are in `x_wiro.pricing_tiers`.
- A model that is not in the list can still run through Wiro's Run API (see the wiro-ai skill).

## Chat Completions

```bash
curl -s "https://llm.wiro.ai/v1/chat/completions" \
  -H "Authorization: Bearer ${WIRO_API_KEY}" -H "Content-Type: application/json" \
  -d '{"model": "openai/gpt-5-4-nano", "max_completion_tokens": 512,
       "messages": [{"role": "user", "content": "Say hello in five words."}]}'
```

With the OpenAI SDK (`npm i openai`; the Python package takes the same values as `base_url` and `api_key`):

```javascript
import OpenAI from "openai";

const client = new OpenAI({ baseURL: "https://llm.wiro.ai/v1", apiKey: process.env.WIRO_API_KEY });

const completion = await client.chat.completions.create({
  model: "openai/gpt-5-4-nano", max_completion_tokens: 512,
  messages: [{ role: "user", content: "Say hello in five words." }],
});
console.log(completion.choices[0].message.content, completion.usage?.cost);

const stream = await client.chat.completions.create({
  model: "openai/gpt-5-4-nano", max_completion_tokens: 512, stream: true,
  stream_options: { include_usage: true }, // adds a last chunk with the usage and cost
  messages: [{ role: "user", content: "Count from one to five." }],
});
for await (const chunk of stream) {
  process.stdout.write(chunk.choices[0]?.delta?.content ?? "");
  if (chunk.usage) console.log("\ncost:", chunk.usage.cost);
}
```

- The answer is in `choices[0].message.content` (streamed: `choices[0].delta.content`, ending with `data: [DONE]`) and the charge, in USD, in `usage.cost`. `client.models.list()` returns the model list.
- Each call stands alone: send the conversation so far in `messages` (`system`, `developer`, `user`, `assistant`, `tool`) every time.
- `max_completion_tokens` covers reasoning as well as the answer. If a reply ends with `finish_reason: "length"` and empty content, raise it or lower `reasoning_effort`.
- Tools: `tools`, `tool_choice`, `parallel_tool_calls`. Run `message.tool_calls` only when `finish_reason` is `tool_calls`, append that assistant message unchanged plus one `{"role": "tool", "tool_call_id": ..., "content": ...}` message per tool call, then send the next request. Your code runs the tools.
- Structured output, nested: `"response_format": {"type": "json_schema", "json_schema": {"name": "city", "schema": {...}, "strict": true}}`, or `{"type": "json_object"}` for any valid JSON.
- Reasoning: `"reasoning_effort": "low"` on models that list it in `supported_parameters`. Returned reasoning is in `message.reasoning`.

## Responses

```javascript
// with the client from Chat Completions
const response = await client.responses.create({
  model: "openai/gpt-5-4-nano", max_output_tokens: 512, store: false,
  input: "Say hello in five words.",
});
console.log(response.output_text, response.usage?.cost);
```

- Replies are stored unless you pass `store: false`. Continue a stored one with `previous_response_id: response.id`.
- Tools: send each result as a `function_call_output` input item with the call's `call_id`.
- Structured output, flat: `"text": {"format": {"type": "json_schema", "name": "city", "schema": {...}, "strict": true}}`.
- Streaming sends events from `response.created` to `response.completed` (or `response.incomplete`), then `data: [DONE]`.

## Anthropic Messages

```javascript
import Anthropic from "@anthropic-ai/sdk"; // npm i @anthropic-ai/sdk

const anthropic = new Anthropic({
  baseURL: "https://llm.wiro.ai", // the origin: the SDK adds /v1
  apiKey: process.env.WIRO_API_KEY,
  authToken: null, // send only the Wiro key, even if ANTHROPIC_AUTH_TOKEN is set
});

const message = await anthropic.messages.create({
  model: "openai/gpt-5-4-nano", max_tokens: 512,
  messages: [{ role: "user", content: "Say hello in five words." }],
});
console.log(message.content.find((b) => b.type === "text")?.text, message.usage.cost);
```

```bash
curl -s "https://llm.wiro.ai/v1/messages" \
  -H "x-api-key: ${WIRO_API_KEY}" -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  -d '{"model": "openai/gpt-5-4-nano", "max_tokens": 512,
       "messages": [{"role": "user", "content": "Say hello in five words."}]}'
```

- Claude models such as `claude/sonnet-5` work here, and so does every other model whose `capabilities.endpoints` lists `anthropic`.
- `max_tokens` is required. System text goes in the top-level `system` field. Resend the history on every call.
- The cost is in `usage.cost` and `usage.cost_usd`. Streaming (`"stream": true`) sends Anthropic events and ends with `message_stop`; the final `message_delta` carries both cost fields.
- Tools take `name`, `description` and `input_schema`. Run the `tool_use` blocks when `stop_reason` is `tool_use`, then send `tool_result` blocks in the next user message.
- Structured output: `"output_config": {"format": {"type": "json_schema", "schema": {...}}}`, with exactly those two keys. It is always strict, so the model needs `capabilities.strict_json_schema`.
- Reasoning: `"thinking": {"type": "enabled", "budget_tokens": 2048}` (`enabled`, `adaptive` or `disabled`), or `output_config.effort`.

## Vercel AI SDK: @wiro-ai/wiro-llm

`npm install @wiro-ai/wiro-llm ai zod` (Node.js 22 or later). The provider uses Chat Completions, reads `WIRO_API_KEY` when a request is made, reports usage on streamed calls, sends `Output.object` schemas as a `json_schema` `response_format`, and puts each call's cost in `providerMetadata.wiro.cost`.

```javascript
import { wiro } from "@wiro-ai/wiro-llm";
import { generateText, isStepCount, Output, streamText, tool } from "ai";
import { z } from "zod";

const model = wiro("openai/gpt-5-4-nano");

const result = await generateText({ model, prompt: "Say hello in five words." });
console.log(result.text, result.providerMetadata?.wiro?.cost);

const stream = streamText({ model, prompt: "Count from one to five." });
for await (const part of stream.textStream) process.stdout.write(part);
console.log("\ncost:", (await stream.providerMetadata)?.wiro?.cost);

// The SDK runs execute and sends the result back. Each step is a call with its own cost.
const withTools = await generateText({
  model,
  tools: {
    getWeather: tool({
      description: "Get the current weather for a city",
      inputSchema: z.object({ city: z.string() }),
      execute: async ({ city }) => ({ city, temperatureC: 21 }),
    }),
  },
  stopWhen: isStepCount(3),
  prompt: "What is the weather in Istanbul right now?",
});
const total = withTools.steps.reduce((sum, s) => sum + Number(s.providerMetadata?.wiro?.cost ?? 0), 0);
console.log(withTools.text, total);

const { output } = await generateText({
  model,
  output: Output.object({ schema: z.object({ city: z.string(), country: z.string() }) }),
  prompt: "Name the largest city in Turkey.",
});
console.log(output);
```

- `createWiro({ apiKey, baseURL, runBaseURL, poll, headers, fetch })` builds a provider with other settings; `wiro` is `createWiro()` with the defaults.
- `providerOptions: { wiro: { reasoningEffort: "low" } }` sends `reasoning_effort`. Reasoning, when the model returns it, is in `reasoningText`.
- The same provider runs Wiro's media models through the Run API (`https://api.wiro.ai/v1`), with the same key: `wiro.image(id)` with `generateImage` (text to image, and editing through `prompt.images`), `wiro.speech(id)` with `generateSpeech`, `wiro.transcription(id)` with `transcribe` and `wiro.video(id)` with `experimental_generateVideo`. Ids come from https://wiro.ai/models, such as `pruna/p-image`, `google/nano-banana`, `elevenlabs/eleven-v4-turbo`, `openai/whisper-large-v3` or `bytedance/seedance-v1-pro-fast`. The model's own settings go in `providerOptions.wiro`, and each result names its task and cost in `providerMetadata.wiro` (for images, in `images[i]`; for videos, in `videos[i]`). A task that gives no result throws `WiroTaskError` with `reason` and `taskId`.

```javascript
import { wiro } from "@wiro-ai/wiro-llm";
import { generateImage, generateSpeech } from "ai";

const { image, providerMetadata } = await generateImage({
  model: wiro.image("pruna/p-image"),
  prompt: "A red lighthouse at dusk",
  aspectRatio: "16:9",
});
console.log(image.mediaType, providerMetadata.wiro.images[0]); // { taskId, cost, url, mediaType }

const speech = await generateSpeech({ model: wiro.speech("wiro/kokoro-tts"), text: "Hello there.", voice: "nova" });
console.log(speech.providerMetadata.wiro.cost);
```

## Cost and money rules

- `GET /v1/generation?id=...` looks up a finished call by the response `id` (Chat Completions, Responses) or the `request-id` response header (Messages). It returns `status`, `model`, `protocol`, timestamps and token `usage`.

```bash
curl -s "https://llm.wiro.ai/v1/generation?id=RESPONSE_ID" \
  -H "Authorization: Bearer ${WIRO_API_KEY}"
```

- Calls are paid from your Wiro wallet. Before paid work, tell the user the model and the expected cost: tokens times `pricing.prompt` and `pricing.completion`, or the `usage.cost` of one small call.
- Test with a small model such as `openai/gpt-5-4-nano`, short prompts and a capped output. Set `maxRetries: 0` (OpenAI and Anthropic clients, AI SDK calls) so a failed call is not sent again on its own.
- Ask first before large or open-ended jobs (loops, batches, long contexts) and before any paid call the user did not ask for, retries included.
- Never retry a paid call blindly. Read the error first, and when the outcome of a call is unclear, look it up with `/v1/generation` before you send it again.

## Errors and retries

- Chat Completions, Responses, models and generation errors look like `{"error": {"message", "type", "param", "code"}}`: decide on `error.code`. Messages errors look like `{"type": "error", "error": {"type", "message"}}`: decide on `error.type`. Once a stream has started, errors arrive as events: an error `data:` frame then `[DONE]` on Chat Completions, `response.failed` on Responses, `error` on Messages.
- `unsupported_capability`: the model does not declare something the request asked for, such as a structured output mode. It is refused before anything is billed; pick another model or change the request.
- `model_not_found` or `invalid_model`: check the id with `GET /v1/models`. HTTP 403 `permission_denied`: the team's Model Access settings do not allow this model.
- HTTP 429: wait the seconds in `retry-after`, then retry. HTTP 503 and 529 can be retried. Every reply carries `ratelimit-remaining`, `ratelimit-reset` and `request-id` headers.

## Links

- Gateway docs: https://wiro.ai/docs/completions-api
- Wiro LLM gateway: https://wiro.ai/llm
- Gateway models: https://wiro.ai/models?categories=llm-tool-call
- npm package: https://www.npmjs.com/package/@wiro-ai/wiro-llm
- Source and examples: https://github.com/wiroai/Wiro-LLM
- New project and API key: https://wiro.ai/panel/project/new
