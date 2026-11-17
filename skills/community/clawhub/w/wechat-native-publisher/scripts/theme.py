# -*- coding: utf-8 -*-
"""
wechat-native-publisher 主题系统（多主题可换肤）

主题由 scripts/themes.json 驱动，三套内置：
  signature  绿橙旗舰  —— 绿主导(结构) + 橙点缀(焦点)，职场/观点/个人IP（默认）
  mono       黑白极简  —— 石墨黑结构 + 经典蓝唯一强调，通用职场/科技/方法论
  paper      暖棕纸感  —— 暖棕结构 + 陶土橙强调 + 米纸卡片，读书/随笔/文化

用法（关键：必须在 import renderer 之前调用 apply_theme，renderer 是
from theme import X 的即时绑定，先换肤后 import 即拿到新主题色）：

    import theme
    theme.apply_theme("paper")          # 换肤
    from renderer import p, ...         # 此刻绑定的即 paper 色

未调用 apply_theme 时，模块变量 = signature（绿橙旗舰）默认值。

所有值为微信可存活的 rgb() 格式（不要用 hex，微信富文本清洗会丢 hex 颜色）。
"""
import json
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_THEMES_FILE = os.path.join(_HERE, "themes.json")

# ===== 槽位默认值（= signature 绿橙旗舰，保持向后兼容） =====
GREEN          = "rgb(45,157,92)"        # 结构主色：徽章/竖线/装饰/PART
GREEN_DARK     = "rgb(31,122,68)"        # 结构深色：重点/小标/图注
GREEN_LIGHT    = "rgb(123,196,152)"      # 结构浅色：英文小标
GREEN_BG       = "rgb(238,247,241)"      # 结构浅卡底
GREEN_BORDER   = "rgb(210,231,220)"      # 结构浅卡边
ORANGE_TEXT    = "rgb(183,64,18)"        # 焦点深色：概念文字/强调
ORANGE_BG      = "rgb(255,236,227)"      # 焦点荧光笔底
ORANGE_ACCENT  = "rgb(255,120,73)"       # 焦点主色：icon/左边条/强调
ORANGE_CARD_BG = "rgb(255,246,241)"      # 焦点浅卡底（比荧光笔更浅）
ORANGE_CARD_BRD = "rgb(255,222,208)"     # 焦点浅卡边
ORANGE_SHADOW  = "rgba(183,64,18,0.15)"  # 焦点投影
BODY           = "rgb(26,26,26)"         # 正文黑
GRAY           = "rgb(138,138,138)"      # 次要灰
GRAY_LT        = "rgb(231,231,231)"      # 分隔灰
FOOT           = "rgb(153,153,153)"      # 注释灰

# ===== 内置主题兜底（themes.json 缺失时用） =====
_DEFAULT_COLORS = {k: globals()[k] for k in (
    "GREEN", "GREEN_DARK", "GREEN_LIGHT", "GREEN_BG", "GREEN_BORDER",
    "ORANGE_TEXT", "ORANGE_BG", "ORANGE_ACCENT", "ORANGE_CARD_BG",
    "ORANGE_CARD_BRD", "ORANGE_SHADOW", "BODY", "GRAY", "GRAY_LT", "FOOT",
)}


def _load_themes():
    """从 themes.json 读取全部主题；文件缺失/损坏时返回 {signature: 兜底}"""
    if os.path.exists(_THEMES_FILE):
        try:
            with open(_THEMES_FILE, encoding="utf-8") as f:
                data = json.load(f)
            if data:
                return data
        except Exception:
            pass
    return {"signature": {
        "id": "signature", "name": "绿橙旗舰", "name_en": "Signature",
        "desc": "内置兜底", "scenes": "",
        "colors": dict(_DEFAULT_COLORS),
        "hex": {k: v for k, v in {
            "GREEN": "#2d9d5c", "GREEN_DARK": "#1f7a44", "GREEN_LIGHT": "#7bc498",
            "GREEN_BG": "#eef7f1", "GREEN_BORDER": "#d2e7dc",
            "ORANGE_TEXT": "#b74012", "ORANGE_BG": "#ffece3", "ORANGE_ACCENT": "#ff7849",
            "ORANGE_CARD_BG": "#fff6f1", "ORANGE_CARD_BRD": "#ffded0",
            "BODY": "#1a1a1a", "GRAY": "#8a8a8a", "GRAY_LT": "#e7e7e7", "FOOT": "#999999",
        }.items()},
    }}


THEMES = _load_themes()


def theme_names():
    """可用主题 id 列表（保持 json 顺序）"""
    return list(THEMES.keys())


def get_theme(name):
    """取主题 dict；未知主题名返回 None"""
    return THEMES.get(name)


