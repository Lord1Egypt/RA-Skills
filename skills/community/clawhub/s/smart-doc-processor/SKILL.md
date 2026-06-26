---
name: smart-doc-processor
description: 智能文档处理助手 - 一站式文档处理工具，支持 PDF 转换、智能摘要、多语言翻译、格式转换等功能。自动提取关键信息，生成结构化报告，提升文档处理效率10倍。
homepage: https://github.com/openclaw/smart-doc-processor
metadata:
  openclaw:
    emoji: 📄
    requires:
      bins: ["node", "pdftotext"]
---

# 智能文档处理助手

一站式文档处理工具，让文档处理效率提升 10 倍。

## ✨ 功能特点

- 📄 **PDF 智能处理** - 提取文本、表格、图片，保留原始格式
- 📝 **AI 智能摘要** - 自动提取关键信息，生成结构化摘要
- 🌐 **多语言翻译** - 支持 50+ 语言，保持专业术语准确
- 🔄 **格式转换** - PDF ↔ Word ↔ Markdown ↔ HTML
- 🔍 **信息提取** - 自动识别日期、金额、人名等关键信息
- 📊 **报告生成** - 一键生成专业的分析报告

## 🚀 使用方法

### PDF 转文本

```bash
node {baseDir}/scripts/process.mjs --input ./document.pdf --output ./output.md
```

### 生成智能摘要

```bash
node {baseDir}/scripts/summarize.mjs --input ./report.pdf --length medium
```

### 翻译文档

```bash
node {baseDir}/scripts/translate.mjs --input ./doc.pdf --from zh --to en
```

### 提取关键信息

```bash
node {baseDir}/scripts/extract.mjs --input ./contract.pdf --type entities
```

## 📋 支持的文档类型

- PDF（扫描件和文本型）
- Word（.doc, .docx）
- Markdown
- HTML
- 图片（JPG, PNG, 带文字）

## 🔧 输出格式

- Markdown（推荐）
- Word
- HTML
- JSON（结构化数据）

## License

MIT
