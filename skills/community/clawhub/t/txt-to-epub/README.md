# txt-to-epub

A lightweight, rule-based converter from `.txt` to `.epub`, designed for novels, tutorials, and other long-form text.

[简体中文 README](README.zh.md)

## Features

- Rule-based chapter splitting (no built-in model API dependency)
- Automatic text encoding detection (UTF-8/GBK/Big5/UTF-16, etc.)
- Multiple heading patterns for novels and tutorials
- Length-based fallback splitting when no headings are found
- Standard EPUB output with navigable TOC

## Project Structure

```text
txt-to-epub/
  SKILL.md
  requirements.txt
  scripts/
    txt_to_epub.py
```

## Installation

```bash
python3 -m pip install -r requirements.txt
```

## Quick Start

Run in the `txt-to-epub` directory:

```bash
python3 scripts/txt_to_epub.py --input /path/to/book.txt
```

By default, the output EPUB is created next to the input TXT file with the same base name.

## Common Commands

Novel mode (recommended, keep full chapter titles):

```bash
python3 scripts/txt_to_epub.py \
  --input /path/to/novel.txt \
  --split-mode novel \
  --title-style full \
  --verbose
```

Tutorial mode:

```bash
python3 scripts/txt_to_epub.py \
  --input /path/to/tutorial.txt \
  --split-mode tutorial \
  --title-style full
```

Force length-based splitting:

```bash
python3 scripts/txt_to_epub.py \
  --input /path/to/long_text.txt \
  --split-mode length \
  --chunk-chars 8000
```

## Arguments

- `--input`: Input TXT path (required)
- `--output`: Output EPUB path (optional)
- `--title`: Book title (optional; defaults to file name)
- `--author`: Author (optional)
- `--language`: Language (default: `zh-CN`)
- `--split-mode`: `auto | novel | tutorial | length`
- `--title-style`: `full | clean` (default: `full`)
  - `full`: Keep full headings, such as `第一章 旧土`
  - `clean`: Remove numbering prefixes and keep only heading text
- `--min-chapter-chars`: Merge threshold for very short chapters (default: `300`)
- `--chunk-chars`: Chunk size for length mode (default: `8000`)
- `--verbose`: Print extra logs

## Heading Patterns (Summary)

- Chinese novel: `第一章 ...`, `第十回 ...`
- English headings: `Chapter 1 ...`, `Part 2 ...`
- Numbered tutorial headings: `1.2 ...`, `2.3.4 ...`
- Chinese list-style headings: `一、...`

If no valid chapter headings are detected, the tool falls back to length-based sections (`Part 1/2/...`).
