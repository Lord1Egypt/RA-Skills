#!/usr/bin/env python3
"""Report form gate: body length, the title-page claim, footnote sources, exhibits, sentence density, leaked internal codes.

    python3 scripts/check_report.py research/<report-id>/<lang>.md [--min-exhibits 6] [--json]

Why: set next to a strong investigative report (54 pages, 159 footnotes, 19 exhibits of original documents), a deep dive
written with version 1.0 of this skill ran past 60,000 words in the body, had almost no links and leaked audit codes into
the text. The gap is form: the reader cannot restate the conclusion or check a source. Those things can be counted, so they
are gates. The standard: references/investigative.md and references/pipeline/03-writing.md.

The language comes from the front matter (lang: en | zh; default en). Exit code 0 when every gate passes, 1 otherwise.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# Gate thresholds (rationale in references/pipeline/03-writing.md, "Length and density")
MAX_BODY = {"zh": 30000, "en": 15000}          # body without appendices: Chinese characters / English words
MAX_THESIS = {"zh": 160, "en": 90}             # title-page thesis paragraph
MAX_SUBTITLE = {"zh": 40, "en": 22}            # subtitle
MIN_NOTES_PER_K = 5.0                           # footnotes per 1,000 English words (2,000 Chinese characters)
MIN_URL_SHARE = 0.9                             # share of external-source notes that carry a URL
MIN_LOCATOR_SHARE = 0.8                         # share that cite a page / section / table / Item
MAX_DENSE_SHARE = 0.05                          # share of sentences carrying more than four numbers
MAX_PROSE_GRADES = 10                           # inline [A]-[D] tags allowed in body paragraphs (grades go in notes)

LEAK = [  # internal codes and pipeline traces a reader cannot decode
    (r"(?<![\w-])[JX]\d{1,2}(?![\w-])", "judgment / cross-check numbers (J5, X12)"),
    (r"(?<![\w-])E[1-5](?![\w-])", "mispricing-evidence codes (E1-E5)"),
    (r"§\s?\d", "model output section numbers (§5b)"),
    (r"\[A[-/][A-Za-z]+\]", "compound grade tags ([A-f], [A/C])"),
    (r"⟦(?:待定|OPEN)", "open-conflict placeholders"),
    (r"model-v\d|calc/|notes-[a-z]|data-[a-z-]+\.json|audit-v\d", "note and model file names"),
    (r"\[\[t:", "unresolved table references"),
]
LOCATOR = re.compile(
    r"第\s*\d+\s*[页頁]|[页頁]\s*\d|\bpp?\.\s*\d|\bat\s+\d+|\bpage\s+\d|§|第[\d一二三四五六七八九十]+[节節条項]|"
    r"\bItem\s+\d|表\s*\d|\btbl\.?\s*\d|\bTable\s+\d|附注|\bNote\s+\d|\bslide\s+\d|幻灯片|第\s*\d+\s*行|\bline\s+\d|"
    r"\bExhibit\s+\d|附件|\bPart\s+[IVX]+|\bSection\s+\d|\bsheet\b|\bcol\.|栏|附表|"
    r"现金流量表|资产负债表|利润表|损益表|股东权益变动表|管理层讨论|风险因素|"
    r"cash flows?|balance sheet|statements? of operations|income statement|MD&A|Risk Factors|\bcover page|封面页", re.I)
OWN = re.compile(r"本报告(计算|估算|加总|推算|测量|整理)|this report'?s? (calculation|estimate|measurement|sum)|"
                 r"our (calculation|estimate|measurement)", re.I)
SHORTREF = re.compile(r"^\s*(同注|见注|Id\.|See note|Same as note|supra)", re.I)


def parse(path: Path):
    raw = path.read_text(encoding="utf-8")
    meta, body = {}, raw
    if raw.startswith("---"):
        end = raw.find("\n---", 3)
        for line in raw[3:end].splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
        body = raw[end + 4:]
    tp = {}
    m = re.search(r"^::: *titlepage *\n([\s\S]*?)^::: *$", body, re.M)
    if m:
        try:
            tp = json.loads(m.group(1))
        except json.JSONDecodeError:
            tp = {"_bad": True}
        body = body[:m.start()] + body[m.end():]
    return meta, tp, body


def size(text: str, lang: str) -> int:
    if lang == "zh":
        return len(re.findall(r"[㐀-鿿]", text))
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'’.,%$-]*", text))


def split_notes(chapter: str):
    """Pull out this chapter's footnote definitions (with indented continuation lines): (text without them, [(label, body)])."""
    notes, keep, cur = [], [], None
    for line in chapter.splitlines():
        m = re.match(r"^\[\^([^\]]+)\]:\s*(.*)$", line)
        if m:
            cur = [m.group(1), m.group(2)]
            notes.append(cur)
            continue
        if cur is not None and (line.startswith(("    ", "\t")) and line.strip()):
            cur[1] += " " + line.strip()
            continue
        cur = None
        keep.append(line)
    return "\n".join(keep), [(a, b) for a, b in notes]


