from __future__ import annotations

"""Generate Instagram reels from HTML templates with beautiful CSS styling.

v3.0 — 4 viral video formats (timer challenge, shocking stat, comparison, loop)
that rotate by day for maximum IG Reels & YT Shorts watch-through rate.

Platform rules baked in:
- Hook in first 1-2s
- 13s target duration (proven sweet spot)
- Bold, high-contrast, mobile-first 9:16
- Text on screen > voiceover
- Loop content (end connects to start)
"""

import logging
import random
import shutil
import tempfile
from datetime import datetime
from pathlib import Path

# Heavy imports are lazy-loaded to avoid crashes when only get_video_format_for_day is needed
np = None
Html2Image = None
AudioFileClip = None
ImageClip = None
concatenate_videoclips = None
Image = None

def _ensure_heavy_imports():
    global np, Html2Image, AudioFileClip, ImageClip, concatenate_videoclips, Image
    if np is None:
        import numpy as _np
        np = _np
    if Html2Image is None:
        from html2image import Html2Image as _H2I
        Html2Image = _H2I
    if AudioFileClip is None:
        from moviepy import AudioFileClip as _A, ImageClip as _I, concatenate_videoclips as _C
        AudioFileClip = _A
        ImageClip = _I
        concatenate_videoclips = _C
    if Image is None:
        from PIL import Image as _Img
        Image = _Img

try:
    from bot.ig_config import OUTPUT_DIR, TEMPLATES_DIR
except ImportError:
    OUTPUT_DIR = Path("output")
    TEMPLATES_DIR = Path("templates")

logger = logging.getLogger(__name__)

VIDEO_W, VIDEO_H = 1080, 1920

# ── Color themes (rotate per video) ──────────────────────────────────────────
_THEMES = [
    {"name": "Dark Fire",    "bg": "#0a0a0a", "accent": "#ff6b35", "green": "#22c55e", "red": "#ef4444", "accent_bg": "#1a0a00"},
    {"name": "Royal Gold",   "bg": "#0a0a1a", "accent": "#ffd700", "green": "#22c55e", "red": "#ef4444", "accent_bg": "#1a1500"},
    {"name": "Neon Green",   "bg": "#0a1a0a", "accent": "#00ff88", "green": "#00ff88", "red": "#ef4444", "accent_bg": "#001a0a"},
    {"name": "Deep Purple",  "bg": "#1a0a2a", "accent": "#c084fc", "green": "#22c55e", "red": "#ef4444", "accent_bg": "#1a0a1a"},
    {"name": "Blood Red",    "bg": "#1a0a0a", "accent": "#ef4444", "green": "#22c55e", "red": "#ff6b6b", "accent_bg": "#1a0000"},
    {"name": "Ocean Cyan",   "bg": "#0a1a2a", "accent": "#00d4ff", "green": "#22c55e", "red": "#ef4444", "accent_bg": "#001a2a"},
    {"name": "Hot Pink",     "bg": "#1a0a1a", "accent": "#ff69b4", "green": "#22c55e", "red": "#ef4444", "accent_bg": "#1a0010"},
    {"name": "Amber",        "bg": "#0a0a05", "accent": "#f59e0b", "green": "#22c55e", "red": "#ef4444", "accent_bg": "#1a1000"},
]

def _pick_theme() -> dict:
    """Pick a random color theme."""
    return random.choice(_THEMES)

# Legacy constants (default theme)
_BG = "#0a0a0a"
_ORANGE = "#ff6b35"
_GREEN = "#22c55e"
_RED = "#ef4444"

# ── Data pools ───────────────────────────────────────────────────────────────
SHOCKING_STATS = [
    {
        "hook": "UPSC ka sabse bada pattern",
        "stat": "28/30",
        "detail": "Constitutional Amendments appeared in 28 out of 30 UPSC papers",
        "source": "1995-2025 analysis",
    },
    {
        "hook": "Ye subject 7x badh gaya",
        "stat": "7x",
        "detail": "Environment questions grew 7x since the 1990s",
        "source": "3274 PYQs analyzed",
    },
    {
        "hook": "Paper ka 1/3 sirf 2 subjects se",
        "stat": "33%",
        "detail": "Polity (17.7%) + Economy (15.9%) = 33% of every UPSC paper",
        "source": "30 years data",
    },
    {
        "hook": "Science ab important nahi raha",
        "stat": "↓50%",
        "detail": "Science questions dropped from 15-20 to 5-8 per paper",
        "source": "Trend analysis",
    },
    {
        "hook": "Galat answer ki asli keemat",
        "stat": "-0.67",
        "detail": "One wrong answer costs you 0.67 marks. 3 wrong = 1 right answer wasted",
        "source": "UPSC marking scheme",
    },
    {
        "hook": "Art & Culture ka sach",
        "stat": "6.7%",
        "detail": "Only 6.7% of paper but mostly factual — easiest marks if prepared",
        "source": "Subject analysis",
    },
    {
        "hook": "Current Affairs ka weight",
        "stat": "10.1%",
        "detail": "10% of paper is pure current affairs — 30 min daily newspaper is enough",
        "source": "3274 PYQs",
    },
    {
        "hook": "Geography surprise",
        "stat": "12.5%",
        "detail": "Geography is 12.5% — Indian Geography alone is 8% of that",
        "source": "Topic breakdown",
    },
]

