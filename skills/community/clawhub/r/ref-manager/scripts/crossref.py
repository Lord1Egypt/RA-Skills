"""Crossref authoritative lookup and field cross-checking."""
import requests

from common import clean_text, parse_author, TYPE_MAP, DEFAULT_TYPE, UA


def lookup_doi(doi):
    """Query Crossref for a DOI. Returns a normalized dict or None."""
    if not doi:
        return None
    url = f"https://api.crossref.org/works/{requests.utils.quote(doi, safe='')}"
    try:
        r = requests.get(url, headers=UA, timeout=20)
    except requests.RequestException:
        return None
    if r.status_code != 200:
        return None
    try:
        msg = r.json()["message"]
    except (ValueError, KeyError):
        return None

    authors = []
    for a in msg.get("author", []):
        fam = a.get("family", "")
        giv = a.get("given", "")
        if fam or giv:
            name = f"{fam}, {giv}" if (fam and giv) else (fam or giv)
            authors.append(parse_author(name))

    title = ""
    if msg.get("title"):
        title = msg["title"][0]
    journal = msg.get("container-title", [""])[0] if msg.get("container-title") else ""

    year = ""
    for key in ("published-print", "published-online", "issued", "created"):
        d = msg.get(key)
        if d and d.get("date-parts") and d["date-parts"][0] and d["date-parts"][0][0]:
            year = str(d["date-parts"][0][0])
            break

    return {
        "title": clean_text(title),
        "authors": authors,
        "year": year,
        "journal": clean_text(journal),
        "publisher": msg.get("publisher", ""),
        "volume": msg.get("volume", ""),
        "issue": msg.get("issue", ""),
        "pages": msg.get("page", ""),
        "doi": msg.get("DOI"),
        "type": msg.get("type", ""),
        "url": msg.get("resource", {}).get("primary", {}).get("URL", ""),
    }


def crosscheck(rec, text_hint=None):
    """Fill and correct rec against Crossref; set check_result and notes.

    Returns the record with enriched fields plus a 'check_result' string
    (已修正 / 原样正确 / 待人工确认) and a 'notes' list.
    """
    notes = []
    doi = rec.get("doi")
    auth = lookup_doi(doi) if doi else None

    if auth:
        fixed = []
        for field, cfield in (("title", "title"), ("journal", "journal"),
                              ("volume", "volume"), ("issue", "issue"),
                              ("pages", "pages"), ("year", "year"),
                              ("publisher", "publisher"), ("doi", "doi")):
            aval = clean_text(auth.get(cfield) or "")
            rval = clean_text(rec.get(field) or "")
            if aval:
                if not rval:
                    rec[field] = aval
                    fixed.append(f"{field} 缺失，已回填")
                elif aval.lower() != rval.lower():
                    fixed.append(f"{field} 由「{rval}」修正为「{aval}」")
                    rec[field] = aval
        if auth.get("authors"):
            if not rec.get("authors"):
                fixed.append("authors 缺失，已回填")
            else:
                a_names = sorted([a.get("name", "") for a in rec["authors"]])
                b_names = sorted([a.get("name", "") for a in auth["authors"]])
                if a_names != b_names:
                    fixed.append("authors 已按 Crossref 修正")
            rec["authors"] = auth["authors"]
        if not rec.get("url"):
            rec["url"] = auth.get("url") or rec.get("url")
        ris_type, name = TYPE_MAP.get(auth.get("type", ""), DEFAULT_TYPE)
        rec["ref_type_ris"] = ris_type
        rec["ref_type_name"] = name
        rec["check_result"] = "已修正" if fixed else "原样正确"
        if fixed:
            notes.extend(fixed)
    else:
        ris_type, name = DEFAULT_TYPE
        if "ref_type_ris" not in rec:
            rec["ref_type_ris"] = ris_type
            rec["ref_type_name"] = name
        rec["check_result"] = "待人工确认"
        if doi:
            notes.append("DOI 在 Crossref 未命中（可能是中文文献或数据库未收录），请人工核对")
        else:
            notes.append("未找到 DOI，无法权威核对，请人工确认字段")

    rec["notes"] = notes
    return rec
