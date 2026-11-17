---
name: text-stat
description: Count words, characters, lines, and estimate reading time for any text. Use when you need quick text analytics on a file or pasted content.
version: 1.0.0
---

# Text Stat

A lightweight text statistics tool for word count, character count, line count, and estimated reading time.

## Usage

Run the bundled script on any text file:

```bash
bash scripts/text-stat.sh /path/to/file.txt
```

Or pipe text in:

```bash
echo "hello world" | bash scripts/text-stat.sh
```

## Output

```
Lines:       42
Words:       318
Characters:  2,047
Reading time (200 wpm): 1m 35s
```