COMPARISONS = [
    {
        "wrong": [
            "Reading 10 books",
            "Year-wise PYQ solving",
            "12 hours daily",
            "Starting PYQ after syllabus",
        ],
        "right": [
            "Mastering 3 books",
            "Topic-wise PYQ solving",
            "6 focused hours",
            "PYQ from Day 1",
        ],
    },
    {
        "wrong": [
            "₹2 Lakh coaching",
            "Following 5 CA sources",
            "Random mock tests",
            "Memorizing facts",
        ],
        "right": [
            "₹0 self-study",
            "One newspaper daily",
            "Timed weekly mocks",
            "Understanding concepts",
        ],
    },
    {
        "wrong": [
            "Watching 10 YouTube channels",
            "Notes from coaching PDFs",
            "Group study daily",
            "Attempting all 100 Qs",
        ],
        "right": [
            "One trusted source",
            "Self-written short notes",
            "Solo deep work",
            "Strategic 75 Qs with accuracy",
        ],
    },
]

# Modern gradient palettes (used only for quiz Saturday format)
GRADIENT_PALETTES = [
    ("linear-gradient(135deg, #667eea 0%, #764ba2 100%)", "Purple Dream"),
    ("linear-gradient(135deg, #f093fb 0%, #f5576c 100%)", "Pink Sunset"),
    ("linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)", "Ocean Blue"),
    ("linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)", "Mint Fresh"),
    ("linear-gradient(135deg, #fa709a 0%, #fee140 100%)", "Warm Glow"),
    ("linear-gradient(135deg, #30cfd0 0%, #330867 100%)", "Deep Sea"),
    ("linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)", "Pastel Sky"),
    ("linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)", "Soft Rose"),
]

# Keep legacy alias so existing imports of HTML_TEMPLATE don't break
HTML_TEMPLATE = ""  # replaced by _build_quiz_html()


# ── Day rotation ─────────────────────────────────────────────────────────────

def get_video_format_for_day() -> str:
    """Return video format name based on today's weekday.

    Monday    → shocking_stat
    Tuesday   → comparison
    Wednesday → timer_challenge
    Thursday  → shocking_stat
    Friday    → comparison
    Saturday  → quiz
    Sunday    → loop_format
    """
    formats = [
        "shocking_stat",    # Monday   (0)
        "comparison",       # Tuesday  (1)
        "timer_challenge",  # Wednesday(2)
        "shocking_stat",    # Thursday (3)
        "comparison",       # Friday   (4)
        "quiz",             # Saturday (5)
        "loop_format",      # Sunday   (6)
    ]
    return formats[datetime.now().weekday()]


# ── Shared HTML helpers ───────────────────────────────────────────────────────

_BASE_STYLE = f"""
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{
    width: 1080px; height: 1920px;
    background: {_BG};
    font-family: system-ui, -apple-system, 'Segoe UI', sans-serif;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    padding: 80px 60px;
    position: relative; overflow: hidden;
}}
.brand {{
    position: absolute; bottom: 44px; left: 0; right: 0;
    text-align: center;
    font-size: 30px; font-weight: 600;
    color: rgba(255,255,255,0.35);
    letter-spacing: 1px;
}}
"""


