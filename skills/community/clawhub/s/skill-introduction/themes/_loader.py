"""主题加载器：读取 themes/<name>.css，返回 CSS 字符串。

设计原则（严守 feedback_preset_visual_only_no_layout.md）：
- base.css = 布局骨架（display/flex/grid/width/padding/margin/position 等），主题无关，永远加载
- <theme>.css = 仅视觉（color/background/border/box-shadow/font + :root 变量），按 --theme 选择
- 深色主题的 card-body 绝不写 background；hover 改 border 必须给 transparent 基准
"""
from pathlib import Path

THEMES_DIR = Path(__file__).resolve().parent
DEFAULT_THEME = "light"
AVAILABLE = ["light", "aurora", "techblue", "finance"]


def load_theme_css(theme: str = DEFAULT_THEME) -> str:
    """返回 base.css + <theme>.css 拼接结果。未知主题回退默认。"""
    if theme not in AVAILABLE:
        theme = DEFAULT_THEME
    base = (THEMES_DIR / "base.css").read_text(encoding="utf-8")
    theme_css = (THEMES_DIR / f"{theme}.css").read_text(encoding="utf-8")
    return base + "\n" + theme_css


def list_themes() -> list:
    return list(AVAILABLE)
