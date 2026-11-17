#!/usr/bin/env python3
"""微信公众号风格 / 品牌元素提取器。

核心能力：
1. 抓取公众号文章 HTML（支持 mp.weixin.qq.com）
2. 提取颜色调色板（主色、背景色、文字色、强调色）
3. 提取排版规则（字号、行高、间距、字重）
4. 从品牌素材提取元素（图片主色 / PDF 文本与首页配色 / 品牌文档色值）
5. 生成标准主题组件库格式（兼容 WeChatLayout Mode A）

用法:
    style_extractor.py <url>                        # 公众号文章 URL
    style_extractor.py <url> --output <theme-name>
    style_extractor.py --html <file.html> --output <name>   # 本地 HTML
    style_extractor.py --image <logo.png> --output <name>   # 品牌图/参考图
    style_extractor.py --pdf <brand-manual.pdf> --output <name>  # 品牌手册 PDF
    style_extractor.py --doc <brand.md> --output <name>     # 品牌文档（md/txt/docx）

依赖: requests, beautifulsoup4（基础）；pillow（图片提色）；pymupdf（PDF）
安装: pip install -r requirements.txt
"""
import argparse
import json
import re
import sys
import zipfile
from collections import Counter
from pathlib import Path

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    _script_dir = Path(__file__).resolve().parent
    _req_file = _script_dir.parent / "requirements.txt"
    print(
        f"❌ 缺少外部依赖（requests / beautifulsoup4）。\n"
        f"   Mode B 风格提取需要这两个库，Mode A 排版和校验脚本不需要。\n"
        f"   安装命令:  pip install -r {_req_file}\n"
        f"   或:        pip install requests beautifulsoup4"
    )
    sys.exit(1)


WECHAT_URL_PATTERN = re.compile(r"https://mp\.weixin\.qq\.com/s/[\w-]+")


