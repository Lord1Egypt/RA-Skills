# Image Generation API Reference

## DashScope Wanx (Default)

Alibaba Cloud's text-to-image service. Uses async submit + poll pattern.

### Submit Request

```
POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis
Headers:
  Authorization: Bearer {DASHSCOPE_API_KEY}
  Content-Type: application/json
  X-DashScope-Async: enable
Body:
{
  "model": "wanx2.1-t2i-turbo",
  "input": {
    "prompt": "soft abstract watercolor texture...",
    "negative_prompt": "text, letters, words, ..."
  },
  "parameters": {
    "size": "768*1024",
    "n": 1
  }
}
```

### Poll Response

```
GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}
Headers:
  Authorization: Bearer {DASHSCOPE_API_KEY}
```

Response (on success):
```json
{
  "output": {
    "task_status": "SUCCEEDED",
    "results": [{"url": "https://..."}]
  }
}
```

Poll every 2 seconds, max 40 attempts (~80s timeout). Status values: `PENDING`, `RUNNING`, `SUCCEEDED`, `FAILED`, `UNKNOWN`.

### Configuration

| Env Var | Default | Description |
|---------|---------|-------------|
| `DASHSCOPE_API_KEY` | — | API key from https://dashscope.console.aliyun.com/ |
| `WANX_MODEL_BG` | `wanx2.1-t2i-turbo` | Model ID for background generation |

## Gemini Native API (Alternative)

Google's Gemini model with native image generation. Uses synchronous request (no polling).

### Request

```
POST https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent
Headers:
  Content-Type: application/json
  x-goog-api-key: {LLM_API_KEY}
Body:
{
  "contents": {
    "parts": [{"text": "soft abstract watercolor texture..."}]
  },
  "generationConfig": {
    "responseModalities": ["TEXT", "IMAGE"],
    "outputMimeType": "image/png"
  }
}
```

### Response

```json
{
  "candidates": [{
    "content": {
      "parts": [
        {"text": "..."},
        {
          "inlineData": {
            "mimeType": "image/png",
            "data": "<base64-encoded-png>"
          }
        }
      ]
    }
  }]
}
```

The base64 image data is converted to a `data:image/png;base64,...` URI for direct use in HTML/CSS.

### Configuration

| Env Var | Default | Description |
|---------|---------|-------------|
| `LLM_API_KEY` | — | Gemini API key (auto-detected if `LLM_BASE_URL` contains `googleapis.com`) |
| `GEMINI_IMAGE_MODEL` | `gemini-2.5-flash-preview-image-generation` | Gemini model with image generation capability |

## Provider Auto-Selection

The skill automatically selects the image provider:

1. If `LLM_API_KEY` is set AND `LLM_BASE_URL` contains `googleapis.com` → try **Gemini** first
2. If Gemini fails or is unavailable, and `DASHSCOPE_API_KEY` is set → fall back to **DashScope wanx**
3. If neither is available → skip background generation, render plain card

## Prompt Enhancement

Both providers receive an enhanced prompt that enforces subtlety:

```
{llm_generated_prompt},
extremely soft and subtle, very low contrast, whisper-light illustration,
background color {theme_bg_hex}, monochromatic tones matching {theme_bg_hex},
ultra minimalist, no text, no letters, no words, no human faces
```

DashScope wanx additionally uses a negative prompt to exclude unwanted elements.
