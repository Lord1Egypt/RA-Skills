---
name: tra-extract-text
description: Extract text content from web pages using trafilatura CLI. Use when user wants to extract readable text, markdown, or raw HTML from a URL. Triggers on requests like: "extract text from URL", "scrape web page content", "get article text", "convert web page to markdown", "trafilatura".
---

# tra-extract-text

Extract text from web pages using the `trafilatura` command-line tool.

## Installation

```bash
pip install trafilatura
```

## Usage

### Basic text extraction (Markdown)

```bash
trafilatura -u URL --markdown
```

### Extract raw text (no formatting)

```bash
trafilatura -u URL --text
```

### Output to file

```bash
trafilatura -u URL --markdown > output.md
trafilatura -u URL --text > output.txt
```

### CLI Options

| Option | Description |
|--------|-------------|
| `-u, --url` | Target URL (required) |
| `--markdown` | Output as Markdown (default) |
| `--text` | Output as plain text |
| `--html` | Output as HTML |
| `--json` | Output as JSON |
| `--xml` | Output as XML |
| `-o, --output` | Write to file instead of stdout |
| `--with-metadata` | Include metadata (title, author, date) |
| `--license` | Show license info |

## Examples

Extract a Medium article to markdown:
```bash
trafilatura -u "https://medium.com/example/article" --markdown
```

Extract and save:
```bash
trafilatura -u "https://news.example.com/article" --markdown -o article.md
```

Extract with metadata:
```bash
trafilatura -u "https://example.com/post" --markdown --with-metadata
```
