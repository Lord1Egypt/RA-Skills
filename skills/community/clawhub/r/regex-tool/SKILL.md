---
name: regex-tool
description: Match and extract text patterns using regular expressions. Use for data validation, text parsing, and pattern-based extraction tasks.
---
# Regex - Regular Expression Matcher

Search text using regular expressions to find, extract, and replace patterns. Supports standard regex syntax with capturing groups, alternation, and quantifiers for advanced text processing.

## Usage
```bash
regex-tool [options] <pattern> <file>
```

## Options

- `-i`: Case-insensitive matching
- `-o`: Show only matched text
- `-r REPLACE`: Replace matches with text
- `-g`: Global match (all occurrences)

## Examples

```bash
regex-tool "\d{4}-\d{2}-\d{2}" dates.txt
regex-tool -i "error|warning" log.txt
regex-tool -r "[REDACTED]" "\b\d{3}-\d{2}-\d{4}\b" data.txt
```