"""pv_textio - input parsing (v6.4.0 split of verify_pmids.py).

Everything that turns bytes into text and text into citation entries:
document extractors (.docx/.pptx/.html/JATS), the citation-context
parser, the BibTeX/RIS/plain-text bibliography parsers and the
content-based format sniffer. Stdlib-only."""

import re
import json
import os
import time
import sys
import urllib.parse
import urllib.request
import urllib.error
import http.client
import sqlite3
import csv
import zipfile
import html
import random
import io
import itertools
from collections import defaultdict
from html.parser import HTMLParser
from difflib import SequenceMatcher
from pathlib import Path
import xml.etree.ElementTree as ET

# cross-module imports (explicit — underscore names are excluded
# from `import *`, so every private helper is named here)


_MD_TITLE_RE = re.compile(r"##\s+([^.]{10,240}\.)")
from pv_meta import (ARXIV_OLD_RE, CT_KEY, CT_NL, CT_SEP, _HAS_CJK, _HEADING_MARK_RE, _LINT_KNOWN_KEYS, _META_LINE_RE, _QUOTE_MARK_RE, _TABLE_ROW_RE, _TEXT_NUM_RE, _TOOL_VERSION, _UA_TOOL, _arxiv_id_valid_shape, _clean_doi, _extract_author_surnames)

_META_SEG_RE = re.compile(r"(?:[-\u2022*]\s*)?(?:DOI|PMID|arXiv|[A-Za-z\u4e00-\u9fff]{1,12}ID|url)\s*[:\uff1a]\s*\S+", re.I)

_TABLE_SEG_RE = re.compile(r"(?:19|20)\d{2}\s*\|[^|]*\|[^|]*(?:\||$)")

DOI_PATTERNS = [
    # anchored forms (url / doi:) — most reliable; ? cuts tracking params
    # (utm_source etc. on real-world doi.org links — v2.8.0 attacker P1)
    re.compile(r'(?:https?://(?:dx\.)?doi\.org/|doi:\s*)(10\.\d{4,9}/[^\s"\'<>),;\]?&=]+)', re.IGNORECASE),
    # bare 10.x/y — requires the 4-9-digit registrant segment, still noisy-prone:
    # strip trailing punctuation after match
    re.compile(r'\b(10\.\d{4,9}/[^\s"\'<>),;\]?&=]+)', re.IGNORECASE),
]

def extract_dois_from_file(filepath: str) -> list:
    """Extract (doi, context) pairs from a file (v2.8.0). Returns cleaned DOIs."""
    results = []
    try:
        text, _fmt = _read_text_any(filepath)
    except Exception:
        return results
    seen = set()
    for pattern in DOI_PATTERNS:
        for m in pattern.finditer(text):
            doi = _clean_doi(m.group(1))
            if not doi or doi in seen or "/" not in doi:
                continue
            seen.add(doi)
            start = max(0, m.start() - 200)
            end = min(len(text), m.end() + 40)
            context = text[start:end].replace("\n", " ").strip()
            results.append((doi, context))
    return results

ARXIV_PATTERNS = [
    re.compile(r'arxiv\.org/(?:abs|pdf|format)/([^\s"\'<>),;\]]+)', re.IGNORECASE),
    re.compile(r'arxiv:\s*([^\s"\'<>),;\]]+)', re.IGNORECASE),
]


def extract_arxivs_from_file(filepath: str) -> list:
    """Extract arXiv IDs (with shape validation) from a file. Returns
    (arxiv_id, context) pairs."""
    results = []
    try:
        text, _fmt = _read_text_any(filepath)
    except Exception:
        return results
    seen = set()
    for pattern in ARXIV_PATTERNS:
        for m in pattern.finditer(text):
            raw = m.group(1).strip()
            if raw.lower().startswith("arxiv:"):
                raw = raw[6:]
            # A sentence-final period is the single most common character
            # after a reference — strip trailing dots but KEEP internal dots
            # (old-style math.GT/0309136). Shape validation happens in
            # verify_arxiv_entry — a malformed ID found in a scanned document
            # is exactly the kind of fabrication/mistake to surface, not skip.
            raw = raw.rstrip(".")
            if raw.lower() in seen:
                continue
            seen.add(raw.lower())
            start = max(0, m.start() - 150)
            end = min(len(text), m.end() + 40)
            results.append((raw, text[start:end].replace("\n", " ").strip()))
    return results



def _strip_metadata_lines(text: str, out_claimed: dict = None) -> str:
    """Strip bibliography-database export lines before citation
    segmentation (v4.7.0). "- DOI: 10.x/...", "PMID: ...",
    "<Database>ID: ... (any library name, CJK included)", "2025 | Journal | Authors" table rows are registry
    metadata, not claims — the last such line before a PMID used to be
    taken as the claimed title and manufactured mass false mismatches
    on real literature exports (85% of rows in a rheumatology export
    sample, found 2026-10-14). Markdown heading/quote markers are
    unwrapped so a surviving title line reads clean."""
    if "\n" not in text:
        # flattened single-line context (extract_pmids_from_file joins the
        # window with spaces): strip metadata SEGMENTS inline, and a "## "
        # residue mark yields the entry title directly — anything else stays
        # honestly empty (existence path)
        t = _META_SEG_RE.sub(" ", text)
        t = _TABLE_SEG_RE.sub(" ", t)
        m = _MD_TITLE_RE.search(t)
        if m:
            if out_claimed is not None:
                out_claimed["claimed_title"] = m.group(1).strip().rstrip(".")
                yr = re.search(r"\b((?:19|20)\d{2})\b", t)
                out_claimed["claimed_year"] = yr.group(1) if yr else ""
            return m.group(1).strip().rstrip(".")
        # the year must come from the CLEANED text — the "2064 | Journal"
        # table-row year was leaking in as a claimed year
        yr = re.search(r"\b((?:19|20)\d{2})\b", t)
        if out_claimed is not None:
            out_claimed["claimed_year"] = yr.group(1) if yr else ""
        return t
    out = []
    for ln in text.splitlines():
        t = ln.strip()
        if _META_LINE_RE.match(t) or t in ("-", "\u2022", "*"):
            continue
        if _TABLE_ROW_RE.match(t):
            continue
        ln = _HEADING_MARK_RE.sub("", ln)
        ln = _QUOTE_MARK_RE.sub("", ln)
        if t and not ln.strip():
            continue
        out.append(ln)
    return chr(10).join(out)

