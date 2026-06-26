---
name: text-stats
description: Analyze text documents for word count, reading time, readability scores (Flesch-Kincaid, Gunning Fog), keyword density, and sentence statistics. Supports multiple languages including CJK. Zero dependencies.
author: zacjiang
version: 1.0.0
tags: text, analysis, readability, word count, statistics, seo, content, writing
---

# Text Stats

Analyze any text document for readability, word count, keyword density, and more. Perfect for content optimization, SEO analysis, or writing improvement.

## Usage

### Full analysis
```bash
python3 {baseDir}/scripts/text_stats.py analyze document.txt
python3 {baseDir}/scripts/text_stats.py analyze document.md
```

### Word count only
```bash
python3 {baseDir}/scripts/text_stats.py wc document.txt
```

### Keyword density
```bash
python3 {baseDir}/scripts/text_stats.py keywords document.txt --top 20
```

### Reading time
```bash
python3 {baseDir}/scripts/text_stats.py time document.txt
```

## Output Example

```
📊 Text Analysis: article.md
━━━━━━━━━━━━━━━━━━━━━━━━━━
Words:          2,847
Characters:     16,203
Sentences:      142
Paragraphs:     38
Avg words/sent: 20.0
Reading time:   ~11 min (at 250 wpm)

Readability:
  Flesch-Kincaid Grade: 8.2 (8th grade)
  Flesch Reading Ease:  62.1 (Standard)
  Gunning Fog Index:    10.4

Top Keywords:
  AI (47x, 1.65%)
  agent (31x, 1.09%)
  data (28x, 0.98%)
```

## Features

- 📏 Word, character, sentence, paragraph counts
- ⏱️ Estimated reading time
- 📖 Readability scores (Flesch-Kincaid, Gunning Fog, Flesch Reading Ease)
- 🔑 Keyword frequency and density
- 🇨🇳 CJK character counting (Chinese characters = words)
- 🪶 Zero dependencies — Python stdlib only

## Dependencies

None! Uses only Python standard library.
