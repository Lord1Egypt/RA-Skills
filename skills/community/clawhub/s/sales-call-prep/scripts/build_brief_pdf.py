#!/usr/bin/env python3
"""
build_brief_pdf.py - render a call-prep JSON payload into a formatted PDF brief.

Usage:
    python build_brief_pdf.py payload.json output.pdf            # build
    python build_brief_pdf.py payload.json --validate            # check only

Requires: reportlab (pip install reportlab). No other dependencies, no network.

Design rules
------------
* Every section is OPTIONAL. A missing/empty section renders as a visible GAP box,
  never as silence and never as invented filler.
* Every item may carry "tag": "sourced" | "inferred" | "gap"  (renders a small badge)
  and "src": ["S1","S3"] (ids that must exist in the top-level "sources" list).
* Text is plain text. **double asterisks** make bold. \\n becomes a line break.

Payload schema (all keys optional unless marked *)
-------------------------------------------------
{
  "meta": {                                  *
    "company": str *, "website": str, "prepared_for": str, "prepared_on": "YYYY-MM-DD",
    "contact": {"name": str, "title": str}, "deal_type": str, "our_solution": str,
    "sample": bool,                          # true stamps SAMPLE DATA on every page
    "practice_note": str                     # optional line shown under the battle card
  },
  "snapshot": {"takeaways": [str, str, str]},
  "s1_account_brief": {"summary": [str], "business": str, "customers": str,
       "priorities": [str], "recent_changes": [{"date","item","src","tag"}]},
  "s2_pain_points":  [{"challenge","quote","speaker","call_date","how_we_help","src","tag"}],
  "s3_contact":      {"cares_about": [str], "evidence": [{"signal","src","tag"}], "note": str},
  "s4_discovery":    [{"question","follow_up","why"}],
  "s5_opener":       {"text","anchor","src"},
  "s6_committee":    [{"role","person","type","judges_us_on","verified": bool}],
  "s7_objections":   [{"objection","response","basis","tag"}],
  "s8_competitors":  [{"name","positioning","pricing","gaps","src","tag"}],
  "s9_battlecard":   [{"objection","real_concern","response","proof_point","question_back"}],
  "s10_followup":    {"email": {"subject","body"},
                      "touches": [{"timing","channel","touch","tied_to"}]},
  "gaps":            [{"stage": int|str, "missing": str, "ask": str}],
  "sources":         [{"id","title","url","accessed"}]
}
"""
import json
import re
import sys
import datetime
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph,
                                Spacer, Table, TableStyle, KeepTogether,
                                PageBreak, CondPageBreak, NextPageTemplate)

# ---------------------------------------------------------------- palette
INK = colors.HexColor("#14213D")
TEAL = colors.HexColor("#0F766E")
TEAL_BG = colors.HexColor("#E6F4F1")
AMBER = colors.HexColor("#B45309")
AMBER_BG = colors.HexColor("#FEF3C7")
GRAY_BG = colors.HexColor("#F3F4F6")
RULE = colors.HexColor("#D1D5DB")
TEXT = colors.HexColor("#1F2937")
MUTED = colors.HexColor("#6B7280")
RED = colors.HexColor("#B91C1C")

PAGE_W, PAGE_H = letter
MARGIN = 0.75 * inch
CW = PAGE_W - 2 * MARGIN  # content width

# ---------------------------------------------------------------- text utils
_SUBS = {"\u2192": "->", "\u2190": "<-", "\u2265": ">=", "\u2264": "<=",
         "\u2713": "yes", "\u2717": "no", "\u00a0": " ", "\u2009": " ",
         "\u200b": "", "\u2011": "-", "\u2212": "-", "\u00d7": "x"}


def clean(s):
    """Make text safe for the built-in PDF fonts (WinAnsi)."""
    s = "" if s is None else str(s)
    for k, v in _SUBS.items():
        s = s.replace(k, v)
    return s.encode("cp1252", "replace").decode("cp1252")


