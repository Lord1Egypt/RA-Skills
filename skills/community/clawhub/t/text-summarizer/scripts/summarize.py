#!/usr/bin/env python3
"""
Extractive Text Summarizer — TextRank + TF-IDF hybrid algorithm.

Usage:
    summarize.py <input_file> [--length {short|medium|long}] [--format {bullet|paragraph}]
    summarize.py --text "<text>" [--length {short|medium|long}] [--format {bullet|paragraph}]

Output formats:
    bullet      — One sentence per line (default)
    paragraph   — Single flowing paragraph

Length presets:
    short    — 20% of original sentences
    medium   — 30% of original sentences
    long     — 50% of original sentences
"""

import sys
import argparse
import re
import math
from collections import Counter


def tokenize(text):
    """Split text into lowercase words, stripping punctuation."""
    return re.findall(r"[a-zA-Z]+", text.lower())


def build_word_freq(sentences):
    """Build word frequency dictionary from sentences."""
    freq = Counter()
    for sent in sentences:
        words = tokenize(sent)
        freq.update(words)
    # Normalize by max frequency
    if freq:
        max_freq = max(freq.values())
        for word in freq:
            freq[word] /= max_freq
    return freq


def score_sentences(sentences, freq):
    """Score each sentence using TF-IDF-like weighting."""
    scores = {}
    for i, sent in enumerate(sentences):
        words = tokenize(sent)
        score = sum(freq.get(w, 0) for w in words)
        # Bonus for sentences near the beginning (news/document convention)
        position_weight = 1.0 / (i + 1)
        scores[i] = score * (1 + 0.1 * position_weight)
    return scores


def textrank_sentences(sentences, damping=0.85, iterations=30):
    """
    TextRank algorithm for sentence importance.
    Sentences are nodes; edges weighted by word overlap (Jaccard similarity).
    """
    n = len(sentences)
    if n == 0:
        return {}
    if n == 1:
        return {0: 1.0}

    # Tokenize all sentences
    tokenized = [set(tokenize(s)) for s in sentences]

    # Build adjacency matrix (edge weight = Jaccard similarity)
    # Keep top-k edges per node to sparse the graph
    k = min(10, n - 1)
    adj = {}
    for i in range(n):
        similarities = []
        for j in range(n):
            if i == j:
                continue
            inter = len(tokenized[i] & tokenized[j])
            union = len(tokenized[i] | tokenized[j])
            if union > 0:
                similarities.append((j, inter / union))
        similarities.sort(key=lambda x: -x[1])
        adj[i] = similarities[:k]

    # Initialize scores
    scores = {i: 1.0 for i in range(n)}

    # TextRank iteration
    for _ in range(iterations):
        new_scores = {}
        for i in range(n):
            rank_sum = 0.0
            edges = adj[i]
            if edges:
                total_weight = sum(sim for _, sim in edges)
                for j, sim in edges:
                    out_edges = adj[j]
                    if out_edges:
                        out_weight = sum(s for _, s in out_edges)
                        if out_weight > 0:
                            rank_sum += damping * sim * scores[j] / out_weight
            new_scores[i] = 1 - damping + rank_sum
        scores = new_scores

    return scores


def summarize_text(text, length_preset="medium", output_format="bullet", min_sentences=1):
    """
    Main summarization function.

    Args:
        text: Raw input text.
        length_preset: 'short' (20%), 'medium' (30%), or 'long' (50%).
        output_format: 'bullet' (one sentence per line) or 'paragraph'.
        min_sentences: Minimum number of sentences to return.

    Returns:
        Summary string.
    """
    # Split into sentences using heuristics (periods, exclamation, question marks)
    # that are not abbreviations
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    sentences = [s.strip() for s in sentences if s.strip()]

    if len(sentences) <= 2:
        return text.strip()

    # Determine how many sentences to extract
    length_map = {"short": 0.20, "medium": 0.30, "long": 0.50}
    ratio = length_map.get(length_preset, 0.30)
    target_count = max(min_sentences, round(len(sentences) * ratio))

    # Build word frequency
    freq = build_word_freq(sentences)

    # Score with TF-IDF
    tfidf_scores = score_sentences(sentences, freq)

    # Score with TextRank
    tr_scores = textrank_sentences(sentences)

    # Normalize both score sets to [0, 1] and combine
    def normalize(scores_dict):
        vals = list(scores_dict.values())
        mn, mx = min(vals), max(vals)
        if mx == mn:
            return {k: 0.5 for k in scores_dict}
        return {k: (v - mn) / (mx - mn) for k, v in scores_dict.items()}

    norm_tfidf = normalize(tfidf_scores)
    norm_tr = normalize(tr_scores)

    # Weighted combination: 40% TF-IDF, 60% TextRank
    combined = {i: 0.4 * norm_tfidf[i] + 0.6 * norm_tr[i] for i in range(len(sentences))}

    # Pick top-N sentences, sorted by original order
    ranked = sorted(combined.items(), key=lambda x: -x[1])
    top_indices = sorted([idx for idx, _ in ranked[:target_count]])

    summary_sentences = [sentences[i] for i in top_indices]

    if output_format == "paragraph":
        return " ".join(summary_sentences)
    else:  # bullet
        return "\n".join(f"• {s}" for s in summary_sentences)


def main():
    parser = argparse.ArgumentParser(description="Extractive text summarizer")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", metavar="TEXT", help="Text to summarize directly")
    group.add_argument("input_file", nargs="?", metavar="input_file", help="File to summarize")
    parser.add_argument(
        "--length",
        choices=["short", "medium", "long"],
        default="medium",
        help="Summary length (default: medium)",
    )
    parser.add_argument(
        "--format",
        dest="format",
        choices=["bullet", "paragraph"],
        default="bullet",
        help="Output format (default: bullet)",
    )

    args = parser.parse_args()

    if args.input_file:
        try:
            text = open(args.input_file, "r", encoding="utf-8").read()
        except UnicodeDecodeError:
            # Fallback to system encoding
            text = open(args.input_file, "r", encoding="utf-8", errors="replace").read()
    else:
        text = args.text

    result = summarize_text(text, length_preset=args.length, output_format=args.format)
    print(result)


if __name__ == "__main__":
    main()
