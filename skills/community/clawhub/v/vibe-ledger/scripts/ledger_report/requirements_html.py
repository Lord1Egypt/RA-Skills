"""The 需求对照 / Your asks tab: every requirement the user gave, grouped by area, checked against the code."""
from __future__ import annotations

from collections import defaultdict
from pathlib import PurePosixPath

from ledger_report.bits import evidence_html, fmt_date, h, ht
from ledger_report.i18n import t
from requirements import FIXABLE, GLYPH, ORDER, counts


def _quote(ev: dict, i: str | None, n: int = 240) -> str:
    e = ev.get(i or "", {})
    return ht(e.get("quote", ""), n) if e.get("ok") else ""


def _card(x: dict, ev: dict, lang: str) -> str:
    s = x["status"]
    said = t(lang, "said_on", who=t(lang, "said_by_user"), date=fmt_date(x.get("said_at")))
    out = [f'<article class="card req-card s-{s}" data-rstatus="{s}" id="{h(x["id"])}">',
           f'<div class="card-head"><span class="pill s-{s}">{GLYPH[s]} {h(t(lang, "r_status_" + s))}</span>'
           f'<span class="origin">{h(said)}</span></div>',
           f'<p class="promise">{h(x["plain"])}</p>']
    q = _quote(ev, x["source"][0])
    if q:
        out.append(f'<blockquote class="req-quote">{q}</blockquote>')
    unverified = bool(x.get("downgraded_from"))
    verdict = (f'<span class="uc-label">{h(t(lang, "unverified_claim"))}</span><span class="unverified-claim">{h(x["verdict_plain"])}</span>'
               if unverified else h(x["verdict_plain"]))
    out.append(f'<p class="verdict">{verdict}</p>')
    out.append(f'<p class="verdict-dev dev-only">{h(x["verdict_dev"])}</p>')
    if s == "changed" or (unverified and x.get("changed_to")):
        out.append(f'<p class="req-line">{h(t(lang, "r_changed_to", text=x.get("changed_to", "")))}</p>')
        agreed = [ev[i] for i in x.get("agreed_in", []) if ev.get(i, {}).get("ok")]
        if agreed:
            out.append(f'<p class="req-line ok">{h(t(lang, "r_agreed", date=fmt_date(agreed[0].get("ts"))))}</p>')
        elif s == "changed":
            out.append(f'<p class="req-line warn">{h(t(lang, "r_not_agreed"))}</p>')
    if s == "superseded":
        sb = ev.get(x.get("superseded_by") or "", {})
        out.append(f'<p class="req-line">{h(t(lang, "r_superseded_by", date=fmt_date(sb.get("ts"))))}</p>'
                   f'<blockquote class="req-quote">{_quote(ev, x.get("superseded_by"))}</blockquote>')
    if x.get("absent_verified"):
        terms = t(lang, "sep").join(f"“{w}”" for w in x["searched"])
        out.append(f'<p class="req-line">{h(t(lang, "r_searched", terms=terms))}</p>')
    if unverified:
        old = t(lang, "r_status_" + x["downgraded_from"])
        out.append(f'<p class="note">{h(t(lang, "downgraded", old=old))}</p>'
                   f'<p class="note dev-only">{ht(x.get("downgrade_reason", ""), 300)}</p>')
    if x.get("files"):
        chips = "".join(f'<button type="button" class="req-file" data-file="{h(f)}" title="{h(f)}">'
                        f'{h(PurePosixPath(f).name)}</button>' for f in x["files"])
        out.append(f'<div class="req-files"><span>{h(t(lang, "r_files"))}</span>{chips}</div>')
    ids = list(x["source"]) + list(x.get("evidence", [])) + list(x.get("agreed_in", []))
    if x.get("superseded_by"):
        ids.append(x["superseded_by"])
    out.append(evidence_html(list(dict.fromkeys(ids)), ev, lang))
    if s in FIXABLE and x.get("fix_prompt"):
        out.append(f'<button class="copy" type="button" data-text="{h(x["fix_prompt"])}" '
                   f'data-done="{h(t(lang, "copied"))}">{h(t(lang, "copy_fix"))}</button>')
    out.append("</article>")
    return "".join(out)