def rich(s):
    s = escape(clean(s))
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    return s.replace("\n", "<br/>")


TAGS = {
    "sourced": ("SOURCED", TEAL),
    "inferred": ("INFERRED", AMBER),
    "gap": ("GAP", RED),
}


def badge(tag):
    if not tag or str(tag).lower() not in TAGS:
        return ""
    label, col = TAGS[str(tag).lower()]
    return f' <font size="6.5" color="{col.hexval().replace("0x", "#")}"><b>[{label}]</b></font>'


def srcs(item):
    ids = item.get("src") if isinstance(item, dict) else None
    if not ids:
        return ""
    if isinstance(ids, str):
        ids = [ids]
    return (' <font size="7" color="#6B7280">[' + ", ".join(escape(clean(i)) for i in ids) + "]</font>")


# ---------------------------------------------------------------- styles
def S(name, **kw):
    base = dict(fontName="Helvetica", fontSize=9.5, leading=13.2, textColor=TEXT)
    base.update(kw)
    return ParagraphStyle(name, **base)


ST = {
    "body": S("body"),
    "small": S("small", fontSize=8.2, leading=11, textColor=MUTED),
    "muted_i": S("muted_i", fontName="Helvetica-Oblique", fontSize=8.8, leading=12, textColor=MUTED),
    "h1": S("h1", fontName="Helvetica-Bold", fontSize=15, leading=19, textColor=INK, spaceBefore=4, spaceAfter=4),
    "h2": S("h2", fontName="Helvetica-Bold", fontSize=12.5, leading=16, textColor=INK, spaceBefore=12, spaceAfter=1),
    "h3": S("h3", fontName="Helvetica-Bold", fontSize=9.8, leading=13, textColor=INK),
    "label": S("label", fontName="Helvetica-Bold", fontSize=7.4, leading=10, textColor=TEAL),
    "cell": S("cell", fontSize=8.6, leading=11.6),
    "cellb": S("cellb", fontName="Helvetica-Bold", fontSize=8.6, leading=11.6, textColor=INK),
    "th": S("th", fontName="Helvetica-Bold", fontSize=7.6, leading=10, textColor=colors.white),
    "quote": S("quote", fontName="Helvetica-Oblique", fontSize=9.2, leading=13, textColor=INK),
    "bullet": S("bullet", leftIndent=12, bulletIndent=2, spaceAfter=1.5),
    "grp_l": S("grp_l", fontName="Helvetica-Bold", fontSize=17, leading=20, textColor=colors.white, alignment=1),
    "grp_t": S("grp_t", fontName="Helvetica-Bold", fontSize=11.5, leading=14, textColor=colors.white),
    "grp_s": S("grp_s", fontSize=8.4, leading=11, textColor=colors.HexColor("#CBD5E1")),
    "takeaway": S("takeaway", fontSize=10.2, leading=14.2),
}


def P(text, style="body"):
    return Paragraph(rich(text), ST[style])


def bullets(items, style="bullet"):
    return [Paragraph(rich(i), ST[style], bulletText="\u2022") for i in (items or [])]


# ---------------------------------------------------------------- building blocks
def group_banner(letter_, title, sub, need=2.2):
    t = Table([[Paragraph(letter_, ST["grp_l"]),
                [Paragraph(clean(title), ST["grp_t"]), Paragraph(clean(sub), ST["grp_s"])]]],
              colWidths=[0.55 * inch, CW - 0.55 * inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), INK),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    return [CondPageBreak(need * inch), Spacer(1, 6), t, Spacer(1, 2)]


def stage_head(num, title, why, need=1.6):
    return [CondPageBreak(need * inch),
            Paragraph(f'<font color="#0F766E">{num:02d}</font>&nbsp;&nbsp;{escape(clean(title))}', ST["h2"]),
            Paragraph(escape(clean(why)), ST["muted_i"]), Spacer(1, 5)]


