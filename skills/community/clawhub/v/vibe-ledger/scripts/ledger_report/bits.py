"""Small pieces every part of the report uses. Everything that reaches the
page goes through h() or ht(): mask secrets first, then escape."""
from __future__ import annotations

import unicodedata
from html import escape

from ledger_report.i18n import t
from redact import redact

GLYPH = {"kept": "✅", "broken": "❌", "partial": "⚠️", "pending": "⏳", "unknown": "❓"}
ORDER = ("broken", "partial", "pending", "unknown", "kept")


def h(value) -> str:
    return escape(redact("" if value is None else str(value)), quote=True)


def trunc(text, n: int) -> str:
    text = str(text)
    return text if len(text) <= n else text[: max(n - 1, 0)] + "…"


def ht(value, n: int) -> str:
    """Mask, then truncate, then escape: truncating first could cut a secret
    into a fragment too short to be recognised and masked."""
    return escape(trunc(redact("" if value is None else str(value)), n), quote=True)


def width(text: str) -> int:
    """Display width in half-width units: CJK and other wide characters count 2."""
    return sum(2 if unicodedata.east_asian_width(c) in ("W", "F") else 1 for c in text)


def fit(text, units: int) -> str:
    """Truncate to `units` of display width (see width), ending with … when cut."""
    text = str(text)
    if width(text) <= units:
        return text
    out, used = [], 1
    for c in text:
        w = width(c)
        if used + w > units:
            break
        out.append(c)
        used += w
    return "".join(out) + "…"


def hf(value, units: int) -> str:
    """Mask, then fit to a display width, then escape."""
    return escape(fit(redact("" if value is None else str(value)), units), quote=True)


def fmt_date(ts) -> str:
    ts = str(ts or "")
    return ts[:16].replace("T", " ")


def evidence_html(ids, evidence: dict, lang: str) -> str:
    items = []
    for i in ids:
        e = evidence.get(i)
        if not e:
            continue
        if e["kind"] == "transcript":
            who = t(lang, "said_by_user") if e.get("role") == "user" else t(lang, "said_by_ai")
            head = f'{h(t(lang, "transcript"))} · {h(who)} · {h(fmt_date(e.get("ts")))}'
            body = f'<blockquote>{ht(e.get("quote", ""), 600)}</blockquote>'
        elif e["kind"] == "code":
            fixed = f' · {h(t(lang, "line_corrected"))}' if e.get("line_corrected") else ""
            head = f'{h(t(lang, "code"))} · <code>{ht(e.get("path", ""), 80)}:{h(e.get("line", ""))}</code>{fixed}'
            body = f'<pre>{ht(e.get("snippet", ""), 800)}</pre>'
        else:
            head = (f'{h(t(lang, "probe"))} · <code>{ht(e.get("probe", ""), 40)}</code> · '
                    f'<code>{ht(e.get("path", ""), 80)}:{h(e.get("line", ""))}</code>')
            body = f'<p>{ht(e.get("message", ""), 300)}</p><pre>{ht(e.get("snippet", ""), 400)}</pre>'
        fail = "" if e.get("ok") else f'<p class="fail">✗ {ht(e.get("reason", ""), 200)}</p>'
        cls = "ev ok" if e.get("ok") else "ev failed"
        items.append(f'<li class="{cls}"><div class="ev-head">{head}</div>{body}{fail}</li>')
    if not items:
        return ""
    return (f'<details class="evidence"><summary>{h(t(lang, "evidence"))} ({len(items)})</summary>'
            f'<ul>{"".join(items)}</ul></details>')