def parse_citation_context(context: str) -> dict:
    """Parse a citation context string to extract claimed metadata.
    
    Handles common reference formats:
      Author1 A, Author2 B. Title. Journal. Year;Vol(Issue):Pages. PMID: XXXXXXXX
      Author1 A, Author2 B, et al. Title. <i>Journal</i>. Year;Vol:Pages.
      HTML variants with <br>, <sup>, etc.
    
    Returns dict with claimed_title, claimed_authors, claimed_journal, claimed_year.
    """
    claimed = {
        "claimed_title": "",
        "claimed_authors": [],
        "claimed_journal": "",
        "claimed_year": "",
    }
    if not context:
        return claimed

    text = context.strip()
    # Remove HTML tags except <i>...</i> which we need for journal detection
    journal_italic = re.findall(r'<i>([^<]+)</i>', text)
    
    # Extract year (4-digit, 19xx or 20xx)
    year_match = re.search(r'\b((?:19|20)\d{2})\b', text)
    if year_match:
        claimed["claimed_year"] = year_match.group(1)

    # Extract journal from <i>...</i> if present
    if journal_italic:
        claimed["claimed_journal"] = journal_italic[0].strip().rstrip(".")
    
    # Strategy: find PMID position, work backwards
    # v3.9.0 strict-round (external-audit-style dense lists): anchor on the LAST PMID
    # in the context — extract_pmids_from_file hands us the 200 chars BEFORE
    # this record's PMID, so the nearest marker is this record's; re.search
    # used to grab a NEIGHBOUR's PMID and cross-contaminate claims.
    _pmid_matches = list(re.finditer(r'PMID[:\s]*(\d{4,9})', text, re.IGNORECASE))
    pmid_match = _pmid_matches[-1] if _pmid_matches else None
    if not pmid_match:
        # v4.0.0: markerless entries (plain-text reference lists) get the
        # full Latin sentence segmentation below — the freeform-only early
        # return under-extracted and starved the title-search leg of usable
        # titles. CJK markerless entries keep the documented weak-parsing
        # boundary: the GB/T branch anchors on a PMID marker (it reads
        # text after the marker for the DOI tail), so it must not run here —
        # feed a PMID/DOI for exact routing instead.
        pre_text = text.strip().rstrip(".")
        if any('\u4e00' <= ch <= '\u9fff' for ch in pre_text):
            _parse_freeform_citation(text, claimed)
            return claimed
        claimed["claimed_source_format"] = "plaintext"
        _markerless = True
    else:
        _markerless = False
        # Get text before PMID
        pre_text = text[:pmid_match.start()].strip().rstrip(".")

    # v4.7.0: registry metadata rows are not claims — strip them before
    # any segmentation, and when a single title line survives it IS the
    # claim (bibliography-export reality fix, 2026-10-14)
    if claimed.get("claimed_title"):
        return claimed   # flattened-export title already extracted
    _pre_lines = _strip_metadata_lines(pre_text, claimed)
    _pre_clean = [l.strip() for l in _pre_lines.splitlines() if l.strip()]
    # single-title shortcut ONLY when the raw context was multi-line and
    # metadata stripping left one line (bibliography-export shape) — a
    # normal single-line citation (authors. title. journal. PMID) keeps
    # the regular segmentation path
    _raw_nonempty = [l for l in pre_text.splitlines() if l.strip()]
    if len(_pre_clean) == 1 and len(_raw_nonempty) >= 2:
        _t0 = _pre_clean[0].rstrip(".")
        if len(_t0.split()) >= 4:
            claimed[CT_KEY] = CT_SEP.join(_t0.split())
            return claimed
        pre_text = _t0
    elif len(_pre_clean) == 1:
        pre_text = _pre_clean[0]
    elif _pre_clean:
        pre_text = CT_NL.join(_pre_clean).strip().rstrip(".")

    # v3.9.0 (external-audit B5): GB/T 7714-style Chinese references ("……标题[J]. 刊名, 年…"
    # with a PMID marker) — the English sentence parser extracts almost nothing
    # here. Pull the reliably-present fields; the title comparison against
    # Latin registries is skipped cross-language in cross_check, so a Chinese
    # title can never manufacture a false mismatch.
    if pmid_match and any('\u4e00' <= ch <= '\u9fff' for ch in pre_text):
        claimed["claimed_source_format"] = "gbt7714"
        # Scope to THIS record: the scan window may span the previous
        # reference (including its "PMID: xxx." tail). Everything the GB/T
        # extractor looks at must come after the LAST PMID marker —
        # otherwise the neighbour's DOI/year leak into this claim and
        # manufacture false splice accusations (v3.9.0 strict-round P0).
        work = pre_text
        for pm in re.finditer(r'PMID[:：]?\s*\d{4,9}', pre_text, re.IGNORECASE):
            work = pre_text[pm.end():].lstrip(" .。、]　")
        # drop the previous record's trailing DOI/URL tail: scope from the
        # last record-start marker ("[2]" / "2.") if one is present
        rec_start = None
        for rm in re.finditer(r'(?:^|\n)\s*\[?\d+\]?[.．、]?\s*', work):
            rec_start = rm
        if rec_start and rec_start.end() < len(work):
            work = work[rec_start.end():]
        # The type tag ([J]/[M]/[R]...) closes the title sentence — take the
        # LAST sentence-ending before it so ASCII ". " separators (GB/T uses
        # them too) cannot drag the author segment into the title
        tag_m = None
        for tm in re.finditer(r'\[([JMRDSC])\]', work):
            tag_m = tm
        sent_ends = [rm.end() for rm in re.finditer(r'[.。．]\s*', work[:tag_m.start()])] if tag_m else []
        seg_start = max(sent_ends) if sent_ends else 0
        title_txt = work[seg_start:tag_m.start()].strip() if tag_m else ""
        title_txt = re.sub(r'^\[?\d+\]?[.．、]?\s*', '', title_txt)
        if 5 <= len(title_txt) <= 140:
            claimed["claimed_title"] = " ".join(title_txt.split())
            head = work[:seg_start].strip()
            head = re.sub(r'^\s*\[?\d+\]?[.．、]?\s*', '', head)
            head = head.rstrip("．.。,， ")
            if head:
                claimed["claimed_authors"] = [
                    a.strip() for a in re.split(r"[，,;；]|\s{2,}", head) if a.strip()]
            if tag_m:
                # v4.3.0: only [J] (journal article) carries a journal name —
                # for [M] monographs / [R] reports / [D] theses the segment
                # after the tag is the PUBLISHER, and using it as the claimed
                # journal manufactured false journal mismatches
                if tag_m.group(1) == "J":
                    j_m = re.search(r'\[[J]\][.．]?\s*([^,，.。\[\]]{2,40})', work[tag_m.start():])
                    if j_m:
                        claimed["claimed_journal"] = j_m.group(1).strip()
        # greedy: internal dots are part of the DOI; a trailing sentence
        # period is stripped by _clean_doi. URL forms are unwrapped too.
        # Scoped to `work` (previous record's tail can never leak) plus the
        # reference's own tail after the PMID (up to 80 chars, stopping at
        # the next PMID marker) — GB/T puts the DOI there.
        doi_m = re.search(
            r'(?:https?://(?:dx\.)?doi\.org/|\bdoi\s*[:：]?\s*)(10\.\S+)', work)
        if not doi_m:
            tail = text[pmid_match.end():pmid_match.end() + 80]
            tail = re.split(r'PMID[:：]?\s*\d{4,9}', tail)[0]
            doi_m = re.search(
                r'(?:https?://(?:dx\.)?doi\.org/|\bdoi\s*[:：]?\s*)(10\.\S+)', tail)
        if doi_m:
            cd = _clean_doi(doi_m.group(1))
            if cd:
                claimed["claimed_doi"] = cd
        if claimed.get("claimed_title") or claimed.get("claimed_doi"):
            return claimed
        # nothing reliable — fall through to the English heuristics, which
        # will honestly yield little for Chinese prose (documented)

    # Split on ". " — first segment is usually authors, second is title.
    # v3.3.0: sentence-internal abbreviations ("U.S.", "e.g.", "vs.", "Vol.")
    # do NOT end a sentence — a title like "Blood pressure in the U.S.
    # population" used to be truncated at the abbreviation. Protect them
    # with a sentinel before splitting. Deliberately NOT protected: "et al.",
    # "Jr.", "Sr.", "Ed." — they legitimately terminate the author/editor
    # segment, and keeping them would merge authors with the title.
    _ABBREV_PAT = re.compile(
        r'\b(e\.g|i\.e|cf|vs|ca|approx|U\.S|U\.K|Dr|Prof|Mr|Mrs|Ms'
        r'|St|No|Vol|pp|Fig|Ref)\.(\s+)', re.IGNORECASE)
    protected = _ABBREV_PAT.sub(lambda m: m.group(1) + '\x00' + m.group(2),
                                pre_text)
    segments = re.split(r'\.\s+', protected)
    segments = [s.replace('\x00', '.').strip() for s in segments if s.strip()]


    # v3.8.0 (external-audit B1): when the citation is NOT the first sentence of its
    # block, segments[0] is preceding prose and segments[1] is the AUTHOR
    # line ("Zaripova LN, Midgley A, Christmas SE") — treating it as the
    # claimed title mis-reported correct references as mismatch. If
    # segments[1] is entirely author-shaped, the title lives in segments[2].
    # NOTE: the initials group must stay case-SENSITIVE (scoped (?-i:...)) —
    # under re.I it swallows short lowercase words ("of", "in") and turned
    # short-word titles like "Use of CT in ICU" into fake author lines
    _AUTHOR_SEG = re.compile(
        r"^[A-ZÀ-ÿ][\w'’.-]+(?:(?-i: [A-Z]{1,3})\b\.?)+"
        r"(?:(?:,| and | &) [A-ZÀ-ÿ][\w'’.-]+(?:(?-i: [A-Z]{1,3})\b\.?)+)*$"
        r"(?:,? (?i:et al))\.?$", re.I)
    # v4.0.0: markerless numbered references ("[2] Long descriptive title
    # words here. Journal. Year.") often LEAD with the title — treating
    # segments[0] as the author line hands the title-search leg a one-word
    # "title" (the journal). When the first segment is not author-shaped
    # and carries enough words, it IS the title (same author-shape guards
    # as the B1 fix, conservative word floor).
    if _markerless and len(segments) >= 2:
        seg0 = segments[0].strip().rstrip(".")
        # the lone-initial probe skips a leading article ("A study of...")
        seg0_probe = re.sub(r"^A ", "", seg0)
        seg0_authorish = (bool(_AUTHOR_SEG.match(seg0))
                          or "et al" in seg0.lower()
                          or bool(re.search(r"(?:^|[\s,])[A-Z]\.?(?=$|[\s,])", seg0_probe)))
        seg0_words = len(seg0.replace(",", " ").split())
        if not seg0_authorish and seg0_words >= 6:
            claimed["claimed_title"] = seg0
            claimed["claimed_authors"] = []
            for seg in segments[1:]:
                if re.match(r'^\d{4}', seg):
                    continue
                if re.search(r'[a-zA-Z]{3,}', seg) and not re.match(r'^\d', seg):
                    claimed["claimed_journal"] = seg.strip().rstrip(".")
                    break
            return claimed

    title_idx = 1
    author_seg_idx = 0
    if len(segments) >= 3 and segments[0]:
        seg1 = segments[1].strip().rstrip(".")
        # strong author-line features: "et al", a full author-shape match, a
        # lone-initial token ("Van Dijk M"), or comma groups that EACH carry
        # a case-sensitive initials token — a bare comma is not enough
        # (titles like "trials, e.g. dosage effects" contain commas too)
        _groups = [g for g in (x.strip().rstrip(".") for x in seg1.split(",")) if g]
        _comma_authorish = len(_groups) >= 2 and all(
            re.search(r"(?-i:\b[A-Z]{1,3}\b\.?)", g) for g in _groups)
        authorish = ("et al" in seg1.lower()
                     or _AUTHOR_SEG.match(seg1)
                     or _comma_authorish
                     or re.search(r"(?:^|[\s,])[A-Z]\.?(?=$|[\s,])", seg1))
        if authorish and not _AUTHOR_SEG.match(segments[0].strip().rstrip(".")):
            title_idx = 2
            author_seg_idx = 1
    if len(segments) >= 2:
        # First segment: authors (the author-shaped segment when shifted)
        claimed["claimed_authors"] = _extract_author_surnames(segments[author_seg_idx])

        # Title segment (shifted past an author-shaped segment when present)
        claimed["claimed_title"] = segments[title_idx].strip().rstrip(".")

        # Try to find journal in remaining segments if not already found
        if not claimed["claimed_journal"] and len(segments) >= title_idx + 2:
            # Journal is typically the segment after title, possibly with year/volume
            for seg in segments[title_idx + 1:]:
                # Skip volume/issue patterns like "2021;17(4):e90285"
                if re.match(r'^\d{4};', seg):
                    continue
                # If it looks like a journal name (words, not just numbers)
                if re.search(r'[a-zA-Z]{3,}', seg) and not re.match(r'^\d', seg):
                    if not claimed["claimed_journal"]:
                        claimed["claimed_journal"] = seg.strip().rstrip(".")
    elif len(segments) == 1:
        # Only one segment — try to split authors from title differently
        _parse_freeform_citation(pre_text, claimed)
    
    return claimed

