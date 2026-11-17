"""
Generate certificate image from order detail JSON.
Usage: python generate_cert.py <order_detail.json>
Output: Desktop/{title}_证书.png
"""

import json
import os
import shutil
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

from common import BASE_DIR, load_json

# ============ Path config ============
TEMPLATE_PATH = os.path.join(BASE_DIR, "template", "模板.png")
CASE_PATH = os.path.join(BASE_DIR, "template", "案例.png")
DESKTOP_DIR = os.path.join(str(Path.home() / "Desktop"), "certificate")
OUTPUT_PATH = os.path.join(DESKTOP_DIR, "{title}_证书.png")

# ============ 字体配置 ============
FONT_DIR = r"C:\Windows\Fonts"
FONT_TITLE = os.path.join(FONT_DIR, "simhei.ttf")       # 黑体 - 标题
FONT_LABEL = os.path.join(FONT_DIR, "simsun.ttc")        # 宋体 - 标签
FONT_VALUE = os.path.join(FONT_DIR, "simsun.ttc")        # 宋体 - 值
FONT_CASE_NO = os.path.join(FONT_DIR, "simhei.ttf")      # 黑体 - 备案号

# ============ 颜色配置 ============
COLOR_TITLE = (0, 0, 0)          # 黑色 - 标题
COLOR_LABEL = (0, 0, 0)          # 黑色 - 标签（与值一致）
COLOR_VALUE = (0, 0, 0)          # 黑色 - 值
COLOR_CASE_NO = (200, 0, 0)      # 红色 - 备案号

# ============ 布局配置（基于模板 1380x1952）=============
# 从案例图片(1021x1444)坐标按缩放比1.3516换算
TITLE_FONT_SIZE = 62
LABEL_FONT_SIZE = 32
VALUE_FONT_SIZE = 32
HASH_FONT_SIZE = 28
CASE_NO_FONT_SIZE = 36

TITLE_Y = 366           # 标题 y 坐标（居中）
TITLE_X_CENTER = 690    # 标题居中 x

LABEL_X = 190           # 标签起始 x
VALUE_X = 500           # 值起始 x
COLON_GAP = 10          # 冒号后间距

ROW_POSITIONS = {
    "作品名称":     553,
    "证书持有人":   669,
    "证件类型":     779,
    "证件号码":     895,
    "存证时间":    1005,
    "确权文件哈希": 1120,
}

HASH_LINE_HEIGHT = 46    # 哈希换行行高
HASH_CHARS_PER_LINE = 43 # 每行字符数（128位/3行≈43）

CASE_NO_Y = 1680         # 备案号 y 坐标
CASE_NO_X_CENTER = 690   # 备案号居中 x


def extract_app_data(app):
    """Extract certificate data from a single app entry"""
    opus = app.get("opus", {})
    ownership = opus.get("ownership", {})
    preservation = app.get("preservation", {})

    # Cert type mapping
    cert_type_map = {"IDENTITY_CARD": "身份证"}
    cert_type = cert_type_map.get(ownership.get("certType", ""), ownership.get("certType", ""))

    # Format preservation time: 2026-06-04 15:01:37 -> 2026年06月04日
    raw_time = app.get("preservationTime", "")
    formatted_time = ""
    if raw_time:
        try:
            from datetime import datetime
            dt = datetime.strptime(raw_time, "%Y-%m-%d %H:%M:%S")
            formatted_time = f"{dt.year}年{dt.month:02d}月{dt.day:02d}日"
        except Exception:
            formatted_time = raw_time

    # File hash: prefer sha512Hash, fallback to fileHash
    file_hash = preservation.get("sha512Hash") or opus.get("fileHash", "")

    # Preservation ID
    preservation_id = preservation.get("preservationId", "") or app.get("preservationId", "")

    return {
        "title": opus.get("title", ""),
        "realName": ownership.get("realName", ""),
        "certType": cert_type,
        "certNumber": ownership.get("certNumber", ""),
        "preservationTime": formatted_time,
        "fileHash": file_hash,
        "preservationId": str(preservation_id),
    }


