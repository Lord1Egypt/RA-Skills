"""Offline, escaped HTML presentation of the same validated universe as MD/TXT."""

from html import escape
from pathlib import Path

from display_core import display_view


def render_html(universe: dict, report: dict, language: str | None = None) -> str:
    # Imported at call time: universe_core owns the shared presentation vocabulary and writer.
    from universe_core import (
        _brief_reason,
        _glossed,
        _measurement_diagnostic,
        artifact_stem,
        load_lexicon,
        report_language,
    )

    language = language or report_language(universe)
    lex = load_lexicon(language)
    translations = universe.get("report_translations", {}).get(language, {})
    stem = artifact_stem(universe)
    labels, grouped = display_view(universe)
    members = universe["members"]
    references = universe.get("coverage_plan", {}).get("references", [])
    quality = report["stats"].get("quality") or {}
    held = {m["ticker"] for m in universe.get("heavy_base", {}).get("members", [])}

    def text(value: object) -> str:
        original = str(value)
        return escape(translations.get(original, original), quote=True)

    def brief(row: dict) -> str:
        original = row.get("reason_summary") or _brief_reason(row)
        value = _brief_reason({"reason_summary": translations[original]}) \
            if original in translations else _brief_reason(row)
        return escape(value.replace("\\|", "|"))

    def link(extension: str, label: str) -> str:
        return f'<a href="{escape(stem + extension, quote=True)}" download>{escape(label)}</a>'

    title = lex["title"].format(market=universe["market"].upper())
    status = "PARTIAL" if universe.get("delivery", {}).get("status") == "partial" else (
        "PASS" if report["passed"] else "FAIL"
    )
    # Archived under-target replay also needs a visible incomplete-delivery notice.
    legacy_shortfall = universe.get("selection_model") != "coverage_first" and (
        len(members) < universe.get("limits", {}).get("target_count", 0)
    )
    if legacy_shortfall:
        status = "PARTIAL"
    css = (Path(__file__).resolve().parents[1] / "assets/report.css").read_text(encoding="utf-8")
    lines = [
        '<!doctype html>',
        f'<html lang="{escape(language, quote=True)}"><head><meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        '<meta name="color-scheme" content="dark">',
        f'<title>{escape(title)} · {escape(universe["profile"].title())}</title>',
        f'<style>{css}</style></head><body><main>',
        '<div class="brand">ticker-universe-builder <span>/ universe report</span></div>',
        '<header class="hero"><div>',
        f'<h1>{escape(title)}</h1><span class="profile">'
        f'{text(lex.get("profile." + universe["profile"], universe["profile"]))}</span>',
        '</div>',
        f'<span class="verdict {status.lower()}">{escape(lex["label.validation"])}'
        f' · {status}</span></header>',
        '<p class="meta">'
        f'{escape(lex["label.facts_as_of"])} {escape(universe["source_as_of"])}'
        f' · <code>{escape(universe["version_hash"])}</code></p>',
        '<nav class="files" aria-label="Artifacts">',
        link(f'.{language}.md', 'Markdown'), link('.txt', 'TradingView TXT'),
        link('.json', 'JSON'), link('.validation.json', lex['label.validation']),
        '</nav>',
        '<div class="stats">',
    ]
    for count, label in (
        (len(members), lex["label.tickers"]),
        (len(references), lex["html.references"]),
        (sum(any("asset_id" in r for r in rows) for rows in grouped.values()), lex["label.themes"]),
        (len(members) + len(references), lex["html.symbols"]),
    ):
        lines.append(f'<div><strong>{count}</strong><span>{escape(label)}</span></div>')
    lines.append('</div>')
    if status == "PARTIAL":
        delivery = universe.get("delivery", {})
        target = delivery.get("required_entities", universe["limits"]["target_count"])
        lines.append('<p class="notice partial">PARTIAL: '
                     f'{len(members)} / {target}; '
                     f'{escape(lex["column.count"])} −{target - len(members)}. '
                     'Growth/size target not met; see validation and resume research.</p>')
    if declaration := universe.get("market_spec"):
        lines.append(f'<p class="notice">{escape(lex["label.market_rules"])}: '
                     f'{text(declaration["label"])} · '
                     f'{text(", ".join(declaration["venues"]))}</p>')
    if expansion := quality.get("expansion"):
        lines.append('<p class="expansion">Heavy → Max · '
                     f'{expansion["heavy_entities"]} → {len(members)} · '
                     f'+{expansion["added_beta"]} Beta ({expansion["growth"]:.1%})</p>')
    if report.get("warnings"):
        lines.append(f'<aside class="notice"><h2>{escape(lex["section.warnings"])}</h2><ul>')
        lines.extend(f'<li>{escape(str(w))}</li>' for w in report["warnings"])
        lines.append('</ul></aside>')
    if review := report.get("maintenance"):
        lines.append(f'<aside class="notice"><h2>{escape(lex["section.review"])}</h2><ul>')
        for key in ("depth", "turnover", "added", "removed", "deferred"):
            value = {
                "depth": lex.get("depth." + review["review_depth"], review["review_depth"]),
                "turnover": f'{review["turnover"]:.1%}',
                "added": ", ".join(review["added"]) or lex["value.none"],
                "removed": ", ".join(review["removed"]) or lex["value.none"],
                "deferred": len(review["deferred"]),
            }[key]
            lines.append(f'<li>{escape(lex["review." + key])}: {text(value)}</li>')
        lines.append('</ul></aside>')

    def cards(reference: bool) -> None:
        section = lex["html.references"] if reference else lex["section.members"]
        lines.extend([f'<h2 class="section-title">{escape(section)}</h2>', '<div class="grid">'])
        for code in sorted(grouped):
            rows = [r for r in grouped[code] if ("asset_id" not in r) == reference]
            if not rows:
                continue
            kind = "reference" if reference else "member"
            lines.extend([
                f'<section class="card" data-group="{escape(code, quote=True)}">',
                '<header><span class="code">' + escape(code) + '</span>'
                f'<span class="count">{len(rows)}</span></header>',
                f'<h3>{text(labels[code]).replace("_", " ")}</h3><div class="entries">',
            ])
            for row in sorted(rows, key=lambda r: r["ticker"]):
                venue, symbol = row["ticker"].split(":", 1)
                role = row.get("kind", "reference") if reference else _glossed(
                    lex, "role", row["role"]
                )
                added = held and not reference and row["ticker"] not in held
                lines.extend([
                    f'<article class="entry" data-kind="{kind}" '
                    f'data-ticker="{escape(row["ticker"], quote=True)}">',
                    f'<div class="ticker"><b>{escape(symbol)}</b><small>{escape(venue)}</small>',
                    f'<span class="role">{escape(role)}</span></div>',
                ])
                if not reference:
                    lines.append(f'<div class="name">{text(row["name"])}</div>')
                if added:
                    lines.append(f'<span class="added">+ {escape(lex["html.new_beta"])}</span>')
                description = text(row.get("observes", "")) if reference else brief(row)
                lines.append(f'<p class="description">{description}</p></article>')
            lines.append('</div></section>')
        lines.append('</div>')

    cards(False)
    if references:
        cards(True)
    notes = [text(n) for n in universe.get("notes", []) if not _measurement_diagnostic(n)]
    if notes:
        lines.extend(['<details class="notes">',
                      f'<summary>{escape(lex["html.notes"])}</summary><ul>',
                      *[f'<li>{n}</li>' for n in notes], '</ul></details>'])
    lines.extend([
        f'<footer>{escape(lex["html.notes"])} · ' + link('.json', 'JSON')
        + ' · ' + link('.validation.json', lex['label.validation']) + '</footer>',
        '</main></body></html>',
    ])
    return '\n'.join(lines) + '\n'
