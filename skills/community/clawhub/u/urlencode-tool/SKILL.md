---
name: urlencode-tool
description: URL-encode or decode text for safe transmission in URLs and query strings, with support for form data, partial encoding, and batch file processing.
---

# URL Encode/Decode Tool — Percent-Encoding Utility

Encode and decode URL components per RFC 3986. Handles query strings, path segments, form bodies (application/x-www-form-urlencoded), and partial encoding where only unsafe characters are escaped.

## Quick Start

```bash
# Encode a string for URL use
urlencode-tool --encode "hello world & more"

# Decode a percent-encoded string
urlencode-tool --decode "hello%20world%20%26%20more"

# Encode a full query string
urlencode-tool --encode "name=Alice & age=30" --query
```

## Usage

```bash
urlencode-tool [COMMAND] [TEXT] [OPTIONS]

Commands:
  --encode TEXT   Percent-encode the input string
  --decode TEXT   Decode percent-encoded input

Options:
  --query         Encode as form query (spaces → +)
  --path-safe     Only encode unsafe chars for path segment
  --component     Encode entire URI component (default, full RFC 3986)
  --charset UTF-8 Character encoding (default: UTF-8)
  --batch FILE    Encode/decode lines from a file
  --json          Output as JSON
```

## Examples

```bash
# Basic encoding
urlencode-tool --encode "user input with spaces & symbols"

# Decode back
urlencode-tool --decode "user%20input%20with%20spaces%20%26%20symbols"

# Form-encoded query string (spaces as +)
urlencode-tool --encode "name=Alice Smith&city=New York" --query

# Path-segment safe (preserves /)
urlencode-tool --encode "dir/sub dir/file name.txt" --path-safe

# Batch process a file of URLs
urlencode-tool --encode --batch urls.txt --json
```

## Features

- **Encode & decode** full RFC 3986 percent-encoding
- **3 encoding modes:** component, query (form), path-safe
- **UTF-8 encoding** standard (configurable charset)
- **Batch processing** from file input
- **JSON output** for script pipelines
- **Round-trip safety:** decode(encode(x)) === x for valid Unicode
- **Unicode safe:** handles CJK, emoji, and multi-byte characters
