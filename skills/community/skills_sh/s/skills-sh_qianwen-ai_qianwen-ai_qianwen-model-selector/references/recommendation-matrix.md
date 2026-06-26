# Recommendation Matrix — qianwen-model-selector

Detailed model recommendation tables. SKILL.md keeps only the canonical `Default` table; this file
provides the in-depth selection logic for cross-skill resolution and per-domain comparison.

> **Reminder**: For latest model availability and pricing, always prefer CLI (`qianwen models list/info/search`).
> See [cli-usage.md](cli-usage.md) for when CLI is required vs. when these snapshot tables are acceptable.

## Cross-Skill Model Resolution

When an execution skill needs to choose a model without user interaction, evaluate across three dimensions:
**Requirement → Scenario → Pricing**. If the user explicitly specified a model, use it as given — but still
verify availability via CLI; if restricted, warn the user and suggest an alternative.

### Dimension 1 · Requirement (select)

Match task capability to the right model. Use when the user's need points to a specialized model, or when
the task is ambiguous and you need to compare capabilities.

| Signal                         | Keywords                                          | Model                                                        |
|--------------------------------|---------------------------------------------------|--------------------------------------------------------------|
| Reasoning                      | "think step by step", "reason", "analyze"         | qwq-plus (text) · qvq-max (vision)                           |
| Coding                         | "write code", "implement", "debug"                | qwen3-coder-plus                                             |
| OCR / document                 | "extract text", "OCR", "scan"                     | qwen-vl-ocr                                                  |
| Long context                   | "long document", "large file"                     | qwen3.6-plus (1M context)                                    |
| Multimodal (text+image+video)  | "analyze image", "understand video" + text        | qwen3.6-plus (unified multimodal)                            |
| Voice interaction / omni       | "voice chat", "speak", "listen"                   | qwen3-omni-flash                                             |
| Built-in tools                 | "search the web", "run code", "use tools"         | qwen3-max (web search, code interpreter)                     |
| Image editing / style transfer | "edit image", "style transfer", "reference image" | wan2.6-image (preferred) · wan2.5-i2i-preview                |
| Image-to-image fusion          | "place object", "combine images", "fuse images"   | wan2.6-image · wan2.5-i2i-preview                            |
| Open-source / lowest cost T2I  | "open-source", "free model", "z-image"            | z-image-turbo                                                |
| Video editing                  | "edit video", "modify video", "video repaint"     | wan2.7-videoedit · happyhorse-1.0-video-edit                 |
| Style TTS                      | "emotion", "tone", "pace"                         | qwen3-tts-instruct-flash                                     |
| Ambiguous                      | task doesn't clearly map to one model             | compare Recommendation Matrix; ask user to clarify if needed |

### Dimension 2 · Scenario (tune)

Adjust model tier based on how the model will be used.

| Pattern                 | Signals                                 | Guidance                                                                |
|-------------------------|-----------------------------------------|-------------------------------------------------------------------------|
| Interactive / real-time | "chat", "real-time", "interactive"      | Prefer flash/turbo variants; enable streaming                           |
| Batch / offline         | "batch", "offline", "background"        | Quality model + Batch API (50% off)                                     |
| One-off trial           | "try", "test", "experiment"             | Quality model; use `qianwen usage free-tier` to check remaining quota   |
| High-volume production  | "production", "at scale", "high volume" | Cost-optimize: flash/turbo + context cache                              |
| Repeated context        | "template", "same prompt", "repeated"   | Enable context caching for input token discount                         |

### Dimension 3 · Pricing (optimize)

Given the candidates from dimensions 1–2, compare costs and apply modifiers.

- **Latest pricing**: When precise figures are needed, run `qianwen models info <model> --format json` —
  it returns structured pricing tiers (input/output per 1M tokens, tiered breakpoints). Snapshot
  ([pricing.md](pricing.md)) is for structural overview only.
- **Free quota**: Some models offer a limited free quota after activation. Quotas may be consumed, expired,
  or changed. **Never assume remaining free quota** — always present the paid unit price. Use
  `qianwen usage free-tier --format json` to check remaining quota.
- **Batch API**: 50% off both input and output tokens for non-realtime workloads.
- **Context cache**: Input token discount for repeated/templated contexts.
- **Tiered pricing**: Some models charge more per token as input length increases — check pricing tables
  for breakpoints.
