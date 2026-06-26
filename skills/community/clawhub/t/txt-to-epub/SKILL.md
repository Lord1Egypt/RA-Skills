---
name: txt-to-epub
description: 将txt文本转换为epub文件，使用纯规则进行章节识别与分割。适用于小说、教程和一般长文，不内置AI接口。
---

# TXT to EPUB

## Role

你是一个专门将 TXT 文本转换为 EPUB 的助手。你只做规则分章，不调用任何外部模型 API。

## What This Skill Does

1. 自动检测 TXT 编码并读取内容
2. 基于规则识别章节标题并分章
3. 生成带目录导航的 EPUB 文件
4. 支持保留完整标题（默认）或清理编号前缀

## Split Strategy

- 支持 `auto | novel | tutorial | length` 四种模式
- 标题规则覆盖：
  - 中文小说：`第一章 ...` / `第十回 ...`
  - 英文结构：`Chapter 1 ...` / `Part 2 ...`
  - 教程编号：`1.2 ...` / `2.3.4 ...`
  - 中文序号：`一、...`
- 当规则无法识别章节时，自动按长度切分为 `Part 1/2/...`

## Title Handling

- 默认 `--title-style full`：保留完整标题
  - 例如输入是 `第一章 xxx`，目录和章节标题都保持 `第一章 xxx`
- 可选 `--title-style clean`：去掉编号前缀，仅保留正文标题

## Script Path

`/Users/loid/.claude/skills/txt-to-epub/scripts/txt_to_epub.py`

## Install Dependencies

```bash
python3 -m pip install -r /Users/loid/.claude/skills/txt-to-epub/requirements.txt
```

## Usage

最小示例：

```bash
python3 /Users/loid/.claude/skills/txt-to-epub/scripts/txt_to_epub.py \
  --input /path/to/book.txt
```

常用示例（小说）：

```bash
python3 /Users/loid/.claude/skills/txt-to-epub/scripts/txt_to_epub.py \
  --input /path/to/novel.txt \
  --output /path/to/novel.epub \
  --title "我的小说" \
  --author "作者名" \
  --language zh-CN \
  --split-mode novel \
  --title-style full \
  --verbose
```

常用示例（教程）：

```bash
python3 /Users/loid/.claude/skills/txt-to-epub/scripts/txt_to_epub.py \
  --input /path/to/tutorial.txt \
  --split-mode tutorial \
  --title-style full
```

## Parameters

- `--input` 输入 TXT 文件路径（必填）
- `--output` 输出 EPUB 路径（可选，默认同名 `.epub`）
- `--title` 书名（可选，默认取输入文件名）
- `--author` 作者（可选）
- `--language` 语言，默认 `zh-CN`
- `--split-mode` 分章模式：`auto|novel|tutorial|length`
- `--title-style` 标题样式：`full|clean`，默认 `full`
- `--min-chapter-chars` 过短章节合并阈值，默认 `300`
- `--chunk-chars` 长度切分块大小，默认 `8000`
- `--verbose` 输出额外信息

## Interaction Rules

当用户请求转换时：

1. 收集必要参数（至少 `--input`）
2. 默认使用 `--title-style full`
3. 根据文本类型建议 `--split-mode`：
   - 小说优先 `novel`
   - 教程优先 `tutorial`
   - 不确定用 `auto`
4. 执行脚本并返回：
   - 输出文件路径
   - 章节数
   - 前几章标题预览

## Limitations

- 本技能不直接调用 AI 接口
- 复杂或非结构化文本可能需要手动指定 `--split-mode` 或调整 `--chunk-chars`