def fetch_wechat_html(url):
    """抓取公众号文章 HTML。

    合规说明：
    - 仅用于白名单内 mp.weixin.qq.com 公开文章的风格提取
    - 模拟浏览器 User-Agent 是为了与微信公开页面正常交互（避免被基础 UA 拦截）
    - 本脚本不实现绕过验证码/登录态/IP 代理池等规避反爬措施的手段
    - 使用者需自行确保抓取行为符合腾讯服务条款与当地法律法规，自行承担合规责任
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }
    try:
        resp = requests.get(url, headers=headers, timeout=30)
        resp.encoding = "utf-8"
        return resp.text
    except Exception as e:
        print(f"❌ 抓取失败: {e}")
        sys.exit(1)


def parse_html(html):
    return BeautifulSoup(html, "html.parser")


def extract_colors(soup):
    colors = Counter()
    
    def extract_from_attr(attr_value):
        if not attr_value:
            return
        # 注意：`#` 不能放进字符类，否则 6 位色值会被截成 5 位（如 #374151 → #37415）
        color_pattern = re.compile(r"color:\s*((?:#[0-9a-fA-F]{6})|(?:#[0-9a-fA-F]{3})|rgb\([^)]+\)|rgba\([^)]+\))", re.I)
        for match in color_pattern.finditer(attr_value):
            colors[match.group(1).lower()] += 1
        bg_pattern = re.compile(r"background:\s*((?:#[0-9a-fA-F]{6})|(?:#[0-9a-fA-F]{3})|rgb\([^)]+\)|rgba\([^)]+\)|linear-gradient\([^)]+\))", re.I)
        for match in bg_pattern.finditer(attr_value):
            colors[match.group(1).lower()] += 1

    for tag in soup.find_all(True):
        style = tag.get("style", "")
        extract_from_attr(style)

    return colors


def extract_typography(soup):
    fonts = Counter()
    font_sizes = Counter()
    line_heights = Counter()
    font_weights = Counter()

    for tag in soup.find_all(["p", "span", "h1", "h2", "h3", "h4", "section"]):
        style = tag.get("style", "")
        if "font-family" in style.lower():
            m = re.search(r"font-family:\s*([^;]+)", style, re.I)
            if m:
                fonts[m.group(1).strip()] += 1
        if "font-size" in style.lower():
            m = re.search(r"font-size:\s*([\d.]+)(px|em|rem)", style, re.I)
            if m:
                font_sizes[m.group(1)] += 1
        if "line-height" in style.lower():
            m = re.search(r"line-height:\s*([\d.]+)", style, re.I)
            if m:
                line_heights[m.group(1)] += 1
        if "font-weight" in style.lower():
            m = re.search(r"font-weight:\s*(\d+|bold)", style, re.I)
            if m:
                font_weights[m.group(1)] += 1

    return {
        "font": fonts.most_common(1)[0][0] if fonts else "PingFang SC, Microsoft YaHei, sans-serif",
        "font_sizes": [k for k, _ in font_sizes.most_common(5)],
        "line_heights": [k for k, _ in line_heights.most_common(3)],
        "font_weights": [k for k, _ in font_weights.most_common(3)],
    }


def extract_spacing(soup):
    margins = Counter()
    paddings = Counter()

    for tag in soup.find_all(True):
        style = tag.get("style", "")
        for prop in ["margin", "margin-top", "margin-bottom", "padding", "padding-top", "padding-bottom"]:
            if prop in style.lower():
                m = re.search(f"{prop}:\\s*([\\d.]+)px", style, re.I)
                if m:
                    if "margin" in prop:
                        margins[m.group(1)] += 1
                    else:
                        paddings[m.group(1)] += 1

    return {
        "margins": [k for k, _ in margins.most_common(5)],
        "paddings": [k for k, _ in paddings.most_common(5)],
    }



HEX_COLOR_RE = re.compile(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b")


def _load_optional(name, pip_name):
    """按需导入可选依赖（pillow / pymupdf），失败给出精确安装提示。"""
    try:
        if name == "PIL":
            from PIL import Image
            return Image
        if name == "fitz":
            try:
                import fitz  # PyMuPDF < 1.26 的导入名
            except ImportError:
                import pymupdf as fitz  # PyMuPDF >= 1.26 改为主名
            return fitz
    except ImportError:
        print(
            f"❌ 缺少可选依赖 {name}。\n"
            f"   该输入类型（{pip_name}）需要此库，其余功能不受影响。\n"
            f"   安装命令:  pip install {pip_name}"
        )
        sys.exit(1)


def extract_image_colors(image_path):
    """从品牌图/参考图提取主色板（PIL 颜色量化）。

    返回 Counter: 十六进制色值 → 像素占比权重（放大 10000 便于频次统计）。
    品牌图配色通常集中在少数色块，量化后按占比降序即可还原品牌色板。
    """
    Image = _load_optional("PIL", "pillow")
    img = Image.open(image_path).convert("RGB")
    img.thumbnail((160, 160))  # 缩小提速，不影响主色判断
    quantized = img.quantize(colors=8, method=2)  # MEDIANCUT 聚类
    palette = quantized.getpalette()
    counts = Counter(quantized.getdata())
    total = sum(counts.values()) or 1
    result = Counter()
    for idx, cnt in counts.most_common(8):
        r, g, b = palette[idx * 3: idx * 3 + 3]
        result[f"#{r:02x}{g:02x}{b:02x}"] = round(cnt / total * 10000)
    return result


def extract_docx_text(path):
    """提取 .docx 纯文本（zipfile + 正则，零额外依赖）。"""
    parts = []
    with zipfile.ZipFile(path) as zf:
        xml = zf.read("word/document.xml").decode("utf-8", errors="replace")
    for m in re.finditer(r"<w:t[^>]*>([^<]*)</w:t>", xml):
        parts.append(m.group(1))
    return "".join(parts)


def extract_doc_text(path):
    """从品牌文档（md/txt/docx）提取文本与色值。"""
    suffix = Path(path).suffix.lower()
    if suffix == ".docx":
        text = extract_docx_text(path)
    else:
        text = Path(path).read_text(encoding="utf-8", errors="replace")
    colors = Counter()
    for m in HEX_COLOR_RE.finditer(text):
        colors[m.group(0).lower()] += 1
    return colors, text


def extract_pdf(path):
    """从品牌手册 PDF 提取文本 + 首页配色（PyMuPDF 渲染首页提色）。"""
    fitz = _load_optional("fitz", "pymupdf")
    doc = fitz.open(path)
    text = "".join(page.get_text() for page in doc)
    colors = Counter()
    for m in HEX_COLOR_RE.finditer(text):
        colors[m.group(0).lower()] += 1
    # 渲染首页为像素，走图片提色（品牌手册首页通常是品牌视觉核心）
    try:
        pix = doc[0].get_pixmap(dpi=72)
        png_path = Path(path).with_suffix(".firstpage.png")
        pix.save(str(png_path))
        img_colors = extract_image_colors(png_path)
        colors.update(img_colors)
        png_path.unlink(missing_ok=True)
    except Exception:
        pass  # 渲染失败不影响文本色值提取
    doc.close()
    return colors, text


def _hex_to_hsl(hex_color):
    """#RRGGBB → (h, s, l)，h∈[0,360)，s/l∈[0,1]。"""
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255
    cmax, cmin = max(r, g, b), min(r, g, b)
    l = (cmax + cmin) / 2
    if cmax == cmin:
        return 0.0, 0.0, l
    d = cmax - cmin
    s = d / (2 - cmax - cmin) if l > 0.5 else d / (cmax + cmin)
    if cmax == r:
        hue = ((g - b) / d) % 6
    elif cmax == g:
        hue = (b - r) / d + 2
    else:
        hue = (r - g) / d + 4
    return hue * 60, s, l