def _wrap(body: str, extra_css: str = "", bg: str = "") -> str:
    """Wrap body in standard 1080×1920 dark shell."""
    bg_override = f"\nbody {{ background: {bg}; }}" if bg else ""
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<style>{_BASE_STYLE}{extra_css}{bg_override}</style>
</head>
<body>
{body}
<div class="brand">{BRAND_URL}</div>
</body></html>"""


def _esc(text: str) -> str:
    """Minimal HTML escaping."""
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


# ── Format 0: Quiz (Saturday) — existing template preserved ──────────────────

def _build_quiz_html(question_data: dict, gradient: str) -> list[tuple[str, float]]:
    """Single-frame colorful quiz card. Returns [(html, 15.0)]."""
    q = _esc(question_data.get("question", ""))
    year = _esc(str(question_data.get("year", "2023")))
    oa = _esc(question_data.get("option_a", ""))
    ob = _esc(question_data.get("option_b", ""))
    oc = _esc(question_data.get("option_c", ""))
    od = _esc(question_data.get("option_d", ""))

    html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{
    width:1080px; height:1920px;
    background:{gradient};
    font-family:system-ui,-apple-system,sans-serif;
    display:flex; flex-direction:column;
    align-items:center; padding:60px 40px;
    position:relative; overflow:hidden;
}}
.header {{ background:rgba(255,255,255,.95); padding:16px 40px; border-radius:50px;
    box-shadow:0 8px 32px rgba(0,0,0,.15); margin-bottom:40px; z-index:10; }}
.header-text {{ font-size:28px; font-weight:700;
    background:linear-gradient(135deg,#667eea,#764ba2);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; text-align:center; }}
.qcard {{ background:rgba(255,255,255,.98); border-radius:30px; padding:40px;
    margin-bottom:30px; box-shadow:0 20px 60px rgba(0,0,0,.2);
    width:100%; max-width:1000px; z-index:10; }}
.qtext {{ font-size:38px; font-weight:600; color:#1a1a2e; line-height:1.4; margin-bottom:20px; }}
.ybadge {{ display:inline-block;
    background:linear-gradient(135deg,#f093fb,#f5576c);
    color:#fff; padding:10px 28px; border-radius:25px;
    font-size:26px; font-weight:700; }}
.opts {{ width:100%; max-width:1000px; z-index:10; }}
.opt {{ background:rgba(255,255,255,.95); border-radius:25px;
    padding:24px 30px; margin-bottom:20px;
    display:flex; align-items:center; box-shadow:0 8px 25px rgba(0,0,0,.12); }}
.oletter {{ width:56px; height:56px; border-radius:50%;
    background:linear-gradient(135deg,#667eea,#764ba2);
    color:#fff; display:flex; align-items:center; justify-content:center;
    font-size:28px; font-weight:700; margin-right:20px; flex-shrink:0; }}
.otext {{ font-size:32px; color:#2d3748; line-height:1.4; font-weight:500; }}
.hint {{ background:rgba(255,255,255,.95); border-radius:25px;
    padding:20px 35px; margin-top:10px; margin-bottom:30px;
    box-shadow:0 8px 25px rgba(0,0,0,.12); z-index:10; }}
.hint-text {{ font-size:28px; font-weight:600;
    background:linear-gradient(135deg,#fa709a,#fee140);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; text-align:center; }}
.footer {{ background:linear-gradient(135deg,#f093fb,#f5576c);
    border-radius:25px; padding:30px 40px; margin-top:auto;
    width:100%; max-width:1000px; z-index:10; }}
.ftitle {{ font-size:32px; font-weight:700; color:#fff; text-align:center; margin-bottom:8px; }}
.fsub {{ font-size:26px; font-weight:600; color:rgba(255,255,255,.95); text-align:center; }}
</style></head>
<body>
<div class="header"><div class="header-text">📚 UPSC Previous Year Quiz</div></div>
<div class="qcard">
    <div class="qtext">{q}</div>
    <div class="ybadge">UPSC {year}</div>
</div>
<div class="opts">
    <div class="opt"><div class="oletter">A</div><div class="otext">{oa}</div></div>
    <div class="opt"><div class="oletter">B</div><div class="otext">{ob}</div></div>
    <div class="opt"><div class="oletter">C</div><div class="otext">{oc}</div></div>
    <div class="opt"><div class="oletter">D</div><div class="otext">{od}</div></div>
</div>
<div class="hint"><div class="hint-text">💡 Answer &amp; Explanation in comments!</div></div>
<div class="footer">
    <div class="ftitle">{BRAND_NAME}</div>
    <div class="fsub">30 Years PYQs • Mock Tests • Current Affairs</div>
</div>
</body></html>"""
    return [(html, 15.0)]


# ── Format 1: Timer Challenge ("90% fail this") ──────────────────────────────

def _timer_frame(question_data: dict, count: int, theme: dict | None = None) -> str:
    """One frame of the countdown — question shown, big timer digit."""
    t = theme or _THEMES[0]
    _accent = t["accent"]
    _rd = t["red"]
    _grn = t["green"]
    _bg = t["bg"]

    q = _esc(question_data.get("question", ""))
    oa = _esc(question_data.get("option_a", ""))
    ob = _esc(question_data.get("option_b", ""))
    oc = _esc(question_data.get("option_c", ""))
    od = _esc(question_data.get("option_d", ""))
    year = _esc(str(question_data.get("year", "")))
    timer_color = _rd if count > 2 else (_accent if count == 2 else _grn)

    css = f"""
.hook {{ font-size:52px; font-weight:900; color:{_rd};
    text-align:center; line-height:1.2; margin-bottom:40px; letter-spacing:-1px; }}
.qcard {{ background:#1a1a1a; border-radius:24px; padding:44px;
    width:100%; margin-bottom:30px; border:2px solid {_accent}33; }}
.qtext {{ font-size:36px; font-weight:700; color:#fff; line-height:1.45; margin-bottom:20px; }}
.ybadge {{ font-size:22px; color:{_accent}; font-weight:700; }}
.opts {{ width:100%; margin-bottom:30px; }}
.opt {{ background:#161616; border-radius:16px; padding:20px 28px;
    margin-bottom:16px; display:flex; align-items:center;
    border:2px solid #222; }}
.oletter {{ width:50px; height:50px; border-radius:50%;
    background:#222; color:{_accent};
    display:flex; align-items:center; justify-content:center;
    font-size:26px; font-weight:800; margin-right:20px; flex-shrink:0; }}
.otext {{ font-size:30px; color:#e0e0e0; font-weight:600; line-height:1.3; }}
.timer-ring {{
    width:220px; height:220px; border-radius:50%;
    border: 14px solid {timer_color};
    display:flex; align-items:center; justify-content:center;
    box-shadow: 0 0 40px {timer_color}88;
}}
.timer-num {{ font-size:120px; font-weight:900; color:{timer_color};
    line-height:1; }}
"""
    body = f"""
<div class="hook">⚡ Can you answer in time?</div>
<div class="qcard">
    <div class="qtext">{q}</div>
    <div class="ybadge">UPSC {year}</div>
</div>
<div class="opts">
    <div class="opt"><div class="oletter">A</div><div class="otext">{oa}</div></div>
    <div class="opt"><div class="oletter">B</div><div class="otext">{ob}</div></div>
    <div class="opt"><div class="oletter">C</div><div class="otext">{oc}</div></div>
    <div class="opt"><div class="oletter">D</div><div class="otext">{od}</div></div>
</div>
<div class="timer-ring"><div class="timer-num">{count}</div></div>
"""
    return _wrap(body, css, bg=_bg)


