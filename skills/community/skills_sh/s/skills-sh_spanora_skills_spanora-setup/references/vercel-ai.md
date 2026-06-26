# Pattern A: Vercel AI SDK

Spanora captures Vercel AI SDK activity through three instrumentation approaches. Use the highest-fidelity approach available for each call site.

## Choosing an Instrumentation Approach

| Approach                                 | When to use                                                                                                        | What you get                                                      |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------- |
| `experimental_telemetry`                 | `generateText` / `streamText` with telemetry support                                                               | Auto-captured model, tokens, prompts — zero manual work           |
| `trackVercelAI` / `trackVercelAIStream`  | Tool-loop agents, `agent.generate()` / `agent.stream()`, or any call where `experimental_telemetry` is unavailable | Outer agent span with aggregated usage + per-step LLM child spans |
| `trackLlm` / `trackLlmStream` (core SDK) | Custom wrappers or full manual control                                                                             | Full control over span attributes                                 |

**Rule:** Every AI execution must produce at least one trace. If auto-telemetry covers a call, use it. If not, wrap with `trackVercelAI` / `trackVercelAIStream`. Fall back to core SDK functions as a last resort.

## Setup — add `init()` at application startup

```typescript
import { init } from "@spanora-ai/sdk";

const { shutdown } = init({ apiKey: process.env.SPANORA_API_KEY });

// Call `await shutdown()` before process exit in scripts/CLIs.
// See references/common.md for the full init/shutdown pattern.
```

## Model Setup

The Vercel AI SDK uses provider-specific packages. Example with OpenAI:

```typescript
import { openai } from "@ai-sdk/openai";

const model = openai("gpt-4o");
```