def _parse_freeform_citation(text: str, claimed: dict) -> None:
    """Fallback parser for less structured citation text."""
    # Try to find year
    if not claimed["claimed_year"]:
        ym = re.search(r'\b((?:19|20)\d{2})\b', text)
        if ym:
            claimed["claimed_year"] = ym.group(1)
    
    # Try to find journal from <i> or known journal patterns
    if not claimed["claimed_journal"]:
        # Common journal abbreviations
        jm = re.search(
            r'(?:in\s+|published\s+in\s+)?'
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*'
            r'(?:\s+(?:Med|J|Clin|Pediatr|Rheumatol|Lancet|BMJ|Nature|Science|Blood|Ann|Arch|Int|Immunol|Allergy|Res|Rev|Dis))'
            r'(?:\s+(?:Online\s+J\.?|J\.?|Dis\.?))?)',
            text
        )
        if jm:
            claimed["claimed_journal"] = jm.group(1).strip()

    # Try to extract authors from beginning of text
    if not claimed["claimed_authors"]:
        author_match = re.match(r'^([A-Z][a-z]+(?:\s+[A-Z]\.?,?\s*)+)', text)
        if author_match:
            claimed["claimed_authors"] = _extract_author_surnames(author_match.group(1))

PMID_PATTERNS = [
    re.compile(r'PMID[:\s]*(\d{4,9})', re.IGNORECASE),
    re.compile(r'pubmed[:\s]*(\d{4,9})', re.IGNORECASE),
    re.compile(r'https?://pubmed\.ncbi\.nlm\.nih\.gov/(\d+)/', re.IGNORECASE),
]

