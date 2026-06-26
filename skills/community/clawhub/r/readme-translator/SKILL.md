---
name: readme-translator
description: 将 GitHub README 自动翻译成多种语言，支持中文、英文、日文、韩文等。
metadata: {"clawdbot":{"emoji":"🌐","requires":{},"primaryEnv":""}}
---

# README Translator

将 README.md 文件自动翻译成多种语言。

## 功能

- 🌐 多语言支持
- 📝 保持 Markdown 格式
- 🔄 批量翻译
- 📖 术语一致性

## 支持语言

- English
- 中文 (简体)
- 日本語
- 한국어
- Español
- Français
- Deutsch

## 使用方法

```bash
readme-translator --input README.md --lang zh
readme-translator --input README.md --lang ja --output README_JA.md
```

## 选项

- `--input, -i` 输入文件
- `--output, -o` 输出文件
- `--lang, -l` 目标语言
- `--api` 翻译 API