def _build_timer_challenge_html(question_data: dict) -> list[tuple[str, float]]:
    """3-phase timer challenge: hook(2s) + countdown(5×1s) + answer reveal(5s).
    Total: ~12s.
    """
    theme = _pick_theme()
    logger.info("Theme: %s", theme["name"])
    _accent = theme["accent"]
    _bg = theme["bg"]
    _abg = theme["accent_bg"]
    _grn = theme["green"]
    _rd = theme["red"]

    frames: list[tuple[str, float]] = []

    # ── Screen 1: Question + Options thumbnail (2s) ────────────────────────
    q = _esc(question_data.get("question", ""))
    oa = _esc(question_data.get("option_a", ""))
    ob = _esc(question_data.get("option_b", ""))
    oc = _esc(question_data.get("option_c", ""))
    od = _esc(question_data.get("option_d", ""))
    category = question_data.get("category", "").strip()
    year = question_data.get("year", "")

    # Auto-size question font based on length
    q_len = len(question_data.get("question", ""))
    q_font = "34px" if q_len > 150 else ("38px" if q_len > 100 else "42px")

    css1 = f"""
.top-bar {{ display:flex; justify-content:space-between; align-items:center;
    width:100%; margin-bottom:40px; }}
.badge {{ font-size:24px; color:{_accent}; font-weight:700;
    background:{_abg}; padding:10px 24px; border-radius:50px;
    border:2px solid {_accent}; }}
.year-badge {{ font-size:22px; color:#fff; font-weight:700;
    background:#333; padding:8px 20px; border-radius:50px; }}
.qcard {{ background:#1a1a1a; border-radius:24px; padding:36px;
    width:100%; margin-bottom:30px; border:2px solid {_accent}33; }}
.qtext {{ font-size:{q_font}; font-weight:700; color:#fff; line-height:1.45; }}
.opts {{ width:100%; }}
.opt {{ background:#161616; border-radius:16px; padding:18px 24px;
    margin-bottom:14px; display:flex; align-items:center;
    border:2px solid #222; }}
.oletter {{ width:44px; height:44px; border-radius:50%;
    background:#222; color:{_accent};
    display:flex; align-items:center; justify-content:center;
    font-size:24px; font-weight:800; margin-right:18px; flex-shrink:0; }}
.otext {{ font-size:28px; color:#e0e0e0; font-weight:600; line-height:1.3; }}
.cta {{ font-size:32px; font-weight:800; color:{_accent};
    text-align:center; margin-top:30px; }}
"""
    _ctas = [
        "Answer in 3 sec ⏱️",
        "Comment your answer 👇",
        "Can you solve this? 🤔",
        f"UPSC {year} — try it!",
        "Pause and think 🧠",
    ]
    cta_text = random.choice(_ctas)

    hook_body = f"""
<div class="top-bar">
    <div class="badge">⚡ UPSC PYQ</div>
    <div class="year-badge">{_esc(str(year))}</div>
</div>
<div class="qcard">
    <div class="qtext">{q}</div>
</div>
<div class="opts">
    <div class="opt"><div class="oletter">A</div><div class="otext">{oa}</div></div>
    <div class="opt"><div class="oletter">B</div><div class="otext">{ob}</div></div>
    <div class="opt"><div class="oletter">C</div><div class="otext">{oc}</div></div>
    <div class="opt"><div class="oletter">D</div><div class="otext">{od}</div></div>
</div>
<div class="cta">{cta_text}</div>
"""
    frames.append((_wrap(hook_body, css1, bg=_bg), 7.0))

    # ── Screen 3: CTA — check comments for answer (3s) ─────────────────────
    css3 = f"""
.cta-icon {{ font-size:120px; margin-bottom:40px; }}
.cta-big {{ font-size:64px; font-weight:900; color:#fff;
    text-align:center; line-height:1.2; margin-bottom:30px; }}
.cta-big em {{ color:{_accent}; font-style:normal; }}
.cta-sub {{ font-size:36px; font-weight:600; color:rgba(255,255,255,.6);
    text-align:center; }}
.cta-brand {{ font-size:30px; font-weight:700; color:{_accent};
    text-align:center; margin-top:40px; }}
"""
    _end_ctas = [
        ("👇", "Answer in<br><em>comments</em>", "Check below!"),
        ("💬", "Comment your<br><em>answer</em> first!", "Then check 👇"),
        ("🤔", "Did you get<br>it <em>right</em>?", "Answer in comments 👇"),
        ("⬇️", "Scroll down<br>for the <em>answer</em>", "👇"),
    ]
    _ec = random.choice(_end_ctas)
    reveal_body = f"""
<div class="cta-icon">{_ec[0]}</div>
<div class="cta-big">{_ec[1]}</div>
<div class="cta-sub">{_ec[2]}</div>
<div class="cta-brand">{BRAND_URL}</div>
"""
    frames.append((_wrap(reveal_body, css3, bg=_bg), 3.0))

    return frames


# ── Format 2: Shocking Stat Counter ("Data Bomb") ────────────────────────────