def apply_theme(name="signature"):
    """
    应用主题：把该主题 colors 覆盖到本模块的槽位变量。
    必须在 import renderer 之前调用。返回实际生效的主题 dict。
    """
    theme = THEMES.get(name) or THEMES.get("signature")
    for k, v in theme["colors"].items():
        globals()[k] = v
    return theme


# 供 PIL 封面等本地场景取 hex（按主题）
def hex_colors(name="signature"):
    theme = THEMES.get(name) or THEMES.get("signature")
    return theme.get("hex") or theme.get("colors")


# ===== 买家自定义主题：给定主色/强调色 → 衍生 16 色槽 =====
# 衍生逻辑：结构族(主色)用于徽章/竖线/列表/章节方块等骨架，
#          焦点族(强调色)用于荧光笔/概念/结尾卡等「想让人看见」的元素。
#          中性色(BODY/GRAY/GRAY_LT/FOOT)不随买家色变动，保证正文可读。

def _hex_to_rgb(h):
    h = h.strip().lstrip("#")
    if len(h) != 6:
        raise ValueError(f"颜色需为 #RRGGBB 格式：{h}")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _rgb_to_hex(r, g, b):
    return "#{:02x}{:02x}{:02x}".format(int(round(r)), int(round(g)), int(round(b)))


def _mix_hex(a, b, t):
    """t=0 → a，t=1 → b（线性混合），返回 hex"""
    ar, ag, ab = _hex_to_rgb(a)
    br, bg, bb = _hex_to_rgb(b)
    return _rgb_to_hex(ar + (br - ar) * t, ag + (bg - ag) * t, ab + (bb - ab) * t)


def _rgba_str(hex_color, alpha):
    r, g, b = _hex_to_rgb(hex_color)
    return f"rgba({r},{g},{b},{alpha})"


def build_custom(primary="#2d9d5c", accent="#ff7849", name="custom",
                 name_en="Custom", desc="买家自定义配色（主色/强调色衍生）"):
    """由买家主色/强调色衍生一套完整主题 dict（含 colors rgb + hex 两版）。
    内置中性槽保持默认。primary/accent 接受 #RRGGBB（兼容不带 #）。"""
    primary, accent = _hex_to_rgb(primary), _hex_to_rgb(accent)
    p_hex, a_hex = _rgb_to_hex(*primary), _rgb_to_hex(*accent)

    def rgb(h):
        r, g, b = _hex_to_rgb(h)
        return f"rgb({r},{g},{b})"

    def mix_to(c, target, t):
        return _mix_hex(c, target, t)

    # 先生成 hex 中间值（colors/hexmap 同源，避免二次转换）
    hv = {
        "GREEN": p_hex,
        "GREEN_DARK": mix_to(p_hex, "#000000", 0.24),
        "GREEN_LIGHT": mix_to(p_hex, "#ffffff", 0.60),
        "GREEN_BG": mix_to(p_hex, "#ffffff", 0.90),
        "GREEN_BORDER": mix_to(p_hex, "#ffffff", 0.80),
        "ORANGE_ACCENT": a_hex,
        "ORANGE_TEXT": mix_to(a_hex, "#000000", 0.38),
        "ORANGE_BG": mix_to(a_hex, "#ffffff", 0.86),
        "ORANGE_CARD_BG": mix_to(a_hex, "#ffffff", 0.93),
        "ORANGE_CARD_BRD": mix_to(a_hex, "#ffffff", 0.80),
        "BODY": "#1a1a1a", "GRAY": "#8a8a8a", "GRAY_LT": "#e7e7e7", "FOOT": "#999999",
    }
    colors = {k: rgb(v) for k, v in hv.items()}
    colors["ORANGE_SHADOW"] = _rgba_str(a_hex, 0.15)
    hexmap = dict(hv)
    return {
        "id": name, "name": "自定义配色", "name_en": name_en,
        "desc": desc, "scenes": "买家自定义：主色(结构) + 强调色(焦点)",
        "colors": colors, "hex": hexmap,
    }


def apply_custom(primary="#2d9d5c", accent="#ff7849"):
    """把自定义主题注入 THEMES['custom'] 并立即换肤。返回主题 dict。
    供买家 wnp_profile.json 的 theme=custom + colors{primary,accent} 使用。"""
    t = build_custom(primary, accent, name="custom")
    THEMES["custom"] = t
    for k, v in t["colors"].items():
        globals()[k] = v
    return t


if __name__ == "__main__":
    import sys
    for t in theme_names():
        meta = THEMES[t]
        print(f"[{t}] {meta['name']} · {meta['name_en']} · {meta['scenes']}")
    if len(sys.argv) > 1:
        apply_theme(sys.argv[1])
        print(f"-> applied {sys.argv[1]}, GREEN={GREEN}, ORANGE_ACCENT={ORANGE_ACCENT}")
