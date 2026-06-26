---
name: word-counter
description: A comprehensive text analysis tool that counts words, characters, sentences, and paragraphs. Calculates reading time, speaking time, reading level (Flesch-Kincaid), and keyword density.
---

# Word Counter

## Overview

This skill provides comprehensive text analysis including word count, character count, sentence/paragraph count, reading/speaking time estimates, readability scoring, and keyword density analysis.

## Use Cases

 Use when users need to analyze text length, check word count for essays/blogs/social media posts, estimate reading time, assess readability, or analyze keyword frequency for SEO content.

## Capabilities

1. **Word Count** - Accurate word counting handling multiple spaces, line breaks, and special characters
2. **Character Count** - With and without spaces (useful for Twitter, meta descriptions)
3. **Sentence & Paragraph Count** - Track document structure
4. **Reading Time** - Based on 200 words/minute average
5. **Speaking Time** - Based on 130 words/minute natural pace
6. **Reading Level** - Flesch-Kincaid grade level estimation
7. **Keyword Density** - Top keywords ranked by frequency for SEO analysis

## Common Word Count Requirements

| Content Type | Word Count | Reading Time |
|--------------|------------|--------------|
| X (Twitter) post | 40-50 | < 1 min |
| Facebook post | 40-80 | < 1 min |
| LinkedIn post | 50-100 | < 1 min |
| Email subject line | 6-10 | < 1 min |
| Meta description | 25-30 | < 1 min |
| Short blog post | 300-600 | 2-3 min |
| Standard blog post | 1,000-1,500 | 5-7 min |
| Long-form article | 2,000-3,000 | 10-15 min |
| College essay | 500-5,000 | 3-25 min |

## Usage

### Basic Analysis

```python
from scripts.word_counter import analyze_text

result = analyze_text("Your text here...")
print(result)
```

### Command Line

```bash
python scripts/word_counter.py "Your text here"
# or
python scripts/word_counter.py --file path/to/file.txt
```

## Scripts

- `scripts/word_counter.py` - Main text analysis script

## References

- `references/formulas.md` - Detailed formulas for reading level and time calculations