def gap_box(stage_label, note=None):
    msg = f"<b>GAP - {escape(clean(stage_label))}.</b> " + escape(clean(
        note or "No verified data was available for this stage. See 'Gaps and asks' at the end of this brief."))
    t = Table([[Paragraph(msg, S("gapt", fontSize=8.8, leading=12, textColor=AMBER))]], colWidths=[CW])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), AMBER_BG),
        ("LINEBEFORE", (0, 0), (0, -1), 3, AMBER),
        ("LEFTPADDING", (0, 0), (-1, -1), 9), ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return [t, Spacer(1, 6)]


def callout(flowables, bg=TEAL_BG, bar=TEAL, width=CW):
    t = Table([[flowables]], colWidths=[width])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg), ("LINEBEFORE", (0, 0), (0, -1), 3, bar),
        ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return t


def grid(header, rows, widths, zebra=True):
    data = [[Paragraph(clean(h), ST["th"]) for h in header]] + rows
    t = Table(data, colWidths=widths, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), INK), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 1), (-1, -1), 0.4, RULE),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]
    if zebra:
        for i in range(2, len(data), 2):
            style.append(("BACKGROUND", (0, i), (-1, i), GRAY_BG))
    t.setStyle(TableStyle(style))
    return t


def kv_card(title, pairs, accent=TEAL):
    """Card with a title row and label/value rows."""
    rows = [[Paragraph(title, ST["h3"]), ""]]
    for label, val in pairs:
        if val in (None, "", []):
            continue
        rows.append([Paragraph(clean(label).upper(), ST["label"]), val if not isinstance(val, str) else Paragraph(val, ST["cell"])])
    t = Table(rows, colWidths=[1.05 * inch, CW - 1.05 * inch])
    t.setStyle(TableStyle([
        ("SPAN", (0, 0), (-1, 0)), ("BACKGROUND", (0, 0), (-1, 0), GRAY_BG),
        ("LINEBEFORE", (0, 0), (0, -1), 3, accent), ("BOX", (0, 0), (-1, -1), 0.4, RULE),
        ("LINEBELOW", (0, 1), (-1, -2), 0.3, RULE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    return KeepTogether([t, Spacer(1, 7)])


def has(v):
    return bool(v) and v != [] and v != {}


# ---------------------------------------------------------------- stage renderers
def r_snapshot(d, meta, gaps):
    out = [Paragraph("Call-day snapshot", ST["h1"])]
    tk = (d or {}).get("takeaways") or []
    if tk:
        rows = [[Paragraph(f'<font color="#0F766E"><b>{i}</b></font>', ST["takeaway"]),
                 Paragraph(rich(t), ST["takeaway"])] for i, t in enumerate(tk[:5], 1)]
        t = Table(rows, colWidths=[0.3 * inch, CW - 0.3 * inch])
        t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                               ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
        out += [P("The few things most likely to change how this call goes.", "muted_i"), Spacer(1, 4), t]
    else:
        out += gap_box("Snapshot", "Takeaways were not generated.")
    return out


def r_meta_table(meta):
    c = meta.get("contact") or {}
    contact = ", ".join(x for x in [c.get("name"), c.get("title")] if x) or "Not specified"
    pairs = [("Company", meta.get("company")), ("Website", meta.get("website") or "-"),
             ("Contact", contact), ("Deal type", meta.get("deal_type") or "-"),
             ("Our solution", meta.get("our_solution") or "-"),
             ("Research date", meta.get("prepared_on") or "-")]
    rows = [[Paragraph(k.upper(), ST["label"]), Paragraph(rich(v), ST["cell"])] for k, v in pairs]
    t = Table(rows, colWidths=[1.1 * inch, CW - 1.1 * inch])
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), 0.3, RULE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    return [Spacer(1, 8), t]


def r_route_status(payload):
    keys = [("s1_account_brief", "Account brief"), ("s2_pain_points", "Pain from earnings calls"),
            ("s3_contact", "Contact's role"), ("s4_discovery", "Discovery questions"),
            ("s5_opener", "Specific opener"), ("s6_committee", "Buying committee"),
            ("s7_objections", "Likely objections"), ("s8_competitors", "Competitor landscape"),
            ("s9_battlecard", "Battle card"), ("s10_followup", "Follow-up plan")]
    gap_stages = set()
    for g in payload.get("gaps") or []:
        try:
            gap_stages.add(int(str(g.get("stage")).strip().lstrip("sS")))
        except (ValueError, TypeError):
            pass
    cells = []
    for i, (k, label) in enumerate(keys, 1):
        if not has(payload.get(k)):
            status, col = "GAP", RED
        elif i in gap_stages:
            status, col = "PARTIAL", AMBER
        else:
            status, col = "COMPLETE", TEAL
        cells.append(Paragraph(
            f'<b>{i:02d}</b> {escape(label)}<br/><font size="7" color="{col.hexval().replace("0x", "#")}"><b>{status}</b></font>',
            ST["cell"]))
    rows = [cells[0:5], cells[5:10]]
    t = Table(rows, colWidths=[CW / 5] * 5)
    t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.4, RULE), ("INNERGRID", (0, 0), (-1, -1), 0.4, RULE),
                           ("BACKGROUND", (0, 0), (-1, -1), GRAY_BG), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    return [Spacer(1, 12), Paragraph("Route status", ST["h3"]), Spacer(1, 3), t]


def r_s1(d):
    out = stage_head(1, "One-page account brief", "What they do, who they serve, what changed lately.")
    if not has(d):
        return out + gap_box("Stage 01")
    for para in d.get("summary") or []:
        out.append(P(para))
        out.append(Spacer(1, 4))
    pairs = []
    if d.get("business"):
        pairs.append(("Business", d["business"]))
    if d.get("customers"):
        pairs.append(("Customers", d["customers"]))
    if d.get("priorities"):
        pairs.append(("Priorities", bullets(d["priorities"])))
    if pairs:
        out.append(kv_card("Snapshot", pairs))
    ch = d.get("recent_changes") or []
    if ch:
        rows = [[Paragraph(rich(c.get("date", "")), ST["cell"]),
                 Paragraph(rich(c.get("item", "")) + badge(c.get("tag")) + srcs(c), ST["cell"])] for c in ch]
        out += [Paragraph("What changed lately", ST["h3"]), Spacer(1, 3),
                grid(["Date", "Change"], rows, [0.9 * inch, CW - 0.9 * inch])]
    return out


def r_s2(d):
    out = stage_head(2, "Pain from earnings calls", "Problems leadership has already admitted in public.")
    if not has(d):
        return out + gap_box("Stage 02", "No earnings-call transcript was available (private company or gated source).")
    for i, p in enumerate(d, 1):
        q = p.get("quote")
        who = " - ".join(x for x in [p.get("speaker"), p.get("call_date")] if x)
        rows_ = [("Challenge", Paragraph(rich(p.get("challenge", "")) + badge(p.get("tag")) + srcs(p), ST["cellb"]))]
        if q:
            rows_.append(("Their words", Paragraph(f'\u201c{escape(clean(q))}\u201d' + (f'<br/><font size="7.6" color="#6B7280">{escape(clean(who))}</font>' if who else ""), ST["quote"])))
        rows_.append(("Where we fit", p.get("how_we_help")))
        out.append(kv_card(f"Challenge {i}", rows_))
    return out


def r_s3(d, meta):
    c = meta.get("contact") or {}
    who = ", ".join(x for x in [c.get("name"), c.get("title")] if x)
    out = stage_head(3, "Your contact's role", f"What a {c.get('title', 'this role')} cares about right now." if c.get("title") else "What this role cares about right now.")
    if not has(d):
        return out + gap_box("Stage 03", "No contact was provided or their profile could not be read.")
    pairs = [("Contact", who or None), ("Cares about", bullets(d.get("cares_about")))]
    out.append(kv_card("Role read", pairs))
    ev = d.get("evidence") or []
    if ev:
        rows = [[Paragraph(rich(e.get("signal", "")) + badge(e.get("tag")) + srcs(e), ST["cell"])] for e in ev]
        out += [Paragraph("Evidence behind the read", ST["h3"]), Spacer(1, 3), grid(["Signal"], rows, [CW])]
    if d.get("note"):
        out += [Spacer(1, 4)] + gap_box("Note", d["note"])
    return out


def r_s4(d):
    out = stage_head(4, "Discovery questions", "Open questions surface stories; yes/no questions surface politeness.")
    if not has(d):
        return out + gap_box("Stage 04")
    for i, q in enumerate(d, 1):
        pairs = [("Ask", Paragraph(f'<b>{rich(q.get("question", ""))}</b>', ST["cell"])),
                 ("Follow-up", q.get("follow_up")), ("Why this", Paragraph(rich(q.get("why", "")), ST["small"]) if q.get("why") else None)]
        out.append(kv_card(f"Q{i}", pairs))
    return out


def r_s5(d):
    out = stage_head(5, "A specific opener", "Answers 'why should I care' in two sentences.")
    if not has(d):
        return out + gap_box("Stage 05")
    body = [Paragraph(rich(d.get("text", "")), S("op", fontSize=10.6, leading=15, textColor=INK))]
    if d.get("anchor"):
        body += [Spacer(1, 4), Paragraph("Anchored on: " + rich(d["anchor"]) + srcs(d), ST["small"])]
    return out + [callout(body), Spacer(1, 6)]


def r_s6(d):
    out = stage_head(6, "Buying committee", "Decision-makers, influencers, blockers.")
    if not has(d):
        return out + gap_box("Stage 06")
    rows = []
    for m in d:
        ver = "Verified" if m.get("verified") else "Unverified"
        col = "#0F766E" if m.get("verified") else "#B45309"
        rows.append([Paragraph(rich(m.get("role", "")), ST["cellb"]),
                     Paragraph(rich(m.get("person") or "Not identified") + f'<br/><font size="7" color="{col}"><b>{ver}</b></font>', ST["cell"]),
                     Paragraph(rich(m.get("type", "")), ST["cell"]),
                     Paragraph(rich(m.get("judges_us_on", "")), ST["cell"])])
    return out + [grid(["Role", "Person", "Type", "How they will judge us"], rows,
                       [1.2 * inch, 1.4 * inch, 1.2 * inch, CW - 3.8 * inch])]


def r_s7(d):
    out = stage_head(7, "Likely objections", "Prepared sellers stay calm and hold price.")
    if not has(d):
        return out + gap_box("Stage 07")
    for i, o in enumerate(d, 1):
        out.append(kv_card(f"Objection {i}: " + escape(clean(o.get("objection", ""))) + badge(o.get("tag")),
                           [("Response", o.get("response")), ("Basis", Paragraph(rich(o.get("basis", "")), ST["small"]) if o.get("basis") else None)],
                           accent=AMBER))
    return out


def r_s8(d):
    out = stage_head(8, "Competitor landscape", "Know the gaps before the buyer points them out.")
    if not has(d):
        return out + gap_box("Stage 08")
    rows = []
    for c in d:
        rows.append([Paragraph(rich(c.get("name", "")) + badge(c.get("tag")), ST["cellb"]),
                     Paragraph(rich(c.get("positioning", "")), ST["cell"]),
                     Paragraph(rich(c.get("pricing") or "Not public - not estimated."), ST["cell"]),
                     Paragraph(rich(c.get("gaps", "")) + srcs(c), ST["cell"])])
    return out + [grid(["Competitor", "Positioning", "Pricing", "Gaps / where we win"], rows,
                       [1.15 * inch, 1.9 * inch, 1.35 * inch, CW - 4.4 * inch])]


def r_s9(d, meta):
    out = stage_head(9, "Objections battle card", "The five pushbacks most likely to come up, with the concern behind each.")
    if not has(d):
        return out + gap_box("Stage 09")
    for i, o in enumerate(d, 1):
        out.append(kv_card(f"{i}. " + escape(clean(o.get("objection", ""))), [
            ("Real concern", o.get("real_concern")), ("My response", o.get("response")),
            ("Proof point", o.get("proof_point")), ("Ask back", Paragraph(f'<b>{rich(o.get("question_back", ""))}</b>', ST["cell"]) if o.get("question_back") else None)],
            accent=INK))
    if meta.get("practice_note"):
        out.append(callout([Paragraph(rich(meta["practice_note"]), ST["cell"])]))
    return out


def r_s10(d):
    out = stage_head(10, "Custom follow-up plan", "One email, three useful touchpoints. Drafts only - review before sending.", need=4.2)
    if not has(d):
        return out + gap_box("Stage 10")
    em = d.get("email") or {}
    if em:
        body = [Paragraph("SUBJECT", ST["label"]), Paragraph(f'<b>{rich(em.get("subject", ""))}</b>', ST["body"]),
                Spacer(1, 6), Paragraph(rich(em.get("body", "")), ST["body"])]
        out += [callout(body, bg=GRAY_BG, bar=INK), Spacer(1, 8)]
    tc = d.get("touches") or []
    if tc:
        rows = [[Paragraph(rich(t.get("timing", "")), ST["cellb"]), Paragraph(rich(t.get("channel", "")), ST["cell"]),
                 Paragraph(rich(t.get("touch", "")), ST["cell"]), Paragraph(rich(t.get("tied_to", "")), ST["cell"])] for t in tc]
        out += [Paragraph("Value-adding touches", ST["h3"]), Spacer(1, 3),
                grid(["When", "Channel", "Touch", "Tied to"], rows, [0.9 * inch, 0.9 * inch, CW - 2.9 * inch, 1.1 * inch])]
    return out


def r_gaps_sources(payload):
    out = [PageBreak(), Paragraph("Gaps and asks", ST["h1"]),
           P("Anything that could not be verified is listed here instead of being guessed. Paste the item and the affected stage can be re-run.", "muted_i"),
           Spacer(1, 4)]
    gaps = payload.get("gaps") or []
    if gaps:
        rows = [[Paragraph(f'<b>{escape(clean(str(g.get("stage", ""))))}</b>', ST["cell"]),
                 Paragraph(rich(g.get("missing", "")), ST["cell"]), Paragraph(rich(g.get("ask", "")), ST["cell"])] for g in gaps]
        out.append(grid(["Stage", "What is missing", "What to paste or confirm"], rows, [0.6 * inch, 3.0 * inch, CW - 3.6 * inch]))
    else:
        out.append(P("No gaps recorded."))
    out += [Spacer(1, 14), Paragraph("Sources", ST["h1"])]
    so = payload.get("sources") or []
    if so:
        rows = [[Paragraph(clean(s.get("id", "")), ST["cellb"]),
                 Paragraph(rich(s.get("title", "")) + (f'<br/><font size="7.4" color="#0F766E">{escape(clean(s.get("url", "")))}</font>' if s.get("url") else ""), ST["cell"]),
                 Paragraph(rich(s.get("accessed", "")), ST["cell"])] for s in so]
        out.append(grid(["ID", "Source", "Accessed"], rows, [0.5 * inch, CW - 1.5 * inch, 1.0 * inch]))
    else:
        out.append(P("No sources recorded."))
    return out


# ---------------------------------------------------------------- validation
def validate(payload):
    warns = []
    meta = payload.get("meta") or {}
    if not meta.get("company"):
        warns.append("meta.company is required")
    ids = {s.get("id") for s in payload.get("sources") or []}

    def walk(o, path=""):
        if isinstance(o, dict):
            for k, v in o.items():
                if k == "src":
                    for i in ([v] if isinstance(v, str) else v or []):
                        if i not in ids:
                            warns.append(f"{path}: source id '{i}' not in sources[]")
                else:
                    walk(v, f"{path}.{k}" if path else k)
        elif isinstance(o, list):
            for n, v in enumerate(o):
                walk(v, f"{path}[{n}]")
    walk({k: v for k, v in payload.items() if k != "sources"})
    for k in ["s1_account_brief", "s2_pain_points", "s3_contact", "s4_discovery", "s5_opener",
              "s6_committee", "s7_objections", "s8_competitors", "s9_battlecard", "s10_followup"]:
        if not has(payload.get(k)):
            warns.append(f"{k} is empty -> will render as a GAP box (add an entry to gaps[] explaining why)")
    if len(payload.get("s4_discovery") or []) not in (0, 5):
        warns.append("s4_discovery: source route asks for exactly 5 questions")
    if len(payload.get("s7_objections") or []) not in (0, 3):
        warns.append("s7_objections: source route asks for exactly 3 objections")
    if len(payload.get("s9_battlecard") or []) not in (0, 5):
        warns.append("s9_battlecard: source route asks for exactly 5 objections")
    if len(payload.get("s2_pain_points") or []) not in (0, 3):
        warns.append("s2_pain_points: source route asks for exactly 3 challenges")
    return warns


# ---------------------------------------------------------------- page furniture
class NumberedCanvas(rl_canvas.Canvas):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self._saved = []

    def showPage(self):
        self._saved.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        n = len(self._saved)
        for st in self._saved:
            self.__dict__.update(st)
            self.setFont("Helvetica", 7.5)
            self.setFillColor(MUTED)
            self.drawRightString(PAGE_W - MARGIN, 0.45 * inch, f"Page {self._pageNumber} of {n}")
            super().showPage()
        super().save()


def make_page_fns(meta):
    company = clean(meta.get("company", ""))
    sample = bool(meta.get("sample"))
    foot = ("SAMPLE DATA - fictional company, for format inspection only."
            if sample else "AI-assisted draft. Verify facts marked INFERRED and every quote before use.")

    def first(c, doc):
        c.saveState()
        c.setFillColor(INK)
        c.rect(0, PAGE_H - 1.75 * inch, PAGE_W, 1.75 * inch, stroke=0, fill=1)
        c.setFillColor(TEAL)
        c.rect(0, PAGE_H - 1.75 * inch, PAGE_W, 0.06 * inch, stroke=0, fill=1)
        c.setFillColor(colors.HexColor("#94A3B8"))
        c.setFont("Helvetica-Bold", 8)
        c.drawString(MARGIN, PAGE_H - 0.6 * inch, "CALL PREP BRIEF")
        c.setFillColor(colors.white)
        size = 28 if len(company) < 26 else 21
        c.setFont("Helvetica-Bold", size)
        c.drawString(MARGIN, PAGE_H - 1.13 * inch, company)
        c.setFont("Helvetica", 9.5)
        c.setFillColor(colors.HexColor("#CBD5E1"))
        line = " | ".join(x for x in [
            f"Prepared for {clean(meta['prepared_for'])}" if meta.get("prepared_for") else None,
            clean(meta.get("prepared_on")) if meta.get("prepared_on") else None,
            clean(meta.get("deal_type")) if meta.get("deal_type") else None] if x)
        c.drawString(MARGIN, PAGE_H - 1.42 * inch, line)
        if sample:
            c.setFillColor(colors.HexColor("#FBBF24"))
            c.setFont("Helvetica-Bold", 8)
            c.drawRightString(PAGE_W - MARGIN, PAGE_H - 0.6 * inch, "SAMPLE DATA")
        _footer(c)
        c.restoreState()

    def later(c, doc):
        c.saveState()
        c.setStrokeColor(RULE)
        c.line(MARGIN, PAGE_H - 0.55 * inch, PAGE_W - MARGIN, PAGE_H - 0.55 * inch)
        c.setFont("Helvetica-Bold", 7.8)
        c.setFillColor(INK)
        c.drawString(MARGIN, PAGE_H - 0.45 * inch, company + "  |  Call prep brief")
        if sample:
            c.setFillColor(AMBER)
            c.drawRightString(PAGE_W - MARGIN, PAGE_H - 0.45 * inch, "SAMPLE DATA")
        _footer(c)
        c.restoreState()

    def _footer(c):
        c.setStrokeColor(RULE)
        c.line(MARGIN, 0.62 * inch, PAGE_W - MARGIN, 0.62 * inch)
        c.setFont("Helvetica", 7.5)
        c.setFillColor(MUTED)
        c.drawString(MARGIN, 0.45 * inch, foot)

    return first, later


# ---------------------------------------------------------------- main build
def build(payload, out_path):
    meta = payload.get("meta") or {}
    first, later = make_page_fns(meta)
    doc = BaseDocTemplate(out_path, pagesize=letter, leftMargin=MARGIN, rightMargin=MARGIN,
                          topMargin=0.8 * inch, bottomMargin=0.85 * inch,
                          title=f"Call Prep Brief - {clean(meta.get('company', ''))}",
                          author="Call-Prep Route skill")
    f1 = Frame(MARGIN, 0.85 * inch, CW, PAGE_H - 1.75 * inch - 0.95 * inch - 0.85 * inch + 0.2 * inch, id="f1", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    f2 = Frame(MARGIN, 0.85 * inch, CW, PAGE_H - 0.8 * inch - 0.85 * inch, id="f2", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id="first", frames=[f1], onPage=first),
                          PageTemplate(id="later", frames=[f2], onPage=later)])

    st = [NextPageTemplate("later"), Spacer(1, 0.15 * inch)]
    st += r_snapshot(payload.get("snapshot"), meta, payload.get("gaps"))
    st += r_meta_table(meta)
    st += r_route_status(payload)

    st.append(PageBreak())
    st += group_banner("A", "Know the account", "Earn your first five minutes with context.")
    st += r_s1(payload.get("s1_account_brief"))
    st += r_s2(payload.get("s2_pain_points"))
    st += r_s3(payload.get("s3_contact"), meta)

    st += group_banner("B", "Shape the conversation", "Turn research into words you will actually say.")
    st += r_s4(payload.get("s4_discovery"))
    st += r_s5(payload.get("s5_opener"))

    st += group_banner("C", "Map the deal", "Prepare for the room, not just the person.")
    st += r_s6(payload.get("s6_committee"))
    st += r_s7(payload.get("s7_objections"))
    st += r_s8(payload.get("s8_competitors"))
    st += r_s9(payload.get("s9_battlecard"), meta)

    st += group_banner("D", "Follow through", "Where most deals are won or quietly lost.", need=5.4)
    st += r_s10(payload.get("s10_followup"))

    st += r_gaps_sources(payload)
    doc.build(st, canvasmaker=NumberedCanvas)


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    with open(argv[1], encoding="utf-8") as fh:
        payload = json.load(fh)
    if not payload.get("meta", {}).get("prepared_on"):
        payload.setdefault("meta", {})["prepared_on"] = datetime.date.today().isoformat()
    warns = validate(payload)
    for w in warns:
        print("WARN:", w)
    if "--validate" in argv:
        return 1 if any("required" in w for w in warns) else 0
    if len(argv) < 3:
        print("Missing output path.")
        return 2
    build(payload, argv[2])
    print("Wrote", argv[2])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
