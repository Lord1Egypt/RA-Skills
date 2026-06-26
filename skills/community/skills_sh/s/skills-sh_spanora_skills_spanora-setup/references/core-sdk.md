# Pattern D: Raw Core SDK

Use the generic `trackLlm()`, `trackLlmStream()`, `recordLlm()`, and `recordTool()` functions. Works with any LLM provider — you supply an `extractResult` callback to map provider-specific responses to Spanora's format.

## Setup

```typescript
import {
  init,
  track,
  trackLlm,
  trackLlmStream,
  recordLlm,
  recordTool,
  trackToolHandler,
  runTool,
} from "@spanora-ai/sdk";

const { shutdown } = init({
  apiKey: process.env.SPANORA_API_KEY,
});
```

## Non-streaming with `extractResult`

`trackLlm()` wraps an LLM call and uses the `extractResult` callback to pull metrics from the response:

```typescript
const response = await track({ agent: "geography-agent" }, () =>
  trackLlm(
    {
      provider: "my-provider",
      model: "my-model",
      prompt: prompt,
    },
    () => myLlmClient.chat(prompt),
    (result) => ({
      output: result.text,
      inputTokens: result.inputTokens,
      outputTokens: result.outputTokens,
    }),
  ),
);
```

### Operation Type

LLM calls default to `operation: "chat"`. Override when calling embeddings or completions APIs:

```typescript
const embeddings = await trackLlm(
  {
    provider: "openai",
    model: "text-embedding-3-small",
    operation: "embeddings",
    prompt: texts,
  },
  () => myEmbeddingClient.embed(texts),
  (result) => ({ inputTokens: result.tokens }),
);
```

Standard values: `"chat"` (default), `"text_completion"`, `"embeddings"`.

## Streaming (manual end)

`trackLlmStream()` opens the span immediately and returns an `endStream()` closure. Call it after the stream completes:

```typescript
await track({ agent: "science-agent" }, async () => {
  const endStream = trackLlmStream({
    provider: "my-provider",
    model: "my-model",
    prompt: prompt,
  });

  let fullText = "";
  const stream = myLlmClient.stream(prompt);
  for await (const chunk of stream.chunks) {
    fullText += chunk;
  }

  const result = await stream.finalResult();

  endStream({
    output: fullText,
    inputTokens: result.inputTokens,
    outputTokens: result.outputTokens,
  });
});
```

## Streaming (SSE / async generator)

Same `trackLlmStream()` pattern inside an async generator for SSE endpoints:

```typescript
async function* streamSSE(prompt: string): AsyncGenerator<string> {
  const endStream = trackLlmStream({
    provider: "my-provider",
    model: "my-model",
    prompt: prompt,
  });

  try {
    const stream = myLlmClient.stream(prompt);

    let fullText = "";
    for await (const chunk of stream.chunks) {
      fullText += chunk;
      yield `data: ${JSON.stringify({ content: chunk })}\n\n`;
    }

    const result = await stream.finalResult();

    endStream({
      output: fullText,
      inputTokens: result.inputTokens,
      outputTokens: result.outputTokens,
    });
  } catch (err) {
    endStream({ error: err instanceof Error ? err : new Error(String(err)) });
    throw err;
  }

  yield "data: [DONE]\n\n";
}
```

## Fire-and-Forget: `recordLlm()`

If you already have all the data from a completed LLM call and just want to record it (no wrapping):

```typescript
import { recordLlm } from "@spanora-ai/sdk";

recordLlm({
  provider: "anthropic",
  model: "claude-sonnet-4-20250514",
  prompt: "Hello",
  output: "Hi there!",
  inputTokens: 5,
  outputTokens: 10,
  durationMs: 450,
});
```

## Fire-and-Forget: `recordTool()`

Same pattern for tool calls — records a completed tool execution as a single span:

```typescript
import { recordTool } from "@spanora-ai/sdk";

recordTool({
  name: "get_weather",
  input: { city: "Paris" },
  status: "success",
  durationMs: 120,
});
```

`recordTool()` accepts: `name`, `input`, `status` (`"success"` | `"error"`), `durationMs`, and `attributes`.

## Tool Call Loop

Complete two-step tool loop using `trackToolHandler()` + `trackLlm()` inside `track()`:

```typescript
const getWeather = trackToolHandler(
  "get_weather",
  async (input: { city: string }) => {
    return await weatherApi.lookup(input.city);
  },
);

await track({ agent: "weather-agent" }, async () => {
  // Step 1: LLM call that requests a tool
  const step1 = await trackLlm(
    { provider: "my-provider", model: "my-model", prompt: userPrompt },
    () => myLlmClient.chat(userPrompt),
    (result) => ({
      output: result.text,
      inputTokens: result.inputTokens,
      outputTokens: result.outputTokens,
    }),
  );

  // Execute the tool
  const toolResult = await getWeather({ city: "Paris" });

  // Step 2: Send tool result back to LLM
  const followUp = `Tool result: ${JSON.stringify(toolResult)}. Summarize.`;
  const step2 = await trackLlm(
    { provider: "my-provider", model: "my-model", prompt: followUp },
    () => myLlmClient.chat(followUp),
    (result) => ({
      output: result.text,
      inputTokens: result.inputTokens,
      outputTokens: result.outputTokens,
    }),
  );
});
```

## Error-Safe Tool Execution: `runTool()`

`runTool()` wraps tool execution in a try/catch, returning `{ output, error }` instead of throwing. Useful for manual tool loops where you need to handle failures gracefully:

```typescript
import { runTool } from "@spanora-ai/sdk";

const success = await runTool(
  "calculator",
  { expression: "2 + 2" },
  async (input: { expression: string }) => {
    return evaluate(input.expression);
  },
);

if (success.error) {
  console.log("Tool failed:", success.error);
} else {
  console.log("Result:", success.output);
}
```

## Multi-Agent Shared Context

Pass `userId`, `orgId`, and `agentSessionId` to `track()` to link traces from multiple agents in the same session:

```typescript
const sharedContext = {
  userId: "user-42",
  orgId: "org-acme",
  agentSessionId: "session-abc-123",
};

// Agent 1: Planner
const plan = await track(
  { agent: "planner-agent", ...sharedContext },
  async () => {
    return await trackLlm(
      { provider: "my-provider", model: "my-model", prompt: prompt },
      () => myLlmClient.chat(prompt),
      (result) => ({
        output: result.text,
        inputTokens: result.inputTokens,
        outputTokens: result.outputTokens,
      }),
    );
  },
);

// Agent 2: Executor
await track({ agent: "executor-agent", ...sharedContext }, async () => {
  // ... executor logic with tool calls and LLM calls ...
});
```

The shared context links all traces together in the Spanora dashboard, letting you see the full session across agent boundaries.
