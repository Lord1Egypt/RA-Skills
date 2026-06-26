---
name: indexion-segment
description: Split text into contextual chunks for RAG/embedding pipelines. Document segmentation and section extraction using window, tfidf, punctuation, or hybrid strategies chosen by intent.
---

# indexion segment

Split text into contextual segments using divergence-based, TF-IDF, or punctuation strategies.

## When to Use

- User needs to chunk text for RAG or embedding pipelines
- User wants to split a document into meaningful sections
- User asks to segment text for processing
- Preparing text for similarity analysis at sub-document level

## Usage

```bash
# Default window divergence strategy
indexion segment <input-file> <output-dir>

# TF-IDF based segmentation
indexion segment --strategy=tfidf <input-file> <output-dir>

# Punctuation-based segmentation
indexion segment --strategy=punctuation <input-file> <output-dir>

# Custom segment sizes
indexion segment --min-size=200 --max-size=3000 --target-size=800 document.txt output/

# Custom divergence threshold
indexion segment --threshold=0.5 document.txt output/

# Adaptive threshold mode (default)
indexion segment --adaptive document.txt output/

# Hybrid NCD+TF-IDF mode
indexion segment --hybrid --ncd-weight=0.6 --tfidf-weight=0.4 document.txt output/

# Custom window size
indexion segment --window-size=5 document.txt output/

# Custom output prefix
indexion segment --prefix=chunk document.txt output/
```

## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--strategy=NAME` | window | Strategy: window, tfidf, punctuation |
| `--min-size=INT` | 100 | Minimum segment characters |
| `--max-size=INT` | 2000 | Maximum segment characters |
| `--target-size=INT` | 500 | Target segment characters |
| `--threshold=FLOAT` | 0.42 | Divergence threshold |
| `--window-size=INT` | 3 | Window size |
| `--adaptive` | true | Adaptive threshold mode |
| `--hybrid` | false | NCD+TF-IDF hybrid mode |
| `--ncd-weight=FLOAT` | 0.5 | NCD weight in hybrid mode |
| `--tfidf-weight=FLOAT` | 0.5 | TF-IDF weight in hybrid mode |
| `--prefix=NAME` | segment | Output file prefix |

## Strategies

| Strategy | Description |
|----------|-------------|
| `window` (default) | Sliding window divergence detection |
| `tfidf` | TF-IDF based topic change detection |
| `punctuation` | Punctuation/sentence boundary based |

## Workflow

1. Run `indexion segment <input-file> <output-dir>` to split text with defaults
2. Adjust `--threshold` and `--target-size` to tune segmentation granularity
3. Use `--hybrid` mode for better accuracy on mixed-content documents
