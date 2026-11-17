"""
SkillGate Badge Generator — 生成漂亮的 SVG Trust Score 徽章。
"""


def generate_badge(score: int, grade: str) -> str:
    """Generate a beautiful SVG badge for Trust Score."""

    # Color based on grade
    color_map = {
        "A+": "#238636",
        "A": "#2da44e",
        "B": "#d29922",
        "C": "#da3633",
        "D": "#6e7681",
    }

    bg_color = color_map.get(grade, "#6e7681")
    label = "trust score"
    value = f"{score}/100"

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="140" height="20">
  <linearGradient id="g" x2="0" y2="1">
    <stop offset="0" stop-color="#555"/>
    <stop offset="1" stop-color="#333"/>
  </linearGradient>
  <rect width="140" height="20" rx="3" fill="url(#g)"/>
  <rect x="70" width="70" height="20" rx="3" fill="{bg_color}"/>
  <rect x="67" width="4" height="20" fill="{bg_color}"/>
  <text x="35" y="14.5" font-family="DejaVu Sans, Verdana, sans-serif" font-size="11" fill="#fff" text-anchor="middle">{label}</text>
  <text x="105" y="14.5" font-family="DejaVu Sans, Verdana, sans-serif" font-size="11" font-weight="bold" fill="#fff" text-anchor="middle">{value}</text>
</svg>'''

    return svg


def generate_grade_badge(grade: str) -> str:
    """Generate a grade-only badge."""

    color_map = {
        "A+": "#238636",
        "A": "#2da44e",
        "B": "#d29922",
        "C": "#da3633",
        "D": "#6e7681",
    }

    bg_color = color_map.get(grade, "#6e7681")

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="80" height="20">
  <linearGradient id="g" x2="0" y2="1">
    <stop offset="0" stop-color="#555"/>
    <stop offset="1" stop-color="#333"/>
  </linearGradient>
  <rect width="80" height="20" rx="3" fill="url(#g)"/>
  <rect x="40" width="40" height="20" rx="3" fill="{bg_color}"/>
  <rect x="37" width="4" height="20" fill="{bg_color}"/>
  <text x="20" y="14.5" font-family="DejaVu Sans, Verdana, sans-serif" font-size="11" fill="#fff" text-anchor="middle">grade</text>
  <text x="60" y="14.5" font-family="DejaVu Sans, Verdana, sans-serif" font-size="11" font-weight="bold" fill="#fff" text-anchor="middle">{grade}</text>
</svg>'''

    return svg


if __name__ == "__main__":
    badge = generate_badge(95, "A+")
    print(badge)
