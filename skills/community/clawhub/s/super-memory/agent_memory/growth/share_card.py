"""share_card.py — Shareable Insight Card Generator"""

from __future__ import annotations

import html as _html
import json
import logging
import re
from collections import Counter
from datetime import datetime

logger = logging.getLogger(__name__)

# Chinese number character normalization map for PII detection
_CHINESE_NUM_MAP = str.maketrans(
    '一二三四五六七八九零壹贰叁肆伍陆柒捌玖〇两幺',
    '1234567890123456789021'
)


def _normalize_chinese_numbers(text: str) -> str:
    """Convert Chinese number characters to digits for PII detection.

    This is used only for detection; the original text is not modified.
    """
    return text.translate(_CHINESE_NUM_MAP)


# PII patterns for redaction
_PII_PATTERNS = [
    (re.compile(r'(?<!\d)\d{3}[-.\s]?\d{4}[-.\s]?\d{4}(?!\d)'), '[PHONE]'),
    (re.compile(r'\b[\w.+-]+@[\w-]+\.[\w.-]+\b'), '[EMAIL]'),
    (re.compile(r'(?<!\d)\d{6,}(?:\d{2})?(?!\d)'), '[ID_NUMBER]'),
    (re.compile(r'(?:身份证|护照|社保)\s*[:：]?\s*\S+'), '[ID_DOC]'),
]


def _redact_pii(text: str) -> str:
    """Redact PII from text, with Chinese number normalization for detection."""
    normalized = _normalize_chinese_numbers(text)
    for pattern, replacement in _PII_PATTERNS:
        for match in pattern.finditer(normalized):
            text = text[:match.start()] + replacement + text[match.end():]
            normalized = normalized[:match.start()] + replacement + normalized[match.end():]
    return text


class ShareCardGenerator:
    """Generate shareable insight cards from memory data."""

    def __init__(self, store):
        self.store = store

    def generate_recall_card(self, query: str, results: list[dict], tenant_id: str = 'default') -> str:
        """Generate a share card from recall results (PII redacted)."""
        # Redact PII from query
        safe_query = _redact_pii(query)

        # Redact and truncate top 3 results
        result_items = []
        for m in results[:3]:
            content = m.get("content", "")
            safe_content = _redact_pii(content[:120])
            if len(content) > 120:
                safe_content += "..."
            result_items.append({
                "content": safe_content,
                "importance": m.get("importance", "medium"),
                "topics": [
                    t.get("code", t) if isinstance(t, dict) else t
                    for t in m.get("topics", [])[:3]
                ],
            })

        card_data = {
            "type": "recall",
            "query": safe_query,
            "result_count": len(results),
            "results": result_items,
        }
        return self.render_to_html(card_data)

    def generate_stat_card(self, tenant_id: str = 'default') -> str:
        """Generate a stat summary card."""
        try:
            total = self.store.count()
            stats = self.store.get_aggregated_stats()
        except Exception as e:
            logger.warning("ShareCard: stats query failed: %s", e)
            total = 0
            stats = {}

        top_topics = list(stats.get("topic_distribution", {}).items())[:5]
        emotion_sums = stats.get("emotion_sums", {})

        card_data = {
            "type": "stats",
            "total_memories": total,
            "top_topics": [{"topic": t, "count": c} for t, c in top_topics],
            "emotion_sums": emotion_sums,
            "avg_valence": stats.get("avg_valence", 0),
        }
        return self.render_to_html(card_data)

    def render_to_html(self, card_data: dict) -> str:
        """Render card data to self-contained HTML."""
        card_type = card_data.get("type", "stats")

        if card_type == "recall":
            return self._render_recall_card(card_data)
        return self._render_stat_card(card_data)

    def _render_recall_card(self, data: dict) -> str:
        """Render a recall results card."""
        results_html = ""
        for i, r in enumerate(data.get("results", [])):
            topics_str = ", ".join(_html.escape(t) for t in r.get("topics", []))
            imp_icon = {"high": "🔴", "medium": "🟡", "low": "⚪"}.get(r["importance"], "⚪")
            results_html += f"""
            <div class="result-item">
                <span class="result-num">{i + 1}</span>
                <div class="result-content">
                    <div class="result-text">{imp_icon} {_html.escape(r['content'])}</div>
                    <div class="result-meta">{topics_str}</div>
                </div>
            </div>"""

        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
  :root {{
    --bg: #0d1117; --card: #161b22; --border: #30363d;
    --text: #e6edf3; --muted: #8b949e; --accent: #58a6ff;
  }}
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{
    background: var(--bg); color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    width: 600px; padding: 1.5rem;
  }}
  .query {{ font-size: 1.1rem; font-weight: 600; margin-bottom: 1rem; }}
  .query em {{ color: var(--accent); font-style: normal; }}
  .result-item {{ display: flex; gap: 0.8rem; margin-bottom: 0.8rem; padding: 0.8rem; background: var(--card); border-radius: 8px; border: 1px solid var(--border); }}
  .result-num {{ color: var(--accent); font-weight: 700; font-size: 1.2rem; min-width: 1.5rem; }}
  .result-text {{ font-size: 0.9rem; margin-bottom: 0.3rem; }}
  .result-meta {{ font-size: 0.75rem; color: var(--muted); }}
  .footer {{ text-align: center; color: var(--muted); font-size: 0.65rem; margin-top: 1rem; padding-top: 0.5rem; border-top: 1px solid var(--border); }}
