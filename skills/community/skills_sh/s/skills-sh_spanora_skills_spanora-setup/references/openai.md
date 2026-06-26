# Pattern C: OpenAI SDK

Use `trackOpenAI()` and `trackOpenAIStream()` from `@spanora-ai/sdk/openai`. These auto-extract model, tokens, and output from OpenAI response types.

## Setup

```typescript
import { init, track } from "@spanora-ai/sdk";
import { trackOpenAI, trackOpenAIStream } from "@spanora-ai/sdk/openai";
import OpenAI from "openai";

const { shutdown } = init({
  apiKey: process.env.SPANORA_API_KEY,
});

const client = new OpenAI();
```

## Non-streaming

Wrap `client.chat.completions.create()` with `trackOpenAI()` inside a `track()` boundary:

```typescript
const completion = await track({ agent: "geography-agent" }, () =>
  trackOpenAI({ prompt: prompt }, () =>
    client.chat.completions.create({
      model: "gpt-4o",
      max_tokens: 256,
      messages: [
        { role: "system", content: "You are a helpful assistant." },
        { role: "user", content: prompt },
      ],
    }),
  ),
);
```

## Streaming (wrap pattern)

Use `trackOpenAI()` with an async function that collects the stream and returns `finalChatCompletion()`:

```typescript
const completion = await track({ agent: "science-agent" }, () =>
  trackOpenAI({ prompt: prompt }, async () => {
    const stream = client.chat.completions.stream({
      model: "gpt-4o",
      max_tokens: 256,
      messages: [
        { role: "system", content: "You are a helpful assistant." },
        { role: "user", content: prompt },
      ],
    });

    for await (const chunk of stream) {
      const delta = chunk.choices[0]?.delta?.content;
      if (delta) {
        process.stdout.write(delta);
      }
    }

    return await stream.finalChatCompletion();
  }),
);
```

## Streaming (SSE / manual end)

Use `trackOpenAIStream()` for SSE endpoints where you yield chunks before the final completion is available. It opens the span immediately and returns an `endStream()` closure:

```typescript
async function* streamSSE(prompt: string): AsyncGenerator<string> {
  const endStream = trackOpenAIStream({ prompt: prompt });

  try {
    const stream = client.chat.completions.stream({
      model: "gpt-4o",
      max_tokens: 256,
      messages: [
        { role: "system", content: "You are a helpful assistant." },
        { role: "user", content: prompt },
      ],
    });

    for await (const chunk of stream) {
      const delta = chunk.choices[0]?.delta?.content;
      if (delta) {
        yield `data: ${JSON.stringify({ content: delta })}\n\n`;
      }
    }

    endStream({ completion: await stream.finalChatCompletion() });
  } catch (err) {
    endStream({ error: err instanceof Error ? err : new Error(String(err)) });
    throw err;
  }

  yield "data: [DONE]\n\n";
}
```

**Important:** `endStream()` takes `{ completion }` (not the completion directly). Pass the full `ChatCompletion` object.

## Tool Call Loop

Complete tool-use cycle with `trackToolHandler()` and multiple `trackOpenAI()` calls inside a single `track()` trace:

```typescript
import { track, trackToolHandler } from "@spanora-ai/sdk";
import { trackOpenAI } from "@spanora-ai/sdk/openai";

const getWeather = trackToolHandler(
  "get_weather",
  (input: { city: string }) => ({
    city: input.city,
    temperature: 22,
    unit: "celsius",
    condition: "sunny",
  }),
);

const tools: OpenAI.ChatCompletionTool[] = [
  {
    type: "function",
    function: {
      name: "get_weather",
      description: "Get the current weather for a given city.",
      parameters: {
        type: "object",
        properties: { city: { type: "string", description: "The city name" } },
        required: ["city"],
      },
    },
  },
];

await track({ agent: "weather-agent" }, async () => {
  const messages: OpenAI.ChatCompletionMessageParam[] = [
    { role: "user", content: "What is the weather like in Paris?" },
  ];

  // Step 1: Initial LLM call
  const response = await trackOpenAI(
    { prompt: "What is the weather like in Paris?" },
    () =>
      client.chat.completions.create({
        model: "gpt-4o",
        max_tokens: 1024,
        messages: [
          { role: "system", content: "You are a weather assistant." },
          ...messages,
        ],
        tools,
      }),
  );

  const toolCalls = response.choices[0]?.message.tool_calls;

  if (
    response.choices[0]?.finish_reason === "tool_calls" &&
    toolCalls?.length
  ) {
    const toolMessages: OpenAI.ChatCompletionToolMessageParam[] = [];
    for (const toolCall of toolCalls) {
      if (toolCall.type === "function") {
        const args = JSON.parse(toolCall.function.arguments) as {
          city: string;
        };
        const result = await getWeather(args);
        toolMessages.push({
          role: "tool",
          tool_call_id: toolCall.id,
          content: JSON.stringify(result),
        });
      }
    }

    // Step 2: Send tool results back
    const finalResponse = await trackOpenAI({}, () =>
      client.chat.completions.create({
        model: "gpt-4o",
        max_tokens: 1024,
        messages: [
          { role: "system", content: "You are a weather assistant." },
          ...messages,
          response.choices[0]!.message,
          ...toolMessages,
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

LLM calls default to `operation: "chat"`. Override when calling embeddings or completions APIs:

```typescript
trackOpenAI({ prompt: texts, operation: "embeddings" }, () =>
  client.embeddings.create({ model: "text-embedding-3-small", input: texts }),
);
```

Standard values: `"chat"` (default), `"text_completion"`, `"embeddings"`.
