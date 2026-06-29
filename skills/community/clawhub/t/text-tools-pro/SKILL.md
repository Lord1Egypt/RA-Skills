---
name: text-tools-pro
description: Text processing toolkit - format, clean, convert, analyze text. Includes markdown formatting, text cleaning, word count, case conversion, find/replace, text comparison, and more. Use when users need to process, format, clean, or analyze text content.
---

# Text Tools Pro

A comprehensive text processing toolkit for everyday text manipulation tasks.

## Features

- **Text Cleaning**: Remove extra spaces, fix line breaks, normalize encoding
- **Format Conversion**: Markdown ↔ HTML, Case conversion (upper/lower/title)
- **Text Analysis**: Word count, character count, reading time estimate
- **Find & Replace**: Batch text replacement with regex support
- **Text Comparison**: Diff two texts and highlight differences
- **Line Operations**: Sort lines, remove duplicates, reverse order
- **Text Extraction**: Extract URLs, emails, phone numbers from text

## Quick Start

### Clean Text
```bash
text-tools clean --input file.txt --output clean.txt
```

### Convert Case
```bash
text-tools case --input file.txt --to upper  # upper, lower, title, sentence
```

### Count Words
```bash
text-tools count --input file.txt
```

### Find & Replace
```bash
text-tools replace --input file.txt --find "old" --replace "new" --output result.txt
```

### Compare Texts
```bash
text-tools diff --file1 a.txt --file2 b.txt --output diff.html
```

### Extract Data
```bash
text-tools extract --input file.txt --type urls    # urls, emails, phones
```

## Scripts

All functionality available in `scripts/`:
- `text_clean.py` - Text cleaning and normalization
- `text_convert.py` - Format and case conversion
- `text_analyze.py` - Text analysis and statistics
- `text_replace.py` - Find and replace operations
- `text_diff.py` - Text comparison
- `text_extract.py` - Data extraction from text
