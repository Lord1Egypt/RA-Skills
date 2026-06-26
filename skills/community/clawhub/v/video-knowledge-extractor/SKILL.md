---
name: video-knowledge-extractor
description: 从视频、音频、播放列表或本地文件中抽取知识，生成摘要、要点、章节和适合知识库沉淀的 Markdown/JSON。适用于链接、文件路径和文件夹输入。
---

# 中文视频知识抽取器

把视频内容整理成可复用的知识资产。

## 何时使用

- 用户给出视频或音频链接，希望整理成笔记
- 用户给出本地文件、文件夹或批量列表，希望自动处理
- 用户需要摘要、要点、章节、行动项，而不只是转写
- 用户要把内容沉淀到 Obsidian、Notion 或其他知识库

## 核心流程

1. 识别输入类型
2. 下载或直接读取媒体
3. Whisper 转写
4. 长内容自动分块总结
5. LLM 后处理生成摘要、要点、章节和行动项
6. 输出固定格式文件

## 处理原则

- 优先输出可入库内容，而不是只返回原文
- 本地文件和文件夹直接读取，不强制下载
- 长视频自动分块，避免单次上下文过大
- LLM 可用时自动增强，不可用时回退本地规则

## 输出

- `summary.md`
- `notes.md`
- `chapters.md`
- `knowledge.json`
- `manifest.json`

## 参考文件

- 运行说明：`README.md`
- 示例输入输出：`examples.md`
- 输出模板：`output_templates/`
- 处理脚本：`scripts/process_media.py`

