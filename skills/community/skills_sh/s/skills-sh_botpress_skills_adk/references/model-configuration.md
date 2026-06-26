# Model Configuration Reference

Quick reference for configuring AI models at different levels in ADK agents.

---

## 1. Global Defaults (agent.config.ts)

```typescript
import { defineConfig } from '@botpress/runtime'

export default defineConfig({
  name: 'my-agent',

  defaultModels: {
    autonomous: 'openai:gpt-4o', // Used by execute()
    zai: 'openai:gpt-4o-mini', // Used by Zai operations
  },
})
```

### With Fallback Arrays

```typescript
defaultModels: {
  autonomous: [
    "openai:gpt-4o",
    "anthropic:claude-3-5-sonnet",
    "openai:gpt-4o-mini"
  ],
  zai: "openai:gpt-4o-mini"
}
```

---

## 2. Per-Call Override (execute)

```typescript
await execute({
  instructions: 'You are a helpful assistant',
  model: 'anthropic:claude-3-5-sonnet',
  temperature: 0.7,
})
```

### With Fallback Array

```typescript
await execute({
  instructions: 'You are a helpful assistant',
  model: ['openai:gpt-4o', 'anthropic:claude-3-5-sonnet'],
})
```

---

## 3. Zai Model Override

Override the default Zai model per-instance using `.with()`:

```typescript
import { adk } from '@botpress/runtime'

const preciseZai = adk.zai.with({ modelId: 'openai:gpt-4o' })
await preciseZai.extract(text, schema)
```

> For full Zai configuration (initialization, chaining, learning, operations), see [zai-agent-reference.md](./zai-agent-reference.md) and [zai-complete-guide.md](./zai-complete-guide.md).

---

## 4. Available Models

### Model Name Format

Models follow the pattern: `{provider}:{model-name}`

```typescript
'openai:gpt-4o' // Short name
'openai:gpt-4.1-2025-04-14' // Dated version (more specific)
'anthropic:claude-3-5-sonnet' // Short name
'anthropic:claude-sonnet-4-5-20250929' // Dated version
'best' // Zai shortcut (highest quality)
'fast' // Zai shortcut (fastest/cheapest)
```

**Finding Available Models:**

- The Models type accepts any string, so new models work automatically
- For current available models, check the `Models` type in `@botpress/cognitive`
- Use TypeScript autocomplete: Start typing a provider name to see suggestions
- Dated versions (e.g., `gpt-4.1-2025-04-14`) are more explicit about which version you're using

### Common Models

### OpenAI

```
openai:gpt-4o
openai:gpt-4o-mini
openai:gpt-4-turbo
openai:gpt-3.5-turbo
```

### Anthropic

```
anthropic:claude-3-5-sonnet
anthropic:claude-3-opus
anthropic:claude-3-haiku
```

### Google

```
google:gemini-1.5-pro
google:gemini-1.5-flash
```

### Cerebras

```
cerebras:gpt-oss-120b
```

### Zai Shortcuts

```
best    # Highest quality model
fast    # Fastest/cheapest model
```

---

## 5. Precedence Order

**For execute():**

1. `execute({ model: "..." })` - Per-call override
2. `agent.config.ts defaultModels.autonomous` - Global default

**For Zai:**

1. `zai.with({ modelId: "..." })` - Instance override
2. `new Zai({ modelId: "..." })` - Constructor config
3. `agent.config.ts defaultModels.zai` - Global default

---

## 6. Environment-Based Configuration

```typescript
export default defineConfig({
  name: 'my-agent',
  defaultModels: {
    autonomous: process.env.AI_MODEL || 'openai:gpt-4o',
    zai: process.env.ZAI_MODEL || 'openai:gpt-4o-mini',
  },
})
```

---

## Quick Examples

### Conversation with Custom Model

```typescript
export default new Conversation({
  channel: '*',
  handler: async ({ execute }) => {
    await execute({
      instructions: 'You are a helpful assistant',
      model: 'anthropic:claude-3-5-sonnet',
    })
  },
})
```

### Workflow with Model Override

```typescript
export default Workflow({
  name: 'research',
  handler: async ({ step, execute }) => {
    const result = await step('analyze', async () => {
      return await execute({
        instructions: 'Analyze this data',
        model: 'openai:gpt-4o',
      })
    })
    return result
  },
})
```

### Zai Operation with Specific Model

```typescript
import { adk } from '@botpress/runtime'

const analysis = await adk.zai.with({ modelId: 'anthropic:claude-3-5-sonnet' }).extract(document, schema)
```
