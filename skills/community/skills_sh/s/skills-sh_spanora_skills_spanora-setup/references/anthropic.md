# Pattern B: Anthropic SDK

Use `trackAnthropic()` and `trackAnthropicStream()` from `@spanora-ai/sdk/anthropic`. These auto-extract model, tokens, and output from Anthropic response types.

## Setup

```typescript
import { init, track } from "@spanora-ai/sdk";
import {
  trackAnthropic,
  trackAnthropicStream,
} from "@spanora-ai/sdk/anthropic";
import Anthropic from "@anthropic-ai/sdk";

const { shutdown } = init({
  apiKey: process.env.SPANORA_API_KEY,
});

const client = new Anthropic();
```

## Non-streaming

Wrap `client.messages.create()` with `trackAnthropic()` inside a `track()` boundary:

```typescript
const message = await track({ agent: "geography-agent" }, () =>
  trackAnthropic({ prompt: prompt }, () =>
    client.messages.create({
      model: "claude-sonnet-4-20250514",
      max_tokens: 256,
      messages: [{ role: "user", content: prompt }],
    }),
  ),
);
```

## Streaming (wrap pattern)

Use `trackAnthropic()` with an async function that collects the stream and returns `finalMessage()`:

```typescript
const message = await track({ agent: "science-agent" }, () =>
  trackAnthropic({ prompt: prompt }, async () => {
    const stream = client.messages.stream({
      model: "claude-sonnet-4-20250514",
      max_tokens: 256,
      messages: [{ role: "user", content: prompt }],
    });

    for await (const event of stream) {
      if (
        event.type === "content_block_delta" &&
        event.delta.type === "text_delta"
      ) {
        process.stdout.write(event.delta.text);
      }
    }

    return await stream.finalMessage();
  }),
);
```

## Streaming (SSE / manual end)

Use `trackAnthropicStream()` for SSE endpoints where you yield chunks before the final message is available. It opens the span immediately and returns an `endStream()` closure:

```typescript
async function* streamSSE(prompt: string): AsyncGenerator<string> {
  const endStream = trackAnthropicStream({ prompt: prompt });

  try {
    const stream = client.messages.stream({
      model: "claude-sonnet-4-20250514",
      max_tokens: 256,
      messages: [{ role: "user", content: prompt }],
    });

    for await (const event of stream) {
      if (
        event.type === "content_block_delta" &&
        event.delta.type === "text_delta"
      ) {
        yield `data: ${JSON.stringify({ content: event.delta.text })}\n\n`;
      }
    }

    endStream({ message: await stream.finalMessage() });
  } catch (err) {
    endStream({ error: err instanceof Error ? err : new Error(String(err)) });
    throw err;
  }

  yield "data: [DONE]\n\n";
}
```

**Important:** `endStream()` takes `{ message }` (not the message directly). Pass the full `Anthropic.Message` object.

## Tool Call Loop

Complete tool-use cycle with `trackToolHandler()` and multiple `trackAnthropic()` calls inside a single `track()` trace:

```typescript
import { track, trackToolHandler } from "@spanora-ai/sdk";
import { trackAnthropic } from "@spanora-ai/sdk/anthropic";

const getWeather = trackToolHandler(
  "get_weather",
  (input: { city: string }) => ({
    city: input.city,
    temperature: 22,
    unit: "celsius",
    condition: "sunny",
  }),
);

const tools: Anthropic.Messages.Tool[] = [
  {
    name: "get_weather",
    description: "Get the current weather for a given city.",
    input_schema: {
      type: "object" as const,
      properties: { city: { type: "string", description: "The city name" } },
      required: ["city"],
    },
  },
];

await track({ agent: "weather-agent" }, async () => {
  const messages: Anthropic.Messages.MessageParam[] = [
    { role: "user", content: "What is the weather like in Paris?" },
  ];

  // Step 1: Initial LLM call
  const response = await trackAnthropic(
    { prompt: "What is the weather like in Paris?" },
    () =>
      client.messages.create({
        model: "claude-sonnet-4-20250514",
        max_tokens: 1024,
        messages,
        tools,
      }),
  );

  if (response.stop_reason === "tool_use") {
    const toolUseBlocks = response.content.filter(
      (block): block is Anthropic.Messages.ToolUseBlock =>
        block.type === "tool_use",
    );

    const toolResults: Anthropic.Messages.ToolResultBlockParam[] = [];
    for (const block of toolUseBlocks) {
      const result = await getWeather(block.input as { city: string });
      toolResults.push({
        type: "tool_result" as const,
        tool_use_id: block.id,
        content: JSON.stringify(result),
      });
    }

    // Step 2: Send tool results back
    const finalResponse = await trackAnthropic({}, () =>
      client.messages.create({
        model: "claude-sonnet-4-20250514",
        max_tokens: 1024,
        messages: [
          ...messages,
          { role: "assistant", content: response.content },
          { role: "user", content: toolResults },
        ],
        tools,
      }),
    );
  }
});
```

## Optional Enrichments

### User & Org Context

All fields on `track()` besides `agent` are optional. Pass `userId`, `orgId`, and `agentSessionId` when your code has access to user/tenant context — this links traces to end users and organizations in the Spanora dashboard:

```typescript
await track(
  {
    agent: "support-agent",
    userId: "user-123", // optional — end-user identifier
    orgId: "org-acme", // optional — organization / tenant
    agentSessionId: "sess-789", // optional — conversation / session
  },
  async () => {
    /* ... */
  },
);
```

### Operation Type

LLM calls default to `operation: "chat"`. Override when the call type differs:

```typescript
trackAnthropic({ prompt: prompt, operation: "text_completion" }, () =>
  client.completions.create({ model: "claude-sonnet-4-20250514", prompt }),
);
```

Standard values: `"chat"` (default), `"text_completion"`, `"embeddings"`.
