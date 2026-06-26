---
name: skillboss
description: "Swiss-knife for AI agents. 50+ models for image generation, video generation, text-to-speech, speech-to-text, music, chat, web search, document parsing, email, and SMS — with smart routing for cost saving."
allowed-tools: Bash, Read
metadata: {"clawdbot":{"requires":{"env":["SKILLBOSS_API_KEY"]},"primaryEnv":"SKILLBOSS_API_KEY"}}
---

# SkillBoss

One API key, 50+ models across providers (Bedrock, OpenAI, Vertex, ElevenLabs, Replicate, Minimax, and more). Call any model directly by ID, or use smart routing to auto-select the cheapest or highest-quality option for a task.

**Base URL:** `https://api.heybossai.com/v1`

## List Models

```bash
curl -s -X POST https://api.heybossai.com/v1/models \
  -H "Content-Type: application/json" \
  -d "{\"api_key\":\"$SKILLBOSS_API_KEY\"}"
```

Filter by type:

```bash
curl -s -X POST https://api.heybossai.com/v1/models \
  -H "Content-Type: application/json" \
  -d "{\"api_key\":\"$SKILLBOSS_API_KEY\",\"types\":\"image\"}"
```

Types: `chat`, `image`, `video`, `tts`, `stt`, `music`, `search`, `tools`

## Smart Mode (auto-select best model)

List available task types:

```bash
curl -s -X POST https://api.heybossai.com/v1/pilot \
  -H "Content-Type: application/json" \
  -d "{\"api_key\":\"$SKILLBOSS_API_KEY\",\"discover\":true}"
```

Run a task (auto-selects best model):

```bash
curl -s -X POST https://api.heybossai.com/v1/pilot \
  -H "Content-Type: application/json" \
  -d "{\"api_key\":\"$SKILLBOSS_API_KEY\",\"type\":\"image\",\"inputs\":{\"prompt\":\"A sunset over mountains\"}}"
```

## Chat

```bash
curl -s -X POST https://api.heybossai.com/v1/run \
  -H "Content-Type: application/json" \
  -d "{\"api_key\":\"$SKILLBOSS_API_KEY\",\"model\":\"bedrock/claude-4-5-sonnet\",\"inputs\":{\"messages\":[{\"role\":\"user\",\"content\":\"Explain quantum computing\"}]}}"
```

| Parameter | Description |
|-----------|-------------|
| `model` | `bedrock/claude-4-5-sonnet`, `bedrock/claude-4-6-opus`, `openai/gpt-5`, `vertex/gemini-2.5-flash`, `deepseek/deepseek-chat` |
| `inputs.messages` | Array of `{role, content}` objects |
| `inputs.system` | Optional system prompt string |
| `inputs.temperature` | Optional, 0.0–1.0 |
| `inputs.max_tokens` | Optional, max output tokens |

Response: `choices[0].message.content` or `content[0].text`

## Image Generation

```bash
curl -s -X POST https://api.heybossai.com/v1/run \
  -H "Content-Type: application/json" \
  -d "{\"api_key\":\"$SKILLBOSS_API_KEY\",\"model\":\"mm/img\",\"inputs\":{\"prompt\":\"A sunset over mountains\"}}"
```

Save to file:

```bash
URL=$(curl -s -X POST https://api.heybossai.com/v1/run \
  -H "Content-Type: application/json" \
  -d "{\"api_key\":\"$SKILLBOSS_API_KEY\",\"model\":\"mm/img\",\"inputs\":{\"prompt\":\"A sunset over mountains\"}}" \
  | grep -o '"image_url":"[^"]*"' | cut -d'"' -f4)
curl -sL "$URL" -o sunset.png
```

| Parameter | Description |
|-----------|-------------|
| `model` | `mm/img`, `replicate/black-forest-labs/flux-2-pro`, `replicate/black-forest-labs/flux-1.1-pro-ultra`, `vertex/gemini-2.5-flash-image-preview`, `vertex/gemini-3-pro-image-preview` |
| `inputs.prompt` | Text description of the image |
| `inputs.size` | Optional, e.g. `"1024*768"` |
| `inputs.aspect_ratio` | Optional, e.g. `"16:9"` |

Response: `image_url`, `data[0]`, or `generated_images[0]`

## Video Generation

```bash
curl -s -X POST https://api.heybossai.com/v1/run \
  -H "Content-Type: application/json" \
  -d "{\"api_key\":\"$SKILLBOSS_API_KEY\",\"model\":\"mm/t2v\",\"inputs\":{\"prompt\":\"A cat playing with yarn\"}}"
```

Image-to-video:

```bash
curl -s -X POST https://api.heybossai.com/v1/run \
  -H "Content-Type: application/json" \
  -d "{\"api_key\":\"$SKILLBOSS_API_KEY\",\"model\":\"mm/i2v\",\"inputs\":{\"prompt\":\"Zoom in slowly\",\"image\":\"https://example.com/photo.jpg\"}}"
```

| Parameter | Description |
|-----------|-------------|
| `model` | `mm/t2v` (text-to-video), `mm/i2v` (image-to-video), `vertex/veo-3-generate-preview` |
| `inputs.prompt` | Text description |
| `inputs.image` | Image URL (for i2v) |
| `inputs.duration` | Optional, seconds |

Response: `video_url`

## Text-to-Speech

```bash
curl -s -X POST https://api.heybossai.com/v1/run \
  -H "Content-Type: application/json" \
  -d "{\"api_key\":\"$SKILLBOSS_API_KEY\",\"model\":\"minimax/speech-01-turbo\",\"inputs\":{\"text\":\"Hello world\",\"input\":\"Hello world\",\"voice\":\"alloy\"}}"
```

