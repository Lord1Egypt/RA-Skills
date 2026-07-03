#!/usr/bin/env python3
"""
图片元信息提取工具 — 供 SKILL.md 图片/流程图处理使用。
获取图片的基本信息（尺寸、模式、类型）并生成可读的描述。

不执行 OCR 或视觉识别 —— 只提取文件元信息供 AI 参考。

用法:
    python scripts/extract_images.py <path/to/image.png> [-o output.txt]
    python scripts/extract_images.py <path/to/image.png>  # 输出描述到 stdout
    python scripts/extract_images.py <dir/>                # 扫描整个目录

依赖: Pillow (PIL)
"""
import sys, os, argparse
from pathlib import Path
from datetime import datetime


def describe_image(path: str) -> dict:
    """提取图片元信息"""
    from PIL import Image

    img = Image.open(path)
    info = {
        "文件名": Path(path).name,
        "路径": str(Path(path).resolve()),
        "格式": img.format or "未知",
        "尺寸": f"{img.width} × {img.height} 像素",
        "宽": img.width,
        "高": img.height,
        "色彩模式": img.mode,
        "文件大小": f"{os.path.getsize(path):,} 字节",
        "文件大小_bytes": os.path.getsize(path),
        "修改时间": datetime.fromtimestamp(os.path.getmtime(path)).isoformat(),
    }

    # 检测可能的图表类型
    aspect = img.width / img.height if img.height > 0 else 0
    is_wide = aspect > 1.5
    is_tall = aspect < 0.67
    is_square = 0.67 <= aspect <= 1.5

    if is_wide and img.width > 500:
        info["推测图表类型"] = "流程图 / 状态图（宽幅横向布局）"
    elif is_tall and img.height > 500:
        info["推测图表类型"] = "序列图 / UI 原型（纵向布局）"
    elif is_square:
        info["推测图表类型"] = "UI 截图 / 原型图（接近方形）"
    else:
        info["推测图表类型"] = "普通图片"

    return info


def format_markdown(infos: list[dict]) -> str:
    """将图片信息格式化为 Markdown"""
    lines = [f"# 图片分析报告", f"# 图片数: {len(infos)}", ""]
    for info in infos:
        lines.append(f"## {info['文件名']}")
        lines.append(f"- **格式**: {info['格式']}")
        lines.append(f"- **尺寸**: {info['尺寸']}")
        lines.append(f"- **色彩模式**: {info['色彩模式']}")
        lines.append(f"- **文件大小**: {info['文件大小']}")
        lines.append(f"- **推测类型**: {info['推测图表类型']}")
        lines.append(f"- **修改时间**: {info['修改时间']}")
        lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="提取图片元信息")
    parser.add_argument("input", help="图片文件或目录路径")
    parser.add_argument("-o", "--output", help="输出文件路径（默认输出到 stdout）")
    parser.add_argument("-r", "--recursive", action="store_true", help="递归扫描目录")
    args = parser.parse_args()

    src = Path(args.input)
    if not src.exists():
        print(f"错误: 路径不存在 - {src}", file=sys.stderr)
        sys.exit(1)

    # 收集图片文件
    image_exts = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".tiff", ".svg"}
    files = []
    if src.is_file():
        files.append(src)
    elif src.is_dir():
        pattern = "**/*" if args.recursive else "*"
        for f in sorted(src.glob(pattern)):
            if f.suffix.lower() in image_exts and f.is_file():
                files.append(f)

    if not files:
        print(f"错误: 未找到支持的图片文件（支持: {', '.join(image_exts)}）", file=sys.stderr)
        sys.exit(1)

    try:
        infos = []
        for f in files:
            try:
                infos.append(describe_image(str(f)))
            except Exception as e:
                print(f"[警告] 无法处理 {f.name}: {e}", file=sys.stderr)

        text = format_markdown(infos)
        text += f"\n---\n# 处理时间: {datetime.now().isoformat()}\n"

        if args.output:
            dst = Path(args.output)
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text(text, encoding="utf-8")
            print(f"图片分析已保存到: {dst}", file=sys.stdout)
        else:
            sys.stdout.write(text)

    except ImportError:
        print("错误: 需要安装 Pillow (pip install Pillow)", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
