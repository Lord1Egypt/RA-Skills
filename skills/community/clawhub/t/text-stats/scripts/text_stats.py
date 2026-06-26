#!/usr/bin/env python3
"""Text statistics analyzer: word count, readability, keyword density."""

import argparse
import re
import sys
from collections import Counter


def load_text(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def count_syllables(word):
    """Rough English syllable count."""
    word = word.lower().rstrip("e")
    vowels = re.findall(r'[aeiouy]+', word)
    return max(1, len(vowels))


def is_cjk(char):
    """Check if character is CJK."""
    cp = ord(char)
    return (0x4E00 <= cp <= 0x9FFF or 0x3400 <= cp <= 0x4DBF or
            0xF900 <= cp <= 0xFAFF or 0x20000 <= cp <= 0x2A6DF)


def tokenize(text):
    """Split text into words, treating CJK characters as individual words."""
    words = []
    for token in re.findall(r"[a-zA-Z']+|[\u4e00-\u9fff\u3400-\u4dbf]", text):
        words.append(token)
    return words


def sentences(text):
    """Split text into sentences."""
    # Handle common abbreviations
    text = re.sub(r'\b(Mr|Mrs|Ms|Dr|Jr|Sr|vs|etc|i\.e|e\.g)\.',
                  lambda m: m.group().replace('.', '<DOT>'), text)
    sents = re.split(r'[.!?。！？]+', text)
    return [s.strip() for s in sents if s.strip() and len(s.strip()) > 5]


def paragraphs(text):
    return [p.strip() for p in text.split("\n\n") if p.strip()]


def cmd_analyze(args):
    text = load_text(args.file)
    words = tokenize(text)
    sents = sentences(text)
    paras = paragraphs(text)

    n_words = len(words)
    n_chars = len(text)
    n_chars_nospace = len(text.replace(" ", "").replace("\n", ""))
    n_sents = max(1, len(sents))
    n_paras = len(paras)
    avg_wps = n_words / n_sents

    # Reading time
    wpm = 250
    read_min = max(1, round(n_words / wpm))

    print(f"📊 Text Analysis: {args.file}")
    print("━" * 30)
    print(f"Words:          {n_words:,}")
    print(f"Characters:     {n_chars:,} ({n_chars_nospace:,} excl. spaces)")
    print(f"Sentences:      {n_sents:,}")
    print(f"Paragraphs:     {n_paras:,}")
    print(f"Avg words/sent: {avg_wps:.1f}")
    print(f"Reading time:   ~{read_min} min (at {wpm} wpm)")

    # Readability (English-focused)
    english_words = [w for w in words if re.match(r'^[a-zA-Z]+$', w)]
    if len(english_words) > 30:
        total_syllables = sum(count_syllables(w) for w in english_words)
        n_ew = len(english_words)
        avg_syl = total_syllables / n_ew

        # Flesch Reading Ease
        fre = 206.835 - 1.015 * avg_wps - 84.6 * avg_syl
        fre = max(0, min(100, fre))

        # Flesch-Kincaid Grade
        fkg = 0.39 * avg_wps + 11.8 * avg_syl - 15.59

        # Gunning Fog
        complex_words = sum(1 for w in english_words if count_syllables(w) >= 3)
        fog = 0.4 * (avg_wps + 100 * complex_words / n_ew)

        # FRE description
        if fre >= 90: desc = "Very Easy"
        elif fre >= 80: desc = "Easy"
        elif fre >= 70: desc = "Fairly Easy"
        elif fre >= 60: desc = "Standard"
        elif fre >= 50: desc = "Fairly Difficult"
        elif fre >= 30: desc = "Difficult"
        else: desc = "Very Difficult"

        print(f"\nReadability:")
        print(f"  Flesch-Kincaid Grade: {fkg:.1f} (grade {max(1, round(fkg))})")
        print(f"  Flesch Reading Ease:  {fre:.1f} ({desc})")
        print(f"  Gunning Fog Index:    {fog:.1f}")

    # CJK stats
    cjk_chars = sum(1 for ch in text if is_cjk(ch))
    if cjk_chars > 0:
        print(f"\nCJK Characters: {cjk_chars:,}")


def cmd_wc(args):
    text = load_text(args.file)
    words = tokenize(text)
    lines = text.count("\n") + 1
    print(f"{lines}\t{len(words)}\t{len(text)}\t{args.file}")


def cmd_keywords(args):
    text = load_text(args.file)
    words = tokenize(text)
    # Filter stop words
    stop = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
            "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
            "being", "have", "has", "had", "do", "does", "did", "will", "would",
            "could", "should", "may", "might", "shall", "can", "not", "no", "nor",
            "this", "that", "these", "those", "it", "its", "as", "if", "then",
            "than", "so", "up", "out", "about", "into", "over", "after"}
    filtered = [w.lower() for w in words if w.lower() not in stop and len(w) > 1]
    counter = Counter(filtered)
    n_total = len(filtered)

    print(f"Top {args.top} Keywords ({n_total} total words after filtering):")
    for word, count in counter.most_common(args.top):
        pct = count / n_total * 100
        print(f"  {word} ({count}x, {pct:.2f}%)")


def cmd_time(args):
    text = load_text(args.file)
    words = tokenize(text)
    read_min = max(1, round(len(words) / 250))
    print(f"~{read_min} min read ({len(words):,} words at 250 wpm)")


def main():
    parser = argparse.ArgumentParser(description="Text Stats")
    sub = parser.add_subparsers(dest="command")

    p = sub.add_parser("analyze"); p.add_argument("file")
    p = sub.add_parser("wc"); p.add_argument("file")
    p = sub.add_parser("keywords"); p.add_argument("file"); p.add_argument("--top", type=int, default=15)
    p = sub.add_parser("time"); p.add_argument("file")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    cmds = {"analyze": cmd_analyze, "wc": cmd_wc, "keywords": cmd_keywords, "time": cmd_time}
    cmds[args.command](args)


if __name__ == "__main__":
    main()