def prose_of(md: str) -> str:
    """Body paragraphs only (blank line between paragraphs, wrapped lines joined): drop tables, chart JSON, exhibit blocks, code, headings, box markers and source lines."""
    md = re.sub(r"^::: *(chart|exhibit)[\s\S]*?^::: *$", "", md, flags=re.M)
    md = re.sub(r"^```[\s\S]*?^```", "", md, flags=re.M)
    paras, cur = [], []
    for line in md.splitlines() + [""]:
        s = line.strip()
        skip = s.startswith(("|", "#", ":::", "![", "<")) or re.match(r"^(\*\*)?(Source|Sources|来源|资料来源|附图|Exhibit)\b", s)
        if not s or skip:
            if cur:
                paras.append(" ".join(cur))
                cur = []
            continue
        cur.append(s)
    return "\n\n".join(paras)


def sentences(text: str, lang: str) -> list[str]:
    out = []
    for para in text.split("\n\n"):
        para = re.sub(r"\[\^[^\]]+\]", "", para)
        para = re.sub(r"\b\d{4}-\d{2}-\d{2}\b", "DATE", para)     # 日期算一个数,不算三个 / a date is one number, not three
        parts = re.split(r"(?<=[。！？；])|(?<=[.!?;])\s+(?=[A-Z“\"(])", para)
        out += [x.strip() for x in parts if len(x.strip()) > 8]
    return out


