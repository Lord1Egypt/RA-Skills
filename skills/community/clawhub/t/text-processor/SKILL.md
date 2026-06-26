---
name: text-processor
description: Batch Chinese text processing — clean, normalize, translate, extract keywords, and format text for content production.
---

# Text Processor

A batch text processing utility for content workflows. Handles Chinese text normalization, cleaning, formatting, and structured extraction. Designed for content creators, editors, and automation pipelines.

## Features

- **Text cleaning**: Remove extra whitespace, fix punctuation, normalize quotes
- **Chinese normalization**: Convert full-width/half-width, simplify/traditional
- **Batch processing**: Process multiple text items in one call
- **Format conversion**: Markdown ↔ plain text, numbered lists, tables
- **Keyword extraction**: Extract key terms and phrases from Chinese text

## Usage

```js
const processor = require('./skills/text-processor');

// Clean and normalize
const cleaned = processor.clean("  Hello，世界！  This has ”bad” quotes.  ");
// → "Hello，世界！This has "bad" quotes."

// Extract keywords from Chinese text
const keywords = processor.extractKeywords("今天天气很好，适合出去郊游");
// → ["天气", "郊游", ...]

// Batch process
const results = processor.batch([
  "  文本1  ",
  "  文本2  "
], 'clean');
// → ["文本1", "文本2"]
```

## API

### `clean(text)`
Normalize and clean Chinese/English mixed text:
- Trim whitespace
- Collapse multiple spaces
- Normalize quotes («»「」"" → standard "")
- Normalize full-width/half-width punctuation

### `extractKeywords(text, maxCount?)`
Extract meaningful keywords from Chinese text using TF heuristics.

### `batch(items, operation, options?)`
Process an array of texts with the same operation.

## License

MIT