def load_all_order_data(json_path):
    """Load all app entries from order detail JSON, return list of data dicts"""
    raw = load_json(json_path)

    if "data" in raw and isinstance(raw["data"], dict):
        data = raw["data"]
    else:
        data = raw

    apps = data.get("apps", [])
    if not apps:
        raise ValueError("No apps found in order data")

    return [extract_app_data(app) for app in apps]


def draw_centered_text(draw, text, y, font, fill):
    """绘制居中文本"""
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = TITLE_X_CENTER - tw // 2
    draw.text((x, y), text, font=font, fill=fill)


def draw_hash_text(draw, hash_str, start_y, font, fill, x):
    """绘制哈希值（自动换行）"""
    for i in range(0, len(hash_str), HASH_CHARS_PER_LINE):
        line = hash_str[i:i + HASH_CHARS_PER_LINE]
        draw.text((x, start_y), line, font=font, fill=fill)
        start_y += HASH_LINE_HEIGHT
    return start_y


def generate_single_cert(data):
    """Generate a single certificate image from data dict"""
    output_path = OUTPUT_PATH.format(title=data["title"])
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    shutil.copy2(TEMPLATE_PATH, output_path)

    img = Image.open(output_path)
    draw = ImageDraw.Draw(img)

    font_title = ImageFont.truetype(FONT_TITLE, TITLE_FONT_SIZE)
    font_label = ImageFont.truetype(FONT_LABEL, LABEL_FONT_SIZE)
    font_value = ImageFont.truetype(FONT_VALUE, VALUE_FONT_SIZE)
    font_hash = ImageFont.truetype(FONT_VALUE, HASH_FONT_SIZE)
    font_case_no = ImageFont.truetype(FONT_CASE_NO, CASE_NO_FONT_SIZE)

    # Title
    draw_centered_text(draw, "电子数据确权证书", TITLE_Y, font_title, COLOR_TITLE)

    # Label-value pairs
    label_value_map = [
        ("作品名称",     data["title"]),
        ("证书持有人",   data["realName"]),
        ("证件类型",     data["certType"]),
        ("证件号码",     data["certNumber"]),
        ("存证时间",     data["preservationTime"]),
    ]

    for label, value in label_value_map:
        y = ROW_POSITIONS[label]
        draw.text((LABEL_X, y), f"{label}：", font=font_label, fill=COLOR_LABEL)
        draw.text((VALUE_X, y), value, font=font_value, fill=COLOR_VALUE)

    # Hash (first line aligned with label)
    hash_y = ROW_POSITIONS["确权文件哈希"]
    draw.text((LABEL_X, hash_y), "确权文件哈希：", font=font_label, fill=COLOR_LABEL)
    draw_hash_text(draw, data["fileHash"], hash_y, font_hash, COLOR_VALUE, VALUE_X)

    # Case number
    label_part = "备案号："
    value_part = data["preservationId"]
    bbox_label = draw.textbbox((0, 0), label_part, font=font_case_no)
    label_w = bbox_label[2] - bbox_label[0]
    start_x = CASE_NO_X_CENTER - (label_w + len(value_part) * CASE_NO_FONT_SIZE // 2) // 2
    draw.text((start_x, CASE_NO_Y), label_part, font=font_case_no, fill=COLOR_VALUE)
    draw.text((start_x + label_w, CASE_NO_Y), value_part, font=font_case_no, fill=COLOR_CASE_NO)

    img.save(output_path, "PNG")
    return output_path


def generate_certificate(json_path):
    """Generate certificate images for all apps in order detail"""
    all_data = load_all_order_data(json_path)
    print(f"Found {len(all_data)} app(s) in order")

    output_paths = []
    for i, data in enumerate(all_data, 1):
        print(f"\n[{i}/{len(all_data)}] Generating: {data['title']}")
        print(f"Data: {json.dumps(data, ensure_ascii=False, indent=2)}")
        path = generate_single_cert(data)
        print(f"Certificate saved: {path}")
        output_paths.append(path)

    print(f"\nTotal {len(output_paths)} certificate(s) generated")
    return output_paths


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_cert.py <order_detail.json>")
        sys.exit(1)
    generate_certificate(sys.argv[1])
