"""APA 7th-edition citation formatting (Chinese + English)."""
from common import clean_text, is_chinese


def _initials(given):
    if not given:
        return ""
    return " ".join(f"{t[0]}." for t in given.split() if t)


def _format_authors(authors):
    if not authors:
        return ""
    names = []
    for a in authors:
        if a.get("chinese"):
            names.append(a.get("name", ""))
        else:
            fam = a.get("family", "")
            ini = _initials(a.get("given", ""))
            names.append(f"{fam}, {ini}".strip() if ini else fam)
    names = [n for n in names if n]
    if not names:
        return ""
    all_cjk = all(is_chinese(n) for n in names)
    if all_cjk:
        return "、".join(names)
    if len(names) == 1:
        return names[0]
    if len(names) == 2:
        return f"{names[0]} & {names[1]}"
    return ", ".join(names[:-1]) + ", & " + names[-1]


def _year_part(rec):
    year = clean_text(rec.get("year") or "")
    if not year:
        return "(n.d.)"
    month = clean_text(rec.get("month") or "")
    day = clean_text(rec.get("day") or "")
    if month and day:
        return f"({year}, {month} {day})"
    if month:
        return f"({year}, {month})"
    return f"({year})"


def _doi_or_url(rec):
    doi = rec.get("doi")
    if doi:
        return f"https://doi.org/{doi}"
    url = clean_text(rec.get("url") or "")
    return url


def _cjk(rec):
    return (is_chinese(rec.get("title") or "") or
            is_chinese(rec.get("journal") or "") or
            any(a.get("chinese") for a in rec.get("authors", [])))


def _join_citation(parts, cjk):
    """Join parts into one sentence, using CJK or Western punctuation."""
    if cjk:
        return "".join(parts)
    return " ".join(parts)


def format_apa(rec):
    authors = _format_authors(rec.get("authors", []))
    year = _year_part(rec)
    title = clean_text(rec.get("title") or "")
    rtype = rec.get("ref_type_ris", "ELEC")
    cjk = _cjk(rec)

    doi_url = _doi_or_url(rec)
    tail = f" {doi_url}" if doi_url else ""

    if rtype == "JOUR":
        journal = clean_text(rec.get("journal") or "")
        vol = clean_text(rec.get("volume") or "")
        issue = clean_text(rec.get("issue") or "")
        pages = clean_text(rec.get("pages") or "")
        if cjk:
            s = f"{authors}{year}{title}"
            if journal:
                s += f"《{journal}》"
            if vol or issue:
                s += f", {vol}"
                if issue:
                    s += f"({issue})"
            if pages:
                s += f", {pages}"
            s += "."
            if doi_url:
                s += f" {doi_url}"
            return s
        # English
        s = f"{authors} {year}. {title}."
        if journal:
            s += f" {journal}"
            if vol:
                s += f", {vol}"
                if issue:
                    s += f"({issue})"
            if pages:
                s += f", {pages}"
            s += "."
        if doi_url:
            s += f" {doi_url}"
        return s

    if rtype in ("BOOK", "CHAP"):
        publisher = clean_text(rec.get("publisher") or "")
        pages = clean_text(rec.get("pages") or "")
        if cjk:
            s = f"{authors}{year}{title}."
            if rtype == "CHAP" and pages:
                s += f" 见第 {pages} 页."
            if publisher:
                s += f" {publisher}."
            if doi_url:
                s += f" {doi_url}"
            return s
        s = f"{authors} {year}. {title}."
        if rtype == "CHAP" and pages:
            s += f" (pp. {pages})"
        if publisher:
            s += f" {publisher}."
        if doi_url:
            s += f" {doi_url}"
        return s

    # Default / web page / others
    site = clean_text(rec.get("journal") or rec.get("publisher") or "")
    if cjk:
        s = f"{authors}{year}{title}."
        if site:
            s += f" {site}."
        if doi_url:
            s += f" {doi_url}"
        return s
    s = f"{authors} {year}. {title}."
    if site:
        s += f" {site}."
    if doi_url:
        s += f" {doi_url}"
    return s
