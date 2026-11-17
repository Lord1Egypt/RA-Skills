"""Render the verified ledger as one self-contained, offline HTML page."""
from __future__ import annotations

import os
from collections import Counter
from datetime import datetime
from pathlib import Path

from common import slugify
from ledger_report.access_html import render_access
from ledger_report.bits import GLYPH, ORDER, evidence_html, fmt_date, h, ht
from ledger_report.graph_page import dagre_source, data_script, render_graph_tab
from ledger_report.i18n import t
from ledger_report.map_svg import render_map
from ledger_report.paths_svg import render_paths
from ledger_report.requirements_html import render_requirements
from ledger_report.timeline_svg import render_timeline
from redact import find_secrets

ASSETS = Path(__file__).resolve().parent / "ledger_report" / "assets"
SECTIONS = (("sec_map", ("where_data", "what_costs"), "map"),
            ("sec_access", ("who_can_see",), "access"),
            ("sec_timeline", ("what_breaks", "open_debts"), "timeline"))
FIXABLE = ("broken", "partial", "pending")
DAGRE_SLOT = "<!--VL_DAGRE-->"
STORES = ("database", "storage")


def counts(ledger: dict) -> dict:
    c = Counter(p["status"] for p in ledger["promises"])
    return {s: c.get(s, 0) for s in ORDER}


def summaries(ledger: dict, lang: str, has_transcripts: bool = True) -> dict:
    """Deterministic one-liners built from verified data only."""
    sep = t(lang, "sep")
    nodes = ledger["map"]["nodes"]
    stores = [n["label"] for n in nodes if n["kind"] in STORES]
    sent = [n["label"] for n in nodes if n["kind"] == "third_party"]
    paid = [n["label"] for n in nodes if n.get("paid")]
    where = t(lang, "sum_where", stores=sep.join(stores)) if stores else t(lang, "sum_where_none")
    if sent:
        where += t(lang, "sum_sent", others=sep.join(sent))
    res = ledger["access"]["resources"]
    anon = sum(1 for r in res if r["cells"].get("anonymous", {}).get("read") == "allow")
    conflicts = sum(len(c.get("conflicts", [])) for r in res for c in r["cells"].values())
    if not has_transcripts:  # with nothing to reconcile, "0 broken" would read as "all fine"
        breaks = debts = t(lang, "sum_no_tx")
    else:
        breaks = t(lang, "sum_breaks", comp=sum(1 for c in ledger["compromises"] if c.get("still_present") is True),
                   broken=sum(1 for p in ledger["promises"] if p["status"] == "broken"))
        debts = t(lang, "sum_debts", n=sum(1 for p in ledger["promises"]
                                          if p["type"] == "deferred" and p["status"] == "pending"))
    return {
        "where_data": where,
        "what_costs": t(lang, "sum_costs", paid=sep.join(paid)) if paid else t(lang, "sum_costs_none"),
        "who_can_see": t(lang, "sum_access", n=len(res), anon=anon, conflicts=conflicts) if res else t(lang, "no_database"),
        "what_breaks": breaks,
        "open_debts": debts,
    }


def _origin(p: dict, ev: dict, lang: str) -> str:
    for i in p["source"]:
        e = ev.get(i, {})
        if e.get("ok"):
            who = t(lang, "said_by_user") if e.get("role") == "user" else t(lang, "said_by_ai")
            return t(lang, "said_on", who=who, date=fmt_date(e.get("ts")))
    return ""


def _verdict(p: dict, lang: str, text: str) -> str:
    """A verdict the model wrote for a status that did not survive verification is shown as unverified."""
    if p.get("downgraded_from"):
        return f'<span class="uc-label">{h(t(lang, "unverified_claim"))}</span><span class="unverified-claim">{h(text)}</span>'
    return h(text)