Other providers: `@ai-sdk/anthropic`, `@ai-sdk/google`, etc. See the [Vercel AI SDK docs](https://sdk.vercel.ai/providers) for the full list.

---

## Auto-Telemetry (`experimental_telemetry`)

The simplest approach. Enable `experimental_telemetry` on each AI SDK call — Spanora receives spans automatically via OTEL.

### Text Generation

```typescript
import { generateText } from "ai";

const result = await generateText({
  model,
  prompt: "What is the capital of France?",
  experimental_telemetry: {
    isEnabled: true,
    functionId: "geography-query",
    metadata: {
      userId: "user-123",
      environment: "production",
    },
  },
});
```

`functionId` names the telemetry span. `metadata` attaches arbitrary key-value pairs to the span.

### Streaming

```typescript
import { streamText } from "ai";

const result = streamText({
  model,
  prompt: "Write a haiku about observability.",
  experimental_telemetry: {
    isEnabled: true,
    functionId: "haiku-stream",
  },
});

for await (const chunk of result.textStream) {
  process.stdout.write(chunk);
}

const usage = await result.usage;
```

### Multi-Turn Conversation

Use `messages` instead of `prompt` for multi-turn history:

```typescript
import { generateText } from "ai";

const result = await generateText({
  model,
  system: "You are a math tutor. Explain step by step.",
  messages: [
    { role: "user", content: "What is 2+2?" },
    { role: "assistant", content: "The answer is 4." },
    { role: "user", content: "Now multiply that by 3." },
  ],
  experimental_telemetry: {
    isEnabled: true,
    functionId: "multi-turn-chat",
  },
});
```

### Tool Calls with Auto-Telemetry

Use `inputSchema` (not `parameters`) and `stopWhen: stepCountIs(N)` (not `maxSteps`) for AI SDK v6:

```typescript
import { trackToolHandler } from "@spanora-ai/sdk";
import { generateText, tool, stepCountIs } from "ai";
import { z } from "zod";

const getWeather = tool({
  description: "Get the current weather for a given city",
  inputSchema: z.object({
    city: z.string().describe("The city to get weather for"),
  }),
  execute: trackToolHandler("getWeather", async ({ city }) => ({
    city,
    temperature: 22,
    unit: "celsius",
    condition: "sunny",
  })),
});

const result = await generateText({
  model,
  prompt: "What is the weather like in Paris?",
  tools: { getWeather },
  stopWhen: stepCountIs(3),
  experimental_telemetry: {
    isEnabled: true,
    functionId: "weather-tool-call",
  },
});
```

---

## Wrapper Functions (`trackVercelAI` / `trackVercelAIStream`)

Use these when `experimental_telemetry` is unavailable or you need structured agent-level spans. Import from `@spanora-ai/sdk/vercel-ai`.

These wrappers:

- Create an outer **agent span** (operation: `"agent"`) with aggregated `totalUsage`
- Auto-record **per-step LLM child spans** (operation: `"chat"`) with per-step token counts
- Auto-extract **model** from the response (no need to pass `model` in meta)
- Do **not** auto-record tool call spans — wrap tools with `trackToolHandler` (they nest naturally as children)

### `trackVercelAI()` — Non-streaming

Wraps `generateText()` or `agent.generate()`. Pass a `VercelAIMeta` and an async function that returns the result:

```typescript
import { init, track, trackToolHandler } from "@spanora-ai/sdk";
import { trackVercelAI } from "@spanora-ai/sdk/vercel-ai";
import { generateText, tool, stepCountIs } from "ai";
import { z } from "zod";

init({ apiKey: process.env.SPANORA_API_KEY });

const getWeather = tool({
  description: "Get the current weather for a given city",
  inputSchema: z.object({ city: z.string() }),
  execute: trackToolHandler("getWeather", async ({ city }) => ({
    city,
    temperature: 22,
    condition: "sunny",
  })),
});

const result = await track({ agent: "weather-agent" }, () =>
  trackVercelAI({ prompt: "What is the weather in Paris?" }, () =>
    generateText({
      model,
      prompt: "What is the weather in Paris?",
      tools: { getWeather },
      stopWhen: stepCountIs(3),
    }),
  ),
);
```

**Span hierarchy produced:**

```
track("weather-agent")              <- root span
  └─ trackVercelAI (agent)          <- outer agent span (aggregated tokens)
       ├─ recordLlm (chat)          <- step 1: LLM requests tool call
       ├─ trackToolHandler          <- tool execution (from trackToolHandler)
       └─ recordLlm (chat)          <- step 2: LLM produces final text
```

### `trackVercelAIStream()` — Streaming

Opens the span immediately and returns an `endStream()` closure. Pass the `StreamTextResult` when the stream completes — promises are resolved internally:

```typescript
import { track } from "@spanora-ai/sdk";
import { trackVercelAIStream } from "@spanora-ai/sdk/vercel-ai";
import { streamText } from "ai";

const result = await track({ agent: "support-agent" }, async () => {
  const endStream = trackVercelAIStream({
    prompt: "Write a haiku about observability.",
  });

  const stream = streamText({
    model,
    prompt: "Write a haiku about observability.",
  });

  for await (const chunk of stream.textStream) {
    process.stdout.write(chunk);
  }

  endStream({ result: stream });
  return stream;
});
```

**`endStream()` options:**

| Option   | Type               | Description                                                                                             |
| -------- | ------------------ | ------------------------------------------------------------------------------------------------------- |
| `result` | `StreamTextResult` | The stream result object — promises (`text`, `totalUsage`, `steps`, `response`) are resolved internally |
| `error`  | `Error`            | Pass if the stream failed                                                                               |

Call with no arguments or `{}` if the stream was abandoned.

### VercelAIMeta Options

Same as `LlmMeta` except `model` (auto-extracted from the response):

| Option         | Type                                          | Description                                             |
| -------------- | --------------------------------------------- | ------------------------------------------------------- |
| `operation`    | `string`                                      | Operation type (default: `"agent"`). Override if needed |
| `prompt`       | `string \| Record<string, unknown>[]`         | Input prompt or messages array                          |
| `output`       | `string \| object`                            | Output text (auto-extracted, rarely needed)             |
| `inputTokens`  | `number`                                      | Input token count (auto-extracted from `totalUsage`)    |
| `outputTokens` | `number`                                      | Output token count (auto-extracted from `totalUsage`)   |
| `provider`     | `string`                                      | LLM provider name (optional)                            |
| `attributes`   | `Record<string, string \| number \| boolean>` | Custom span attributes                                  |

---

## With `track()` (optional — for named execution boundaries)

Wrap in `track()` when you want a top-level trace with `agent`. Works with both auto-telemetry and wrapper approaches:

```typescript
import { track } from "@spanora-ai/sdk";
import { generateText } from "ai";

const result = await track({ agent: "support-agent" }, () =>
  generateText({
    model,
    prompt: "Hello!",
    experimental_telemetry: { isEnabled: true },
  }),
);
```

### Optional: User & Org Context

Pass `userId`, `orgId`, and `agentSessionId` to `track()` to link traces to end users and organizations in the dashboard. All fields are optional:

```typescript
const result = await track(
  {
    agent: "support-agent",
    userId: "user-123", // optional
    orgId: "org-acme", // optional
    agentSessionId: "sess-789", // optional
  },
  () =>
    generateText({
      model,
      prompt: "Hello!",
      experimental_telemetry: { isEnabled: true },
    }),
);
```

---

## Key Differences from Other Patterns

- **Auto-telemetry** (`experimental_telemetry`) provides zero-effort instrumentation for simple calls
- **`trackVercelAI` / `trackVercelAIStream`** provide structured agent-level spans when auto-telemetry is unavailable (tool-loop agents, custom agent patterns)
- **`track()` is optional** — only needed for named execution boundaries
- **`trackToolHandler`** works with all approaches — tool spans nest as children automatically
- **`experimental_telemetry`** must be set on every AI SDK call that uses auto-telemetry
