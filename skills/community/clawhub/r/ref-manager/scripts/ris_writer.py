"""Serialize records into RIS (Reference Manager) and EndNote XML text."""
from xml.sax.saxutils import escape

from common import clean_text


def _ris_authors(rec):
    out = []
    for a in rec.get("authors", []):
        if a.get("chinese"):
            out.append(a.get("name", ""))
        else:
            fam = a.get("family", "")
            giv = a.get("given", "")
            out.append(f"{fam}, {giv}".strip() if giv else fam)
    return [x for x in out if x]


def _split_pages(pages):
    pages = clean_text(pages or "")
    if not pages:
        return "", ""
    if "-" in pages:
        sp, ep = pages.split("-", 1)
        return clean_text(sp), clean_text(ep)
    return pages, ""


def records_to_ris(records):
    lines = []
    for rec in records:
        lines.append(f"TY  - {rec.get('ref_type_ris', 'ELEC')}")
        for a in _ris_authors(rec):
            lines.append(f"AU  - {a}")
        if rec.get("title"):
            lines.append(f"TI  - {clean_text(rec['title'])}")
        if rec.get("journal"):
            lines.append(f"T2  - {clean_text(rec['journal'])}")
        if rec.get("year"):
            lines.append(f"PY  - {clean_text(rec['year'])}")
        if rec.get("publisher"):
            lines.append(f"PB  - {clean_text(rec['publisher'])}")
        if rec.get("volume"):
            lines.append(f"VL  - {clean_text(rec['volume'])}")
        if rec.get("issue"):
            lines.append(f"IS  - {clean_text(rec['issue'])}")
        sp, ep = _split_pages(rec.get("pages"))
        if sp:
            lines.append(f"SP  - {sp}")
        if ep:
            lines.append(f"EP  - {ep}")
        if rec.get("doi"):
            lines.append(f"DO  - {rec['doi']}")
        if rec.get("url"):
            lines.append(f"UR  - {rec['url']}")
        if rec.get("apa"):
            lines.append(f"N1  - {rec['apa']}")
        lines.append("ER  - ")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _style(text):
    return f'<style face="normal" font="default" size="100%">{escape(text or "")}</style>'


def records_to_endnote_xml(records):
    buf = ['<?xml version="1.0" encoding="UTF-8" ?>', "<xml>", "<records>"]
    for rec in records:
        rtype = rec.get("ref_type_name", "Web Page")
        buf.append("<record>")
        buf.append(f'<ref-type name="{escape(rtype)}">17</ref-type>')
        authors = _ris_authors(rec)
        if authors:
            buf.append("<contributors>")
            buf.append("<authors>")
            for a in authors:
                buf.append(f"<author>{_style(a)}</author>")
            buf.append("</authors>")
            buf.append("</contributors>")
        buf.append("<titles>")
        buf.append(f"<title>{_style(rec.get('title', ''))}</title>")
        if rec.get("journal"):
            buf.append(f"<secondary-title>{_style(rec.get('journal'))}</secondary-title>")
        buf.append("</titles>")
        if rec.get("journal"):
            buf.append("<periodical>")
            buf.append(f"<full-title>{_style(rec.get('journal'))}</full-title>")
            buf.append("</periodical>")
        if rec.get("volume"):
            buf.append(f"<volume>{_style(rec.get('volume'))}</volume>")
        if rec.get("issue"):
            buf.append(f"<number>{_style(rec.get('issue'))}</number>")
        if rec.get("pages"):
            buf.append(f"<pages>{_style(rec.get('pages'))}</pages>")
        buf.append("<dates>")
        buf.append(f"<year>{_style(rec.get('year', ''))}</year>")
        buf.append("</dates>")
        if rec.get("publisher"):
            buf.append("<publisher>")
            buf.append(f"<name>{_style(rec.get('publisher'))}</name>")
            buf.append("</publisher>")
        if rec.get("doi"):
            buf.append(f"<electronic-resource-num>{_style(rec['doi'])}</electronic-resource-num>")
        if rec.get("url"):
            buf.append("<urls>")
            buf.append("<related-urls>")
            buf.append(f"<url>{_style(rec.get('url'))}</url>")
            buf.append("</related-urls>")
            buf.append("</urls>")
        if rec.get("apa"):
            buf.append("<notes>")
            buf.append(f"<note>{_style(rec.get('apa'))}</note>")
            buf.append("</notes>")
        buf.append(f"<work-type>{escape(rtype)}</work-type>")
        buf.append("</record>")
    buf.append("</records>")
    buf.append("</xml>")
    return "\n".join(buf) + "\n"
