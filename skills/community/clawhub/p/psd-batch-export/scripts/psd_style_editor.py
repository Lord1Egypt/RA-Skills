"""
PSD 样式编辑器 v1.0 — 修改 PSD 图层的渲染样式
===============================================

在渲染阶段（非 PSD 二进制）修改图层的字体、颜色、字号、对齐方式。
支持单图层编辑和批量操作。

用法:
  # 查看图层样式
  python psd_style_editor.py 模板.psd --inspect

  # 渲染单个 PSD 并修改样式
  python psd_style_editor.py 模板.psd --layer "名字" --font simhei.ttf --color 255 0 0 --size 64 --output out.png

  # 批量修改样式（从 JSON 配置文件）
  python psd_style_editor.py 模板.psd --config styles.json --output-dir output/
"""

import argparse
import json
from pathlib import Path
from PIL import Image
from psd_tools import PSDImage
import sys

# 添加同目录脚本路径
sys.path.insert(0, str(Path(__file__).parent))
from console_utils import configure_stdio
from render_psd_batch import (
    prerender_background, render_with_background,
    get_text_style, match_psd_font, find_fonts
)

configure_stdio()


def inspect_psd(psd_path: Path):
    """查看 PSD 所有文字图层的样式信息"""
    psd = PSDImage.open(str(psd_path))
    print(f"\n📋 PSD 样式分析: {psd_path.name}")
    print(f"   尺寸: {psd.width}×{psd.height} px")
    print(f"   {'─'*65}")
    print(f"   {'图层':<16} {'文本':<20} {'字体':<20} {'字号':>5} {'颜色':>16} {'bbox'}")
    print(f"   {'─'*65}")

    layers_info = []
    for layer in psd.descendants():
        if layer.kind != "type":
            continue
        text = layer.text.strip("\x00").strip()
        if not text:
            continue
        style = get_text_style(layer)
        font_family = (style.get("font_family") or "?")[:20]
        font_size = style.get("font_size") or "?"
        fill = style.get("fill_color")
        color_str = f"#{fill[0]:02X}{fill[1]:02X}{fill[2]:02X}" if fill else "auto"
        bbox = f"({layer.bbox[0]},{layer.bbox[1]},{layer.bbox[2]},{layer.bbox[3]})"

        print(f"   {layer.name:<16} {text[:20]:<20} {font_family:<20} {str(font_size):>5} {color_str:>16} {bbox}")

        layers_info.append({
            "name": layer.name,
            "text": text,
            "font_family": font_family,
            "font_size": font_size,
            "fill_color": list(fill) if fill else None,
            "bbox": list(layer.bbox),
        })

    print(f"   {'─'*65}")
    return layers_info


def edit_layer_style(psd_path: Path, output_path: Path,
                     layer_name: str = None,
                     text: str = None,
                     font_path: str = None,
                     color: tuple = None,
                     font_size: int = None,
                     align: str = "center",
                     dpi: int = 300):
    """
    修改指定图层的渲染样式并输出 PNG。
    注意：此操作在渲染阶段修改样式，不改变源 PSD 文件。
    """
    bg_cache = prerender_background(psd_path)
    psd = PSDImage.open(str(psd_path))

    styles = []
    for layer in psd.descendants():
        if layer.kind != "type":
            continue
        s = get_text_style(layer)
        if not s:
            continue
        s["layer_name"] = layer.name

        # 匹配指定图层
        if layer_name and layer.name == layer_name:
            if text is not None:
                s["text"] = text
            if font_path:
                s["font_family"] = font_path
            if color:
                s["fill_color"] = color
            if font_size:
                s["font_size"] = font_size

        styles.append(s)

    if not styles:
        print("❌ 未找到可编辑的文本图层")
        return None

    fonts = [font_path] if font_path else find_fonts()[:5]
    img = render_with_background(bg_cache, styles, fonts, color, font_size, align)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(output_path), "PNG", dpi=(dpi, dpi))
    print(f"✅ 样式编辑完成 → {output_path}")
    return img


def batch_edit_styles(psd_path: Path, config_path: Path, output_dir: Path, dpi: int = 300):
    """
    从 JSON 配置文件批量编辑样式。

    配置文件格式:
    {
        "variants": [
            {
                "name": "variant_1",
                "layers": {
                    "名字": {"text": "张三", "font": "simhei.ttf", "color": [255, 0, 0], "size": 64},
                    "学校": {"text": "清华大学"}
                }
            }
        ]
    }
    """
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    variants = config.get("variants", [])
    if not variants:
        print("❌ 配置文件中没有 variants")
        return

    bg_cache = prerender_background(psd_path)
    psd = PSDImage.open(str(psd_path))
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for vi, variant in enumerate(variants):
        name = variant.get("name", f"variant_{vi:03d}")
        layer_overrides = variant.get("layers", {})

        styles = []
        for layer in psd.descendants():
            if layer.kind != "type":
                continue
            s = get_text_style(layer)
            if not s:
                continue
            s["layer_name"] = layer.name

            # 应用覆盖
            if layer.name in layer_overrides:
                override = layer_overrides[layer.name]
                if "text" in override:
                    s["text"] = override["text"]
                if "color" in override:
                    s["fill_color"] = tuple(override["color"])
                if "size" in override:
                    s["font_size"] = override["size"]

            styles.append(s)

        fonts = find_fonts()[:5]
        img = render_with_background(bg_cache, styles, fonts, None, None, "center")
        out_path = output_dir / f"{name}.png"
        img.save(str(out_path), "PNG", dpi=(dpi, dpi))
        print(f"  [{vi+1}/{len(variants)}] {name}.png")

    print(f"✅ 批量编辑完成 → {output_dir}")


# ═══════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════

def main():
    p = argparse.ArgumentParser(description="PSD 样式编辑器 — 修改图层渲染样式")
    p.add_argument("psd", help="PSD 文件路径")
    p.add_argument("--inspect", action="store_true", help="查看图层样式信息")
    p.add_argument("--layer", help="目标图层名")
    p.add_argument("--text", help="新文本内容")
    p.add_argument("--font", help="字体文件路径")
    p.add_argument("--color", nargs=3, type=int, metavar=("R", "G", "B"), help="文字颜色 RGB")
    p.add_argument("--size", type=int, help="字号")
    p.add_argument("--align", choices=["left", "center", "right"], default="center")
    p.add_argument("--dpi", type=int, default=300)
    p.add_argument("--output", default="output/styled.png", help="输出路径")
    p.add_argument("--config", help="JSON 样式配置文件路径")
    p.add_argument("--output-dir", default="output/styled_batch", help="批量输出目录")

    args = p.parse_args()
    psd_path = Path(args.psd)

    if args.inspect:
        inspect_psd(psd_path)

    elif args.config:
        batch_edit_styles(psd_path, Path(args.config), Path(args.output_dir), args.dpi)

    elif args.layer:
        color = tuple(args.color) if args.color else None
        edit_layer_style(psd_path, Path(args.output),
                         layer_name=args.layer,
                         text=args.text,
                         font_path=args.font,
                         color=color,
                         font_size=args.size,
                         align=args.align,
                         dpi=args.dpi)

    else:
        p.print_help()


if __name__ == "__main__":
    main()