def _read_text_any(filepath: str) -> tuple:
    """Read a --source / --parse-text input as plain text regardless of format (v4.8.0).

    .docx (Word) is unzipped in-memory and the main document body is
    extracted paragraph-by-paragraph (w:p boundaries become newlines, table
    cells included); .pptx (PowerPoint, v4.9.0) reads every slide plus the
    notes in slide order (a:p/a:t DrawingML, same family as docx);
    .html/.htm is tag-stripped with block-level elements turned into
    newlines and script/style content dropped; anything else is read
    as-is. A malformed zip falls back to a raw read rather than failing
    the whole scan. Returns (text, format_label)."""
    lower = str(filepath).lower()
    try:
        if lower.endswith(".docx"):
            with zipfile.ZipFile(filepath) as z:
                # size cap: a hostile/ runaway document.xml (zip bomb) falls
                # back to the raw read instead of ballooning memory
                if z.getinfo("word/document.xml").file_size > 64 * 1024 * 1024:
                    raise ValueError("document.xml exceeds 64MB cap")
                xml_bytes = z.read("word/document.xml")
            root = ET.fromstring(xml_bytes)
            w = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
            paras = []
            for p in root.iter(f"{w}p"):
                para = "".join(t.text or "" for t in p.iter(f"{w}t")).strip()
                if para:
                    paras.append(para)
            if paras:
                return "\n".join(paras), "docx"
        elif lower.endswith(".pptx"):
            with zipfile.ZipFile(filepath) as z:
                a = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
                # slides in numeric order (slide10 must not precede slide2),
                # then the notes; speaker notes carry citations too
                def _slide_no(name):
                    m = re.search(r"[sS]lide(\d+)\.xml$", name)
                    return int(m.group(1)) if m else 0
                xml_parts = sorted(
                    (n for n in z.namelist()
                     if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)),
                    key=_slide_no)
                xml_parts += sorted(
                    (n for n in z.namelist()
                     if re.fullmatch(r"ppt/notesSlides/notesSlide\d+\.xml", n)),
                    key=_slide_no)
                paras = []
                for name in xml_parts:
                    if z.getinfo(name).file_size > 64 * 1024 * 1024:
                        continue   # per-part cap: skip the part, keep the deck
                    root = ET.fromstring(z.read(name))
                    for p in root.iter(f"{a}p"):
                        para = "".join(t.text or "" for t in p.iter(f"{a}t")).strip()
                        if para:
                            paras.append(para)
            if paras:
                return "\n".join(paras), "pptx"
        elif lower.endswith((".html", ".htm")):

            class _TextExtract(HTMLParser):
                _BLOCK = {"p", "div", "li", "tr", "h1", "h2", "h3", "h4",
                          "h5", "h6", "br", "table", "ul", "ol", "section",
                          "article", "blockquote", "pre"}
                _SKIP = {"script", "style"}

                def __init__(self):
                    super().__init__(convert_charrefs=True)
                    self.parts = []
                    self._skip = 0

                def handle_starttag(self, tag, attrs):
                    if tag in self._SKIP:
                        self._skip += 1
                        return
                    if tag in self._BLOCK:
                        self.parts.append("\n")
                    # link/image targets carry the citations in exported
                    # pages (<a href="https://pubmed.ncbi.nlm.nih.gov/N/">) —
                    # keep them in the text stream or the extractors lose them
                    for k, v in attrs:
                        if k in ("href", "src", "cite") and v:
                            self.parts.append(" " + v + " ")

                def handle_endtag(self, tag):
                    if tag in self._SKIP and self._skip:
                        self._skip -= 1
                    elif tag in self._BLOCK:
                        self.parts.append("\n")

                def handle_data(self, data):
                    if not self._skip:
                        self.parts.append(data)

            parser = _TextExtract()
            parser.feed(Path(filepath).read_text(encoding="utf-8", errors="ignore"))
            text = "".join(parser.parts)
            text = re.sub(r"[ \t]+", " ", text)
            text = re.sub(r"\s*\n\s*", "\n", text)
            text = re.sub(r"\n{3,}", "\n\n", text).strip()
            if text:
                return text, "html"
        elif lower.endswith((".nxml", ".jats", ".xml")):
            # JATS/NLM XML (v6.0.0) — the PMC/NLM article format used by
            # journal export pipelines. A random .xml (config, sitemap) is
            # NOT touched: only a document whose root is an NLM <article>
            # (or a JATS-namespace root) is extracted; everything else
            # falls through to the raw read below.
            if os.path.getsize(filepath) > 64 * 1024 * 1024:
                raise ValueError("xml exceeds 64MB cap")
            root = ET.fromstring(Path(filepath).read_bytes())

            def _local(t):
                return t.rsplit("}", 1)[-1]
            if _local(root.tag) in ("article", "pmc-articleset") or \
                    any(_local(el.tag) == "front" for el in root.iter()):
                parts = []

                def _walk(el):
                    tag = _local(el.tag)
                    if tag == "break":
                        parts.append("\n")
                    elif tag in ("p", "title", "article-title", "trans-title",
                                 "subtitle", "td", "th", "li", "ref",
                                 "contrib", "kwd", "label", "caption",
                                 "fn", "graphic", "media"):
                        parts.append("\n")
                    for k, v in el.attrib.items():
                        if k.rsplit("}", 1)[-1] == "href" and v:
                            parts.append(" " + v + " ")
                    if el.text:
                        parts.append(el.text)
                    for child in el:
                        _walk(child)
                    if el.tail:
                        parts.append(el.tail)   # tail after the subtree: document order

                _walk(root)
                text = "".join(parts)
                text = re.sub(r"[ \t]+", " ", text)
                text = re.sub(r"\s*\n\s*", "\n", text)
                text = re.sub(r"\n{3,}", "\n\n", text).strip()
                if text:
                    return text, "jats"
    except Exception:
        pass
    # fallback: raw read (also covers damaged .docx/.pptx and empty html
    # bodies). v6.0.0: the fallback is announced — a structured file that
    # silently degraded to a byte scan used to look like a clean empty run
    text = Path(filepath).read_text(encoding="utf-8", errors="ignore")
    if lower.endswith((".docx", ".pptx", ".html", ".htm", ".nxml", ".jats", ".xml")):
        print(f"[NOTE] {os.path.basename(str(filepath))}: structured parse "
              f"produced no text — reading as plain text; results may be "
              f"incomplete", file=sys.stderr)
    return text, "text"

