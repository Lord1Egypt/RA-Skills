---
name: rxtool
description: Test, extract, replace, split, and explain regular expressions. Use when asked to test a regex pattern, extract matches from text, do regex replacements, split text by pattern, or understand what a regex does. Supports named groups, case-insensitive/multiline/dotall flags, and JSON output. Works with stdin pipes or inline text. Zero dependencies.
---

# rxtool 🔤

Regex Swiss army knife — test, extract, replace, split, explain.

## Commands

```bash
# Test a pattern against text
python3 scripts/rxtool.py test '(\d+)-(\d+)' "order-123-456"

# Extract all matches
python3 scripts/rxtool.py extract '\b\w+@\w+\.\w+\b' "email me at user@example.com"

# Extract with JSON output
echo "text" | python3 scripts/rxtool.py extract '\w+' --json

# Replace matches
python3 scripts/rxtool.py replace '\d+' 'NUM' "got 42 items and 7 boxes"

# Split by pattern
python3 scripts/rxtool.py split '[,;\s]+' "a, b; c d"

# Explain a regex
python3 scripts/rxtool.py explain '(?P<year>\d{4})-(?P<month>\d{2})'
```

## Features
- Group capture (numbered and named)
- Case-insensitive (-i), multiline (-m), dotall (-s) flags
- Stdin pipe support
- JSON output for extraction
- Regex explanation with component breakdown