def _hsl_to_hex(h, s, l):
    """(h, s, l) → #rrggbb（小写）。"""
    h = h % 360
    c = (1 - abs(2 * l - 1)) * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = l - c / 2
    if h < 60:
        r1, g1, b1 = c, x, 0
    elif h < 120:
        r1, g1, b1 = x, c, 0
    elif h < 180:
        r1, g1, b1 = 0, c, x
    elif h < 240:
        r1, g1, b1 = 0, x, c
    elif h < 300:
        r1, g1, b1 = x, 0, c
    else:
        r1, g1, b1 = c, 0, x
    r, g, b = round((r1 + m) * 255), round((g1 + m) * 255), round((b1 + m) * 255)
    return f"#{r:02x}{g:02x}{b:02x}"


def _is_grayscale(h, s):
    """饱和度极低视为灰度色（graphite 风格）。"""
    return s < 0.12


def _derive_palette_from_primary(primary_hex):
    """从主色推导全套色阶变量。

    依据 5 套手工主题的规律：
    - primary_light: 同 hue，lightness +12%（但不超过 0.85）
    - underline:     同 hue，lightness 提至 0.75（灰度主题用 0.65）
    - bg_light:      同 hue，lightness 提至 0.96，饱和度降至 0.5×
    - border_light:  同 hue，lightness 提至 0.88，饱和度降至 0.6×
    - dark_bg:       同 hue，lightness 降至 max(0.25, l-0.15)
    灰度主题（s<0.12）走灰阶变体。
    """
    h, s, l = _hex_to_hsl(primary_hex)
    gray = _is_grayscale(h, s)

    if gray:
        return {
            "primary_light": _hsl_to_hex(h, s, min(0.55, l + 0.12)),
            "underline":     _hsl_to_hex(h, s, 0.65),
            "bg_light":      _hsl_to_hex(h, s, 0.97),
            "border_light":  _hsl_to_hex(h, s, 0.92),
            "dark_bg":       _hsl_to_hex(h, s, max(0.15, l - 0.12)),
        }

    return {
        "primary_light": _hsl_to_hex(h, s, min(0.85, l + 0.12)),
        "underline":     _hsl_to_hex(h, s, 0.75),
        "bg_light":      _hsl_to_hex(h, s * 0.5, 0.96),
        "border_light":  _hsl_to_hex(h, s * 0.6, 0.88),
        "dark_bg":       _hsl_to_hex(h, s, max(0.25, l - 0.15)),
    }


