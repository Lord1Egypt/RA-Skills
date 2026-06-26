# 📄 智能文档处理助手

一站式文档处理工具，让文档处理效率提升 10 倍。

## ✨ 功能特点

- 📄 **PDF 智能处理** - 提取文本、表格、图片
- 📝 **AI 智能摘要** - 自动提取关键信息
- 🌐 **多语言翻译** - 支持 50+ 语言
- 🔍 **信息提取** - 自动识别日期、金额、邮箱等
- 📊 **报告生成** - 一键生成专业分析报告

## 🚀 快速开始

### 安装

```bash
clawhub install smart-doc-processor
```

### PDF 转文本

```bash
node scripts/process.mjs --input ./document.pdf --output ./output.md
```

### 生成智能摘要

```bash
node scripts/process.mjs --input ./report.pdf --action summarize --length medium
```

### 提取关键信息

```bash
node scripts/process.mjs --input ./contract.pdf --action extract --type entities
```

## 📋 支持的文档类型

- PDF（扫描件和文本型）
- Word（.doc, .docx）
- Markdown
- HTML
- 文本文件

## 🔧 输出格式

- Markdown（推荐）
- JSON（结构化数据）
- 纯文本

## 🛠️ 技术架构

- **PDF 处理**: pdftotext / 自定义解析
- **文本分析**: 正则表达式 + AI 辅助
- **输出格式**: Markdown
- **运行环境**: OpenClaw

## 📄 许可证

MIT License

## 📝 更新日志

### v1.0.0 (2026-03-20)
- ✨ 初始版本发布
- 📄 PDF 文本提取
- 📝 智能摘要生成
- 🔍 关键信息提取（日期、金额、邮箱、电话）
