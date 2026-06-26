---
name: summarize-all
description: "智能总结工具 - 自动检测内容类型、智能选择长度、缓存、关键点提取。支持网页、PDF、图片、音频、YouTube。"
---

# Summarize All Pro

**Advanced AI Smart Summarizer v3.0** — Multi-featured AI summarization tool

---

## Features

| Feature | Description |
|---------|-------------|
| 🧠 **Auto Detection** | Automatically detect content type (news/paper/product/code/recipe, etc., 9 types) |
| 📏 **Auto Length** | Auto-select summary depth based on content length |
| 📦 **Smart Cache** | 24-hour cache, skip API for repeated requests |
| 🔄 **Quality Scoring** | Auto-score, auto-rewrite low-quality summaries |
| 🤖 **Multi-Model** | Multi-model comparison (GPT-4o vs GPT-4o-mini) |
| 💬 **Q&A Mode** | Q&A mode: ask questions about content |
| ⚖️ **Compare Mode** | Compare mode: compare multiple articles |
| 🌍 **Translation** | Translation mode: 7 languages |
| 🔗 **Knowledge Graph** | Knowledge graph: entity relationship diagrams |
| 📋 **Structured Report** | Structured report: TOC + sections + key points |
| 🌐 **API Server** | HTTP API server |
| 📡 **Webhooks** | Push results to specified URL |
| 🔔 **Notifications** | Desktop notifications |
| 🏷️ **Auto Tags** | Automatic tag extraction |
| 📑 **PDF Merge** | Merge and summarize multiple PDFs |
| 🎓 **Academic Mode** | Academic paper analysis mode |
| 🔎 **Keyword Tracking** | Keyword tracking alerts |
| 🔍 **History Search** | Search through history |
| 📚 **Batch Mode** | Batch processing |
| 📝 **Markdown Render** | Color-formatted output |

---

## Requirements

- Python 3
- OpenAI-compatible API endpoint and key
- Optional: pdftotext, summarize CLI, yt-dlp

---

## Quick Start

```bash
# Configure API
summarize-all config set endpoint <endpoint>
summarize-all config set key <api_key>
summarize-all config set model <model>

# Interactive mode
summarize-all

# Basic use
summarize-all "https://example.com"
```

---

## Supported Models

**OpenAI:**
- GPT-4o
- GPT-4o-mini
- GPT-4 Turbo
- GPT-3.5

**Anthropic:**
- Claude (via proxy)

**Google:**
- Gemini (via proxy)

**OpenRouter:**
- Llama, Mistral, Phi-4, DeepSeek, etc.

**Chinese Models:**
- Qwen
- DeepSeek
- Kimi
- GLM
- MiniMax
- Yi

---

## Supported Content

| Type | Command |
|------|---------|
| 🌐 Web pages | `summarize-all "https://..."` |
| 📄 PDFs | `summarize-all "/path/file.pdf"` |
| 🖼️ Images | `summarize-all "/path/image.jpg"` |
| 🎵 Audio | `summarize-all "/path/audio.mp3"` |
| 🎬 YouTube | `summarize-all "https://youtube.com/..."` |
| 📝 Plain text | `summarize-all "Text to summarize"` |

---

## Commands

### Q&A Mode
```bash
summarize-all qa "https://article.com" "What is the main point?"
```

### Compare Mode
```bash
summarize-all compare "https://source1.com" "https://source2.com"
summarize-all compare url1 url2 url3  # Multi-article comparison
```

### Multi-Model Comparison
```bash
summarize-all multi "https://example.com"
```

### Translation
```bash
summarize-all translate "https://article.com" zh
# Supports: zh, en, ja, ko, fr, de, es
```

### Knowledge Graph
```bash
summarize-all graph "https://wiki.com/article"
```

### Structured Report
```bash
summarize-all structured "https://long-doc.com"
```

### Academic Mode
```bash
summarize-all academic paper.pdf
```

### API Server
```bash
summarize-all server 8080
```

### URL Monitoring
```bash
summarize-all monitor add "https://news.com" 60
summarize-all monitor list
summarize-all monitor remove "https://news.com"
```

### Batch Mode
```bash
summarize-all batch urls.txt
cat urls.txt | summarize-all batch -
```

### History Search
```bash
summarize-all search "keyword"
summarize-all history 20
summarize-all tags
```

---

## Options

| Option | Description |
|--------|-------------|
| `-l, --length` | short/medium/long/xl/auto (default: auto) |
| `-L, --lang` | en/zh/ja/ko/fr/de/es/auto (default: auto) |
| `--no-cache` | Skip cache |
| `--think` | Show chain of thought reasoning |
| `-v, --verbose` | Verbose output |
| `-q, --quiet` | Minimal output |

---

## Content Types

| Type | Focus |
|------|-------|
| 🎓 academic | Research: methodology, findings, conclusions |
| 📰 news | 5W1H, key quotes, impact |
| 🛒 ecommerce | Features, price, pros/cons |
| 💻 code | Functionality, usage, API |
| 🍳 recipe | Ingredients, time, steps |
| 🎬 video | Topics, insights, timestamps |
| 📖 tutorial | Prerequisites, steps, tips |
| ⭐ review | Verdict, pros/cons, rating |

---

## Length Options

| Option | Output |
|--------|--------|
| short | Few sentences |
| medium | 1-2 paragraphs |
| long | Detailed |
| xl | Very long |
| xxl | Complete |
| auto | Auto-select |

---

## Config

```bash
summarize-all config set endpoint "https://api.minimax.chat/v1"
summarize-all config set key "your-key"
summarize-all config set model "MiniMax-Text-01"
summarize-all config show
summarize-all config clear
summarize-all config reset
```

**Files:**
- Config: `~/.config/summarize-all/config.json`
- History: `~/.config/summarize-all/history.json`
- Cache: `~/.config/summarize-all/cache.json`
- Tags: `~/.config/summarize-all/tags.json`
- Keywords: `~/.config/summarize-all/keywords.json`

---

## Interactive Mode

```bash
summarize-all

> https://example.com          # Summarize
> compare a.com b.com          # Compare
> qa url "question"            # Q&A
> search "keyword"             # Search
> tags                          # Tag cloud
> keywords add "AI" "Alert"    # Track
> server 8080                  # API server
> help                          # Full help
> quit                          # Exit
```

---

## Privacy

⚠️ Content you summarize will be sent to your configured API endpoint.

You control:
- Which API endpoint to use
- Which API key to provide
- Which model processes your data

Use trusted endpoints that comply with your privacy requirements.