def _card(p: dict, ev: dict, lang: str) -> str:
    s = p["status"]
    out = [f'<article class="card s-{s}" id="{h(p["id"])}">',
           f'<div class="card-head"><span class="pill s-{s}">{GLYPH[s]} {h(t(lang, "status_" + s))}</span>'
           f'<span class="origin">{h(_origin(p, ev, lang))}</span></div>',
           f'<p class="promise">{h(p["plain"])}</p>',
           f'<p class="verdict">{_verdict(p, lang, p["verdict_plain"])}</p>',
           f'<p class="verdict-dev dev-only">{_verdict(p, lang, p["verdict_dev"])}</p>']
    if p.get("downgraded_from"):
        old = t(lang, "status_" + p["downgraded_from"])
        out.append(f'<p class="note">{h(t(lang, "downgraded", old=old))}</p>')
    if p.get("conflict_with"):
        out.append(f'<p class="note">{h(t(lang, "conflict"))}{h(t(lang, "colon"))}{h(", ".join(p["conflict_with"]))}</p>')
    out.append(evidence_html(p["source"] + p["evidence"], ev, lang))
    if s in FIXABLE and p.get("fix_prompt"):
        out.append(f'<button class="copy" type="button" data-text="{h(p["fix_prompt"])}" '
                   f'data-done="{h(t(lang, "copied"))}">{h(t(lang, "copy_fix"))}</button>')
    out.append("</article>")
    return "".join(out)


def _ledger_table(ledger: dict, lang: str) -> str:
    ev = ledger["evidence"]
    rows = []
    for p in sorted(ledger["promises"], key=lambda p: ORDER.index(p["status"])):
        s = p["status"]
        rows.append(f'<tr data-status="{s}"><td><span class="pill s-{s}">{GLYPH[s]} {h(t(lang, "status_" + s))}</span></td>'
                    f'<td>{h(p["plain"])}{evidence_html(p["source"] + p["evidence"], ev, lang)}</td>'
                    f'<td>{h(_origin(p, ev, lang))}</td>'
                    f'<td>{_verdict(p, lang, p["verdict_plain"])}<div class="dev-only">{_verdict(p, lang, p["verdict_dev"])}</div></td></tr>')
    if not rows:
        return f'<p class="empty">{h(t(lang, "no_promises"))}</p>'
    c = counts(ledger)
    buttons = (f'<button type="button" class="filter on" data-filter="all">{h(t(lang, "filter_all"))}</button>'
               + "".join(f'<button type="button" class="filter" data-filter="{s}">{GLYPH[s]} {c[s]}</button>'
                         for s in ORDER if c[s]))
    head = "".join(f"<th>{h(t(lang, k))}</th>" for k in ("col_status", "col_promise", "col_who", "col_verdict"))
    return (f'<div class="filters">{buttons}</div><div class="matrix-wrap"><table class="ledger">'
            f'<thead><tr>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>')


def _coverage(ledger: dict, run: dict, probes: dict, lang: str, graph_cov: dict | None = None) -> str:
    s = run.get("sessions", {})
    by = s.get("by_agent", {})
    li = [h(t(lang, "cov_sessions", claude=by.get("claude-code", 0), codex=by.get("codex", 0)))]
    if s.get("archived_threads"):
        li.append(h(t(lang, "cov_archived", n=s["archived_threads"])))
    ignored = sum((s.get("ignored_types") or {}).values())
    if ignored:
        li.append(h(t(lang, "cov_ignored", n=ignored)))
    if s.get("bad_lines"):
        li.append(h(t(lang, "cov_bad", n=s["bad_lines"])))
    un = run.get("unattributed", [])
    if un:
        files = "".join(f"<li><code>{ht(f, 90)}</code></li>" for f in un[:20]) + ("<li>…</li>" if len(un) > 20 else "")
        li.append(f'{h(t(lang, "cov_unattributed", n=len(un)))}<ul>{files}</ul>')
    li.append(h(t(lang, "cov_probes", ran=", ".join(probes.get("ran", [])) or t(lang, "cov_none"))))
    if probes.get("skipped"):
        skipped = t(lang, "sep").join(
            t(lang, "cov_skip_needs", probe=x["probe"], needs=", ".join(x["needs"])) if x.get("needs")
            else f'{x["probe"]} ({x["reason"]})' for x in probes["skipped"])
        li.append(h(t(lang, "cov_skipped", skipped=skipped)))
    unsupported = probes.get("stack", {}).get("unsupported", [])
    items = [f"<li>{x}</li>" for x in li]
    if unsupported:
        items.append(f'<li class="warn">{h(t(lang, "cov_unsupported", stacks=", ".join(unsupported)))}</li>')
    if graph_cov:
        ex = graph_cov.get("excluded", {})
        if ex.get("tests") or ex.get("config"):
            items.append(f'<li>{h(t(lang, "cov_graph_excluded", tests=ex.get("tests", 0), config=ex.get("config", 0)))}</li>')
        if ex.get("ignored by git"):
            items.append(f'<li>{h(t(lang, "cov_graph_ignored", n=ex["ignored by git"]))}</li>')
        unres = graph_cov.get("unresolved", [])
        if unres:
            sub = "".join(f'<li><code>{ht(u["from"], 80)}:{u["line"]}</code> → <code>{ht(u["spec"], 80)}</code></li>'
                          for u in unres[:30])
            items.append(f'<li>{h(t(lang, "cov_unresolved", n=len(unres)))}<ul>{sub}</ul></li>')
        bad = ([(r["path"], r["reason"]) for r in graph_cov.get("rejected", [])]
               + [(" · ".join(x for x in (d["path"], d["name"]) if x), d["reason"]) for d in graph_cov.get("dropped", [])])
        if bad:
            sub = "".join(f"<li><code>{ht(a, 90)}</code> — {ht(b, 160)}</li>" for a, b in bad[:30])
            items.append(f'<li>{h(t(lang, "cov_explain_dropped", n=len(bad)))}<ul>{sub}</ul></li>')
    failed = [(k, e) for k, e in ledger["evidence"].items() if not e.get("ok")]
    if failed:
        sub = "".join(f'<li><code>{h(k)}</code> {ht(e.get("reason", ""), 160)}</li>' for k, e in failed[:30])
        items.append(f'<li>{h(t(lang, "cov_failed", n=len(failed)))}<ul>{sub}</ul></li>')
    rejected = ledger.get("rejected", [])
    if rejected:
        sub = "".join(f'<li>{ht(r.get("plain") or r.get("id", ""), 120)} — {ht(r.get("reason", ""), 160)}</li>'
                      for r in rejected[:30])
        items.append(f'<li>{h(t(lang, "cov_rejected", n=len(rejected)))}<ul>{sub}</ul></li>')
    warnings = s.get("warnings", [])
    if warnings:
        sub = "".join(f"<li>{ht(w, 200)}</li>" for w in warnings[:20])
        items.append(f'<li class="warn">{h(t(lang, "cov_warnings"))}<ul>{sub}</ul></li>')
    return f'<ul class="coverage">{"".join(items)}</ul>'


