---
name: unifuncs-reader
description: Use UniFuncs Reader API to read web pages and documents such as PDF and Word and Excel and PPTX URL, with AI-powered content extraction. Use this skill when users need to read, crawl, or extract content from web pages or documents.
argument-hint: [URL]
allowed-tools: Bash(python*:*)
---

# UniFuncs Reader Skill

Read web pages url and documents (PDF, Word, Excel, and PPTX) url with AI-powered extraction.

## First-Time Setup

1. Go to <https://unifuncs.com/account> to get your API key.
2. Set the environment variable: `export UNIFUNCS_API_KEY="sk-your-api-key"`

## When to Use

You have a web page or document URL and need to extract readable content from it.

## Usage

```bash
python3 read.py "https://example.com"
```

## Options

```text
usage: read.py [-h] [--format {markdown,md,text,txt}] [--no-images]
               [--only-css-selectors ONLY_CSS_SELECTORS [ONLY_CSS_SELECTORS ...]]
               [--wait-for-css-selectors WAIT_FOR_CSS_SELECTORS [WAIT_FOR_CSS_SELECTORS ...]]
               [--exclude-css-selectors EXCLUDE_CSS_SELECTORS [EXCLUDE_CSS_SELECTORS ...]]
               [--link-summary] [--ignore-cache]
               [--set-cookie SET_COOKIE] [--max-words MAX_WORDS]
               [--read-timeout READ_TIMEOUT] [--topic TOPIC]
               [--preserve-source] [--extract-timeout EXTRACT_TIMEOUT]
               url

UniFuncs Web Reader API client

positional arguments:
  url                   Target URL to read.

options:
  -h, --help            show this help message and exit
  --format {markdown,md,text,txt}
                        Output format (default: md).
  --no-images           Exclude images from output.
  --only-css-selectors ONLY_CSS_SELECTORS [ONLY_CSS_SELECTORS ...]
                        Only include elements matching CSS selectors
                        (e.g. ".article_content").
  --wait-for-css-selectors WAIT_FOR_CSS_SELECTORS [WAIT_FOR_CSS_SELECTORS ...]
                        Wait until these CSS selectors appear before
                        parsing (e.g. "#main" ".content").
  --exclude-css-selectors EXCLUDE_CSS_SELECTORS [EXCLUDE_CSS_SELECTORS ...]
                        Exclude elements matching CSS selectors (e.g.
                        "#footer" ".copyright").
  --link-summary        Append all page links to the end of content.
  --ignore-cache        Ignore cache and fetch fresh content.
  --set-cookie SET_COOKIE
                        Set Cookie header value for pages requiring
                        authentication.
  --max-words MAX_WORDS
                        Maximum character count to read, range 0-1000000
                        (default: 1000000).
  --read-timeout READ_TIMEOUT
                        Read timeout in milliseconds (default: 180000).
  --topic TOPIC         Extract topic-focused content using an LLM.
  --preserve-source     Attach source references to each extracted
                        paragraph.
  --extract-timeout EXTRACT_TIMEOUT
                        Topic extraction timeout in milliseconds
                        (default: 180000).

Examples:
  read.py "https://mp.weixin.qq.com/s/wmoNh44A4ofkawPNVx_g6A" --format md
```