def _brightness(hex_color):
    """#RRGGBB → 0-255 亮度值。"""
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return (r * 299 + g * 587 + b * 114) / 1000


def analyze_color_palette(colors):
    """从提取的颜色频次构建完整色阶。

    策略：
    1. primary = 频次最高的非中性色（fallback: emerald #059669）
    2. dark_bg = 频次中亮度<80 的最深色，否则从 primary 派生
    3. bg_light = 频次中亮度 180-250 的浅色，否则从 primary 派生
    4. 其余色阶从 primary 经 HSL 派生（primary_light/underline/border_light）
    5. 中性色（title/body/aux/divider/highlight）用通用灰阶默认值
    """
    palette = {
        "primary": "#059669",
        "primary_light": "#10b981",
        "bg_light": "#ecfdf5",
        "border_light": "#d1fae5",
        "highlight": "#fef08a",
        "title": "#1f2937",
        "body": "#374151",
        "aux": "#6b7280",
        "divider": "#e5e7eb",
        "underline": "#6ee7b7",
        "dark_bg": "#059669",
    }

    sorted_colors = colors.most_common(20)
    if not sorted_colors:
        return palette

    # 选主色：优先非灰度的高频色
    primary_found = False
    for color, _ in sorted_colors:
        if not color.startswith("#"):
            continue
        h, s, l = _hex_to_hsl(color)
        if not _is_grayscale(h, s):
            palette["primary"] = color
            primary_found = True
            break
    if not primary_found:
        palette["primary"] = sorted_colors[0][0]

    # 从提取数据补 dark_bg / bg_light（优先用真实值）
    for color, _ in sorted_colors:
        if not color.startswith("#"):
            continue
        bri = _brightness(color)
        if bri < 80:
            palette["dark_bg"] = color
        elif 180 < bri < 250:
            palette["bg_light"] = color

    # 从 primary 派生其余色阶（覆盖默认值 + 真实数据补齐）
    derived = _derive_palette_from_primary(palette["primary"])
    palette["primary_light"] = derived["primary_light"]
    palette["underline"] = derived["underline"]
    palette["border_light"] = derived["border_light"]
    # bg_light / dark_bg：提取数据未命中时用派生值兜底
    if palette["bg_light"] == "#ecfdf5":
        palette["bg_light"] = derived["bg_light"]
    if palette["dark_bg"] == palette["primary"]:
        palette["dark_bg"] = derived["dark_bg"]

    return palette


