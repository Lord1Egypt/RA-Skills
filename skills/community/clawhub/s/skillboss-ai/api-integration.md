# API Integration

Embed SkillBoss API directly in user code (TypeScript/JavaScript).

## API Format

- **Base URL:** `https://api.heybossai.com/v1`
- **Auth:** Include `api_key` in the JSON request body
- **Endpoint:** POST `/pilot` for smart model selection, POST `/run` for direct model calls

## Quick Example

```typescript
const API_KEY = "<your-api-key>";
const API_BASE = "https://api.heybossai.com/v1";

// Smart model selection (recommended)
const resp = await fetch(`${API_BASE}/pilot`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    api_key: API_KEY,
    type: "image",
    inputs: { prompt: "A sunset over mountains" },
  }),
});
const data = await resp.json();
// data.result.image_url → "https://..."
```

## Endpoints

### POST /pilot — Smart Model Navigator

```typescript
// Discover available types
await post("/pilot", { api_key, discover: true });

// Get recommendations
await post("/pilot", { api_key, type: "image", prefer: "price", limit: 3 });

// Execute (auto-selects best model)
await post("/pilot", { api_key, type: "chat", inputs: { messages: [{ role: "user", content: "Hello" }] } });
await post("/pilot", { api_key, type: "image", inputs: { prompt: "A cat" } });
await post("/pilot", { api_key, type: "tts", inputs: { text: "Hello", voice: "alloy" } });
await post("/pilot", { api_key, type: "video", inputs: { prompt: "Ocean waves", duration: 5 } });
```

### POST /run — Direct Model Call

```typescript
await post("/run", {
  api_key,
  model: "bedrock/claude-4-5-sonnet",
  inputs: { messages: [{ role: "user", content: "Hello" }] },
});
```

## Response Formats

| Type | Result Location |
|------|----------------|
| Chat | `result.choices[0].message.content` or `result.content[0].text` |
| Image | `result.image_url` |
| Video | `result.video_url` |
| TTS | `result.audio_url` or `result.audio_base64` |
| STT | `result.text` |
| Music | `result.audio_url` |