def _get_counter_steps(stat: str) -> list[str]:
    """Generate 3 counter steps for rolling animation: [start, mid, final]."""
    s = stat.strip()
    if "/" in s:
        try:
            num_s, denom_s = s.split("/", 1)
            num, denom = int(num_s.strip()), int(denom_s.strip())
            return [f"0/{denom}", f"{num // 2}/{denom}", s]
        except Exception:
            pass
    if "%" in s:
        try:
            val = float(s.replace("%", "").replace("↑", "").replace("↓", "").strip())
            prefix = "↓" if s.startswith("↓") else ("↑" if s.startswith("↑") else "")
            return ["0%", f"{prefix}{val / 2:.1f}%", s]
        except Exception:
            pass
    if s.lower().endswith("x"):
        try:
            val = float(s.lower().rstrip("x"))
            return ["1x", f"{val / 2:.0f}x", s]
        except Exception:
            pass
    return ["...", s, s]


def _stat_counter_frame(hook: str, counter_val: str, source: str, is_final: bool = False) -> str:
    accent = _ORANGE
    counter_size = "160px" if len(counter_val) <= 5 else "120px"
    extra_glow = f"box-shadow: 0 0 80px {accent}55;" if is_final else ""
    css = f"""
.hook {{ font-size:54px; font-weight:900; color:#fff;
    text-align:center; line-height:1.2; margin-bottom:60px; }}
.counter-ring {{
    width:340px; height:340px; border-radius:50%;
    background:#111; border: 8px solid {accent};
    display:flex; align-items:center; justify-content:center;
    {extra_glow}
    margin-bottom:50px;
}}
.counter-val {{ font-size:{counter_size}; font-weight:900; color:{accent};
    line-height:1; text-align:center; }}
.source {{ font-size:26px; color:rgba(255,255,255,.4);
    text-align:center; font-style:italic; }}
"""
    body = f"""
<div class="hook">{_esc(hook)}</div>
<div class="counter-ring">
    <div class="counter-val">{_esc(counter_val)}</div>
</div>
<div class="source">{_esc(source)}</div>
"""
    return _wrap(body, css)


def _build_shocking_stat_html(question_data: dict) -> list[tuple[str, float]]:
    """3-phase stat reveal: hook(2s) + counter roll(3×2s) + CTA(5s).
    Total: 13s.
    """
    # Pick stat — use day-of-year for variety so each day gets a different stat
    idx = (datetime.now().timetuple().tm_yday + datetime.now().weekday()) % len(SHOCKING_STATS)
    stat_data = SHOCKING_STATS[idx]

    hook = stat_data["hook"]
    stat = stat_data["stat"]
    detail = stat_data["detail"]
    source = stat_data["source"]

    frames: list[tuple[str, float]] = []

    # ── Screen 1: Hook (2s) ─────────────────────────────────────────────────
    css1 = f"""
.badge {{ font-size:28px; color:{_ORANGE}; font-weight:700;
    border:2px solid {_ORANGE}; padding:12px 30px; border-radius:40px;
    margin-bottom:60px; }}
.hook {{ font-size:72px; font-weight:900; color:#fff;
    text-align:center; line-height:1.15; }}
.hook em {{ color:{_ORANGE}; font-style:normal; }}
"""
    hook_body = f"""
<div class="badge">📊 DATA ALERT</div>
<div class="hook">{_esc(hook).replace(" ", "<br>", 2)}</div>
"""
    frames.append((_wrap(hook_body, css1), 2.0))

    # ── Screen 2: Counter rolling (3 steps × 2s) ───────────────────────────
    steps = _get_counter_steps(stat)
    for i, val in enumerate(steps):
        is_final = i == len(steps) - 1
        frames.append((_stat_counter_frame(hook, val, source, is_final), 2.0))

    # ── Screen 3: Detail + CTA (5s) ─────────────────────────────────────────
    css3 = f"""
.stat-big {{ font-size:120px; font-weight:900; color:{_ORANGE};
    text-align:center; margin-bottom:40px; line-height:1; }}
.detail {{ background:#111; border-radius:20px; padding:36px 44px;
    width:100%; margin-bottom:44px; border-left:6px solid {_ORANGE}; }}
.detail-text {{ font-size:36px; font-weight:700; color:#fff; line-height:1.5; }}
.source-text {{ font-size:26px; color:rgba(255,255,255,.45); margin-top:14px; }}
.cta-box {{ background:{_ORANGE}; border-radius:20px; padding:28px 44px; width:100%; }}
.cta-text {{ font-size:36px; font-weight:900; color:#fff; text-align:center; }}
"""
    cta_body = f"""
<div class="stat-big">{_esc(stat)}</div>
<div class="detail">
    <div class="detail-text">{_esc(detail)}</div>
    <div class="source-text">Source: {_esc(source)}</div>
</div>
<div class="cta-box">
    <div class="cta-text">Practice karo → {BRAND_URL}</div>
</div>
"""
    frames.append((_wrap(cta_body, css3), 5.0))

    return frames


# ── Format 3: Comparison Split ("This vs That") ──────────────────────────────