def generate_theme(name, palette, typography, spacing):
    theme = f"""# {name}主题组件库（{name.lower()}）

> 从公众号文章自动提取的主题。主色 `{palette['primary']}` 只在锚点出现（全文 ≤5 处），大面积白底＋灰阶，彩色只做点缀。

---

## 一、设计变量速查表

| 变量 | 色值 | 用途 |
|------|------|------|
| 主色 | `{palette['primary']}` | 章节编号、CTA 背景、加粗锚点（≤5 处） |
| 主色浅 | `{palette['primary_light']}` | 英文标签、子标题竖条、装饰点 |
| 浅底色 | `{palette['bg_light']}` | 引言卡、引用块、数据卡背景 |
| 浅边框 | `{palette['border_light']}` | 表格边框、徽章边框 |
| 高亮色 | `{palette['highlight']}` | 黄底高亮起始色 |
| 高亮渐变终色 | `#fde68a` | 黄底高亮结束色 |
| 标题色 | `{palette['title']}` | 文章标题、章节标题、子标题 |
| 正文色 | `{palette['body']}` | 正文段落 |
| 辅助文字色 | `{palette['aux']}` | 副标题、说明文字、日期 |
| 分割线色 | `{palette['divider']}` | 封面底部分割线、表格行线 |
| 下划线色 | `{palette['underline']}` | 关键词下划线 |
| 深底白字背景 | `{palette['dark_bg']}` | CTA 区域、表头背景 |

---

## 二、各组件完整 HTML

### 1. 全局容器

```html
<section style="max-width:677px;margin:0 auto;padding:20px 16px;">
<!-- 文章内容 -->
</section>
```

### 2. 封面／标题区

```html
<section style="margin:0 0 32px;">
<section style="width:36px;height:4px;background:{palette['primary']};border-radius:2px;margin-bottom:16px;"></section>
<p style="margin:0 0 10px;line-height:1.4;font-size:24px;font-weight:bold;color:{palette['title']};"><span leaf="">文章标题</span></p>
<p style="margin:0;line-height:1.6;font-size:14px;color:{palette['aux']};"><span leaf="">副标题或日期信息</span></p>
<section style="margin-top:20px;height:1px;background:{palette['divider']};"></section>
</section>
```

### 3. 引言卡

```html
<section style="margin:0 0 28px;padding:20px 24px;background:{palette['bg_light']};border-radius:8px;">
<p style="margin:0 0 12px;line-height:1.8;font-size:15px;color:{palette['body']};"><span leaf="">这是一段引言或导读文字，用浅底卡片突出文章核心价值，帮助读者快速判断是否继续阅读。</span></p>
<p style="margin:0;line-height:1.6;font-size:13px;color:{palette['primary']};text-align:right;"><span leaf="">—— {{作者名}}</span></p>
</section>
```

### 4. 目录导读

```html
<section style="margin:0 0 32px;padding:20px 24px;background:#f9fafb;border-radius:8px;">
<p style="margin:0 0 16px;line-height:1.5;font-size:14px;font-weight:bold;color:{palette['title']};"><span leaf="">本文看点</span></p>
<section style="margin:0 0 12px;display:flex;align-items:flex-start;">
<section style="flex-shrink:0;margin-right:10px;width:20px;height:20px;background:{palette['primary']};border-radius:4px;display:flex;align-items:center;justify-content:center;"><p style="margin:0;line-height:1;font-size:11px;color:#ffffff;font-weight:bold;"><span leaf="">1</span></p></section>
<p style="margin:0;line-height:1.6;font-size:15px;color:{palette['body']};"><span leaf="">核心看点一描述</span></p>
</section>
<section style="margin:0 0 12px;display:flex;align-items:flex-start;">
<section style="flex-shrink:0;margin-right:10px;width:20px;height:20px;background:{palette['primary']};border-radius:4px;display:flex;align-items:center;justify-content:center;"><p style="margin:0;line-height:1;font-size:11px;color:#ffffff;font-weight:bold;"><span leaf="">2</span></p></section>
<p style="margin:0;line-height:1.6;font-size:15px;color:{palette['body']};"><span leaf="">核心看点二描述</span></p>
</section>
<section style="margin:0;display:flex;align-items:flex-start;">
<section style="flex-shrink:0;margin-right:10px;width:20px;height:20px;background:{palette['primary']};border-radius:4px;display:flex;align-items:center;justify-content:center;"><p style="margin:0;line-height:1;font-size:11px;color:#ffffff;font-weight:bold;"><span leaf="">3</span></p></section>
<p style="margin:0;line-height:1.6;font-size:15px;color:{palette['body']};"><span leaf="">核心看点三描述</span></p>
</section>
</section>
```

### 5. 章节标题

```html
<section style="margin:40px 0 20px;display:flex;align-items:baseline;">
<p style="margin:0 12px 0 0;line-height:1;font-size:40px;font-weight:bold;color:{palette['primary']};"><span leaf="">01</span></p>
<section>
<p style="margin:0 0 4px;line-height:1.3;font-size:20px;font-weight:bold;color:{palette['title']};"><span leaf="">章节中文标题</span></p>
<p style="margin:0;line-height:1.4;font-size:12px;color:{palette['primary_light']};letter-spacing:1px;"><span leaf="">ENGLISH LABEL</span></p>
</section>
</section>
```

### 6. 子标题

```html
<section style="margin:28px 0 12px;padding-left:12px;border-left:3px solid {palette['primary_light']};">
<p style="margin:0;line-height:1.5;font-size:17px;font-weight:bold;color:{palette['title']};"><span leaf="">子标题内容</span></p>
</section>
```

### 7. 正文段落

```html
<p style="margin:0 0 20px;line-height:1.9;font-size:16px;color:{palette['body']};"><span leaf="">这是标准正文段落，行高 1.9，字号 16px。每个段落之间保持 20px 间距，确保阅读舒适。</span></p>
```

### 8. 关键词下划线

```html
<span leaf="" style="border-bottom:2px solid {palette['underline']};">关键词</span>
```

### 9. 加粗标记

```html
<span leaf="" style="color:{palette['primary']};font-weight:bold;">加粗文字</span>
```

### 10. 高亮标记

```html
<span leaf="" style="background:linear-gradient(to top,{palette['highlight']} 0%,#fde68a 100%);padding:2px 4px;border-radius:3px;">高亮文字</span>
```

### 11. 引用块

```html
<section style="margin:24px 0;padding:16px 20px;background:{palette['bg_light']};border-left:3px solid {palette['primary']};border-radius:0 6px 6px 0;">
<p style="margin:0;line-height:1.8;font-size:15px;color:{palette['body']};"><span leaf="">引用块内容，用于强调重要观点或补充说明。</span></p>
</section>
```

### 12. 数据卡

```html
<section style="margin:24px 0;padding:24px;background:{palette['bg_light']};border-radius:8px;text-align:center;">
<p style="margin:0 0 6px;line-height:1;font-size:36px;font-weight:bold;color:{palette['primary']};"><span leaf="">98%</span></p>
<p style="margin:0;line-height:1.6;font-size:14px;color:{palette['aux']};"><span leaf="">数据说明文字</span></p>
</section>
```

### 13. 表格

```html
<section style="margin:24px 0;border:1px solid {palette['border_light']};border-radius:8px;overflow:hidden;">
<section style="display:flex;background:{palette['dark_bg']};">
<section style="flex:1;padding:12px 16px;"><p style="margin:0;line-height:1.5;font-size:14px;font-weight:bold;color:#ffffff;"><span leaf="">列标题A</span></p></section>
<section style="flex:1;padding:12px 16px;"><p style="margin:0;line-height:1.5;font-size:14px;font-weight:bold;color:#ffffff;"><span leaf="">列标题B</span></p></section>
</section>
<section style="display:flex;border-top:1px solid {palette['border_light']};">
<section style="flex:1;padding:12px 16px;"><p style="margin:0;line-height:1.5;font-size:14px;color:{palette['body']};"><span leaf="">数据A1</span></p></section>
<section style="flex:1;padding:12px 16px;"><p style="margin:0;line-height:1.5;font-size:14px;color:{palette['body']};"><span leaf="">数据B1</span></p></section>
</section>
<section style="display:flex;border-top:1px solid {palette['border_light']};">
<section style="flex:1;padding:12px 16px;"><p style="margin:0;line-height:1.5;font-size:14px;color:{palette['body']};"><span leaf="">数据A2</span></p></section>
<section style="flex:1;padding:12px 16px;"><p style="margin:0;line-height:1.5;font-size:14px;color:{palette['body']};"><span leaf="">数据B2</span></p></section>
</section>
</section>
```

### 14. 分割线

```html
<section style="margin:32px 0;display:flex;align-items:center;justify-content:center;">
<section style="width:6px;height:6px;background:{palette['primary_light']};border-radius:50%;margin:0 5px;"></section>
<section style="width:36px;height:2px;background:{palette['primary_light']};border-radius:1px;"></section>
<section style="width:6px;height:6px;background:{palette['primary_light']};border-radius:50%;margin:0 5px;"></section>
</section>
```

### 15. 作者签名区／CTA

```html
<section style="margin:40px 0 0;padding:28px 24px;background:{palette['dark_bg']};border-radius:8px;text-align:center;">
<p style="margin:0 0 8px;line-height:1.6;font-size:15px;color:#ffffff;"><span leaf="">如果这篇文章对你有帮助</span></p>
<p style="margin:0 0 16px;line-height:1.6;font-size:15px;color:#ffffff;"><span leaf="">欢迎点赞、在看、转发分享</span></p>
<section style="display:inline-block;padding:6px 20px;background:#ffffff;border-radius:20px;">
<p style="margin:0;line-height:1.5;font-size:14px;font-weight:bold;color:{palette['primary']};"><span leaf="">{{作者名}}</span></p>
</section>
</section>
```

### 16. 产品徽章

```html
<section style="display:inline-block;padding:3px 10px;background:{palette['bg_light']};border:1px solid {palette['border_light']};border-radius:4px;">
<p style="margin:0;line-height:1.5;font-size:13px;color:{palette['primary']};font-weight:bold;"><span leaf="">产品名</span></p>
</section>
```

---

## 三、完整文章模板骨架

```
全局容器
 ├─ 封面／标题区
 ├─ 引言卡
 ├─ 目录导读
 ├─ 〔 章节标题            ← 循环 N 次
 │    ├─ 子标题（按需）
 │    ├─ 正文段落（含关键词下划线／加粗／高亮／荧光笔）
 │    ├─ 引用块（按需）
 │    ├─ 数据卡（按需）
 │    ├─ 表格（按需）
 │    ├─ 产品徽章（按需）
 │    └─ 通用库组件：代码块／图片（按需）〕
 ├─ 分割线
 └─ 作者签名区／CTA
```

---

## 四、文章类型 → 组件组合配方表

| 文章类型 | 核心组件组合 |
|---------|------------|
| 教程／操作指南 | 封面＋引言＋目录＋章节标题＋正文＋引用块＋代码块（通用库）＋签名 |
| 盘点／工具清单 | 封面＋引言＋目录＋章节标题＋产品徽章＋数据卡＋正文＋表格＋签名 |
| 观点／深度分析 | 封面＋引言＋章节标题＋正文＋引用块＋荧光笔＋分割线＋签名 |
| 数据复盘／报告 | 封面＋引言＋目录＋数据卡＋表格＋正文＋签名 |

---

## 五、Markdown → 组件映射规则表

| Markdown 元素 | 映射组件 |
|--------------|---------|
| `# 标题` | 封面／标题区 |
| `> 引言（开头）` | 引言卡 |
| `## 标题` | 章节标题（自动编号 01／02／03＋英文标签） |
| `### 标题` | 子标题 |
| 正文段落 | 正文段落（每段主动加 1-3 个关键词下划线） |
| `**文字**` | 加粗标记（锚点层，全文 ≤5 处） |
| `==文字==` | 高亮标记 |
| `<u>文字</u>` | 关键词下划线 |
| `> 引用（非开头）` | 引用块 |
| `---` | 分割线 |
| `` \\| 表格 \\| `` | 表格 |
| `- 项` / `1. 项` | 转为带缩进的正文段落（无序列表前缀「·」） |
| `` `code` `` | 通用库行内代码 |
| ` ``` 围栏 ``` ` | 通用库代码块 |
| `![说明](url)` | 通用库图片组件（有说明文字才加说明） |
"""
    return theme


