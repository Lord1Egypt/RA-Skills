# Extractive Summarization Algorithm Reference

## Overview

This skill uses **extractive summarization** — it selects and extracts the most important sentences directly from the original text. Unlike abstractive methods, extractive summarization never invents new words or rephrases ideas, so it has **zero hallucination risk**.

## Algorithm: Hybrid TextRank + TF-IDF

The summarizer combines two well-established NLP algorithms:

### 1. TF-IDF Scoring

**TF-IDF** (Term Frequency – Inverse Document Frequency) measures how important a word is within a document.

- **TF** (Term Frequency): How often a word appears in the document, normalized by the maximum word frequency.
- **IDF** (Inverse Document Frequency): In single-document mode (as here), we treat each sentence as a mini-document. Words that appear in many sentences are penalized.

**Sentence score** = sum of TF-IDF weights for all words in the sentence.

Words unique to a sentence → high score. Common words (the, is, and) → low score.

### 2. TextRank Graph Ranking

TextRank is inspired by Google's PageRank. It treats each sentence as a node in a graph:

1. **Edge weight** between sentence *i* and *j* = Jaccard similarity of their word sets
   `Jaccard(A, B) = |A ∩ B| / |A ∪ B|`
2. For each node, keep only the top-K (≤10) most similar neighbors to sparse the graph.
3. Run PageRank-style iterations (damping factor = 0.85, 30 iterations) to assign each sentence a global importance score.

Sentences that are similar to many other important sentences get ranked highest.

### 3. Hybrid Combination

Final score = `0.4 × normalized_TF-IDF + 0.6 × normalized_TextRank`

The 60/40 weighting toward TextRank reflects TextRank's ability to capture contextual importance and sentence relationships, while TF-IDF provides a complementary signal about term specificity.

## Why These Algorithms Work

| Property | TF-IDF | TextRank |
|---|---|---|
| Captures term specificity | ✅ | ❌ |
| Captures sentence relationships | ❌ | ✅ |
| Handles long documents | ✅ | ✅ |
| Deterministic | ✅ | ✅ |
| Zero hallucination | ✅ | ✅ |

## Length Presets

| Preset | Ratio | Use Case |
|---|---|---|
| short | 20% | Quick overview, headlines |
| medium | 30% | General-purpose default |
| long | 50% | Detailed summaries, when more coverage is needed |

## Limitations

- **Single-document only**: This implementation treats the input as one document. Cross-document summarization (e.g., multi-article) is not supported.
- **Language**: Optimized for English. Multilingual support (Chinese, etc.) requires a different tokenization strategy.
- **Code/structured content**: Not designed for code, tables, or structured data. Treats everything as prose.
- **Very short inputs**: Returns original text if ≤ 2 sentences are detected.
