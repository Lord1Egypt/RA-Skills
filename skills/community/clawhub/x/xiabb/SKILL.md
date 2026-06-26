---
name: 虾BB
description: 免费 macOS 语音转文字，专为 Vibe Coding 设计。按住 Globe 键说话，文字自动出现在光标位置。支持智能模式：翻译、Prompt 优化、邮件生成。Powered by Google Gemini。
version: 1.3.2
license: MIT-0
author: dyz2102
homepage: https://xiabb.lol
repository: https://github.com/dyz2102/xiabb
tags: voice, speech-to-text, macos, gemini, vibe-coding, translate, prompt
---

# 虾BB 🦞

**按住 Globe 键，说话，文字出现。**

专为 Vibe Coding 设计的免费开源 macOS 语音转文字。纯 Swift 原生，341KB，~38MB 内存。

## 功能

- 🌐 **Globe 键一键录音** — 按住说话，松开自动转写+粘贴
- 🔴 **实时流式预览** — 说话时文字实时出现在 HUD 上
- 🌏 **中英完美混输** — "帮我 schedule a meeting" → 完美识别
- 🧠 **LLM 而非 ASR** — Google Gemini 理解语义，标点完美

## 🧠 Smart Modes 智能模式

录音时按快捷键，AI 自动处理：

| 快捷键 | 模式 | 效果 |
|--------|------|------|
| `Globe + `` | 🔄 翻译 | 说中文出英文，说英文出中文，自动识别 |
| `Globe + 1` | ⚡ 提示词 | 口述想法，自动生成专业 AI 提示词 |
| `Globe + 2` | 📧 邮件 | 口述内容，自动生成格式规范的邮件 |
| `Globe + Esc` | ⛔ 取消 | 丢弃录音 |

再按同一键可切换回普通听写模式。

## 竞品对比

| | 虾BB | Typeless | Wispr Flow | SuperWhisper |
|---|---|---|---|---|
| 价格 | **免费** | $12/月 | $15/月 | $8.49/月 |
| 内存 | **~38MB** | **~1GB** | ~200MB | ~500MB+ |
| 体积 | 341KB | ~50MB | ~50MB | ~100MB |
| 开源 | ✅ | ❌ | ❌ | ❌ |

## 安装

```bash
# 下载 DMG
open https://github.com/dyz2102/xiabb/releases/latest

# 或从源码编译
git clone https://github.com/dyz2102/xiabb.git && cd xiabb && bash install.sh
```

需要免费的 Gemini API Key：[aistudio.google.com/apikey](https://aistudio.google.com/apikey)

macOS 14+ · Apple Silicon · MIT License
