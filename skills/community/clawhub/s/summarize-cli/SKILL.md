---
name: summarize-cli
description: Summarize URLs or files with the summarize CLI (web, PDFs, images, audio, YouTube).
homepage: https://summarize.sh
metadata: {"clawdbot":{"emoji":"🧾","requires":{"bins":["summarize"]},"install":[{"id":"brew","kind":"brew","formula":"steipete/tap/summarize","bins":["summarize"],"label":"Install summarize (brew)"}]}}

# Summarize

Summarize URLs or files with the summarize CLI.

## Usage

Summarize a URL:
```bash
summarize https://example.com/article
```

Summarize a file:
```bash
summarize path/to/file.pdf
```

## Supported formats

- URLs (web pages)
- PDFs
- Images (with text content)
- Audio files
- YouTube videos

## Options

- `--length <short|medium|long>` - Control summary length
- `--format <text|markdown|json>` - Output format
- `--output <file>` - Save to file

## Examples

Quick summary:
```bash
summarize https://example.com --length short
```

Markdown output:
```bash
summarize document.pdf --format markdown --output summary.md
```

JSON output:
```bash
summarize https://example.com --format json | jq
```