def extract_pmids_from_file(filepath: str) -> list[tuple[str, str]]:
    """Extract (pmid, context_line) from a file. Returns list of (pmid, surrounding_text)."""
    results = []
    try:
        text, _fmt = _read_text_any(filepath)
    except Exception:
        return results
    for pattern in PMID_PATTERNS:
        for m in pattern.finditer(text):
            pmid = m.group(1)
            start = max(0, m.start() - 200)
            end = min(len(text), m.end() + 40)
            context = text[start:end].replace("\n", " ").strip()
            results.append((pmid, context))
    return results

def extract_pmids_from_directory(dirpath: str, extensions: tuple = (".html", ".md", ".txt", ".htm", ".json", ".docx", ".pptx", ".nxml", ".jats", ".xml")) -> dict:
    """Scan directory for files containing PMIDs. Returns {filename: [(pmid, context)]}."""
    results = {}
    for root, dirs, files in os.walk(dirpath):
        for fname in files:
            if fname.lower().endswith(extensions):
                fpath = os.path.join(root, fname)
                found = extract_pmids_from_file(fpath)
                if found:
                    results[fpath] = found
    return results

def extract_keywords_from_path(filepath: str) -> list[str]:
    """Extract disease/topic keywords from filename."""
    name = Path(filepath).stem.lower()
    for prefix in ("ev_", "case_", "paper_", "ref_"):
        name = name.replace(prefix, "")
    parts = re.split(r"[_\-]", name)
    return [p for p in parts if len(p) > 2]

