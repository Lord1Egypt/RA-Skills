---
name: wc-words-tool
description: Count words in text — total, unique, per-line, with frequency analysis. Useful for readability metrics, content analysis, translation estimation, and document summarization.
---

# WC Words Tool — Word Counting & Text Analysis Utility

Count words with smart tokenization, language-aware word splitting, frequency distribution, and readability metrics. Ideal for content pipelines, writing analytics, and SEO keyword density checks.

## Quick Start

```bash
# Count words in a string
wc-words-tool "The quick brown fox jumps over the lazy dog"

# Count words from stdin
cat article.txt | wc-words-tool

# Count words in a file
wc-words-tool --file document.txt
```

## Usage

```bash
wc-words-tool [TEXT] [OPTIONS]
wc-words-tool --file FILE [OPTIONS]

Options:
  --file FILE         Read from file instead of argument
  --unique            Count unique words
  --freq N            Show top N most frequent words
  --min-length N      Minimum word length to count
  --stopwords FILE    Remove common stopwords from count
  --per-line          Words per line (useful for code comments)
  --json              Output as structured JSON
```

## Examples

```bash
# Total word count
wc-words-tool --file report.txt

# Unique word count
wc-words-tool --file article.txt --unique

# Top 10 most frequent words
wc-words-tool --file document.txt --freq 10

# Filter short words (min 4 characters)
wc-words-tool --file text.txt --min-length 4

# Words per line
wc-words-tool --file poem.txt --per-line

# With custom stopwords list
wc-words-tool --file content.txt --stopwords stopwords.txt --json
```

## Features

- **Total word count** — standard word tokenization
- **Unique words** — vocabulary size estimation
- **Frequency analysis** — most common words with counts
- **Stopword filtering** — remove common words for meaningful analysis
- **Smart tokenization** — handles punctuation, hyphens, apostrophes
- **Min-length filter** — exclude short/noise words
- **JSON output** — for pipeline integration
- **Multiple input modes** — argument, file, stdin
