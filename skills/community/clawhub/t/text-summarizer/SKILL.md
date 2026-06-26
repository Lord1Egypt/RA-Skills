---
name: text-summarizer
description: Extractive AI text summarizer. Automatically extracts the most important sentences from any text using a hybrid TextRank + TF-IDF algorithm.
---

# Text Summarizer

Condenses long text into a concise summary by extracting the most important sentences. Works on articles, research papers, reports, meeting notes, emails, and any long document. Zero hallucination risk since it extracts exact sentences from the original.

## Use Cases

the user pastes text or a file and asks to summarize, shorten, condense, or extract key points; the user wants to turn a long article/paper/report/notes into a brief overview; the user says 'summarize this', 'TL;DR', 'key points', 'condense', 'extract main ideas'. Supports adjustable length (short 20% / medium 30% / long 50%) and two output formats (bullet points or flowing paragraph).

## Quick Start

**Default (bullet points, medium length):**
```
summarize.py --text "<paste your text here>"
```

**Paragraph format:**
```
summarize.py --text "<text>" --format paragraph
```

**Short summary (20% of original):**
```
summarize.py --text "<text>" --length short
```

**From a file:**
```
summarize.py input.txt
summarize.py input.txt --length long --format paragraph
```

## Algorithm

See [references/algorithms.md](references/algorithms.md) for full details on the hybrid TextRank + TF-IDF approach.

**TL;DR**: The script scores every sentence by (1) TF-IDF term importance and (2) TextRank graph-based importance, then returns the top-ranked sentences. No AI generation — exact sentences from the original are extracted, so there is zero hallucination risk.

## Length Presets

| Flag | Ratio | Best for |
|---|---|---|
| `--length short` | 20% | Headlines, quick scan |
| `--length medium` | 30% | General-purpose (default) |
| `--length long` | 50% | Detailed summaries |

## Output Formats

- **`bullet`** (default): One extracted sentence per line, prefixed with `•`
- **`paragraph`**: A single flowing paragraph of extracted sentences

## What to Summarize

- Articles and blog posts
- Research papers and academic abstracts
- Reports and white papers
- Meeting notes and transcripts
- Long email threads
- Any prose document

## Limitations

- Optimized for English prose. Code, tables, and structured data are treated as plain text.
- Returns original text unchanged if the input has 2 or fewer sentences.
- Single-document only (one article at a time).