def _comparison_frame(wrong_items: list[str], right_items: list[str], show_n: int, show_cta: bool = False) -> str:
    """Render split-screen comparison showing first `show_n` pairs."""

    def item_html(text: str, side: str) -> str:
        bg = f"{_RED}22" if side == "wrong" else f"{_GREEN}22"
        border = _RED if side == "wrong" else _GREEN
        return f"""<div style="background:{bg}; border:2px solid {border};
            border-radius:14px; padding:18px 24px; margin-bottom:14px;">
            <span style="font-size:28px; font-weight:700; color:{'#ff6b6b' if side=='wrong' else _GREEN};">{_esc(text)}</span>
        </div>"""

    wrong_html = "".join(item_html(t, "wrong") for t in wrong_items[:show_n])
    right_html = "".join(item_html(t, "right") for t in right_items[:show_n])

    cta_block = ""
    if show_cta:
        cta_block = f"""<div style="position:absolute; bottom:100px; left:60px; right:60px;
            background:{_ORANGE}; border-radius:20px; padding:26px; text-align:center;">
            <span style="font-size:34px; font-weight:900; color:#fff;">Smart prep → {BRAND_URL}</span>
        </div>"""

    css = f"""
.split {{ display:flex; gap:20px; width:100%; margin-bottom:30px; align-items:flex-start; }}
.col {{ flex:1; }}
.col-header {{ font-size:30px; font-weight:900; padding:16px; border-radius:14px;
    text-align:center; margin-bottom:16px; }}
.wrong-header {{ background:{_RED}; color:#fff; }}
.right-header {{ background:{_GREEN}; color:#fff; }}
.top-label {{ font-size:40px; font-weight:900; color:#fff;
    text-align:center; margin-bottom:36px; }}
"""
    body = f"""
<div class="top-label">UPSC Prep: Right vs Wrong</div>
<div class="split">
    <div class="col">
        <div class="col-header wrong-header">❌ WRONG</div>
        {wrong_html}
    </div>
    <div class="col">
        <div class="col-header right-header">✅ RIGHT</div>
        {right_html}
    </div>
</div>
{cta_block}
"""
    return _wrap(body, css)


def _build_comparison_html(question_data: dict) -> list[tuple[str, float]]:
    """Progressive reveal comparison: 4 frames (1 item, 2, 3, 4+CTA).
    Total: 4 × 3s = 12s.
    """
    idx = datetime.now().weekday() % len(COMPARISONS)
    cmp = COMPARISONS[idx]
    wrong = cmp["wrong"]
    right = cmp["right"]
    max_n = min(len(wrong), len(right), 4)

    frames: list[tuple[str, float]] = []
    for n in range(1, max_n + 1):
        show_cta = n == max_n
        frames.append((_comparison_frame(wrong, right, n, show_cta), 3.0))

    return frames


# ── Format 4: Loop Format ("3 Second Answer") ────────────────────────────────

def _build_loop_format_html(question_data: dict) -> list[tuple[str, float]]:
    """5-screen loop format that visually connects end back to start.
    Total: 1+3+3+3+3 = 13s.
    """
    q = _esc(question_data.get("question", ""))
    correct_letter = str(question_data.get("correct_answer", "A")).upper()
    opts_map = {
        "A": question_data.get("option_a", ""),
        "B": question_data.get("option_b", ""),
        "C": question_data.get("option_c", ""),
        "D": question_data.get("option_d", ""),
    }
    answer_text = _esc(opts_map.get(correct_letter, question_data.get("correct_option_text", "")))
    explanation = _esc((question_data.get("explanation", "") or "")[:140])
    year = _esc(str(question_data.get("year", "")))

    frames: list[tuple[str, float]] = []

    # ── Screen 1 (1s): "Can you answer this?" — matches Screen 5 visually ──
    css1 = f"""
.cta-big {{ font-size:80px; font-weight:900; color:#fff;
    text-align:center; line-height:1.15; }}
.cta-big em {{ color:{_ORANGE}; font-style:normal; }}
.sub {{ font-size:46px; font-weight:700; color:rgba(255,255,255,.5);
    text-align:center; margin-top:30px; }}
.orb {{ width:180px; height:180px; border-radius:50%;
    background:{_ORANGE}; display:flex; align-items:center;
    justify-content:center; margin-bottom:50px;
    box-shadow:0 0 60px {_ORANGE}88; }}
.orb-text {{ font-size:90px; }}
"""
    category = question_data.get("category", "").strip()
    _loop_hooks = [
        ("Can you<br><em>answer</em><br>this?", "Tap to test yourself ↓"),
        (f"<em>{category}</em><br>question —<br>3 seconds", f"UPSC {year}"),
        ("Answer in<br><em>3 seconds</em><br>or less", "Ready? Go ↓"),
        (f"This <em>{year}</em><br>PYQ is<br>tricky", "Think fast 🤔"),
        (f"Quick<br><em>{category}</em><br>challenge", "Can you get it right?"),
    ]
    _lh = random.choice(_loop_hooks)
    body1 = f"""
<div class="orb"><div class="orb-text">🧠</div></div>
<div class="cta-big">{_lh[0]}</div>
<div class="sub">{_lh[1]}</div>
"""
    frames.append((_wrap(body1, css1), 1.0))

    # ── Screen 2 (3s): The Question ─────────────────────────────────────────
    css2 = f"""
.year-tag {{ font-size:28px; color:{_ORANGE}; font-weight:700;
    border:2px solid {_ORANGE}; padding:10px 28px; border-radius:40px;
    margin-bottom:40px; }}
.qtext {{ font-size:44px; font-weight:800; color:#fff; line-height:1.4;
    text-align:center; }}
.hint {{ font-size:32px; color:rgba(255,255,255,.4);
    text-align:center; margin-top:40px; font-weight:600; }}
"""
    body2 = f"""
<div class="year-tag">UPSC {year}</div>
<div class="qtext">{q}</div>
<div class="hint">Answer in 3 seconds ↓</div>
"""
    frames.append((_wrap(body2, css2), 3.0))

    # ── Screen 3 (3s): Countdown 3 → 1 (1s each) ───────────────────────────
    for count in [3, 2, 1]:
        color = _RED if count == 3 else (_ORANGE if count == 2 else _GREEN)
        css_c = f"""
.count-label {{ font-size:40px; font-weight:700; color:rgba(255,255,255,.5);
    text-align:center; margin-bottom:40px; }}
.big-num {{ font-size:280px; font-weight:900; color:{color};
    text-align:center; line-height:1; }}
"""
        body_c = f"""
<div class="count-label">Time's running out...</div>
<div class="big-num">{count}</div>
"""
        frames.append((_wrap(body_c, css_c), 1.0))

    # ── Screen 4 (3s): Answer ───────────────────────────────────────────────
    css4 = f"""
.ans-header {{ font-size:44px; font-weight:900; color:{_GREEN};
    text-align:center; margin-bottom:40px; }}
.ans-badge {{ background:{_GREEN}22; border:3px solid {_GREEN};
    border-radius:20px; padding:32px 40px; width:100%; margin-bottom:30px; }}
.ans-letter {{ font-size:40px; font-weight:900; color:{_GREEN}; margin-bottom:8px; }}
.ans-text {{ font-size:36px; font-weight:700; color:#fff; line-height:1.4; }}
.exp {{ background:#111; border-radius:16px; padding:28px 34px;
    width:100%; border-left:5px solid {_ORANGE}; }}
.exp-text {{ font-size:28px; color:#ccc; line-height:1.6; font-weight:500; }}
"""
    body4 = f"""
<div class="ans-header">✅ ANSWER!</div>
<div class="ans-badge">
    <div class="ans-letter">Option {correct_letter}</div>
    <div class="ans-text">{answer_text}</div>
</div>
<div class="exp"><div class="exp-text">{explanation}</div></div>
"""
    frames.append((_wrap(body4, css4), 3.0))

    # ── Screen 5 (3s): Loop back — mirrors Screen 1 visually ────────────────
    css5 = f"""
.next-big {{ font-size:66px; font-weight:900; color:#fff;
    text-align:center; line-height:1.2; margin-bottom:40px; }}
.next-big em {{ color:{_ORANGE}; font-style:normal; }}
.arrow {{ font-size:100px; text-align:center; margin-bottom:40px; }}
.sub2 {{ font-size:36px; font-weight:700; color:rgba(255,255,255,.5);
    text-align:center; }}
"""
    body5 = f"""
<div class="arrow">👉</div>
<div class="next-big">Next question<br><em>tomorrow</em></div>
<div class="sub2">Follow so you don't miss it!</div>
"""
    frames.append((_wrap(body5, css5), 3.0))

    return frames


