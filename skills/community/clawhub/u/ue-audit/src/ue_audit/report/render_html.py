"""Self-contained HTML report renderer."""

from __future__ import annotations

import html
from pathlib import Path

from .model import Report, Severity


_CSS = """
:root { color-scheme: light; }
* { box-sizing: border-box; }
body { margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; color: #1f2937; background: #f8fafc; }
main { max-width: 1120px; margin: 0 auto; padding: 32px 20px 64px; }
h1 { font-size: 28px; margin: 0 0 4px; }
h2 { font-size: 20px; margin: 32px 0 12px; border-bottom: 1px solid #e5e7eb; padding-bottom: 6px; }
.meta { color: #4b5563; font-size: 13px; line-height: 1.7; }
.cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px; margin: 20px 0; }
.card { background: #fff; border: 1px solid #e5e7eb; border-radius: 10px; padding: 14px; }
.card .num { font-size: 26px; font-weight: 700; }
.card .label { color: #6b7280; font-size: 12px; text-transform: uppercase; letter-spacing: .04em; }
table { width: 100%; border-collapse: collapse; background: #fff; border: 1px solid #e5e7eb; border-radius: 8px; overflow: hidden; font-size: 13px; }
th, td { text-align: left; padding: 9px 10px; border-bottom: 1px solid #eef2f7; vertical-align: top; }
th { background: #f3f4f6; font-weight: 600; }
tr:last-child td { border-bottom: none; }
.sev-blocker, .sev-error { color: #b91c1c; font-weight: 600; }
.sev-warning { color: #b45309; font-weight: 600; }
.sev-info { color: #1d4ed8; }
.status-pass { color: #047857; }
.status-fail, .status-error { color: #b91c1c; }
.status-warn { color: #b45309; }
.status-skip, .status-unknown { color: #6b7280; }
.notice { background: #fffbeb; border: 1px solid #fde68a; border-radius: 8px; padding: 12px 14px; }
.mono { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 12px; }
ul { line-height: 1.8; }
footer { margin-top: 32px; color: #6b7280; font-size: 12px; }
"""


def _e(value: object) -> str:
    return html.escape(str(value if value is not None else ""))


def render_html(report: Report, path: Path) -> Path:
    data = report.to_dict()
    summary = data["summary"]

    cards = []
    for severity in Severity:
        cards.append(
            f'<div class="card"><div class="num">{summary["severity"][severity.value]}</div>'
            f'<div class="label">{_e(severity.value)}</div></div>'
        )
    cards.append(
        f'<div class="card"><div class="num">{summary["check_count"]}</div>'
        f'<div class="label">checks</div></div>'
    )

    check_rows = []
    for check in data["checks"]:
        check_rows.append(
            "<tr>"
            f"<td class=\"mono\">{_e(check['check_id'])}</td>"
            f"<td>{_e(check['title'])}</td>"
            f"<td class=\"status-{_e(check['status'])}\">{_e(check['status'])}</td>"
            f"<td>{_e(check['summary'])}</td>"
            "</tr>"
        )
    if not check_rows:
        check_rows.append('<tr><td colspan="4">No checks.</td></tr>')

    finding_rows = []
    for finding in data["findings"]:
        finding_rows.append(
            "<tr>"
            f"<td class=\"mono\">{_e(finding['id'])}</td>"
            f"<td class=\"mono\">{_e(finding['check_id'])}</td>"
            f"<td class=\"sev-{_e(finding['severity'])}\">{_e(finding['severity'])}</td>"
            f"<td>{_e(finding['title'])}</td>"
            f"<td class=\"mono\">{_e(finding['asset'])}</td>"
            f"<td>{_e(finding['message'])}</td>"
            "</tr>"
        )
    if not finding_rows:
        finding_rows.append('<tr><td colspan="6">No findings.</td></tr>')

    limitations = "".join(f"<li>{_e(item)}</li>" for item in data["limitations"])
    proof = data["readonly_proof"]
    proof_html = (
        f"<p><strong>Content equal:</strong> {_e(proof.get('content_equal'))} &nbsp; "
        f"<strong>Metadata equal:</strong> {_e(proof.get('metadata_equal'))} &nbsp; "
        f"<strong>Unknown files:</strong> {_e(proof.get('unknown_count'))}</p>"
        f"<p><strong>During-write monitor:</strong> {_e(proof.get('during_write_monitor', 'unknown'))}</p>"
        f"<p class=\"notice\">{_e(proof.get('statement', ''))}</p>"
    )

    document = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>UE project audit - {_e(data['project'].get('name', ''))}</title>
<style>{_CSS}</style>
</head>
<body>
<main>
<h1>UE project audit: {_e(data['project'].get('name', ''))}</h1>
<div class="meta">
  Run ID: <span class="mono">{_e(data['run_id'])}</span><br>
  Generated: {_e(data['generated_at'])}<br>
  Tool: {_e(data['tool'])} {_e(data['tool_version'])} &nbsp; Mode: {_e(data['mode'])}<br>
  Project: <span class="mono">{_e(data['project'].get('root', ''))}</span><br>
  Engine: {_e(data['engine'].get('engine_version', 'unknown'))}
</div>
<div class="cards">{''.join(cards)}</div>

<h2>Checks</h2>
<table>
<thead><tr><th>ID</th><th>Check</th><th>Status</th><th>Summary</th></tr></thead>
<tbody>{''.join(check_rows)}</tbody>
</table>

<h2>Findings</h2>
<table>
<thead><tr><th>ID</th><th>Check</th><th>Severity</th><th>Title</th><th>Asset</th><th>Message</th></tr></thead>
<tbody>{''.join(finding_rows)}</tbody>
</table>

<h2>Read-only evidence</h2>
{proof_html}

<h2>Limitations</h2>
<ul>{limitations}</ul>

<footer>
This is an assessment report, not a certification. It records what the tool observed under the configured roots and exclusions.
</footer>
</main>
</body>
</html>
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(document, encoding="utf-8")
    return path
