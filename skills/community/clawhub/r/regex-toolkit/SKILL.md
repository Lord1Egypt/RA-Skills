---
name: regex-toolkit
description: Test, match, extract, replace, explain, and validate regular expressions from the command line. Includes a library of 25+ common patterns (email, URL, IP, phone, date, UUID, etc.) that can be used by name. Use when the user needs to build, debug, or test regex patterns, extract data with regex, do search-and-replace with backreferences, or understand what a regex does. Zero external dependencies.
---

# Regex Toolkit

Test, find, replace, explain, and validate regular expressions. Includes 25+ common named patterns. Pure Python, no dependencies.

## Quick Start

```bash
# Test a pattern
python3 scripts/regex_toolkit.py test '\d+' --text 'abc 123 def'

# Use a named pattern (email, url, ipv4, phone-us, uuid, etc.)
python3 scripts/regex_toolkit.py findall email --text 'Contact hello@example.com or support@test.org'

# Find all matches with positions
python3 scripts/regex_toolkit.py findall '\b\w{5}\b' --file input.txt

# Search and replace
python3 scripts/regex_toolkit.py replace '\bfoo\b' -r bar --text 'foo bar foo'

# Explain a regex in plain English
python3 scripts/regex_toolkit.py explain '(?P<year>\d{4})-(\d{2})-(\d{2})'

# Validate regex syntax
python3 scripts/regex_toolkit.py validate '[a-z'

# List all common patterns
python3 scripts/regex_toolkit.py patterns --list

# Pipe from stdin
echo "Call 555-1234 or 555-5678" | python3 scripts/regex_toolkit.py findall phone-us
```

## Commands

| Command | Description |
|---------|-------------|
| `test` | Check if pattern matches. Shows first match position and groups. |
| `findall` | Find all matches with positions and captured groups. `--json` for JSON output. |
| `replace` | Regex search-and-replace. Supports `\1` backreferences. `--count N` limits replacements. |
| `explain` | Break down a regex into plain-English explanation of each element. |
| `validate` | Check if a regex pattern is syntactically valid. |
| `patterns` | List built-in common patterns or show a specific one by name. |

## Input Options

All matching commands accept: `--text 'string'`, `--file path`, or piped stdin.

## Flags

| Flag | Description |
|------|-------------|
| `-i, --ignorecase` | Case-insensitive matching |
| `-m, --multiline` | `^`/`$` match line boundaries |
| `-s, --dotall` | `.` matches newline |

## Built-in Patterns

Use by name instead of writing regex: `email`, `url`, `ipv4`, `ipv6`, `phone-us`, `phone-intl`, `date-iso`, `date-us`, `time-24h`, `hex-color`, `mac-address`, `uuid`, `ssn`, `zip-us`, `credit-card`, `slug`, `semver`, `domain`, `hashtag`, `mention`, `markdown-link`, `html-tag`, `json-key`, `filepath-unix`, `filepath-win`.