# ── Old non-quiz builder (kept for backward compat) ──────────────────────────

def _build_non_quiz_html(gradient: str, day_format: str, question_data: dict) -> str:
    """Legacy fallback: builds old-style non-quiz HTML. Returns a single HTML string."""
    from bot.formatter import (
        format_shocking_stat,
        format_myth_buster,
        format_this_or_that,
        format_subject_breakdown,
        format_motivation,
    )

    formatters = {
        "shocking_stat": format_shocking_stat,
        "myth_buster": format_myth_buster,
        "this_or_that": format_this_or_that,
        "subject_breakdown": format_subject_breakdown,
        "motivation_data": format_motivation,
    }
    formatter = formatters.get(day_format, format_shocking_stat)
    text_content = formatter() or "UPSC PYQ Analysis"
    lines = [line for line in text_content.split("\n") if line.strip()]
    hook = lines[0] if lines else "UPSC Insight"
    body_html = "".join(
        f'<div class="body-line">{line}</div>' for line in lines[1:][:8]
    )

    return f"""<!DOCTYPE html>
<html><head><style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
    width: 1080px; height: 1920px;
    background: {gradient};
    font-family: 'Segoe UI', sans-serif;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    padding: 60px 50px;
}}
.hook {{ font-size: 64px; font-weight: 800; color: white;
    text-align: center; line-height: 1.3; margin-bottom: 50px;
    text-shadow: 0 4px 20px rgba(0,0,0,0.3); }}
.body-card {{ background: rgba(255,255,255,0.95);
    border-radius: 30px; padding: 50px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.2);
    width: 100%; max-width: 960px; }}
.body-line {{ font-size: 36px; color: #1a1a2e;
    line-height: 1.6; margin-bottom: 12px; font-weight: 500; }}
.footer {{ margin-top: 50px; background: rgba(255,255,255,0.2);
    border-radius: 25px; padding: 20px 40px; }}
.footer-text {{ font-size: 28px; font-weight: 700; color: white; text-align: center; }}
</style></head><body>
    <div class="hook">{hook}</div>
    <div class="body-card">{body_html}</div>
    <div class="footer"><div class="footer-text">{BRAND_NAME}</div></div>
</body></html>"""


# ── Rendering helpers ─────────────────────────────────────────────────────────

def _pick_music() -> Path:
    """Pick a random music file from templates directory."""
    music_files = sorted(TEMPLATES_DIR.glob("*.mp3"))
    if not music_files:
        raise FileNotFoundError(f"No music files found in {TEMPLATES_DIR}")
    return random.choice(music_files)


