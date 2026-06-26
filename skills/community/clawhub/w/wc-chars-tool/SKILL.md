---
name: wc-chars-tool
description: Count characters in text input — total, non-whitespace, CJK, and Unicode-aware character counts. Useful for text analysis, content length limits, and i18n validation.
---

# WC Chars Tool — Character Counting Utility

Count characters in text with Unicode awareness. Supports total characters, non-whitespace characters, CJK character detection, and byte-offset reporting. Essential for validating text constraints (SMS, tweets, form fields, database column limits).

## Quick Start

```bash
# Count characters in a string
wc-chars-tool "Hello, 世界!"

# Count from stdin
echo "Hello World" | wc-chars-tool

# Count characters in a file
wc-chars-tool --file document.txt
```

## Usage

```bash
wc-chars-tool [TEXT] [OPTIONS]
wc-chars-tool --file FILE [OPTIONS]

Options:
  --file FILE       Read from file instead of argument
  --bytes           Count bytes instead of characters
  --no-whitespace   Exclude whitespace from count
  --cjk-only        Count only CJK characters
  --graphemes       Count grapheme clusters (user-perceived characters)
  --json            Output as structured JSON
  --detailed        Show breakdown: total, non-ws, digits, punct, spaces
```

## Examples

```bash
# Count total characters
wc-chars-tool "Hello World"

# Count bytes in a UTF-8 string
wc-chars-tool "Hello, 世界!" --bytes

# Count non-whitespace characters
wc-chars-tool "Hello World" --no-whitespace

# Count CJK characters only
wc-chars-tool "Hello 你好 世界 world" --cjk-only

# Detailed breakdown
wc-chars-tool "Hello, 世界! 123" --detailed --json
```

## Features

- **Unicode-aware** — correctly handles multi-byte characters (CJK, emoji, accents)
- **Grapheme clusters** — counts user-perceived characters, not just code points
- **Multiple modes** — total, non-whitespace, CJK, byte count
- **Detailed breakdown** — digits, punctuation, spaces, letters
- **File and stdin input** — flexible input sources
- **JSON output** — for monitoring and script integration