def assert_no_secrets(doc: str) -> None:
    leaks = find_secrets(doc)
    if leaks:
        kinds = ", ".join(sorted({k for _, _, k in leaks}))
        raise RuntimeError(f"refusing to write the report: it would contain {len(leaks)} unmasked secret(s) ({kinds})")


def render_html(ledger: dict, run: dict, probes: dict, lang: str, graph_data: dict | None = None,
                requirements: dict | None = None) -> str:
    ev = ledger["evidence"]
    c = counts(ledger)
    s = run.get("sessions", {})
    has_tx = bool(s.get("records"))
    sums = summaries(ledger, lang, has_tx)
    sub = (t(lang, "subtitle", threads=s.get("threads", 0), start=fmt_date(s.get("earliest"))[:10],
             end=fmt_date(s.get("latest"))[:10]) if has_tx else t(lang, "subtitle_none"))
    name = run.get("project_name", "")
    tabbed = graph_data is not None
    title = f'<h1>{h(t(lang, "title", name=name))}</h1>'
    toggle = (f'<button id="view-toggle" class="toggle" type="button" aria-pressed="false">'
              f'<span class="plain-only">{h(t(lang, "view_dev"))}</span><span class="dev-only">{h(t(lang, "view_plain"))}</span></button>')
    counts_html = ('<div class="counts">'
                   + "".join(f'<span class="count s-{st}">{GLYPH[st]} {h(t(lang, "status_" + st))} <b>{c[st]}</b></span>' for st in ORDER)
                   + "</div>" if has_tx else f'<p class="note">{h(t(lang, "no_tx_counts"))}</p>')
    body = [f'<header>{"" if tabbed else title}<p class="sub">{h(sub)}</p>{"" if tabbed else toggle}{counts_html}</header>']
    diagrams = {"map": render_map(ledger, lang), "access": render_access(ledger, lang),
                "timeline": render_timeline(ledger, lang, has_tx)}
    for sec_title, questions, key in SECTIONS:
        part = [f"<section><h2>{h(t(lang, sec_title))}</h2>"]
        part += [f'<p class="summary"><b>{h(t(lang, "q_" + q))}{h(t(lang, "colon"))}</b>{h(sums[q])}</p>' for q in questions]
        part.append(diagrams[key])
        cards = sorted((p for p in ledger["promises"] if p["question"] in questions), key=lambda p: ORDER.index(p["status"]))
        if cards:
            part.append('<div class="cards">' + "".join(_card(p, ev, lang) for p in cards) + "</div>")
        part.append("</section>")
        body.append("".join(part))
    body.append(f'<section class="dev-only"><h2>{h(t(lang, "sec_paths"))}</h2>{render_paths(ledger, lang)}</section>')
    body.append(f'<section><h2>{h(t(lang, "sec_ledger"))}</h2>{_ledger_table(ledger, lang)}</section>')
    graph_cov = graph_data.get("coverage") if tabbed else None
    body.append(f'<section><h2>{h(t(lang, "sec_coverage"))}</h2>{_coverage(ledger, run, probes, lang, graph_cov)}</section>')
    css = (ASSETS / "report.css").read_text(encoding="utf-8")
    if tabbed:
        css += "\n" + (ASSETS / "graph.css").read_text(encoding="utf-8")
        if requirements is not None:
            css += "\n" + (ASSETS / "requirements.css").read_text(encoding="utf-8")
    js = (ASSETS / "report.js").read_text(encoding="utf-8")
    html_lang = "zh-CN" if lang == "zh" else "en"
    head = (f'<!doctype html><html lang="{html_lang}"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{h(t(lang, "doc_title", name=name))}</title><style>{css}</style></head>')
    if not tabbed:
        doc = head + f'<body><div class="wrap">{"".join(body)}</div><script>{js}</script></body></html>'
        assert_no_secrets(doc)
        return doc
    names = (("graph", "g_tab_graph"),) + ((("requirements", "r_tab"),) if requirements is not None else ()) + (
        ("overview", "g_tab_overview"),)
    tabs = "".join(f'<button type="button" class="vl-tab{" on" if key == "graph" else ""}" data-tab="{key}">{h(t(lang, label))}</button>'
                   for key, label in names)
    req_tab = ("" if requirements is None else
               f'<section id="tab-requirements" class="vl-tabpanel" hidden>{render_requirements(requirements, lang)}</section>')
    top = (f'<header class="vl-top">{title}<nav class="vl-tabs">{tabs}</nav>'
           f'<input id="vlg-search" type="search" list="vlg-files" placeholder="{h(t(lang, "g_search"))}" autocomplete="off">'
           f'<datalist id="vlg-files"></datalist>{toggle}</header>')
    gjs = (ASSETS / "graph.js").read_text(encoding="utf-8")
    doc = (head + f'<body class="tabbed">{top}<section id="tab-graph" class="vl-tabpanel">{render_graph_tab(lang, bool(graph_data.get("areas")))}</section>'
           f'{req_tab}<section id="tab-overview" class="vl-tabpanel" hidden><div class="wrap">{"".join(body)}</div></section>'
           f'{data_script(graph_data)}<script>{js}</script>{DAGRE_SLOT}<script>{gjs}</script></body></html>')
    assert_no_secrets(doc)  # the vendored library is static, so it goes in after the check
    return doc.replace(DAGRE_SLOT, "<script>" + dagre_source() + "</script>", 1)