def _coverage(doc: dict, lang: str) -> str:
    cov = doc["coverage"]
    items = [h(t(lang, "r_cov_messages", n=cov["messages"], cited=cov["cited"]))]
    if cov["skipped"]:
        parts = t(lang, "sep").join(t(lang, "r_skip_" + k, n=v) for k, v in cov["skipped"].items())
        items.append(h(t(lang, "r_cov_skipped", parts=parts)))
    if cov.get("noise"):
        items.append(h(t(lang, "r_cov_noise", n=cov["noise"])))
    out = [f"<li>{x}</li>" for x in items]
    un = cov["unaccounted"]
    if un:
        sub = "".join(f'<li><span class="origin">{h(fmt_date(u["ts"]))}</span> {ht(" ".join(u["text"].split()), 200)}</li>'
                      for u in un[:40]) + ("<li>…</li>" if len(un) > 40 else "")
        out.append(f'<li class="warn">{h(t(lang, "r_cov_unaccounted", n=len(un)))}<ul>{sub}</ul></li>')
    failed = [(k, e) for k, e in doc["evidence"].items() if not e.get("ok")]
    if failed:
        sub = "".join(f'<li><code>{h(k)}</code> {ht(e.get("reason", ""), 160)}</li>' for k, e in failed[:30])
        out.append(f'<li>{h(t(lang, "cov_failed", n=len(failed)))}<ul>{sub}</ul></li>')
    if doc.get("rejected"):
        sub = "".join(f'<li>{ht(r.get("plain") or r.get("id", ""), 120)} — {ht(r.get("reason", ""), 160)}</li>'
                      for r in doc["rejected"][:30])
        out.append(f'<li>{h(t(lang, "r_cov_rejected", n=len(doc["rejected"])))}<ul>{sub}</ul></li>')
    return f'<ul class="coverage">{"".join(out)}</ul>'


def render_requirements(doc: dict, lang: str) -> str:
    head = f'<h2>{h(t(lang, "r_title"))}</h2><p class="sub">{h(t(lang, "r_intro"))}</p>'
    if doc.get("none"):
        why = t(lang, "r_none_typed", n=doc["threads"]) if doc.get("threads") else t(lang, "r_none_tx")
        return f'<div class="wrap">{head}<p class="empty">{h(why)}</p></div>'
    reqs, ev = doc["requirements"], doc["evidence"]
    c = counts(doc)
    cov = doc["coverage"]
    summary = t(lang, "r_summary", messages=cov["messages"], n=len(reqs), skipped=sum(cov["skipped"].values()))
    if cov["unaccounted"]:
        summary += t(lang, "r_summary_unaccounted", n=len(cov["unaccounted"]))
    problems = sum(c[s] for s in ("missing", "partial", "changed"))
    # the counts are the filters: one row, each status with its label and number
    filters = (f'<button type="button" class="count filter on" data-rfilter="all">{h(t(lang, "filter_all"))} <b>{len(reqs)}</b></button>'
               + (f'<button type="button" class="count filter" data-rfilter="problems">{h(t(lang, "r_filter_problems"))} '
                  f'<b>{problems}</b></button>' if problems else "")
               + "".join(f'<button type="button" class="count filter s-{s}" data-rfilter="{s}">{GLYPH[s]} '
                         f'{h(t(lang, "r_status_" + s))} <b>{c[s]}</b></button>' for s in ORDER if c[s]))
    body = [head, f'<p class="summary">{h(summary)}</p>',
            f'<div class="counts req-filters">{filters}</div>' if reqs else ""]
    if not reqs:
        body.append(f'<p class="empty">{h(t(lang, "r_none"))}</p>')
    groups: dict[str, list] = defaultdict(list)
    for x in reqs:
        groups[x.get("area", "").strip() or t(lang, "r_area_other")].append(x)
    bad = lambda xs: sum(1 for x in xs if x["status"] in ("missing", "partial", "changed"))  # noqa: E731
    for area, xs in sorted(groups.items(), key=lambda kv: (-bad(kv[1]), -len(kv[1]), kv[0])):
        xs.sort(key=lambda x: (ORDER.index(x["status"]), x.get("said_at") or ""))
        g = counts({"requirements": xs})
        tally = " ".join(f"{GLYPH[s]}{g[s]}" for s in ORDER if g[s])
        body.append(f'<section class="req-area"><h3>{h(area)} <span class="req-tally">{h(tally)}</span></h3>'
                    f'<div class="cards">{"".join(_card(x, ev, lang) for x in xs)}</div></section>')
    body.append(f'<section><h2>{h(t(lang, "r_cov_title"))}</h2>{_coverage(doc, lang)}</section>')
    return f'<div class="wrap">{"".join(body)}</div>'


def panel_data(doc: dict | None, lang: str) -> dict | None:
    """What the flowchart's side panel shows: the counts, and each file's requirements."""
    if doc is None:
        return None
    by_file: dict[str, list] = defaultdict(list)
    for x in doc.get("requirements", []):
        for f in x.get("files", []):
            by_file[f].append({"id": x["id"], "glyph": GLYPH[x["status"]], "plain": x["plain"]})
    c = counts(doc)
    none = t(lang, "r_none_typed", n=doc["threads"]) if doc.get("threads") else t(lang, "r_none_tx")
    line = (none if doc.get("none") else
            "  ".join(f"{GLYPH[s]} {t(lang, 'r_status_' + s)} {c[s]}" for s in ORDER if c[s]) or t(lang, "r_none"))
    return {"line": line, "by_file": by_file,
            "unaccounted": len(doc.get("coverage", {}).get("unaccounted", []))}
