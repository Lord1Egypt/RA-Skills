"""在不改写作文照片内容的前提下，为已确认坐标绘制批注。"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps, UnidentifiedImageError


MIN_CONFIDENCE = 0.80
ALLOWED_KINDS = {"correction", "suggestion"}
MARK_COLORS = {"correction": (220, 38, 38), "suggestion": (37, 99, 235)}
SUPPORTED_SOURCE_IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg"}
OUTPUT_IMAGE_SUFFIX = ".png"


def validate_request(payload: dict, image_size: tuple[int, int]) -> list[dict]:
    """校验已确认的批注坐标，并返回原顺序的项目列表。

    此函数刻意不执行 OCR 或坐标推断：调用方必须先提供可信的原图坐标。
    """
    if not isinstance(payload, dict):
        raise ValueError("批注请求必须是对象。")

    width, height = image_size
    if not isinstance(width, int) or not isinstance(height, int) or width <= 0 or height <= 0:
        raise ValueError("图片尺寸必须是正整数。")

    items = payload.get("items")
    if not isinstance(items, list):
        raise ValueError("items 必须是批注项目列表。")

    ids: list[int] = []
    suggestion_count = 0
    for position, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"第 {position} 项批注必须是对象。")

        item_id = item.get("id")
        # bool 是 int 的子类，必须排除，避免 true 被误作为编号 1。
        if isinstance(item_id, bool) or not isinstance(item_id, int) or item_id <= 0:
            raise ValueError(f"第 {position} 项编号必须是从 1 开始的正整数。")
        ids.append(item_id)

        kind = item.get("kind")
        if kind not in ALLOWED_KINDS:
            raise ValueError(f"第 {position} 项类别只能是 correction 或 suggestion。")
        if kind == "suggestion":
            suggestion_count += 1

        message = item.get("message")
        if not isinstance(message, str) or not message.strip():
            raise ValueError(f"第 {position} 项说明不能为空。")

        confidence = item.get("confidence")
        if isinstance(confidence, bool) or not isinstance(confidence, (int, float)):
            raise ValueError(f"第 {position} 项置信度必须是数字。")
        if not MIN_CONFIDENCE <= confidence <= 1:
            raise ValueError(f"第 {position} 项置信度必须在 {MIN_CONFIDENCE:.2f} 到 1 之间。")

        bbox = item.get("bbox")
        if not isinstance(bbox, list) or len(bbox) != 4:
            raise ValueError(f"第 {position} 项坐标必须是四个整数。")
        if any(isinstance(value, bool) or not isinstance(value, int) for value in bbox):
            raise ValueError(f"第 {position} 项坐标必须是四个整数。")
        x1, y1, x2, y2 = bbox
        if not (0 <= x1 < x2 <= width and 0 <= y1 < y2 <= height):
            raise ValueError(f"第 {position} 项坐标越界或顺序无效。")

    # 单页项目可能沿用跨页连续编号，因此只拒绝会造成图例歧义的重复编号。
    if len(ids) != len(set(ids)):
        raise ValueError("批注编号必须是唯一的正整数。")
    if suggestion_count > 5:
        raise ValueError("提升建议数量不能超过 5 条。")

    return items


def _can_render_chinese(font: ImageFont.ImageFont) -> bool:
    """保守地检查字体是否把“中”替换为缺字方框。"""
    try:
        # 对不包含该字符的字体，Pillow 通常会使用与替换字符相同的缺字字形。
        return bytes(font.getmask("中")) != bytes(font.getmask("\ufffd"))
    except (OSError, UnicodeError):
        return False


def _load_chinese_font(payload: dict, size: int) -> ImageFont.ImageFont:
    """校验显式字体，或在未指定时选择常见系统中文字体。"""
    requested_font = payload.get("font_path")
    if "font_path" in payload:
        if not isinstance(requested_font, str) or not requested_font:
            raise ValueError("font_path 必须是非空绝对路径。")
        requested_path = Path(requested_font)
        if not requested_path.is_absolute():
            raise ValueError("font_path 必须是绝对路径。")
        if not requested_path.is_file():
            raise ValueError("font_path 指向的字体文件不存在或不是文件。")
        # 显式 font_path 表示调用方选定了具体字体：文件存在仅是第一道门槛，
        # Pillow 无法解析或字体缺少中文字形都必须立即拒绝，不得悄然换用系统字体。
        try:
            explicit_font = ImageFont.truetype(str(requested_path), size=size)
        except OSError as error:
            raise ValueError("font_path 指向的文件不是可加载的有效字体，未生成批注图片。") from error
        if not _can_render_chinese(explicit_font):
            raise ValueError("font_path 指向的字体不支持中文字形，未生成批注图片。")
        return explicit_font

    # 只有请求没有提供 font_path 时，才能搜索常见系统字体。
    candidates: list[Path] = []
    # Windows 的系统目录可能不在 C 盘；优先使用系统提供的绝对路径，
    # 仅在环境变量为绝对路径时组装 Fonts 子目录，避免受当前工作目录影响。
    windows_font_roots: list[Path] = []
    for environment_name in ("WINDIR", "SystemRoot"):
        environment_value = os.environ.get(environment_name)
        if environment_value:
            environment_path = Path(environment_value)
            if environment_path.is_absolute():
                font_root = environment_path / "Fonts"
                if font_root not in windows_font_roots:
                    windows_font_roots.append(font_root)
    default_windows_font_root = Path("C:/Windows/Fonts")
    if default_windows_font_root not in windows_font_roots:
        windows_font_roots.append(default_windows_font_root)

    candidates.extend(
        [
            Path("/System/Library/Fonts/PingFang.ttc"),
            Path("/System/Library/Fonts/STHeiti Light.ttc"),
            Path("/System/Library/Fonts/STHeiti Medium.ttc"),
            Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
            Path("/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc"),
            Path("/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"),
        ]
    )
    for font_root in windows_font_roots:
        candidates.extend(
            [
                font_root / "msyh.ttc",
                font_root / "msyhbd.ttc",
                font_root / "simsun.ttc",
            ]
        )
    for path in candidates:
        if not path.is_file():
            continue
        try:
            font = ImageFont.truetype(str(path), size=size)
        except OSError:
            continue
        if _can_render_chinese(font):
            return font

    # 默认字体只能作为最后一次尝试；它不能显示中文时绝不能静默生成乱码图。
    default_font = ImageFont.load_default(size=size)
    if _can_render_chinese(default_font):
        return default_font
    raise ValueError("找不到可显示中文的字体，未生成批注图片。")


def _wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, max_width: int) -> list[str]:
    """按实际像素宽度逐字换行，兼容没有空格分隔的中文说明。"""
    lines: list[str] = []
    current = ""
    for character in text:
        trial = current + character
        if current and draw.textlength(trial, font=font) > max_width:
            lines.append(current)
            current = character
        else:
            current = trial
    if current:
        lines.append(current)
    return lines or [""]


def render_annotations(payload: dict) -> Path:
    """将已校验坐标渲染在原图上方，并在图片底部新增编号说明区。"""
    if not isinstance(payload, dict):
        raise ValueError("批注请求必须是对象。")
    source_value = payload.get("source_image")
    output_value = payload.get("output_image")
    if not isinstance(source_value, str) or not source_value:
        raise ValueError("必须提供原图路径。")
    if not isinstance(output_value, str) or not output_value:
        raise ValueError("必须提供输出图片路径。")

    source_path = Path(source_value)
    output_path = Path(output_value)
    if not source_path.is_absolute() or not output_path.is_absolute():
        raise ValueError("source_image 与 output_image 必须都是绝对路径。")
    # resolve 可同时识别文字路径别名和符号链接；在读取图像前就拒绝同源，
    # 确保后续任何校验或渲染失败都不会把输出写回原图。
    resolved_source = source_path.resolve()
    resolved_output = output_path.resolve()
    if resolved_source == resolved_output:
        raise ValueError("原图与输出图片不能指向同一文件。")
    if source_path.exists() and output_path.exists():
        try:
            if source_path.samefile(output_path):
                raise ValueError("原图与输出图片不能指向同一文件。")
        except OSError as error:
            raise ValueError("无法安全比较原图与输出图片，未生成批注图片。") from error
    if source_path.suffix.lower() not in SUPPORTED_SOURCE_IMAGE_SUFFIXES:
        raise ValueError("不支持的原图格式；仅支持 PNG、JPG 和 JPEG。")
    # 原图区域要求像素保真，不能把完整画布重新编码为有损 JPEG。
    if output_path.suffix.lower() != OUTPUT_IMAGE_SUFFIX:
        raise ValueError("输出图片必须为无损 PNG 格式，以保持原图像素不变。")
    if not source_path.is_file():
        raise ValueError("原图不存在或不是文件。")
    try:
        # formats 参数同时限制真实图片编码，不能仅凭被伪装的扩展名绕过格式白名单。
        with Image.open(source_path, formats=["PNG", "JPEG"]) as opened_image:
            # OCR 和 bbox 统一使用 EXIF 归一化后的视觉方向，因此必须先转置再取尺寸。
            visual_image = ImageOps.exif_transpose(opened_image)
            # 含 alpha 的 PNG 保留 RGBA 通道；普通照片则保持 RGB，便于稳定绘制红蓝批注。
            has_alpha = "A" in visual_image.getbands() or "transparency" in visual_image.info
            source_image = visual_image.convert("RGBA" if has_alpha else "RGB")
    except (OSError, UnidentifiedImageError) as error:
        raise ValueError("无法读取原图；请确认图片是有效的 PNG、JPG 或 JPEG 文件。") from error

    # 绘制必须保留请求数组顺序，才能让重叠标记按调用方指定的层级覆盖。
    draw_items = validate_request(payload, source_image.size)
    # 图例独立按全篇编号升序展示，输入数组顺序不影响教师查找编号。
    legend_items = sorted(draw_items, key=lambda item: item["id"])
    font_size = max(16, min(28, source_image.width // 25))
    font = _load_chinese_font(payload, font_size)
    padding = max(12, font_size // 2)
    line_spacing = font_size + max(5, font_size // 3)

    # 先在临时画布计算每条说明占用的行数，再一次性分配底部区域高度。
    measure_image = Image.new("RGB", (source_image.width, 1), "white")
    measure_draw = ImageDraw.Draw(measure_image)
    legend_lines: list[tuple[dict, list[str]]] = []
    for item in legend_items:
        category = "纠错" if item["kind"] == "correction" else "建议"
        text = f"{item['id']}. [{category}] {item['message']}"
        lines = _wrap_text(measure_draw, text, font, source_image.width - padding * 2)
        legend_lines.append((item, lines))
    legend_height = padding * 2 + line_spacing * sum(len(lines) for _, lines in legend_lines)

    canvas_mode = source_image.mode
    white = (255, 255, 255, 255) if canvas_mode == "RGBA" else "white"
    canvas = Image.new(canvas_mode, (source_image.width, source_image.height + legend_height), white)
    canvas.paste(source_image, (0, 0))
    draw = ImageDraw.Draw(canvas)
    for item in draw_items:
        x1, y1, x2, y2 = item["bbox"]
        base_color = MARK_COLORS[item["kind"]]
        color = (*base_color, 255) if canvas_mode == "RGBA" else base_color
        # bbox 的右、下边界是排他的；使用最后有效像素并固定单像素线宽，避免写入说明区。
        draw.line((x1, y2 - 1, x2 - 1, y2 - 1), fill=color, width=1)
        radius = max(10, font_size // 2)
        center_x = min(source_image.width - radius, x2 - 1 + radius)
        center_y = max(radius, y1 - radius)
        draw.ellipse(
            (center_x - radius, center_y - radius, center_x + radius, center_y + radius),
            fill=color,
        )
        draw.text((center_x, center_y), str(item["id"]), font=font, fill="white", anchor="mm")

    current_y = source_image.height + padding
    for item, lines in legend_lines:
        base_color = MARK_COLORS[item["kind"]]
        color = (*base_color, 255) if canvas_mode == "RGBA" else base_color
        for line in lines:
            draw.text((padding, current_y), line, font=font, fill=color)
            current_y += line_spacing

    output_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output_path)
    return output_path


def main() -> None:
    """读取 JSON 请求并将实际输出路径作为一行 JSON 回执写到标准输出。"""
    parser = argparse.ArgumentParser(description="在原照片上绘制已确认坐标的作文批注")
    parser.add_argument("--request", required=True, help="AnnotationRequest JSON 文件路径")
    arguments = parser.parse_args()
    request_path = Path(arguments.request)
    try:
        payload = json.loads(request_path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        parser.error(f"请求文件不存在：{request_path}")
        raise AssertionError("argparse.error 会终止程序") from error
    except json.JSONDecodeError as error:
        parser.error(f"请求文件不是有效 JSON：{error.msg}")
        raise AssertionError("argparse.error 会终止程序") from error

    output_path = render_annotations(payload)
    # ensure_ascii=False 使调用方可直接阅读中文路径，同时 JSON 仍可被程序可靠解析。
    print(json.dumps({"output_image": str(output_path)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
