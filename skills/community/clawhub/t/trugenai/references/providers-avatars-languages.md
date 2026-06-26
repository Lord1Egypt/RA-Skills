# Providers, Avatars & Multilingual Reference

## Avatars

### Stock Avatars (Managed Agent Embed)

Available for the iFrame/widget embed flow: Aman, Chloe, Jack, Matt, Priya, Sameer.

To get the full current list of avatar IDs for API use:
```bash
curl --request GET \
  --url https://api.trugen.ai/v1/ext/avatars \
  --header 'x-api-key: <api-key>'
```

## Providers

The Providers API discovers available LLM, STT, and TTS options:

```bash
curl --request GET \
  --url https://api.trugen.ai/v1/ext/providers \
  --header 'x-api-key: <api-key>'
```

**Provider types:**
- `llm` — Language model providers (OpenAI, Groq, etc.)
- `stt` — Speech-to-text providers (Deepgram)
- `tts` — Text-to-speech providers (ElevenLabs)

**Use cases:**
- Build provider selection UI in your dashboard
- Validate region/capability availability
- Dynamically switch LLM or voice per user preference

## Multilingual Support

Trugen supports multiple languages via Deepgram STT and ElevenLabs TTS.

**Supported language codes** (pass as `stt.language`):

| Language | Code |
|----------|------|
| English | `en` |
| Spanish | `es` |
| French | `fr` |
| German | `de` |
| Hindi | `hi` |
| Portuguese | `pt` |
| Chinese | `zh` |
| Japanese | `ja` |
| Korean | `ko` |

Set `"language": "multi"` for automatic multilingual detection.

**Example (multilingual agent):**
```json
"stt": {
  "provider": "deepgram",
  "model": "nova-3",
  "language": "multi"
}
```

**Additional Resources:**
- Deepgram STT models: https://developers.deepgram.com/docs/models-languages-overview#nova-3
- ElevenLabs TTS languages: https://elevenlabs.io/docs/overview/capabilities/text-to-speech#supported-languages

## Bring Your Own LLM (BYO-LLM)

Connect any OpenAI-compatible LLM to power Trugen agents.

**Compatible external LLMs:**
- Self-hosted models (vLLM, Ollama, TGI)
- Fine-tuned private models
- Third-party providers via OpenAI-compatible proxy (Together AI, Fireworks, Groq, Anthropic)

**Requirements:**
- Endpoint: `POST /chat/completions`
- Payload: Must accept a `messages: []` array
- Streaming: Must support Server-Sent Events (SSE)
- Optional: Function calling (for tool use), Vision (for multimodal)

**Setup via API** — set `provider` to `"custom"` in `avatars[].config.llm`:
```json
"llm": {
  "provider": "custom",
  "model": "MODEL_NAME",
  "url": "API_BASE_URL",
  "token": "YOUR_EXTERNAL_TOKEN"
}
```

**Setup via Developer Studio:**
1. Navigate to Create New Agent
2. Locate the LLM configuration section
3. Select **Bring your own LLM** from the Provider dropdown
4. Enter your API URL, Model Name, and API Token