_BIB_SKIP_TYPES = ("string", "preamble", "comment")

_BIB_ARXIV_IN_TEXT = re.compile(r'arXiv[:\s]*((?:\d{4}\.\d{4,5})|(?:[\w.-]+/\d{7}))', re.I)

def _bib_clean_value(val: str) -> str:
    """Strip protective braces, unescape common BibTeX escapes, fold spaces."""
    val = val.strip()
    if len(val) >= 2 and ((val[0] == '{' and val[-1] == '}') or
                          (val[0] == '"' and val[-1] == '"')):
        val = val[1:-1]
    val = re.sub(r'[{}]', '', val)
    for esc, ch in (r'\&', '&'), (r'\%', '%'), (r'\_', '_'), (r'\$', '$'), (r'\#', '#'), (r'\"', '"'):
        val = val.replace(esc, ch)
    return " ".join(val.split())

def _split_bib_fields(body: str) -> list:
    """Split an entry body into (name, raw_value) pairs at brace/quote depth 0."""
    parts, cur = [], []
    depth = in_q = 0
    for ch in body:
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth = max(0, depth - 1)
        elif ch == '"' and depth == 0:
            in_q = not in_q
        if ch == ',' and depth == 0 and not in_q:
            parts.append(''.join(cur))
            cur = []
        else:
            cur.append(ch)
    parts.append(''.join(cur))
    pairs = []
    for p in parts:
        if '=' not in p:
            continue
        name, _, val = p.partition('=')
        name = name.strip().lower()
        if name and not name.isdigit():
            pairs.append((name, val.strip()))
    return pairs

def parse_bibtex(path: str) -> tuple:
    """Parse a BibTeX file (v3.6.0). Returns (entries, issues); each entry is
    {citekey, entry_type, fields (names lowered, values cleaned), line}.
    @string/@preamble/@comment blocks are skipped."""
    try:
        text = Path(path).read_text(encoding="utf-8-sig", errors="replace")
    except Exception as e:
        return [], [f"ERROR: file unreadable: {e}"]
    entries, issues = [], []
    _AT_HEAD = re.compile(r'@(\w+)\s*[{(]')   # positional: no O(n) slices
    i, n = 0, len(text)
    scan_pos, line_base = 0, 1                 # incremental newline counter
    while i < n:
        at = text.find("@", i)
        if at < 0:
            break
        m = _AT_HEAD.match(text, at)
        if not m:
            i = at + 1
            continue
        etype = m.group(1).lower()
        if etype in _BIB_SKIP_TYPES:
            i = m.end()
            continue
        line_base += text.count("\n", scan_pos, at)
        scan_pos = at
        entry_line = line_base
        open_ch = text[m.end() - 1]
        close_ch = '}' if open_ch == '{' else ')'
        depth, j = 0, m.end() - 1
        while j < n:
            if text[j] == open_ch:
                depth += 1
            elif text[j] == close_ch:
                depth -= 1
                if depth == 0:
                    break
            j += 1
        if j >= n:
            issues.append(f"line {entry_line}: ERROR unclosed "
                          f"@{etype} entry — braces never balance")
            break
        body = text[m.end():j]
        citekey, comma, rest = body.partition(",")
        citekey = citekey.strip()
        if not citekey:
            issues.append(f"line {entry_line}: WARN @{etype} entry "
                          f"without a citekey")
            citekey = f"anon{len(entries) + 1}"
        fields = {name: _bib_clean_value(val) for name, val in _split_bib_fields(rest)}
        entries.append({"citekey": citekey, "entry_type": etype,
                        "fields": fields, "line": entry_line})
        i = j + 1
    return entries, issues

