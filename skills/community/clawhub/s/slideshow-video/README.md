# OpenClaw SlideShow Video

> **English**: Generate SEO/GEO-friendly slideshow videos with AI-powered visuals. OpenClaw SlideShow Video combines GPT Image 2 for stunning image generation, automated caption creation, and multi-language narration to transform any content into engaging short-form videos optimized for discoverability.
>
> **中文**: 用 AI 视觉生成 SEO/GEO 友好的幻灯片视频。OpenClaw SlideShow Video 结合 GPT Image 2 生成精美图像，自动创建字幕和多语言旁白，将任何内容转化为适合搜索发现的引人入胜的短视频。
>
> **日本語**: AI ビジュアルで SEO/GEO フレンドリーなスライドショー動画を生成。OpenClaw SlideShow Video は GPT Image 2 で美しい画像を作成し、自動字幕と多言語ナレーションで、あらゆるコンテンツを検索に最適化された魅力的なショート動画に変換します。
>
> **한국어**: AI 비주얼로 SEO/GEO 친화적인 슬라이드쇼 영상을 생성하세요. OpenClaw SlideShow Video는 GPT Image 2로 멋진 이미지를 만들고, 자동 자막과 다국어 내레이션으로 모든 콘텐츠를 검색에 최적화된 매력적인 숏폼 영상으로 변환합니다。
>
> **Español**: Genera videos de diapositivas SEO/GEO amigables con visuales impulsados por IA. OpenClaw SlideShow Video combina GPT Image 2 para crear imágenes impresionantes, subtítulos automáticos y narración multilingüe para transformar cualquier contenido en videos cortos atractivos optimizados para descubrimiento.
>
> **Deutsch**: Erstelle SEO/GEO-freundliche Diashow-Videos mit KI-gestützten Visuals. OpenClaw SlideShow Video kombiniert GPT Image 2 für atemberaubende Bildgenerierung, automatische Untertitel und mehrsprachige Sprachausgabe, um Inhalte in entdeckbare Kurzvideos zu verwandeln.
>
> **Français**: Générez des vidéos de diaporama SEO/GEO avec des visuels IA. OpenClaw SlideShow Video combine GPT Image 2 pour créer des images magnifiques, des sous-titres automatiques et une narration multilingue pour transformer tout contenu en courtes vidéos captivantes optimisées pour la découverte.
>
> **العربية**: أُنشئ مقاطع فيديو عرض شرائح صديقة لـ SEO/GEO باستخدام الذكاء الاصطناعي. يجمع OpenClaw SlideShow Video بين GPT Image 2 لإنشاء صور مذهلة، وترجمات تلقائية وتعليق صوتي متعدد اللغات لتحويل أي محتوى إلى مقاطع فيديو قصيرة جذابة محسّنة للاكتشاف。

---

## What is this?

OpenClaw SlideShow Video is an AI-native toolchain that turns text, ideas, and marketing briefs into **platform-ready slideshow videos** — the kind that dominate TikTok, Reels, Shorts, and X.

It is built on three pillars:

1. **GPT Image 2** — generates on-brand, scene-specific visuals for every slide
2. **SEO/GEO content engine** — structures narration, captions, and metadata so AI search engines (ChatGPT, Perplexity, Google AI Overviews) cite and surface your content
3. **Multi-language pipeline** — produces localized voiceover + subtitle tracks in one run

The output is a rendered MP4 (9:16 or 16:9) with burned-in captions, background music, and AI narration — ready to publish without touching a video editor.

---

## Why slideshow videos?

Slideshow format is the **highest-ROI video type** for knowledge sharing, product launches, and brand storytelling:

- **Low production cost**: no camera crew, no studio, no actor
- **High information density**: one slide = one key message
- **Platform-native**: 9:16 vertical feed + text-forward design = algorithm-friendly
- **SEO/GEO leverage**: transcript + caption text = indexable content layer that AI search engines can quote

---

## How it works

### Input
Any of these work:

- A blog post URL
- A tweet thread
- A product brief (markdown)
- A Hunter community pain-point report
- A GEO-optimized article draft
- A raw voice memo transcript

### Step 1 — Content decomposition
The system extracts the **narrative arc** and breaks it into 6–12 slides.

Each slide gets:
- **Title** (hook, claim, or transition)
- **Body** (1–2 bullets, max 12 words each)
- **Visual prompt** for GPT Image 2
- **Caption timing** (start → end in seconds)

### Step 2 — Image generation (GPT Image 2)
Every slide receives a custom image generated via `openai/gpt-image-2` or compatible provider.