- When cost is the user's primary concern, explicitly recommend the cheapest viable model and cite the price
  (with mandatory disclaimer — see [pricing-disclaimer.md](pricing-disclaimer.md)).

## Recommendation Matrix by Domain

### Text Models

| Use Case                | Recommended      | Why                                                                  |
|-------------------------|------------------|----------------------------------------------------------------------|
| Best overall            | qwen3.6-plus     | Latest flagship. Multimodal. 1M context. Thinking on by default.     |
| Strongest reasoning     | qwen3-max        | Built-in tools (web search, code interpreter). Hybrid thinking.      |
| Pure CoT reasoning      | qwq-plus         | Always-on chain-of-thought, math/code specialist                     |
| Fast / interactive      | qwen3.5-flash    | Fastest in Qwen3.5 series                                            |
| Cheapest                | qwen-turbo       | Lowest per-token cost                                                |
| Coding                  | qwen3-coder-plus | Best code model, 1M context                                          |
| Coding (balanced)       | qwen3-coder-next | Top recommendation, balances quality/speed/cost, agentic + tools     |
| Role-play (general)     | qwen-plus-character | Character restoration, empathetic dialog                          |
| Role-play (Japanese)    | qwen-plus-character-ja | Japanese role-playing                                          |

### Vision Models

| Use Case                       | Recommended    | Why                                                                                                                            |
|--------------------------------|----------------|--------------------------------------------------------------------------------------------------------------------------------|
| Best accuracy                  | qwen3.6-plus   | **Latest flagship.** Multimodal (text + image + video). Surpasses qwen3-vl series on many benchmarks. Thinking on by default. |
| High-precision localization    | qwen3-vl-plus  | Highest vision understanding for object localization (2D/3D), document/webpage parsing. Thinking mode. 256K context.           |
| Fast analysis                  | qwen3-vl-flash | Quick image understanding. Thinking mode supported.                                                                            |
| Visual reasoning (math/charts) | qvq-max        | Always-on CoT for visual reasoning                                                                                             |
| OCR specialist                 | qwen-vl-ocr    | Document/scan text extraction, max 30K tokens/image                                                                            |
| Unified text+vision            | qwen3.6-plus   | Best when both text quality and vision matter. 1M context.                                                                     |

### Image Models

| Use Case                                  | Recommended        | Why                                                              |
|-------------------------------------------|--------------------|------------------------------------------------------------------|
| Highest quality (4K)                      | wan2.7-image-pro   | Up to 4K, multi-function, thinking mode                          |
| Multi-function (2K)                       | wan2.7-image       | Faster variant of pro, 2K max                                    |
| Quality text-to-image                     | wan2.6-t2i         | Best in wan2.6 series                                            |
| Image **editing** (refs required)         | wan2.6-image       | Style transfer, subject consistency (1–4 refs), interleave 2K    |
| Image-to-image fusion                     | wan2.5-i2i-preview | Multi-image fusion (1–3 refs), async-only                        |
| Interleaved text-image output (tutorials) | wan2.6-image       | Mixed text+image generation                                      |
| Fast iteration                            | wan2.2-t2i-flash   | 50% faster generation                                            |
| Flexible resolution                       | wan2.5-t2i-preview | Custom aspect ratios                                             |
| Open-source SOTA T2I                      | z-image-turbo      | Open-source; sync-only; no `n` / no refs; lightweight payload    |

### Video Models

| Use Case                         | Recommended                | Why                                                            |
|----------------------------------|----------------------------|----------------------------------------------------------------|
| Latest (with audio)              | wan2.7-t2v / i2v           | 720P/1080P, auto-dubbing                                       |
| Quick video creation             | wan2.6-i2v-flash           | Fast, multi-shot narrative                                     |
| High quality                     | wan2.6-i2v                 | Best visual quality                                            |
| With audio (legacy)              | wan2.5-i2v-preview         | Auto-dubbing support                                           |
| First+last frame                 | wan2.2-kf2v-flash          | 5s, silent                                                     |
| Video editing (legacy VACE)      | wan2.1-vace-plus           | Repainting, extension                                          |
| Video editing (Wan)              | wan2.7-videoedit           | New `videoedit` mode, `media[]` protocol, no `function` field  |
| Video editing (HappyHorse)       | happyhorse-1.0-video-edit  | HappyHorse video editing, same `media[]` protocol              |
| Text-to-video (HappyHorse)       | happyhorse-1.0-t2v         | Uses `resolution` + `ratio` parameters                         |
| Image-to-video (HappyHorse)      | happyhorse-1.0-i2v         | HappyHorse i2v, `resolution` + `ratio`                         |
| Reference-to-video (HappyHorse)  | happyhorse-1.0-r2v         | Up to 9 reference images via `media[]`                         |

