"""
Standalone RSFPH watermark detector.

Reimplements the exact detection algorithm from RspfhWtgbblModel.watermark_text_detector
(Hao et al., COLING 2025) without requiring the RSFPH-WTGBBLM project or ParaLS model.

Dependencies: spacy (en_core_web_sm), yake, scipy, nltk

Usage:
    python skills/snswatcher/detect_watermark.py <file>
    python skills/snswatcher/detect_watermark.py comments_raw.md
    python skills/snswatcher/detect_watermark.py MEMORY.md --csv results.csv
"""

import argparse
import csv
import hashlib
import re
import sys
from pathlib import Path
from string import punctuation

import spacy
import yake
from nltk.tokenize import sent_tokenize
from scipy.stats import norm


def preprocess_string(text: str) -> str:
    """Normalize text exactly as the reference detector does."""
    text = text.replace("\\ n", " ").replace("\\n", " ")
    text = text.replace("\n", " ").replace("\t", " ").replace("\r", " ")
    text = re.sub(r"( +)", " ", text)
    text = re.sub(r"( )('[(m)(d)(t)(ll)(re)(ve)(s)])", r"\2", text)
    text = text.replace("s '", "s'")
    text = re.sub(r"(\w)( )(\.)( )(\w)( )(\.)", r"\1\3\5\7", text)
    text = re.sub(r"( )([,\.!?:;)])", r"\2", text)
    text = re.sub(r"([(])( )", r"\1", text)
    text = re.sub(r"( )(')( )(\S+)( )(')", r"\2\4\6", text)
    text = re.sub(r'(\")( )(\S+)( )(\")', r"\1\3\5", text)
    text = re.sub(r"(\w+) (-+) (\w+)", r"\1\2\3", text)
    text = re.sub(r"(\w+) (/+) (\w+)", r"\1\2\3", text)
    text = text.replace("\\n", " ").replace(" ' ", "'")
    return text.strip()


def binary_encoding_function(token: str) -> int:
    hash_value = int(hashlib.sha256(token.encode("utf-8")).hexdigest(), 16)
    return hash_value % 2


ENTITY_BLACK_LIST = {"GPE", "ORG", "PERSON", "WORK_OF_ART", "EVENT"}
YAKE_POS_BLACK_LIST = {"NOUN", "PROPN"}
YAKE_KWARGS = dict(lan="en", n=1, dedupLim=0.9, dedupFunc="seqm", windowsSize=1, top=20)
KEYWORD_EXTRACT_RATE = 0.5


def extract_entity_words(doc) -> list[int]:
    return [t.i for t in doc if t.ent_type_ in ENTITY_BLACK_LIST]


def extract_yake_words(doc) -> list[int]:
    extractor = yake.KeywordExtractor(**YAKE_KWARGS)
    yake_words = {k[0] for k in extractor.extract_keywords(doc.text)}
    return [t.i for t in doc if t.text in yake_words and t.pos_ in YAKE_POS_BLACK_LIST]


def keywords_extractor(doc):
    entity_idx = extract_entity_words(doc)
    punctuation_removed = [t.text for t in doc if not t.is_punct]
    keywords_max = int(KEYWORD_EXTRACT_RATE * len(punctuation_removed))

    yake_idx = [] if len(entity_idx) > keywords_max else extract_yake_words(doc)

    return entity_idx, yake_idx


DEP_ORDERING = [
    "expl", "cc", "auxpass", "agent", "mark", "aux", "prep", "det", "prt",
    "intj", "parataxis", "predet", "case", "csubj", "acl", "advcl", "ROOT",
    "preconj", "ccomp", "relcl", "advmod", "dative", "xcomp", "pcomp",
    "nsubj", "quantmod", "conj", "nsubjpass", "punct", "poss", "dobj",
    "nmod", "attr", "csubjpass", "meta", "pobj", "amod", "npadvmod",
    "appos", "acomp",
]

CUSTOM_KEYWORDS = ["haojifei", "ciwater"]


def _contains_punctuation(token) -> bool:
    return any(p in token.text for p in punctuation)