def bib_entry_route(fields: dict) -> tuple:
    """Routing decision for one parsed entry (v3.6.0).
    Returns (kind, id_string, claimed) with kind in pmid/doi/arxiv/none.
    Priority: PMID > DOI > arXiv (a routed PMID/DOI yields full verdicts)."""
    claimed = {
        "claimed_title": fields.get("title", ""),
        "claimed_authors": [a.strip() for a in re.split(
            r'\s+and\s+', fields.get("author", ""), flags=re.I) if a.strip()],
        "claimed_journal": fields.get("journal", ""),
        "claimed_year": next((y for y in re.findall(
            r'(?:19|20)\d{2}', fields.get("year", "") + " " + fields.get("date", ""))), ""),
    }
    pmid = fields.get("pmid", "").strip()
    if not pmid.isdigit():
        m = re.search(r'PMID[:\s]*(\d{4,9})(?!\d)', fields.get("note", ""), re.I)
        pmid = m.group(1) if m else ""
    if pmid.isdigit():
        return "pmid", pmid, claimed
    doi = _clean_doi(fields.get("doi", ""))
    if doi:
        return "doi", doi, claimed
    hay = fields.get("journal", "") + " " + fields.get("note", "")
    m_arx = _BIB_ARXIV_IN_TEXT.search(hay)
    arx = fields.get("eprint", "").strip() or (m_arx.group(1) if m_arx else "")
    if arx:
        claimed["claimed_doi"] = fields.get("doi", "")
        return "arxiv", arx, claimed
    return "none", "", claimed

_RIS_LINE = re.compile(r'^([A-Z][A-Z0-9])  - ?(.*)$')

def parse_ris(path: str) -> tuple:
    """Parse an RIS bibliography (v3.7.0). Returns (entries, issues) with the
    same entry shape as parse_bibtex; RIS field tags are lowercased, repeated
    tags (AU lines) joined with "; ", continuation lines folded into the
    previous tag. Records are TY..ER pairs; a missing final ER is diagnosed."""
    try:
        text = Path(path).read_text(encoding="utf-8-sig", errors="replace")
    except Exception as e:
        return [], [f"ERROR: file unreadable: {e}"]
    entries, issues = [], []
    cur = None
    cur_tag = None
    for ln, raw in enumerate(text.splitlines(), 1):
        m = _RIS_LINE.match(raw)
        if m:
            tag, val = m.group(1), m.group(2).strip()
            if tag == "TY":
                if cur:
                    entries.append(cur)
                cur = {"citekey": "", "entry_type": (val or "RIS").upper(),
                       "fields": {}, "line": ln}
                cur_tag = None
                continue
            if tag == "ER":
                if cur:
                    an = cur["fields"].get("an", "")
                    cur["citekey"] = ("ris" + an) if an.isdigit() else f"ris{len(entries) + 1}"
                    entries.append(cur)
                    cur = None
                cur_tag = None
                continue
            if cur is None:
                continue   # field before any TY — tolerated as junk
            cur_tag = tag
            key = tag.lower()
            if key in cur["fields"]:
                cur["fields"][key] += "; " + val
            else:
                cur["fields"][key] = val
        elif raw.strip() and cur is not None and cur_tag:
            # fold into the LOWERCASE storage key — cur_tag is uppercase and
            # writing it verbatim created a phantom key, silently dropping
            # continuation lines (v3.7.0 strict-round P1: truncated claimed
            # titles could produce false mismatches on wrapped exports)
            store = cur_tag.lower()
            cur["fields"][store] = (cur["fields"].get(store, "") + " " + raw.strip()).strip()
    if cur:
        issues.append("ERROR: file ends inside an unterminated record "
                      "(missing ER terminator)")
        entries.append(cur)
    if not entries and not issues:
        issues.append("ERROR: no RIS records found (TY..ER pairs)")
    return entries, issues

def ris_to_bib_fields(fields: dict) -> dict:
    """Map RIS tags onto the BibTeX-style names bib_entry_route expects.
    PubMed-style RIS carries the PMID in AN; arXiv URLs in UR are folded
    into the note so the arXiv pattern matcher can see them."""
    journal = next((fields[t] for t in ("jo", "t2", "jf", "ja") if fields.get(t)), "")
    ur = fields.get("ur", "")
    note = " ".join(x for x in (fields.get("n1", ""), fields.get("u1", ""), ur) if x)
    note = note.replace("arxiv.org/abs/", "arXiv:").replace("arxiv.org/pdf/", "arXiv:")
    return {
        "title": fields.get("ti", ""),
        "author": " and ".join(a for a in fields.get("au", "").split("; ") if a),
        "journal": journal,
        "year": fields.get("py", "") or fields.get("y1", ""),
        "doi": fields.get("do", ""),
        "pmid": fields.get("an", "") if fields.get("an", "").isdigit() else "",
        "note": note,
        "eprint": fields.get("eprint", ""),
    }



