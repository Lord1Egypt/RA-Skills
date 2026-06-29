#!/usr/bin/env python3
"""
标准证件照生成工具 — 基于 rembg 去背景 + Pillow 裁剪排版
支持一寸/二寸/小一寸/大一寸/小二寸等规格，红/白/蓝三种底色。
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter


# 标准证件照规格 (宽度, 高度) 单位像素 @300DPI
ID_PHOTO_SPECS = {
    "一寸": (295, 413),
    "小一寸": (260, 378),
    "大一寸": (390, 567),
    "二寸": (413, 579),
    "小二寸": (413, 531),
    "三寸": (649, 991),
    "美国签证": (600, 600),
    "日本签证": (472, 472),
    "护照": (390, 567),
    # 别名
    "1寸": (295, 413),
    "2寸": (413, 579),
    "一寸照": (295, 413),
    "二寸照": (413, 579),
}

# 底色 RGB 值
BACKGROUND_COLORS = {
    "red": (255, 0, 0),       # 红色
    "blue": (67, 142, 219),    # 蓝色 (常用证件照蓝)
    "white": (255, 255, 255),  # 白色
    "红底": (255, 0, 0),
    "蓝底": (67, 142, 219),
    "白底": (255, 255, 255),
    "红色": (255, 0, 0),
    "蓝色": (67, 142, 219),
    "白色": (255, 255, 255),
}


def remove_background(image: Image.Image) -> Image.Image:
    """
    使用 rembg 移除背景，返回 RGBA 图片。
    """
    try:
        from rembg import remove
    except ImportError:
        raise ImportError("需要安装 rembg: pip install rembg onnxruntime")

    result = remove(image)
    return result


def replace_background(
    image: Image.Image, bg_color: tuple, feather_radius: int = 2
) -> Image.Image:
    """
    替换背景色，边缘羽化处理。
    """
    if image.mode != "RGBA":
        image = image.convert("RGBA")

    # 创建背景
    bg = Image.new("RGBA", image.size, bg_color + (255,))

    # 合成
    result = Image.alpha_composite(bg, image).convert("RGB")

    return result


def crop_to_ratio(
    image: Image.Image, target_w: int, target_h: int
) -> Image.Image:
    """
    按目标比例居中裁剪，保持人物在画面中央。
    """
    target_ratio = target_w / target_h
    img_w, img_h = image.size
    img_ratio = img_w / img_h

    if img_ratio > target_ratio:
        # 图片更宽，裁左右
        new_w = int(img_h * target_ratio)
        left = (img_w - new_w) // 2
        image = image.crop((left, 0, left + new_w, img_h))
    elif img_ratio < target_ratio:
        # 图片更高，裁上下（保留上半部分更多，因为头部在上）
        new_h = int(img_w / target_ratio)
        top = (img_h - new_h) // 3  # 偏上裁剪，留更多头部空间
        top = max(0, top)
        image = image.crop((0, top, img_w, top + new_h))

    return image


def auto_detect_face_center(image: Image.Image) -> tuple:
    """
    自动检测人脸中心位置（简易版，基于肤色检测）。
    返回 (cx, cy) 或 (w/2, h*0.4)。
    """
    try:
        import cv2

        img_cv = cv2.cvtColor(np.array(image.convert("RGB")), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

        # 使用 Haar Cascade 检测人脸
        cascade_paths = [
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml",
            cv2.data.haarcascades + "haarcascade_frontalface_alt.xml",
        ]

        for cascade_path in cascade_paths:
            face_cascade = cv2.CascadeClassifier(cascade_path)
            if face_cascade.empty():
                continue

            faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(60, 60))
            if len(faces) > 0:
                # 取最大人脸
                x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
                return (x + w // 2, y + h // 2)

    except Exception:
        pass

    # 默认：偏上中心
    return (image.width // 2, int(image.height * 0.4))


def make_id_photo(
    input_path: str,
    output_path: str,
    spec: str = "一寸",
    bg_color: str = "blue",
    quality: int = 95,
    no_remove_bg: bool = False,
    layout: str = None,
) -> dict:
    """
    生成证件照。
    """
    input_file = Path(input_path)
    if not input_file.exists():
        return {"success": False, "error": f"文件不存在: {input_path}"}

    spec_name = spec
    if spec not in ID_PHOTO_SPECS:
        # 模糊匹配
        matched = None
        for key in ID_PHOTO_SPECS:
            if spec in key or key in spec:
                matched = key
                break
        if matched:
            spec_name = matched
        else:
            return {
                "success": False,
                "error": f"不支持的证件照规格: {spec}。支持: {', '.join(ID_PHOTO_SPECS.keys())}",
            }

    target_w, target_h = ID_PHOTO_SPECS[spec_name]

    if bg_color not in BACKGROUND_COLORS:
        bg_rgb = BACKGROUND_COLORS.get("blue")
    else:
        bg_rgb = BACKGROUND_COLORS[bg_color]

    bg_name = bg_color

    try:
        # 1. 打开原图
        img = Image.open(input_path).convert("RGB")

        # 2. 去背景
        if not no_remove_bg:
            try:
                img_rgba = remove_background(img)
            except ImportError as e:
                return {"success": False, "error": str(e)}
        else:
            img_rgba = img.convert("RGBA")

        # 3. 按比例裁剪
        img_rgba = crop_to_ratio(img_rgba, target_w, target_h)

        # 4. 替换背景色
        img_final = replace_background(img_rgba, bg_rgb)

        # 5. 缩放到目标尺寸
        img_final = img_final.resize((target_w, target_h), Image.LANCZOS)

        # 6. 排版（多张照片拼在一张相纸上）
        if layout:
            layout_configs = {
                "5寸": (89, 127),
                "6寸": (102, 152),
                "4R": (102, 152),
                "A4": (210, 297),
            }

            if layout in layout_configs:
                paper_w_mm, paper_h_mm = layout_configs[layout]
                # 300 DPI: 1mm ≈ 11.81px
                paper_w_px = int(paper_w_mm * 11.81)
                paper_h_px = int(paper_h_mm * 11.81)

                # 计算能排多少张
                margin = 10  # px margin
                cols = (paper_w_px - margin) // (target_w + margin)
                rows = (paper_h_px - margin) // (target_h + margin)
                cols = max(1, cols)
                rows = max(1, rows)

                # 创建相纸
                paper = Image.new(
                    "RGB", (paper_w_px, paper_h_px), (255, 255, 255)
                )

                for row in range(rows):
                    for col in range(cols):
                        x = margin + col * (target_w + margin)
                        y = margin + row * (target_h + margin)
                        paper.paste(img_final, (x, y))

                img_final = paper
                layout_info = {
                    "paper": layout,
                    "cols": cols,
                    "rows": rows,
                    "total": cols * rows,
                }
            else:
                return {
                    "success": False,
                    "error": f"不支持的排版尺寸: {layout}。支持: 5寸, 6寸, 4R, A4",
                }
        else:
            layout_info = None

        # 7. 保存
        output_file = Path(output_path) if output_path else input_file.parent / f"id_photo_{spec_name}_{bg_name}.jpg"
        output_file.parent.mkdir(parents=True, exist_ok=True)

        img_final.save(str(output_file), "JPEG", quality=quality)

        input_size = input_file.stat().st_size
        output_size = output_file.stat().st_size

        return {
            "success": True,
            "output": str(output_file),
            "spec": spec_name,
            "dimensions": {"width": target_w, "height": target_h},
            "dpi": "300",
            "background": bg_name,
            "bg_rgb": list(bg_rgb),
            "layout": layout_info,
            "input_size": input_size,
            "output_size": output_size,
            "output_size_kb": round(output_size / 1024, 2),
            "print_size_mm": {
                "width": round(target_w / 300 * 25.4, 1),
                "height": round(target_h / 300 * 25.4, 1),
            },
        }

    except Exception as e:
        return {"success": False, "error": f"证件照生成失败: {str(e)}"}


def main():
    parser = argparse.ArgumentParser(description="标准证件照生成工具")
    parser.add_argument("input", help="输入人像图片路径")
    parser.add_argument("-o", "--output", help="输出图片路径")
    parser.add_argument(
        "--spec",
        default="一寸",
        help="证件照规格 (默认: 一寸). 可选: 一寸, 小一寸, 大一寸, 二寸, 小二寸, 三寸, 护照, 美国签证, 日本签证",
    )
    parser.add_argument(
        "--bg",
        default="blue",
        help="底色 (默认: blue). 可选: red/红底, blue/蓝底, white/白底",
    )
    parser.add_argument(
        "-q", "--quality", type=int, default=95, help="输出质量 (1-100, 默认95)"
    )
    parser.add_argument(
        "--no-remove-bg",
        action="store_true",
        help="不去背景（如果已经是纯色背景的照片）",
    )
    parser.add_argument(
        "--layout",
        help="排版到相纸上 (可选: 5寸, 6寸, 4R, A4)",
    )

    args = parser.parse_args()

    result = make_id_photo(
        input_path=args.input,
        output_path=args.output,
        spec=args.spec,
        bg_color=args.bg,
        quality=args.quality,
        no_remove_bg=args.no_remove_bg,
        layout=args.layout,
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result.get("success") else 1)


if __name__ == "__main__":
    main()
