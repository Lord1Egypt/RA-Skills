#!/usr/bin/env python3
"""voice_metrics.py — measure the tells that survive AI editing.

Two modes:

    python voice_metrics.py report sample.txt
    python voice_metrics.py compare baseline.txt target.txt

Standard library only. Python 3.8+.

The point of this script is not to score "how AI" a text is. It cannot do that,
and any tool that claims to is guessing. It measures **how far a text has drifted
from one specific author's own baseline**, which is a different and answerable
question.
"""

import argparse
import re
import statistics as st
import sys

# ---------------------------------------------------------------- tokenising

ABBREV = {"mr", "mrs", "ms", "dr", "prof", "st", "al", "e.g", "i.e", "vs", "etc",
          "fig", "eq", "no", "vol", "pp", "cf", "ca", "approx", "u.s", "u.k"}


def split_sentences(text):
    """Split on [.!?] followed by space + capital, protecting abbreviations and
    decimal numbers. Naive re.split on '.' will fabricate 3-word 'sentences' out
    of 'Smith et al. (2012)', which silently destroys every downstream statistic."""
    out, buf = [], ""
    for tok in re.split(r"(?<=[.!?])\s+", text):
        buf = (buf + " " + tok).strip() if buf else tok
        last = buf.rstrip().rsplit(None, 1)[-1].lower().strip(".,;:!?)\"'")
        ends_abbrev = last in ABBREV or re.fullmatch(r"[a-z]", last) is not None
        if re.search(r"[.!?][\"')\]]?$", buf) and not ends_abbrev:
            out.append(buf)
            buf = ""
    if buf.strip():
        out.append(buf)
    return [s for s in out if s.strip()]


def words(text):
    return re.findall(r"[A-Za-z][A-Za-z'’-]*", text)


def prose_only(text):
    """Strip table captions and notes. Footnotes are conventionally semicolon-heavy
    and will otherwise be counted as prose punctuation.

    Careful: body prose that begins "Table 11 reports the coefficient..." is NOT a
    caption. Require the caption punctuation (colon or period) rather than just the
    "Table N" prefix, or real paragraphs get silently dropped and every rate below
    is computed on a short denominator.
    """
    keep = []
    for para in re.split(r"\n\s*\n", text):
        p = para.strip()
        if not p:
            continue
        if re.match(r"^(Table|Figure)\s+\d+[A-Za-z]?\s*[:.]", p):
            continue
        if re.match(r"^Notes?\s*:", p):
            continue
        keep.append(p)
    return "\n\n".join(keep)


def without_parens(text):
    return re.sub(r"\([^()]*\)", "", text)


# ---------------------------------------------------------------- measures

FIRST_PERSON = re.compile(r"\b(I|we|us|our|my|me|ours)\b")

PHRASES = [
    "therefore", "however", "moreover", "furthermore", "notably", "crucially",
    "rather than", "associated with", "consistent with", "in order to",
    "such as", "in particular", "it is important to note", "plays a crucial role",
    "a key role", "shed light on", "in conclusion",
]