def parse_plaintext_references(path: str) -> tuple:
    """Parse a plain-text reference list copied from a paper draft (v4.0.0).

    Numbered lists ("[1] ...", "1. ...", "1、 ...") are split at each number
    marker (continuation lines join the current entry); a file with fewer
    than two number markers falls back to one-entry-per-nonempty-line.
    Inline PMID / DOI / arXiv IDs are extracted for exact routing; the rest
    of the entry goes through the citation heuristic parsers (Latin sentence
    parser + GB/T 7714 CJK branch) for claimed metadata and, with a usable
    title, becomes a title-search candidate. Parsing never fabricates
    fields — what the heuristics cannot see stays empty.

    Returns (entries, issues); entries carry pmid/doi/arxiv_id/claimed_*
    plus routable / title_search_candidate flags."""
    entries, issues = [], []
    try:
        text, _fmt = _read_text_any(path)
    except OSError as e:
        return [], [f"cannot read {path}: {e}"]
    lines = text.splitlines()
    numbered_count = sum(1 for ln in lines if _TEXT_NUM_RE.match(ln))
    numbered_mode = numbered_count >= 2
    # v4.7.0: bibliography-export files use "## Title" headings as entry
    # boundaries — a heading-mode file beats numbering (its "[n]" rows
    # are metadata lines, not entry starts)
    heading_mode = (sum(1 for ln in lines if re.match(r'\s*#{1,6}\s+\S', ln)) >= 2
                    and not numbered_mode)
    blocks, cur = [], None
    for ln in lines:
        s = ln.strip()
        if not s:
            continue
        m = _TEXT_NUM_RE.match(ln) if numbered_mode else None
        _is_head = bool(re.match(r'\s*#{1,6}\s+\S', ln))
        if _is_head:
            if cur is not None:
                blocks.append(cur)
            cur = re.sub(r'\s*#{1,6}\s+', '', ln).strip()
        elif m:
            if cur is not None:
                blocks.append(cur)
            cur = s
        elif (numbered_mode or heading_mode) and cur is not None:
            cur += " " + s
        else:
            blocks.append(s)
    if cur is not None:
        blocks.append(cur)
    if not blocks:
        return [], ["no reference entries found in the file"]
    for i, raw in enumerate(blocks, 1):
        entry_text = (_TEXT_NUM_RE.sub("", raw, count=1).strip()
                      if _TEXT_NUM_RE.match(raw) else raw)
        if not entry_text:
            continue
        claimed = parse_citation_context(entry_text)
        e = {"key": f"text{i}", "raw": entry_text,
             "pmid": "", "doi": "", "arxiv_id": ""}
        pm = list(re.finditer(r'PMID[:\s]*(\d{4,9})', entry_text, re.IGNORECASE))
        if pm:
            e["pmid"] = pm[-1].group(1)
        dm = re.search(
            r'(?:https?://(?:dx\.)?doi\.org/|\bdoi\s*[:：]?\s*)(10\.\S+)',
            entry_text, re.IGNORECASE)
        if not dm:
            dm = re.search(r'\b(10\.\d{4,9}/[^\s,;，。]+)', entry_text)
        if dm:
            e["doi"] = _clean_doi(dm.group(1))
        am = re.search(r'arXiv[:\s]*(\d{4}\.\d{4,5})(v\d+)?', entry_text, re.IGNORECASE)
        if am:
            e["arxiv_id"] = am.group(1) + (am.group(2) or "")
        if not e["doi"] and claimed.get("claimed_doi"):
            e["doi"] = claimed["claimed_doi"]
        e.update({"claimed_title": claimed.get("claimed_title", ""),
                  "claimed_authors": claimed.get("claimed_authors", []),
                  "claimed_journal": claimed.get("claimed_journal", ""),
                  "claimed_year": claimed.get("claimed_year", ""),
                  "claimed_source_format": claimed.get("claimed_source_format", "")})
        e["routable"] = bool(e["pmid"] or e["doi"] or e["arxiv_id"])
        # v4.1.0: CJK entries join the title-search queue too — the OpenAlex
        # CJK leg searches the cleaned raw text, so a parseable title is not
        # required (the Latin freeform parser under-extracts Chinese).
        e["title_search_candidate"] = (not e["routable"]
                                       and (len(e.get("claimed_title", "")) >= 15
                                            or (_HAS_CJK.search(entry_text)
                                                and len(entry_text) >= 12)))
        if e["routable"] or e["title_search_candidate"]:
            entries.append(e)
        else:
            issues.append(f"text#{i}: no routable ID and no usable title — "
                          f"skipped ({e['raw'][:48]})")
    return entries, issues

def sniff_bibliography_format(path: str) -> str:
    """'bib' | 'ris' | 'unknown' by content, not extension (v6.3.0): the
    format markers are distinctive (a BibTeX entry opens with @type{; an
    RIS record opens with 'TY  - '), so a renamed or extensionless sample
    file still runs. Only the first 4 KB are inspected."""
    try:
        head = Path(path).read_text(encoding="utf-8-sig", errors="ignore")[:4096]
    except OSError:
        return "unknown"
    for line in head.splitlines():
        s = line.strip()
        if not s:
            continue
        if re.match(r"@\w+\s*\{", s):
            return "bib"
        if re.match(r"TY\s{1,2}-\s", s):
            return "ris"
    return "unknown"


# __all__ recalculated at the true end of the module so every
# late-appended name is exported to `import *` consumers
_NAMES = [n for n in dir() if not n.startswith('__')]
__all__ = _NAMES
del _NAMES