</style>
</head>
<body>
<div class="query">🔍 <em>{_html.escape(data['query'])}</em> ({data['result_count']} results)</div>
{results_html}
<div class="footer">Powered by Agent Memory V12 — PII redacted</div>
</body>
</html>"""
        return html

    def _render_stat_card(self, data: dict) -> str:
        """Render a stats summary card."""
        topics_html = ""
        for t in data.get("top_topics", []):
            topics_html += f'<div class="topic"><span class="topic-name">{_html.escape(t["topic"])}</span><span class="topic-count">{t["count"]}</span></div>'

        valence = data.get("avg_valence", 0)
        mood = "😊" if valence > 0.2 else "😐" if valence > -0.2 else "😔"

        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
  :root {{
    --bg: #0d1117; --card: #161b22; --border: #30363d;
    --text: #e6edf3; --muted: #8b949e; --accent: #58a6ff; --accent2: #f78166;
  }}
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{
    background: var(--bg); color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    width: 600px; padding: 1.5rem;
  }}
  .header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; }}
  .title {{ font-size: 1.3rem; font-weight: 700; }}
  .total {{ font-size: 2.5rem; font-weight: 800; color: var(--accent); }}
  .total-label {{ font-size: 0.75rem; color: var(--muted); text-align: center; }}
  .section {{ margin-bottom: 1rem; }}
  .section-title {{ font-size: 0.9rem; font-weight: 600; color: var(--muted); margin-bottom: 0.5rem; }}
  .topic {{ display: flex; justify-content: space-between; padding: 0.3rem 0; border-bottom: 1px solid var(--border); }}
  .topic-name {{ font-size: 0.85rem; }}
  .topic-count {{ font-size: 0.85rem; color: var(--accent2); }}
  .mood {{ font-size: 2rem; text-align: center; margin: 0.5rem 0; }}
  .footer {{ text-align: center; color: var(--muted); font-size: 0.65rem; margin-top: 1rem; padding-top: 0.5rem; border-top: 1px solid var(--border); }}
</style>
</head>
<body>
<div class="header">
  <div class="title">Memory Stats</div>
  <div><div class="total">{data['total_memories']}</div><div class="total-label">memories</div></div>
</div>
<div class="section">
  <div class="section-title">📚 Top Topics</div>
  {topics_html}
</div>
<div class="section">
  <div class="section-title">Overall Mood</div>
  <div class="mood">{mood} (valence: {valence:.2f})</div>
</div>
<div class="footer">Powered by Agent Memory V12 — No PII included</div>
</body>
</html>"""
        return html
