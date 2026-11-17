#!/usr/bin/env python3
"""Generate a standalone Signal Outreach HTML report from JSON."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from typing import Any


def esc(value: Any) -> str:
    return html.escape(str(value if value is not None else ""), quote=True)


def clamp(value: Any, maximum: int = 100) -> int:
    try:
        number = round(float(value))
    except (TypeError, ValueError):
        number = 0
    return max(0, min(maximum, number))


def items(value: Any) -> list[Any]:
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def dicts(value: Any) -> list[dict[str, Any]]:
    return [x for x in items(value) if isinstance(x, dict)]


def render_touch(touch: dict[str, Any]) -> str:
    variant = touch.get("variant")
    variant_badge = f'<span class="variant">{esc(variant)}</span>' if variant else ""
    subject = touch.get("subject")
    subject_html = f'<div class="subject"><span>Subject</span><p>{esc(subject)}</p></div>' if subject else ""
    return f"""
    <div class="touch">
      <div class="touch-header">
        <span class="touch-step">Step {esc(touch.get('step', ''))}</span>
        <span class="touch-day">Day {esc(touch.get('day', ''))}</span>
        <span class="touch-channel">{esc(touch.get('channel', ''))}</span>
        {variant_badge}
      </div>
      {subject_html}
      <div class="touch-body"><p>{esc(touch.get('body', ''))}</p></div>
      <div class="touch-notes"><span>Personalization</span><p>{esc(touch.get('personalization_notes', ''))}</p></div>
    </div>"""


def render_sequence(seq: dict[str, Any], index: int) -> str:
    touches = "".join(render_touch(t) for t in items(seq.get("touches")))
    rh = seq.get("response_handling") if isinstance(seq.get("response_handling"), dict) else {}

    response_html = ""
    if rh:
        response_html = f"""
        <div class="response-handling">
          <span>Response handling</span>
          <div class="response-grid">
            <div><span>Positive reply</span><p>{esc(rh.get('positive_reply', ''))}</p></div>
            <div><span>Question reply</span><p>{esc(rh.get('question_reply', ''))}</p></div>
            <div><span>No reply</span><p>{esc(rh.get('no_reply_after_sequence', ''))}</p></div>
          </div>
        </div>"""

    score = clamp(seq.get("prospect_score"))
    recommended = seq.get("variant_recommended", "")

    return f"""
    <article class="sequence reveal">
      <header class="seq-head">
        <div class="seq-rank">{index:02d}</div>
        <div class="seq-identity">
          <h3>{esc(seq.get('prospect_name', f'Prospect {index}'))}</h3>
          <div class="seq-meta">
            <span class="seq-score">Score {score}</span>
            <span class="seq-channel">{esc(seq.get('primary_channel', ''))}</span>
            {f'<span class="seq-channel backup">Backup: {esc(seq.get("backup_channel", ""))}</span>' if seq.get('backup_channel') else ''}
            {f'<span class="seq-variant">Recommended: Variant {esc(recommended)}</span>' if recommended else ''}
          </div>
        </div>
      </header>
      <div class="touches">{touches}</div>
      {response_html}
    </article>"""


def render_segment_brief(brief: dict[str, Any], index: int) -> str:
    score = clamp(brief.get("segment_score"))
    content_plan = dicts(brief.get("content_plan"))
    plan_html = "".join(
        f'<li><span>{esc(piece.get("buyer_stage", ""))}</span><p>{esc(piece.get("piece", ""))} '
        f'<em>({esc(piece.get("format", ""))})</em></p></li>'
        for piece in content_plan
    )
    keywords = "".join(f'<span class="kw-chip">{esc(k)}</span>' for k in items(brief.get("keywords")))
    channels = "".join(f"<li>{esc(c)}</li>" for c in items(brief.get("channel_plan")))
    proof_points = "".join(f"<li>{esc(p)}</li>" for p in items(brief.get("proof_points")))

    return f"""
    <article class="sequence reveal brief-segment">
      <header class="seq-head">
        <div class="seq-rank">{index:02d}</div>
        <div class="seq-identity">
          <h3>{esc(brief.get('segment_name', f'Segment {index}'))}</h3>
          <div class="seq-meta">
            <span class="seq-score">Score {score}</span>
            <span class="seq-channel">{esc(brief.get('angle_type', ''))}</span>
          </div>
        </div>
      </header>
      <div class="brief-grid">
        <div><span>Content plan</span><ul class="plan-list">{plan_html or '<li>Not specified</li>'}</ul></div>
        <div><span>Target keywords</span><div class="kw-row">{keywords or '<span>Not specified</span>'}</div></div>
        <div><span>Channel plan</span><ul>{channels or '<li>Not specified</li>'}</ul></div>
        <div><span>Proof points</span><ul>{proof_points or '<li>Not specified</li>'}</ul></div>
      </div>
    </article>"""


def render_company_pitch(pitch: dict[str, Any], index: int) -> str:
    score = clamp(pitch.get("company_score"))
    return f"""
    <article class="sequence reveal brief-company">
      <header class="seq-head">
        <div class="seq-rank">{index:02d}</div>
        <div class="seq-identity">
          <h3>{esc(pitch.get('company_name', f'Company {index}'))}</h3>
          <div class="seq-meta">
            <span class="seq-score">Score {score}</span>
            <span class="seq-channel">{esc(pitch.get('role', ''))}</span>
            <span class="seq-channel">{esc(pitch.get('execution_path', ''))}</span>
          </div>
        </div>
      </header>
      <div class="touch" style="background:transparent">
        <div class="touch-header"><span class="touch-step">Pitch</span></div>
        <div class="touch-body"><p>{esc(pitch.get('pitch', ''))}</p></div>
      </div>
      <div class="brief-grid">
        <div><span>Contact path</span><p>{esc(pitch.get('contact_path', 'Not specified'))}</p></div>
        <div><span>Fallback ask</span><p>{esc(pitch.get('fallback_ask', 'Not specified'))}</p></div>
      </div>
    </article>"""


def build_html(data: dict[str, Any]) -> str:
    sequences = dicts(data.get("sequences"))
    segment_briefs = dicts(data.get("segment_briefs"))
    company_pitches = dicts(data.get("company_pitches"))
    channel_breakdown = data.get("channel_breakdown") if isinstance(data.get("channel_breakdown"), dict) else {}
    total = len(sequences) + len(segment_briefs) + len(company_pitches)

    seq_html = "".join(render_sequence(x, i) for i, x in enumerate(sequences, 1))
    brief_html = "".join(render_segment_brief(x, i) for i, x in enumerate(segment_briefs, 1))
    pitch_html = "".join(render_company_pitch(x, i) for i, x in enumerate(company_pitches, 1))

    channel_items = "".join(
        f"<div><span>{esc(ch)}</span><strong>{count}</strong></div>"
        for ch, count in channel_breakdown.items()
    )

    individuals_section = f"""
      <section>
        <header class="section-head">
          <h2>Sequences ready to send.</h2>
          <p>Each Individual gets a personalized multi-touch sequence. Open the touches to see the full outreach plan.</p>
        </header>
        <div class="sequences">
          {seq_html}
        </div>
      </section>""" if sequences else ""

    segments_section = f"""
      <section>
        <header class="section-head">
          <h2>Content briefs to execute.</h2>
          <p>Each Segment gets a content/GTM plan, not a message — there's no one person to send it to.</p>
        </header>
        <div class="sequences">
          {brief_html}
        </div>
      </section>""" if segment_briefs else ""

    companies_section = f"""
      <section>
        <header class="section-head">
          <h2>Pitches ready to send.</h2>
          <p>Each Company gets one specific ask through a public contact path — not a drip sequence.</p>
        </header>
        <div class="sequences">
          {pitch_html}
        </div>
      </section>""" if company_pitches else ""

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="dark">
  <title>{esc(data.get('product', 'Signal Outreach'))} — Outreach Package</title>
  <style>
    :root {{
      --bg: #090b0f;
      --panel: #12161d;
      --panel2: #191f28;
      --ink: #f5f2ea;
      --muted: #9ca6b5;
      --line: #2b3340;
      --acid: #d9ff63;
      --blue: #69b7ff;
      --orange: #ff8f5a;
      --cyan: #5ee8d0;
      --purple: #c4a1ff;
      --radius: 18px;
      --shadow: 0 24px 80px rgba(0, 0, 0, .38);
    }}
    *, *::before, *::after {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font-family: Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.55;
    }}
    a {{ color: inherit; }}
    ul {{ margin: 0; padding-left: 1.2em; }}
    .skip {{ position: absolute; left: -9999px; }}
    .skip:focus {{ left: 16px; top: 16px; z-index: 9; background: var(--acid); color: #111; padding: 10px; border-radius: 8px; }}
    button:focus-visible, a:focus-visible {{ outline: 3px solid var(--blue); outline-offset: 3px; }}

    .shell {{ width: min(1180px, calc(100% - 40px)); margin: auto; }}
    .top {{ display: flex; justify-content: space-between; align-items: center; padding: 22px 0; border-bottom: 1px solid var(--line); }}
    .brand {{ font-weight: 850; display: flex; align-items: center; gap: 10px; }}
    .brand i {{ width: 12px; height: 12px; border-radius: 50%; background: var(--acid); box-shadow: 0 0 22px var(--acid); }}
    .meta {{ display: flex; gap: 8px; align-items: center; }}
    .chip {{ border: 1px solid var(--line); border-radius: 999px; padding: 7px 10px; color: var(--muted); font: 750 11px ui-monospace, monospace; text-transform: uppercase; letter-spacing: .07em; }}
    button {{ background: var(--ink); color: #111; border: 0; border-radius: 999px; padding: 9px 14px; font: 800 13px inherit; cursor: pointer; }}

    .hero {{ padding: 72px 0 42px; }}
    .eyebrow {{ color: var(--acid); font: 750 11px ui-monospace, monospace; text-transform: uppercase; letter-spacing: .11em; }}
    h1 {{ font-size: clamp(48px, 7vw, 80px); line-height: .92; letter-spacing: -.065em; margin: 13px 0 24px; }}
    .subtitle {{ font-size: clamp(18px, 2.1vw, 25px); color: #dce1e9; max-width: 820px; margin: 0; }}

    .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); border: 1px solid var(--line); border-radius: var(--radius); overflow: hidden; margin-bottom: 42px; }}
    .stats > div {{ padding: 18px; background: var(--panel); }}
    .stats > div + div {{ border-left: 1px solid var(--line); }}
    .stats span {{ display: block; color: var(--muted); font: 700 10px ui-monospace, monospace; text-transform: uppercase; letter-spacing: .08em; margin-bottom: 6px; }}
    .stats strong {{ font-size: 17px; }}

    .section-head {{ display: flex; justify-content: space-between; align-items: end; gap: 24px; padding-bottom: 18px; border-bottom: 1px solid var(--line); margin-bottom: 18px; }}
    .section-head h2 {{ font-size: clamp(34px, 5vw, 62px); line-height: .98; letter-spacing: -.055em; margin: 0; }}
    .section-head p {{ color: var(--muted); max-width: 470px; margin: 0; }}

    .sequences {{ display: grid; gap: 24px; margin-bottom: 76px; }}
    .sequence {{
      background: linear-gradient(135deg, var(--panel), #0f1319);
      border: 1px solid var(--line);
      border-radius: var(--radius);
      padding: 25px;
      box-shadow: 0 12px 38px rgba(0, 0, 0, .18);
    }}
    .brief-segment {{ border-left: 4px solid var(--blue); }}
    .brief-company {{ border-left: 4px solid var(--orange); }}
    .seq-head {{ display: grid; grid-template-columns: 54px 1fr; gap: 17px; align-items: start; margin-bottom: 20px; }}
    .seq-rank {{ font: 850 24px ui-monospace, monospace; color: var(--acid); padding-top: 8px; }}
    .seq-identity h3 {{ font-size: 29px; letter-spacing: -.04em; margin: 0 0 10px; }}
    .seq-meta {{ display: flex; gap: 8px; flex-wrap: wrap; }}
    .seq-score {{ background: var(--acid); color: #111; padding: 4px 10px; border-radius: 999px; font: 800 11px ui-monospace, monospace; }}
    .seq-channel {{ border: 1px solid var(--line); border-radius: 999px; padding: 4px 10px; color: var(--muted); font: 700 11px ui-monospace, monospace; text-transform: uppercase; }}
    .seq-channel.backup {{ border-color: rgba(105, 183, 255, .4); color: var(--blue); }}
    .seq-variant {{ border: 1px solid rgba(196, 161, 255, .4); border-radius: 999px; padding: 4px 10px; color: var(--purple); font: 700 11px ui-monospace, monospace; text-transform: uppercase; }}

    .touches {{ display: grid; gap: 12px; }}
    .touch {{ border: 1px solid var(--line); border-radius: 14px; padding: 18px; background: var(--panel2); }}
    .touch-header {{ display: flex; gap: 10px; align-items: center; margin-bottom: 12px; flex-wrap: wrap; }}
    .touch-step {{ font: 800 12px ui-monospace, monospace; color: var(--acid); }}
    .touch-day {{ font: 700 11px ui-monospace, monospace; color: var(--muted); }}
    .touch-channel {{ border: 1px solid var(--line); border-radius: 999px; padding: 3px 8px; font: 700 10px ui-monospace, monospace; color: var(--muted); text-transform: uppercase; }}
    .variant {{ border: 1px solid rgba(196, 161, 255, .4); border-radius: 999px; padding: 3px 8px; font: 700 10px ui-monospace, monospace; color: var(--purple); text-transform: uppercase; }}
    .subject {{ margin-bottom: 8px; }}
    .subject span, .touch-notes span, .response-handling > span {{ display: block; color: var(--muted); font: 700 10px ui-monospace, monospace; text-transform: uppercase; letter-spacing: .08em; margin-bottom: 4px; }}
    .touch-body p {{ margin: 0; font-size: 15px; white-space: pre-wrap; }}
    .touch-notes {{ margin-top: 10px; padding-top: 10px; border-top: 1px solid var(--line); }}
    .touch-notes p {{ margin: 0; font-size: 13px; color: var(--muted); }}

    .response-handling {{ margin-top: 16px; padding: 16px; border: 1px dashed rgba(217, 255, 99, .35); border-radius: 12px; }}
    .response-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 10px; }}
    .response-grid > div {{ border: 1px solid var(--line); border-radius: 10px; padding: 12px; background: rgba(255, 255, 255, .018); }}
    .response-grid span {{ display: block; color: var(--muted); font: 700 10px ui-monospace, monospace; text-transform: uppercase; letter-spacing: .08em; margin-bottom: 4px; }}
    .response-grid p {{ margin: 0; font-size: 13px; }}

    .brief-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 16px; }}
    .brief-grid > div {{ border: 1px solid var(--line); border-radius: 12px; padding: 15px; background: rgba(255, 255, 255, .018); }}
    .brief-grid span {{ display: block; color: var(--muted); font: 700 10px ui-monospace, monospace; text-transform: uppercase; letter-spacing: .08em; margin-bottom: 8px; }}
    .brief-grid p {{ margin: 0; }}
    .plan-list {{ list-style: none; padding: 0; }}
    .plan-list li {{ padding: 6px 0; border-bottom: 1px solid var(--line); }}
    .plan-list li:last-child {{ border-bottom: 0; }}
    .plan-list li span {{ display: inline-block; color: var(--blue); font: 700 10px ui-monospace, monospace; text-transform: uppercase; margin-right: 8px; }}
    .plan-list li p {{ display: inline; margin: 0; }}
    .kw-row {{ display: flex; flex-wrap: wrap; gap: 6px; }}
    .kw-chip {{ border: 1px solid var(--line); border-radius: 999px; padding: 4px 10px; font: 700 11px ui-monospace, monospace; color: var(--ink); }}

    .general {{ border: 1px solid var(--line); border-radius: var(--radius); padding: 24px; color: var(--muted); margin-bottom: 60px; }}
    .general h2 {{ color: var(--ink); margin-top: 0; }}

    footer {{ display: flex; justify-content: space-between; gap: 20px; border-top: 1px solid var(--line); padding: 22px 0 40px; color: var(--muted); font-size: 12px; }}

    .reveal {{ animation: rise .4s ease both; }}
    @keyframes rise {{ from {{ opacity: 0; transform: translateY(12px); }} }}

    @media (max-width: 820px) {{
      .shell {{ width: min(100% - 24px, 1180px); }}
      .hero {{ padding-top: 44px; }}
      .seq-head {{ grid-template-columns: 38px 1fr; }}
      .response-grid, .brief-grid {{ grid-template-columns: 1fr; }}
      .stats {{ grid-template-columns: 1fr 1fr; }}
      .stats > div + div {{ border-left: 0; border-top: 1px solid var(--line); }}
    }}
    @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; transition: none !important; }} }}
    @media print {{
      body {{ background: #fff; color: #111; }}
      .top button {{ display: none; }}
      .shell {{ width: 100%; }}
      .sequence, .touch, .brief-grid > div {{ background: #fff; color: #111; break-inside: avoid; }}
    }}
  </style>
</head>
<body>
  <a class="skip" href="#main">Skip to report</a>
  <div class="shell">
    <header class="top">
      <div class="brand"><i></i> Signal Outreach</div>
      <div class="meta">
        <span class="chip">Drafts only — never sent automatically</span>
        <button type="button" onclick="window.print()">Print / Save PDF</button>
      </div>
    </header>

    <main id="main">
      <section class="hero">
        <span class="eyebrow">Outreach package · {esc(data.get('generated_at', ''))}</span>
        <h1>{esc(data.get('product', 'Outreach Package'))}</h1>
        <p class="subtitle">The right next action per prospect type — sequences for Individuals, content briefs for Segments, BD pitches for Companies. Every item references a specific public signal.</p>
      </section>

      <section class="stats">
        <div><span>Total items</span><strong>{total}</strong></div>
        <div><span>Individuals</span><strong>{len(sequences)}</strong></div>
        <div><span>Segments</span><strong>{len(segment_briefs)}</strong></div>
        <div><span>Companies</span><strong>{len(company_pitches)}</strong></div>
        {channel_items}
      </section>

      {individuals_section}
      {segments_section}
      {companies_section}

      <section class="general">
        <h2>General notes</h2>
        <p>{esc(data.get('general_notes', 'No additional notes.'))}</p>
      </section>
    </main>

    <footer>
      <span>Generated by signal-outreach</span>
      <span>Outreach is never sent automatically.</span>
    </footer>
  </div>
</body>
</html>"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Path to outreach JSON")
    parser.add_argument("output", type=Path, help="Path to output HTML")
    args = parser.parse_args()

    with args.input.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise SystemExit("Input JSON must contain an object at the top level.")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(build_html(data), encoding="utf-8")
    print(f"Created report: {args.output.resolve()}")


if __name__ == "__main__":
    main()