NUM = re.compile(r"(?<![A-Za-z])[−\-+$€¥£]?\d[\d,.]*\s?(?:%|bn|M|K|pp|bp|x|倍|亿|万|MW|GW|EH/s|BTC)?")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("--min-exhibits", type=int, default=6, help="minimum number of exhibits (6 for a company deep dive; lower for a short note)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    path = Path(a.src)
    meta, tp, body = parse(path)
    lang = meta.get("lang", "en")

    chapters = re.split(r"(?m)^(?=# )", body)
    body_chs, app_chs = [], []
    for ch in chapters:
        title = ch.split("\n", 1)[0]
        (app_chs if re.match(r"^# *(附录|Appendix)", title, re.I) else body_chs).append(ch)

    notes, refs, prose_body = [], 0, []
    for ch in body_chs + app_chs:
        text, ns = split_notes(ch)
        notes += ns
        if ch in body_chs:
            refs += len(re.findall(r"\[\^[^\]]+\](?!:)", text))
            prose_body.append(text)
    body_text = "\n".join(prose_body)
    body_size = size(prose_of(body_text), lang)

    # footnote sources
    short_names = set()
    need_url = have_url = need_loc = have_loc = graded = own = 0
    for _, c in notes:
        for nm in re.findall(r"(?:下称|hereinafter)\s*[《「“\"]?([^》」”\"\]),。;；]+)", c, re.I):
            short_names.add(nm.strip())
        if re.search(r"\[[ABCD]\]", c):
            graded += 1
        if OWN.search(c) and not re.search(r"https?://", c):   # own calculation only; a note that cites a document and then sums is still held to the source standard
            own += 1
            continue
        if SHORTREF.match(c) or any(n and n in c for n in short_names) and not re.search(r"https?://", c):
            continue
        need_url += 1
        have_url += bool(re.search(r"https?://", c))
        need_loc += 1
        have_loc += bool(LOCATOR.search(c))

    sents = sentences(prose_of(body_text), lang)
    dense = [s for s in sents if len(NUM.findall(s)) > 4]
    prose_grades = len(re.findall(r"\[[ABCD]\]", prose_of(body_text)))
    # An exhibit is an image under exhibits/ (or a ::: exhibit block, if your renderer has one); its source line, within
    # a few lines after the image, must say the red box was added.
    exhibits = re.findall(r"^::: *exhibit[^\n]*\n([\s\S]*?)^::: *$", body, re.M)
    if not exhibits:
        exhibits = [body[m.start():m.end() + 500] for m in re.finditer(r"!\[[^\]]*\]\((?:\./)?exhibits/[^)]+\)", body)]
    exh_marked = sum(bool(re.search(r"本报告所加|added by|box(es)? added|our (red )?box", e, re.I)) for e in exhibits)

    leaks = []
    visible = re.sub(r"^::: *chart[\s\S]*?^::: *$", "", body, flags=re.M)
    for pat, what in LEAK:
        hits = re.findall(pat, visible)
        if hits:
            leaks.append(f"{what} x{len(hits)} (e.g. {hits[0]})")

    thesis = tp.get("thesis", "")
    sub = tp.get("subtitle", meta.get("subtitle", ""))
    per_share = bool(re.search(r"每股|/股|per share|a share", thesis + sub, re.I))
    k = body_size / (1000 if lang == "en" else 2000) or 1
    notes_per_k = len(notes) / k

    def gate(name, ok, reading, why=""):
        return {"item": name, "ok": bool(ok), "reading": reading, "why": "" if ok else why}

    rows = [
        gate("Body length (without appendices)", body_size <= MAX_BODY[lang],
             f"{body_size:,} {'characters' if lang == 'zh' else 'words'} / limit {MAX_BODY[lang]:,}",
             "keep only evidence that serves the claim; full coverage goes to the appendix (03-writing, Length and density)"),
        gate("Title-page thesis length", size(thesis, lang) <= MAX_THESIS[lang],
             f"{size(thesis, lang)} / limit {MAX_THESIS[lang]}", "the thesis is the claim, the per-share impact and the two strongest facts, not a list of numbers"),
        gate("Subtitle length", size(sub, lang) <= MAX_SUBTITLE[lang],
             f"{size(sub, lang)} / limit {MAX_SUBTITLE[lang]}", "one line, at most two numbers"),
        gate("Per-share impact on the title page", per_share, "yes" if per_share else "no",
             "convert the claim into value per share (investigative.md section 1, value bridge)"),
        gate("Footnote density", notes_per_k >= MIN_NOTES_PER_K,
             f"{len(notes)} notes, {notes_per_k:.1f} per {'2,000 characters' if lang == 'zh' else '1,000 words'}",
             f"footnote every key number and quotation; minimum {MIN_NOTES_PER_K}"),
        gate("Footnotes with a URL", not need_url or have_url / need_url >= MIN_URL_SHARE,
             f"{have_url}/{need_url}" + (f"({have_url / need_url:.0%})" if need_url else ""),
             "external sources carry a URL; own figures say \"this report's calculation\"; repeats use \"same as note N\" or the hereinafter name"),
        gate("Footnotes cite page / section / table", not need_loc or have_loc / need_loc >= MIN_LOCATOR_SHARE,
             f"{have_loc}/{need_loc}" + (f"({have_loc / need_loc:.0%})" if need_loc else ""),
             "cite the page, section, table, Item or note number so a reader can find the sentence"),
        gate("Footnotes carry a grade", not notes or graded / max(1, len(notes) - sum(bool(SHORTREF.match(c)) for _, c in notes)) >= 0.8,
             f"{graded}/{len(notes)}", "end every note with [A]-[D]; grades move from the body into the notes"),
        gate("Inline grade tags in body paragraphs", prose_grades <= MAX_PROSE_GRADES, f"{prose_grades} / limit {MAX_PROSE_GRADES}",
             "no [A]-[D] in body paragraphs; the grade goes with the source in the note (table grade columns do not count)"),
        gate("Exhibits from original documents", len(exhibits) >= a.min_exhibits and exh_marked == len(exhibits),
             f"{len(exhibits)} / minimum {a.min_exhibits}; source says the red box was added: {exh_marked}/{len(exhibits)}",
             "show key facts as screenshots of the original (scripts/exhibit.py); the source line says the box was added"),
        gate("Sentences overloaded with numbers", not sents or len(dense) / len(sents) <= MAX_DENSE_SHARE,
             f"{len(dense)}/{len(sents)} sentences carry more than four numbers" + (f"({len(dense) / len(sents):.0%})" if sents else ""),
             "one fact per sentence, two or three numbers at most; detail goes to a table or a note"),
        gate("Internal codes in the text", not leaks, "none" if not leaks else "; ".join(leaks),
             "audit and model codes stay in the notes; write what a reader understands"),
    ]
    if tp.get("_bad"):
        rows.insert(0, gate("Title-page JSON", False, "could not parse", "the titlepage block is not valid JSON"))

    if a.json:
        print(json.dumps({"file": str(path), "lang": lang, "rows": rows,
                          "dense_examples": dense[:3]}, ensure_ascii=False, indent=1))
    else:
        print(f"== Report form gate · {path} · {lang}")
        for r in rows:
            print(f"  {'ok ' if r['ok'] else 'FAIL'} {r['item']}: {r['reading']}" + (f"\n       -> {r['why']}" if r["why"] else ""))
        if dense:
            print("  Examples of overloaded sentences:")
            for s in dense[:3]:
                print(f"    · {s[:140]}{'…' if len(s) > 140 else ''}")
        bad = sum(not r["ok"] for r in rows)
        print(f"== {'all gates passed' if not bad else f'{bad} gate(s) failed'}")
    return 0 if all(r["ok"] for r in rows) else 1


if __name__ == "__main__":
    sys.exit(main())