def measure(text):
    text = text.replace("\u2019", "'")
    prose = prose_only(text)
    sents = split_sentences(prose)
    w = words(prose)
    n = len(w) or 1
    lens = [len(words(s)) for s in sents] or [0]

    fp = FIRST_PERSON.findall(prose)
    fp_forms = {}
    for f in fp:
        fp_forms[f.lower()] = fp_forms.get(f.lower(), 0) + 1

    opens = {}
    for s in sents:
        m = re.match(r"[\"'(\[]*([A-Za-z][A-Za-z'-]*)", s.strip())
        if m:
            k = m.group(1).lower()
            opens[k] = opens.get(k, 0) + 1

    n_s = len(sents) or 1
    art = sum(opens.get(k, 0) for k in ("the", "this", "that", "these", "those",
                                        "a", "an"))
    m = {
        "words": len(w),
        "sentences": len(sents),
        "paragraphs": len([p for p in prose.split("\n\n") if p.strip()]),
        "sent_mean": round(st.mean(lens), 1),
        "sent_cv": round(st.pstdev(lens) / st.mean(lens), 3) if st.mean(lens) else 0,
        "short_ratio": round(sum(1 for x in lens if x <= 10) / n_s, 3),
        "long_ratio": round(sum(1 for x in lens if x >= 30) / n_s, 3),
        "first_person": len(fp),
        "first_person_per_1k": round(1000 * len(fp) / n, 1),
        "first_person_forms": fp_forms,
        "the_open": round(opens.get("the", 0) / n_s, 3),
        "this_open": round(opens.get("this", 0) / n_s, 3),
        "article_open": round(art / n_s, 3),
        "semicolon_prose": without_parens(prose).count(";"),
        "semicolon_per_1k": round(1000 * without_parens(prose).count(";") / n, 2),
        "opener_types": len(opens),
        "opener_type_ratio": round(len(opens) / n_s, 3),
    }
    for p in PHRASES:
        m["ph:" + p] = round(1000 * len(re.findall(re.escape(p), prose, re.I)) / n, 2)
    return m


# ---------------------------------------------------------------- printing

CORE = [
    ("words", "words", ""),
    ("sentences", "sentences", ""),
    ("sent_mean", "sentence mean", ""),
    ("sent_cv", "sentence cv", ""),
    ("short_ratio", "short (<=10w)", "%"),
    ("long_ratio", "long (>=30w)", "%"),
    ("first_person_per_1k", "first person/1k", ""),
    ("the_open", "open: the", "%"),
    ("this_open", "open: this", "%"),
    ("article_open", "open: article", "%"),
    ("semicolon_per_1k", "semicolons/1k", ""),
    ("opener_type_ratio", "opener variety", ""),
]


def fmt(v, unit):
    if isinstance(v, float):
        return f"{v*100:.1f}{unit}" if unit == "%" else f"{v:g}"
    return str(v)


def report(path):
    m = measure(open(path, encoding="utf-8").read())
    print(f"=== {path}")
    for k, label, unit in CORE:
        print(f"  {label:18s} {fmt(m[k], unit):>10s}")
    if m["first_person_forms"]:
        print(f"  {'forms':18s} {m['first_person_forms']}")
    print("  phrase density per 1k (only non-zero shown):")
    for p in PHRASES:
        v = m["ph:" + p]
        if v:
            print(f"    {p:26s} {v:>7.2f}")


def compare(base, target):
    a = measure(open(base, encoding="utf-8").read())
    b = measure(open(target, encoding="utf-8").read())
    print(f"{'metric':20s}{'baseline':>12s}{'target':>10s}{'delta':>10s}")
    print("-" * 52)
    for k, label, unit in CORE:
        va, vb = a[k], b[k]
        d = vb - va if isinstance(va, (int, float)) else ""
        ds = f"{d:+.3f}" if isinstance(d, float) else (f"{d:+d}" if d != "" else "")
        print(f"{label:20s}{fmt(va, unit):>12s}{fmt(vb, unit):>10s}{ds:>10s}")
    if min(a["words"], b["words"]) < 800:
        print("\n⚠️  one side is under 800 words: per-1k phrase rates below are unstable"
              "\n    (a single hit moves the number by several points). Trust the core"
              "\n    table above; treat the phrase list as a checklist, not a measurement.")
    print("\nshared phrases (per 1k): baseline / target")
    for p in PHRASES:
        va, vb = a["ph:" + p], b["ph:" + p]
        if va or vb:
            gap = abs(vb - va) / max(va, vb, 0.01)
            flag = "  <-- off" if gap > 0.5 else ""
            print(f"  {p:26s}{va:7.2f}{vb:9.2f}{flag}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("report")
    r.add_argument("path")
    c = sub.add_parser("compare")
    c.add_argument("baseline")
    c.add_argument("target")
    a = ap.parse_args()
    if a.cmd == "report":
        report(a.path)
    else:
        compare(a.baseline, a.target)


if __name__ == "__main__":
    main()