### Audio Models

| Use Case              | Recommended                | Why                                                           |
|-----------------------|----------------------------|---------------------------------------------------------------|
| **Highest quality**   | `cosyvoice-v3-plus`        | Best naturalness, emotional expression, professional scenarios|
| High quality + speed  | `cosyvoice-v3-flash`       | Good balance of quality and performance                       |
| Standard TTS          | `qwen3-tts-flash`          | Fast, reliable, multi-language, cost-effective                |
| Controlled style      | `qwen3-tts-instruct-flash` | Instruction-guided voice style (tone/emotion)                 |
| ASR (real-time)       | `qwen3-asr-flash`          | Real-time speech recognition                                  |

### Omni Models

| Use Case            | Recommended               | Why                                                                                   |
|---------------------|---------------------------|---------------------------------------------------------------------------------------|
| Voice + vision chat | qwen3-omni-flash          | Text/image/audio/video → text or speech. 49 voices, 10 languages. Thinking supported. |
| Real-time voice     | qwen3-omni-flash-realtime | Streaming audio input + built-in VAD. 49 voices.                                      |

## Token Plan 团队版 Models

Users with a [Token Plan 团队版](https://platform.qianwenai.com/docs/token-plan/overview) subscription
(`sk-sp-` key, endpoint `https://token-plan.cn-beijing.maas.aliyuncs.com`) have access to a fixed
set of models through interactive AI tools only (Cursor, Claude Code, Qwen Code, OpenClaw, OpenCode,
Codex, Kilo Code/CLI, Hermes Agent). The Token Plan key cannot be used in scripts, application
backends, or batch jobs — violations may trigger subscription suspension.

### Text Models (4 total)

| Model           | Context | Thinking         | OpenAI-compat | Anthropic-compat | Notes                                                      |
|-----------------|--------:|------------------|:-------------:|:----------------:|------------------------------------------------------------|
| `qwen3.6-plus`  |      1M | Yes (default on) | ✅            | ✅               | Flagship; multimodal text+image input; built-in Responses API tools (web search, code interpreter, web fetch, image search) |
| `glm-5`         |    198K | Yes (`thinkingFormat: qwen`) | ✅ | ✅            | Max output 16,384                                          |
| `MiniMax-M2.5`  |    192K | Yes              | ✅            | ✅               | budgetTokens + output ≤ 32,768                             |
| `deepseek-v3.2` |    128K | Yes (`thinkingFormat: qwen`) | ✅ | ❌ **OpenAI only** | Not available via Anthropic-compatible endpoint        |

### Image Generation Models (4 total)

> [!IMPORTANT]
> Token Plan image models are **not** invoked through the standard text Base URL. They use a
> dedicated multimodal-generation endpoint and must be wired up via each tool's Skill / Slash Command /
> Agent mechanism.
> Endpoint: `POST https://token-plan.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

| Model                | Notes                                                              |
|----------------------|--------------------------------------------------------------------|
| `qwen-image-2.0`     | Default; general-purpose; strong Chinese text rendering            |
| `qwen-image-2.0-pro` | Higher quality, slightly slower                                    |
| `wan2.7-image`       | Multi-style; returns 4 images by default                           |
| `wan2.7-image-pro`   | Supports 4K; additional sizes 2048×2048, 1440×2560, 2560×1440      |

Available sizes: `1024*1024` (default), `720*1280`, `1280*720`. `wan2.7-image-pro` adds 4K options above.

### Endpoints

| Protocol           | Base URL                                                              |
|--------------------|-----------------------------------------------------------------------|
| OpenAI-compatible  | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`  |
| Anthropic-compatible | `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`    |
| Image generation   | `https://token-plan.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation` |

### Excluded Modalities

Token Plan 团队版 does **not** include video generation, TTS, ASR, embeddings, rerank, translation, or
specialized vision models (qwen3-vl-*, qwen-vl-ocr, qvq-max). Users needing those must fall back to a
standard pay-as-you-go `sk-` key.

When recommending models, note if the user's chosen model falls outside the lists above and they are
using a Token Plan key (`sk-sp-...`). Suggest the closest available alternative or recommend obtaining
a standard `sk-` key.

If `qianwen-ops-auth` is installed, see its `references/tokenplan.md` for endpoint mapping, Credits
billing details, and full error code reference.

### Billing (Credits)

- **Unit**: Credits (not per-token CNY).
- **Tiers**: 标准坐席 (¥198/seat/month, 25,000 Credits) · 高级坐席 (¥698/seat/month, 100,000 Credits) · 尊享坐席 (¥1,398/seat/month, 250,000 Credits).
- **Shared usage package**: ¥5,000 / 625,000 Credits / 1-month validity.
- **Deduction order**: seat quota → shared package (nearest-expiry first) → service paused.
- **Usage queries**: Currently only available via the
  [Token Plan Subscription console](https://platform.qianwenai.com/home/billing/subscription/token-plan).
  The `qianwen` CLI does not yet support `sk-sp-` Token Plan keys.

## Thinking Mode

Several models support hybrid thinking/non-thinking modes:

| Model                               | Thinking Default | Notes                                                                                         |
|-------------------------------------|------------------|-----------------------------------------------------------------------------------------------|
| qwen3.6-plus                        | **On**           | Latest flagship. Thinking enabled by default. Use `enable_thinking: false` to disable.        |
| qwen3.5-plus                        | **On**           | Thinking enabled by default. Use `enable_thinking: false` to disable.                         |
| qwen3.5-flash                       | **On**           | Thinking enabled by default.                                                                  |
| qwen3-max                           | Off              | Use `enable_thinking: true` for complex reasoning. Built-in tools available in thinking mode. |
| qwen-plus / qwen-flash / qwen-turbo | Off              | Hybrid; enable for deeper reasoning at higher output cost.                                    |
| qwen3-vl-plus / qwen3-vl-flash      | Off              | Vision + thinking for complex visual analysis.                                                |
| qwen3-omni-flash                    | Off              | Thinking supported; audio output not available in thinking mode.                              |
| qwq-plus / qvq-max                  | Always on        | Pure reasoning models; CoT always active.                                                     |

**Guidance**: Do not enable thinking by default for simple or conversational tasks — it increases latency and
output token cost. Enable only when the user explicitly asks for deep reasoning or the task requires
multi-step analysis.

## Available Models (snapshot)

> **⚠️ Snapshot warning**: This list is point-in-time and may be outdated. **Prefer**
> `qianwen models list --all --format json` for the up-to-date catalog. See [model-list.md](model-list.md)
> for the structured offline reference.

- **Text (commercial)**: qwen3.6-max-preview, qwen3.6-plus, qwen3.6-flash, qwen3-max, qwen3.5-plus, qwen3.5-flash, qwen-turbo, qwq-plus, qwen3-coder-next/plus/flash, qwen-plus-character, qwen-plus-character-ja, qwen-flash-character
- **Text (open-source)**: qwen3.6-27b, qwen3.5-27b
- **Text (third-party)**: deepseek-v4-flash, glm-5.1, kimi-k2.6, MiniMax-M2.5
- **Vision**: qwen3.6-plus (multimodal), qwen3-vl-plus, qwen3-vl-flash, qvq-max, qwen-vl-ocr, qwen-vl-max, qwen-vl-plus
- **Omni**: qwen3-omni-flash (+ realtime), qwen-omni-turbo (+ realtime)
- **Image generation (text-to-image)**: wan2.7-image-pro, wan2.7-image, wan2.6-t2i, wan2.5-t2i-preview, wan2.2-t2i-flash, z-image-turbo
- **Image editing (requires reference images)**: wan2.6-image, wan2.5-i2i-preview
- **Video generation**: wan2.7-t2v/i2v/videoedit, wan2.6 series (t2v, i2v, i2v-flash, r2v, r2v-flash), wan2.5/2.2 series, vace, happyhorse-1.0-t2v/i2v/r2v/video-edit
- **TTS**: qwen3-tts-flash, qwen3-tts-instruct-flash, cosyvoice-v3 series
- **ASR**: qwen3-asr-flash, fun-asr
- **Embedding/Rerank**: text-embedding-v4, qwen3-rerank
- **Translation**: qwen-mt-plus/flash/lite/turbo