def _make_hti(output_dir: Path) -> Html2Image:
    """Create one Html2Image instance (launches Chrome once)."""
    import os, shutil
    is_ci = os.getenv("CI") == "true" or os.getenv("GITHUB_ACTIONS") == "true"
    flags = [
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--disable-gpu",
        "--headless=new",
        "--disable-software-rasterizer",
    ]
    # Find chromium/chrome binary
    browser_path = None
    for candidate in ["chromium-browser", "chromium", "google-chrome", "google-chrome-stable"]:
        found = shutil.which(candidate)
        if found:
            browser_path = found
            break
    # temp_path must also be accessible by Chrome (snap can't read /tmp)
    temp_dir = os.path.join(os.path.expanduser("~"), "hti_temp")
    os.makedirs(temp_dir, exist_ok=True)
    kwargs = {
        "output_path": str(output_dir),
        "temp_path": temp_dir,
        "custom_flags": flags,
    }
    if browser_path:
        kwargs["browser_executable"] = browser_path
    return Html2Image(**kwargs)


def _render_html_to_image(html_content: str, output_path: Path, hti: Html2Image | None = None) -> None:
    """Render HTML to PNG. Creates its own hti instance if none provided."""
    if hti is None:
        hti = _make_hti(output_path.parent)
    hti.screenshot(html_str=html_content, save_as=output_path.name, size=(VIDEO_W, VIDEO_H))
    if not output_path.exists():
        # html2image may write to its own output_path, check there
        alt = Path(hti.output_path) / output_path.name
        if alt.exists() and str(alt) != str(output_path):
            import shutil
            shutil.move(str(alt), str(output_path))
        else:
            raise FileNotFoundError(f"html2image failed to render: {output_path}")
    logger.debug("Rendered → %s (%d bytes)", output_path.name, output_path.stat().st_size)


def _frames_to_video(
    frames: list[tuple[str, float]],
    output_path: Path,
) -> Path:
    """Render HTML frames to images, sequence into video with music."""
    # Use home-based temp dir (snap chromium can't write to /tmp or hidden dirs)
    import os
    base_tmp = Path(os.path.expanduser("~")) / "hti_render"
    base_tmp.mkdir(exist_ok=True)
    temp_dir = Path(tempfile.mkdtemp(dir=str(base_tmp)))
    try:
        hti = _make_hti(temp_dir)
        clips = []
        for i, (html, duration) in enumerate(frames):
            img_path = temp_dir / f"frame_{i:03d}.png"
            _render_html_to_image(html, img_path, hti)
            img_arr = np.array(Image.open(img_path))
            clips.append(ImageClip(img_arr).with_duration(duration))

        video = concatenate_videoclips(clips, method="compose")
        total_dur = sum(d for _, d in frames)

        music_path = _pick_music()
        raw_audio = AudioFileClip(str(music_path))
        audio = raw_audio.subclipped(0, min(total_dur, raw_audio.duration))
        video = video.with_audio(audio)

        video.write_videofile(
            str(output_path),
            codec="libx264",
            audio_codec="aac",
            fps=30,
            ffmpeg_params=["-movflags", "+faststart"],
            logger=None,
        )

        audio.close()
        raw_audio.close()
        video.close()
        for c in clips:
            c.close()

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

    return output_path


# ── Public API ────────────────────────────────────────────────────────────────

def generate_html_video(
    question_data: dict,
    output_path: Path | None = None,
) -> Path:
    """Generate a viral Instagram/YouTube Shorts video from question data.

    Format is selected automatically by weekday via get_video_format_for_day().

    Args:
        question_data: Dict with keys: question, option_a/b/c/d, year, category,
                       correct_answer, correct_option_text, explanation (optional)
        output_path:   Optional output path (defaults to OUTPUT_DIR/quiz_html_<ts>.mp4)

    Returns:
        Path to the generated .mp4 file.
    """
    if output_path is None:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = OUTPUT_DIR / f"quiz_html_{ts}.mp4"

    _ensure_heavy_imports()
    fmt = get_video_format_for_day()
    logger.info("Generating video — format: %s → %s", fmt, output_path.name)

    try:
        if fmt == "quiz":
            gradient, name = random.choice(GRADIENT_PALETTES)
            logger.info("Quiz gradient: %s", name)
            frames = _build_quiz_html(question_data, gradient)

        elif fmt == "timer_challenge":
            frames = _build_timer_challenge_html(question_data)

        elif fmt == "shocking_stat":
            frames = _build_shocking_stat_html(question_data)

        elif fmt == "comparison":
            frames = _build_comparison_html(question_data)

        elif fmt == "loop_format":
            frames = _build_loop_format_html(question_data)

        else:
            # Fallback: legacy non-quiz HTML as single frame
            gradient, _ = random.choice(GRADIENT_PALETTES)
            html = _build_non_quiz_html(gradient, fmt, question_data)
            frames = [(html, 15.0)]

    except Exception as exc:
        logger.warning("Template build failed (%s) — falling back to quiz", exc)
        gradient, _ = random.choice(GRADIENT_PALETTES)
        frames = _build_quiz_html(question_data, gradient)

    _frames_to_video(frames, output_path)

    mb = output_path.stat().st_size / (1024 * 1024)
    logger.info("Video saved: %s (%.1f MB)", output_path.name, mb)
    return output_path