| Parameter | Description |
|-----------|-------------|
| `model` | `minimax/speech-01-turbo`, `elevenlabs/eleven_multilingual_v2`, `openai/tts-1` |
| `inputs.text` | Text to speak |
| `inputs.voice` | Voice name (e.g. `alloy`, `nova`, `shimmer`) |
| `inputs.voice_id` | Voice ID (for ElevenLabs) |

Response: `audio_url` or binary audio data

## Speech-to-Text

```bash
curl -s -X POST https://api.heybossai.com/v1/run \
  -H "Content-Type: application/json" \
  -d "{\"api_key\":\"$SKILLBOSS_API_KEY\",\"model\":\"openai/whisper-1\",\"inputs\":{\"audio_data\":\"BASE64_AUDIO\",\"filename\":\"recording.mp3\"}}"
```

| Parameter | Description |
|-----------|-------------|
| `model` | `openai/whisper-1` |
| `inputs.audio_data` | Base64-encoded audio |
| `inputs.filename` | Original filename with extension |

Response: `text`

## Music Generation

```bash
curl -s -X POST https://api.heybossai.com/v1/run \
  -H "Content-Type: application/json" \
  -d "{\"api_key\":\"$SKILLBOSS_API_KEY\",\"model\":\"replicate/elevenlabs/music\",\"inputs\":{\"prompt\":\"upbeat electronic\",\"duration\":30}}"
```

| Parameter | Description |
|-----------|-------------|
| `model` | `replicate/elevenlabs/music`, `replicate/meta/musicgen`, `replicate/google/lyria-2` |
| `inputs.prompt` | Music description |
| `inputs.duration` | Duration in seconds |

Response: `audio_url`

## Background Removal

```bash
curl -s -X POST https://api.heybossai.com/v1/run \
  -H "Content-Type: application/json" \
  -d "{\"api_key\":\"$SKILLBOSS_API_KEY\",\"model\":\"replicate/remove-bg\",\"inputs\":{\"image\":\"https://example.com/photo.jpg\"}}"
```

| Parameter | Description |
|-----------|-------------|
| `model` | `replicate/remove-bg`, `replicate/background-remover` |
| `inputs.image` | Image URL |

Response: `image_url` or `data[0]`

## Document Processing

```bash
curl -s -X POST https://api.heybossai.com/v1/run \
  -H "Content-Type: application/json" \
  -d "{\"api_key\":\"$SKILLBOSS_API_KEY\",\"model\":\"reducto/parse\",\"inputs\":{\"document_url\":\"https://example.com/file.pdf\"}}"
```

| Parameter | Description |
|-----------|-------------|
| `model` | `reducto/parse` (PDF/DOCX to markdown), `reducto/extract` (structured extraction) |
| `inputs.document_url` | URL of the document |
| `inputs.instructions` | For extract: `{"schema": {...}}` JSON schema |

Response: `result` (parsed content)

## Web Search

```bash
curl -s -X POST https://api.heybossai.com/v1/run \
  -H "Content-Type: application/json" \
  -d "{\"api_key\":\"$SKILLBOSS_API_KEY\",\"model\":\"linkup/search\",\"inputs\":{\"query\":\"latest AI news\",\"depth\":\"standard\",\"outputType\":\"searchResults\"}}"
```

| Parameter | Description |
|-----------|-------------|
| `model` | `linkup/search`, `perplexity/sonar`, `firecrawl/scrape` |
| `inputs.query` | Search query |
| `inputs.depth` | `standard` or `deep` |
| `inputs.outputType` | `searchResults`, `sourcedAnswer`, `structured` |

## Email

```bash
curl -s -X POST https://api.heybossai.com/v1/run \
  -H "Content-Type: application/json" \
  -d "{\"api_key\":\"$SKILLBOSS_API_KEY\",\"model\":\"email/send\",\"inputs\":{\"to\":\"user@example.com\",\"subject\":\"Hello\",\"html\":\"<p>Hi there</p>\"}}"
```

## SMS Verification

Send OTP:

```bash
curl -s -X POST https://api.heybossai.com/v1/run \
  -H "Content-Type: application/json" \
  -d "{\"api_key\":\"$SKILLBOSS_API_KEY\",\"model\":\"prelude/verify-send\",\"inputs\":{\"target\":{\"type\":\"phone_number\",\"value\":\"+1234567890\"}}}"
```

Verify OTP:

```bash
curl -s -X POST https://api.heybossai.com/v1/run \
  -H "Content-Type: application/json" \
  -d "{\"api_key\":\"$SKILLBOSS_API_KEY\",\"model\":\"prelude/verify-check\",\"inputs\":{\"target\":{\"type\":\"phone_number\",\"value\":\"+1234567890\"},\"code\":\"123456\"}}"
```

## Available Models (50+)

| Category | Models | Details |
|----------|--------|---------|
| Chat | 25+ models — Claude, GPT, Gemini, DeepSeek, Qwen, HuggingFace | `chat-models.md` |
| Image | 9 models — Gemini, FLUX, upscaling, background removal | `image-models.md` |
| Video | 3 models — Veo, text-to-video, image-to-video | `video-models.md` |
| Audio | 11 models — TTS, STT, music generation | `audio-models.md` |
| Search & Scraping | 19 models — Perplexity, Firecrawl, ScrapingDog, CEO interviews | `search-models.md` |
| Tools | 11 models — documents, email, SMS, embeddings, presentations | `tools-models.md` |

Notes:
- Get SKILLBOSS_API_KEY at https://www.skillboss.co
- Use the models endpoint to discover all available models live
- Use smart mode (pilot) to auto-select the best model for any task
