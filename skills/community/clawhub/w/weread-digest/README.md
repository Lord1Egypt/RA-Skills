# WeRead Digest (微信读书笔记智能消化)

> 🧠 AI-powered reading note digestion — turn your WeRead highlights into insights and knowledge.

[![Skill Type](https://img.shields.io/badge/type-skill-blue)]()
[![Platform](https://img.shields.io/badge/platform-OpenClaw-orange)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

---

## What It Does

Takes your WeRead (微信读书) highlights and notes, and uses AI to:

- 📊 **Reading Stats** — Shelf overview, reading time, note distribution
- 📰 **Weekly/Monthly Digest** — Auto-generated reading reports with highlights
- 📖 **Book Note Synthesis** — Turn a book's scattered highlights into a structured summary
- 🔗 **Cross-Book Theme Explorer** — Discover connections across your reading
- 🧠 **Knowledge Base Archive** — Extract concepts from highlights into your Obsidian vault (or any Markdown KB)

## Quick Start

1. Install the companion `weread` skill (handles data fetching)
2. Configure your WeRead cookie
3. Run `export_notes.py` once to pull your data
4. Say "读书统计" or "本周读书报告" to get started

## Dependencies

- `weread` skill (required — provides data pipeline)

## Example Prompts

| You Say | You Get |
|---------|---------|
| "本周读书报告" | Weekly reading digest with stats + highlights + AI insights |
| "总结《思考，快与慢》的笔记" | Structured summary of all your notes from that book |
| "跨书主题分析" | Theme map showing connections across your reading |
| "把《西方思想史十二讲》整理进知识库" | Concepts extracted from highlights → your Obsidian vault |

## Configuration

On first Knowledge Base Archive use, you'll be guided to configure:
- Knowledge base tool (Obsidian / plain Markdown / Notion)
- Knowledge base path
- Optional: custom schema file (e.g., WIKI-SCHEMA.md)

Configuration saved to `~/.weread/kb-config.json`.

## Privacy

All processing is local. Your reading data never leaves your machine. No third-party API calls for content processing.

---

*Built for [OpenClaw](https://openclaw.ai) — the AI assistant that lives on your machine.*