def grammar_mask_select(doc, entity_keywords: list[str], yake_keywords: list[str]) -> list[int]:
    text_deps = [t.dep_ for t in doc]

    mask_candidates = []
    for dep in DEP_ORDERING:
        for index, token_dependency in enumerate(text_deps):
            if token_dependency == dep:
                mask_candidates.append(doc[index])

    mask_words_index = []
    mask_words_set = []
    for candidate in mask_candidates:
        if (candidate.text not in entity_keywords
                and candidate.text not in yake_keywords
                and candidate not in mask_words_set
                and not candidate.is_punct
                and candidate.pos_ != "PART"
                and not _contains_punctuation(candidate)
                and candidate.text not in CUSTOM_KEYWORDS):
            mask_words_set.append(candidate)
            mask_words_index.append(candidate.i)

    return mask_words_index


REPLACEMENT_RATE = 1.0
P = 0.5
Z_ALPHA = norm.isf(0.05)  # ~1.6449


def get_encodings(text: str, nlp):
    text = preprocess_string(text)
    sentences = sent_tokenize(text)

    encodings = []
    for sent_text in sentences:
        doc = nlp(sent_text)

        entity_idx, yake_idx = keywords_extractor(doc)
        entity_kw = [doc[i].text for i in entity_idx]
        yake_kw = [doc[i].text for i in yake_idx]

        mask_words_index = grammar_mask_select(doc, entity_kw, yake_kw)

        if REPLACEMENT_RATE < 5:
            len_keyword = len(entity_idx) + len(yake_idx)
            num_mask = int(REPLACEMENT_RATE * len_keyword)
            mask_words_index = mask_words_index[:num_mask]

        for i in mask_words_index:
            encodings.append(binary_encoding_function(doc[i - 1].text + doc[i].text))

    return encodings


def detect_watermark(text: str, nlp) -> dict:
    encodings = get_encodings(text, nlp)
    n = len(encodings)
    if n == 0:
        return {"watermarked": False, "z_score": 0.0, "p_value": 1.0, "ones_n": "0/0"}

    ones = sum(encodings)
    z = (ones - P * n) / (n * P * (1 - P)) ** 0.5
    p_value = norm.sf(z)

    return {
        "watermarked": bool(z >= Z_ALPHA),
        "z_score": float(z),
        "p_value": float(p_value),
        "ones_n": f"{ones}/{n}",
    }


def parse_comments(filepath: Path) -> list[str]:
    text = filepath.read_text(encoding="utf-8")
    comments = []
    in_saved = False
    has_header = "## Saved Comments" in text

    for line in text.splitlines():
        if line.strip() == "## Saved Comments":
            in_saved = True
            continue
        if line.startswith("- "):
            if has_header and not in_saved:
                continue
            comments.append(line[2:])
    return comments


def main():
    parser = argparse.ArgumentParser(
        description="Standalone RSFPH watermark detector (no model project needed)")
    parser.add_argument("file", help="Path to file containing '- comment' lines")
    parser.add_argument("--csv", type=str, default=None, help="Save results to CSV")
    args = parser.parse_args()

    filepath = Path(args.file)
    if not filepath.exists():
        print(f"[!] File not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    nlp = spacy.load("en_core_web_sm")
    comments = parse_comments(filepath)

    if not comments:
        print("[!] No comments found", file=sys.stderr)
        sys.exit(1)

    print(f"[*] Detecting watermarks in: {filepath}", file=sys.stderr)
    print(f"    Found {len(comments)} comments\n", file=sys.stderr)

    results = []
    for i, comment in enumerate(comments):
        det = detect_watermark(comment, nlp)
        det["comment_idx"] = i
        results.append(det)

        status = "WATERMARKED" if det["watermarked"] else "clean"
        snippet = comment[:80] + "..." if len(comment) > 80 else comment
        print(f"  [{i:2d}] {status:12s}  z={det['z_score']:>8.4f}  "
              f"p={det['p_value']:>12.6f}  ones_n={det['ones_n']:>6s}  | {snippet}")

    detected = sum(1 for d in results if d["watermarked"])
    print(f"\n{'='*60}")
    print(f"SUMMARY: {detected}/{len(results)} comments detected as watermarked")
    print(f"{'='*60}")

    if args.csv:
        with open(args.csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["comment_idx", "watermarked", "z_score", "p_value", "ones_n"])
            writer.writeheader()
            writer.writerows(results)
        print(f"\n[+] CSV saved to {args.csv}")


if __name__ == "__main__":
    main()