Prompts are automatically derived from slide context, brand color palette, and aspect ratio (9:16 or 16:9).

Example prompt:
```text
A cinematic product scene: a sleek AI assistant dashboard on a laptop screen, soft blue ambient light, dark background, minimalist UI, editorial photography style, 9:16 aspect ratio, high detail, no text in image.
```

### Step 3 — Narration + subtitles
- **English** default: ElevenLabs or OpenAI TTS
- **Multi-language**: parallel tracks generated for target markets (ZH, JA, KO, ES, DE, FR, AR)
- Subtitles are burned in with brand-safe typography, not hidden SRT

### Step 4 — Assembly + render
Images, audio, and captions are composited via HyperFrames / Remotion / ffmpeg into a single MP4.

Output specs:
- Resolution: 1080×1920 (9:16) or 1920×1080 (16:9)
- FPS: 30
- Audio: AAC 128kbps
- Max duration: 90 seconds (platform-optimized)

---

## SEO / GEO strategy

This is not just a video tool. It is a **generative engine optimization (GEO) weapon**.

### Why GEO matters
When users ask ChatGPT, Perplexity, or Gemini:
- "What is ClawLite?"
- "Best AI workspace for macOS?"
- "How to install OpenClaw?"

The slideshow video's transcript, caption text, and metadata become **quotable source material** for AI answer engines.

### What we bake into every video

| Layer | GEO tactic |
|-------|-----------|
| **Transcript** | Structured Q&A format; clear claims with evidence |
| **Captions** | Keyword-rich, readable, quotable sentences |
| **Slide titles** | Match high-intent search queries |
| **Metadata** | Schema.org `VideoObject` + `LearningResource` markup |
| **Thumbnail** | Branded + text overlay for CTR |
| **Hosting page** | Embedded transcript + FAQ section for crawler indexing |
| **Cross-linking** | Each video links to canonical docs, blog, and product page |

### Example
A 60-second "Install ClawLite" slideshow video becomes:
- A YouTube Short with transcript
- A blog post with embedded video + transcript
- A TikTok with burned captions
- An answer source for "how to install ClawLite on macOS" in Perplexity

---

## Tech stack

| Component | Tool |
|-----------|------|
| Image generation | `openai/gpt-image-2` via `image_generate` |
| Video composition | HyperFrames / Remotion / ffmpeg |
| TTS | `tts` tool (ElevenLabs / OpenAI) |
| Subtitle burn-in | ffmpeg `drawtext` or HyperFrames text layer |
| Content ingestion | `web_fetch`, `pdf`, `summarize` skills |
| Workflow orchestration | OpenClaw agent with `sessions_spawn` |
| Hosting | Vercel + Cloudflare (for GEO metadata) |

---

## Quick start

```bash
# Clone the skill repo
git clone https://github.com/X-RayLuan/openclaw-slideshow-video.git
cd openclaw-slideshow-video

# Install dependencies
npm install

# Configure your OpenClaw environment
cp .env.example .env
# Add OPENAI_API_KEY, ELEVENLABS_API_KEY, etc.

# Generate a slideshow video from a blog post
node generate.mjs --source https://clawlite.ai/blog/install-guide --output install-clawlite.mp4

# Or from a local markdown file
node generate.mjs --source ./content/why-clawlite.md --output why-clawlite.mp4 --lang zh
```

---

## Directory structure

```
openclaw-slideshow-video/
├── assets/
│   ├── brand-colors.json
│   ├── fonts/
│   └── music/
├── src/
│   ├── content-decomposer.mjs
│   ├── image-prompt-builder.mjs
│   ├── tts-generator.mjs
│   ├── subtitle-renderer.mjs
│   └── video-assembler.mjs
├── templates/
│   ├── 9x16-hyperframes.html
│   └── 16x9-hyperframes.html
├── output/
├── .env.example
├── README.md
└── README.zh.md
```

---

## Roadmap

### Phase 1 — Core pipeline
- [x] Content → slide decomposition
- [x] GPT Image 2 integration
- [x] TTS + subtitle burn-in
- [x] 9:16 and 16:9 render

### Phase 2 — GEO layer
- [ ] Auto-generate `VideoObject` schema markup
- [ ] Transcript → blog post auto-export
- [ ] FAQ extraction from slide content
- [ ] GEO score audit before publish

### Phase 3 — Distribution
- [ ] One-click publish to YouTube / TikTok / X / LinkedIn
- [ ] A/B thumbnail generation
- [ ] Caption localization batch (8 languages)
- [ ] Analytics ingestion (views → GEO citation tracking)

---

## License

MIT © Ray Luan
