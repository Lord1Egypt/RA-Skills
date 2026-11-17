"""Diagram B: who can see what. A matrix is the honest encoding here: rows
are kinds of data, columns are who is asking."""
from __future__ import annotations

from ledger_report.bits import GLYPH, evidence_html, h, ht
from ledger_report.i18n import t

SUBJECTS = ("anonymous", "signed_in", "owner")
BAD = ("broken", "partial")


def is_problem(r: dict, statuses: dict) -> bool:
    if statuses.get(r.get("required_by")) in BAD:
        return True
    for subject, cell in r.get("cells", {}).items():
        if cell.get("conflicts"):
            return True
        if subject == "anonymous" and "allow" in (cell.get("read"), cell.get("write")):
            return True
    return False


def _row(r: dict, statuses: dict, plains: dict, ev: dict, lang: str) -> str:
    req = r.get("required_by")
    bad_req = statuses.get(req) in BAD
    name = t(lang, "all_data") if r["name"] == "*" else r["name"]
    th = f'<th scope="row">{ht(name, 40)}'
    if req:
        th += (f'<small class="req{" bad" if bad_req else ""}">{h(t(lang, "required"))}{ht(plains.get(req, ""), 40)} '
               f'{GLYPH.get(statuses.get(req, "unknown"), "")}</small>')
    th += "</th>"
    tds = []
    for s in SUBJECTS:
        cell = r.get("cells", {}).get(s, {"read": "unknown", "write": "unknown", "evidence": []})
        frame = bad_req and s != "owner" and "allow" in (cell.get("read"), cell.get("write"))
        cls = "cell" + (" frame" if frame else "") + (" conflict" if cell.get("conflicts") else "")
        body = "".join(f'<div class="perm"><span>{h(t(lang, "perm_" + p))}</span>'
                       f'<b class="{cell.get(p, "unknown")}">{h(t(lang, cell.get(p, "unknown")))}</b></div>'
                       for p in ("read", "write"))
        for cf in cell.get("conflicts", []):
            body += (f'<div class="conflict-note">⚠ {h(t(lang, "conflict"))}{h(t(lang, "colon"))}'
                     f'{h(t(lang, "probe_says", msg=cf["message"]))}</div>')
        if cell.get("from_probe"):
            body += f'<div class="probe-note dev-only">{h(t(lang, "probe"))}{h(t(lang, "colon"))}{ht(", ".join(cell["from_probe"]), 80)}</div>'
        body += evidence_html(cell.get("evidence", []), ev, lang)
        tds.append(f'<td class="{cls}">{body}</td>')
    return f"<tr>{th}{''.join(tds)}</tr>"


def render_access(ledger: dict, lang: str) -> str:
    resources = ledger["access"]["resources"]
    if not resources:
        return f'<p class="empty">{h(t(lang, "no_database"))}</p>'
    statuses = {p["id"]: p["status"] for p in ledger["promises"]}
    plains = {p["id"]: p["plain"] for p in ledger["promises"]}
    ev = ledger["evidence"]
    head = "<tr><th></th>" + "".join(f'<th>{h(t(lang, "subj_" + s))}<small>{h(t(lang, "subj_" + s + "_sub"))}</small></th>'
                                     for s in SUBJECTS) + "</tr>"
    problems = [r for r in resources if is_problem(r, statuses)]
    fine = [r for r in resources if not is_problem(r, statuses)]

    def table(rows) -> str:
        return (f'<div class="matrix-wrap"><table class="matrix"><thead>{head}</thead><tbody>'
                + "".join(_row(r, statuses, plains, ev, lang) for r in rows) + "</tbody></table></div>")

    out = table(problems) if problems else ""
    if fine:
        out += f'<details class="ok-rows"><summary>{h(t(lang, "ok_rows", n=len(fine)))}</summary>{table(fine)}</details>'
    return out
