# txt-to-epub

将 `.txt` 文本转换为 `.epub`，使用纯规则进行章节识别与分割，适用于小说、教程和一般长文。

## 特性

- 纯规则分章，不依赖模型 API
- 自动检测文本编码（UTF-8/GBK/Big5/UTF-16 等）
- 支持小说和教程类标题模式
- 无法识别标题时自动按长度切分
- 生成可导航目录（TOC）的标准 EPUB

## 目录结构

```text
txt-to-epub/
  SKILL.md
  requirements.txt
  scripts/
    txt_to_epub.py
```

## 安装依赖

```bash
python3 -m pip install -r requirements.txt
```

## 快速开始

在 `txt-to-epub` 目录下执行：

```bash
python3 scripts/txt_to_epub.py --input /path/to/book.txt
```

默认会在同目录输出同名 `.epub` 文件。

## 常用命令

小说分章（保留完整标题，推荐）：

```bash
python3 scripts/txt_to_epub.py \
  --input /path/to/novel.txt \
  --split-mode novel \
  --title-style full \
  --verbose
```

教程分章：

```bash
python3 scripts/txt_to_epub.py \
  --input /path/to/tutorial.txt \
  --split-mode tutorial \
  --title-style full
```

强制按长度切分：

```bash
python3 scripts/txt_to_epub.py \
  --input /path/to/long_text.txt \
  --split-mode length \
  --chunk-chars 8000
```

## 参数说明

- `--input`：输入 TXT 路径（必填）
- `--output`：输出 EPUB 路径（可选，默认同名）
- `--title`：书名（可选，默认取文件名）
- `--author`：作者（可选）
- `--language`：语言（默认 `zh-CN`）
- `--split-mode`：`auto | novel | tutorial | length`
- `--title-style`：`full | clean`（默认 `full`）
  - `full`：完整保留标题，如 `第一章 旧土`
  - `clean`：去掉编号前缀，仅保留正文标题
- `--min-chapter-chars`：过短章节合并阈值（默认 `300`）
- `--chunk-chars`：长度切分每块字符数（默认 `8000`）
- `--verbose`：输出更多日志

## 标题识别规则（摘要）

- 中文小说：`第一章 ...`、`第十回 ...`
- 英文结构：`Chapter 1 ...`、`Part 2 ...`
- 教程编号：`1.2 ...`、`2.3.4 ...`
- 中文序号：`一、...`

如果没有识别到有效章节标题，会自动降级为按长度分段（`Part 1/2/...`）。
