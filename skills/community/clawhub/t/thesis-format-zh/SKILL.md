---
name: thesis-format-zh
description: 中文论文格式检查工具。解析学校模板docx，提取格式规则，对比论文生成差异报告。支持页边距/标题/正文/页眉/页码/三线表/引用格式检查。触发词：论文排版、格式检查、Word格式、毕业论文。
version: 1.0.0
author: zhaohe
tags: [thesis, word, docx, formatting, chinese, academic, 排版, 论文]
---

# 论文格式检查 (Thesis Format ZH)

> 免费版：格式检查 + 差异报告。自动修复功能需购买完整版。

## 功能（免费版）

- 📐 **模板解析** — 从学校模板 docx 提取格式规则（字体/字号/行距/页边距/页眉）
- 🔍 **格式检查** — 检查论文 docx 是否符合模板规范
- 📊 **差异报告** — 逐段逐属性输出差异表（Markdown 格式）
- ✅ **风险报告** — 交付前格式风险检查

## 功能（完整版 ¥99）

- 🔧 **自动修复** — 一键按模板修复全部格式，输出新 docx
- 📊 **三线表** — 普通表格 → 学术三线表
- 🔢 **引用上标** — [1][2,3] 自动转上标
- 📖 **参考文献交叉引用** — 正文引用与参考文献双向关联
- 📝 **页眉自动跟随** — STYLEREF 域章名跟随
- 📋 **批量处理** — 多篇论文一次排完
- 🏫 **多学校模板** — 河北科技大学、河北经贸大学等

## 使用方式

```bash
# 1. 解析模板，提取规则
python template_reader.py 模板.docx -o rules.json

# 2. 检查论文格式
python reader.py 论文.docx --classify -o paper.json

# 3. 生成差异报告
python differ.py 论文.docx -t 模板.docx -o 差异表.md

# 4. 风险检查
python risk_report.py 论文.docx -o 风险报告.md
```

或通过 OpenClaw 对话：
```
帮我检查论文格式，模板是xxx，论文是xxx
```

## 购买完整版

- 微信咨询：a175311344（备注：论文排版）
- 闲鱼搜索「AI论文自动排版」

## 安装

```bash
clawhub install thesis-format-zh
```

## License

MIT (免费版)。完整版另行授权。