def main():
    ap = argparse.ArgumentParser(description="微信公众号风格 / 品牌元素提取器")
    ap.add_argument("url", nargs="?", help="公众号文章 URL")
    ap.add_argument("--html", help="本地 HTML 文件路径")
    ap.add_argument("--image", help="品牌图/参考图路径（png/jpg）")
    ap.add_argument("--pdf", help="品牌手册 PDF 路径")
    ap.add_argument("--doc", help="品牌文档路径（md/txt/docx）")
    ap.add_argument("--output", help="输出主题名称（品牌模板名）")
    args = ap.parse_args()

    # 兜底默认排版（图片/PDF/文档输入无排版规则时使用，与 theme-generator 标准值一致）
    default_typography = {
        "font": "PingFang SC, Microsoft YaHei, sans-serif",
        "font_sizes": ["16", "15", "14"],
        "line_heights": ["1.9"],
        "font_weights": ["400"],
    }
    source_label = ""
    spacing = {"margins": [], "paddings": []}

    if args.html:
        with open(args.html, encoding="utf-8") as f:
            html = f.read()
        soup = parse_html(html)
        print("🔍 正在提取颜色调色板...")
        colors = extract_colors(soup)
        print("🔍 正在提取排版规则...")
        typography = extract_typography(soup)
        print("🔍 正在提取间距规则...")
        spacing = extract_spacing(soup)
        source_label = "HTML"
    elif args.url:
        if not WECHAT_URL_PATTERN.match(args.url):
            print("❌ 错误：URL 必须是 mp.weixin.qq.com 公众号文章链接（白名单限制）")
            sys.exit(1)
        html = fetch_wechat_html(args.url)
        soup = parse_html(html)
        print("🔍 正在提取颜色调色板...")
        colors = extract_colors(soup)
        print("🔍 正在提取排版规则...")
        typography = extract_typography(soup)
        print("🔍 正在提取间距规则...")
        spacing = extract_spacing(soup)
        source_label = "公众号文章"
    elif args.image:
        print("🔍 正在从品牌图提取主色板...")
        colors = extract_image_colors(args.image)
        typography = default_typography
        source_label = f"品牌图 {Path(args.image).name}"
    elif args.pdf:
        print("🔍 正在从品牌手册 PDF 提取文本与首页配色...")
        colors, _text = extract_pdf(args.pdf)
        typography = default_typography
        source_label = f"品牌手册 {Path(args.pdf).name}"
    elif args.doc:
        print("🔍 正在从品牌文档提取色值...")
        colors, _text = extract_doc_text(args.doc)
        typography = default_typography
        source_label = f"品牌文档 {Path(args.doc).name}"
    else:
        print("用法: style_extractor.py <url> 或 --html/--image/--pdf/--doc <file>")
        sys.exit(1)

    palette = analyze_color_palette(colors)
    theme_name = args.output or "extracted"
    theme_content = generate_theme(theme_name, palette, typography, spacing)

    skill_root = Path(__file__).resolve().parent.parent
    output_dir = skill_root / "references"
    output_path = output_dir / f"theme-{theme_name.lower()}.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(theme_content)

    print(f"\n✅ 主题组件库已生成: {output_path}")
    print(f"\n提取摘要（来源: {source_label}）:")
    print(f"  主色: {palette['primary']}")
    print(f"  背景色: {palette['bg_light']}")
    print(f"  标题色: {palette['title']}")
    print(f"  正文色: {palette['body']}")
    print(f"  字体: {typography['font']}")
    if source_label in ("公众号文章", "HTML"):
        print(f"  字号: {', '.join(typography['font_sizes'])}px")
        print(f"  行高: {', '.join(typography['line_heights'])}")
    print("\n💡 提示: 品牌气质（圆角/字体/版式）需人工或 AI 看图补充描述，"
          "见 references/mode-c-brand.md Step 2。")


if __name__ == "__main__":
    main()