def _unused(path: Path) -> Path:
    """`path`, or `name-2.html`, `name-3.html`… — never overwrite another report."""
    n = 2
    candidate = path
    while candidate.exists():
        candidate = path.with_name(f"{path.stem}-{n}{path.suffix}")
        n += 1
    return candidate


def deliver(html: str, run_dir, project_name: str, out_dir=None) -> Path:
    """Write the report to the run folder and to where the user will look."""
    run_dir = Path(run_dir)
    (run_dir / "report.html").write_text(html, encoding="utf-8")
    name = f"vibe-ledger-{slugify(project_name)}-{datetime.now().strftime('%Y%m%d-%H%M')}.html"
    env = os.environ.get("VIBE_LEDGER_OUT_DIR")
    if out_dir:
        targets = [(Path(out_dir), True)]
    elif env:
        targets = [(Path(env), True)]
    else:
        targets = [(Path.home() / "Desktop", False), (Path.home() / "Downloads", False)]
    for folder, create in targets:
        try:
            if create:
                folder.mkdir(parents=True, exist_ok=True)
            if folder.is_dir():
                target = _unused(folder / name)
                target.write_text(html, encoding="utf-8")
                return target
        except OSError:
            continue  # e.g. macOS privacy settings can block Desktop/Downloads
    return run_dir / "report.html"
