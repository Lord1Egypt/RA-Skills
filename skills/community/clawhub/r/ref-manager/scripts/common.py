"""Shared helpers: DOI regex, text cleaning, name/CJK detection, type mapping."""
import re

DOI_RE = re.compile(r'10\.\d{4,9}/[-._;()/:A-Za-z0-9]+')

UA = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    )
}

CJK_RE = re.compile(r'[\u4e00-\u9fff]')


def clean_text(s):
    if not s:
        return ""
    return re.sub(r'\s+', ' ', s).strip()


def find_doi(text):
    """Return the first DOI-looking token in text, stripped of trailing punct."""
    if not text:
        return None
    m = DOI_RE.search(text)
    if not m:
        return None
    return m.group(0).rstrip('.,;:)}')


def is_chinese(s):
    return bool(s) and CJK_RE.search(s)


def parse_author(raw):
    """Normalize one author string into {'family','given','name'}.

    Accepts 'Family, Given', 'Given Family', 'FAMILY Given-Initials'.
    CJK names are stored as a single 'name' field.
    """
    raw = clean_text(raw)
    if not raw:
        return None
    if is_chinese(raw):
        return {"family": raw, "given": "", "name": raw, "chinese": True}
    if "," in raw:
        parts = [p.strip() for p in raw.split(",", 1)]
        return {"family": parts[0], "given": parts[1] if len(parts) > 1 else "",
                "name": raw, "chinese": False}
    # "Given Family" -> last token is family
    tokens = raw.split()
    if len(tokens) == 1:
        return {"family": tokens[0], "given": "", "name": raw, "chinese": False}
    return {"family": tokens[-1], "given": " ".join(tokens[:-1]),
            "name": raw, "chinese": False}


# Crossref type -> (RIS type, EndNote ref-type name)
TYPE_MAP = {
    "journal-article": ("JOUR", "Journal Article"),
    "book": ("BOOK", "Book"),
    "book-chapter": ("CHAP", "Book Section"),
    "book-section": ("CHAP", "Book Section"),
    "proceedings-article": ("CONF", "Conference Paper"),
    "report": ("RPRT", "Report"),
    "dissertation": ("THES", "Thesis"),
    "monograph": ("BOOK", "Book"),
    "edited-book": ("BOOK", "Edited Book"),
    "reference-entry": ("ELEC", "Web Page"),
    "posted-content": ("ELEC", "Web Page"),
    "webpage": ("ELEC", "Web Page"),
    "standard": ("RPRT", "Report"),
    "dataset": ("DATA", "Dataset"),
}

DEFAULT_TYPE = ("ELEC", "Web Page")
