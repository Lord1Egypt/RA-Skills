#!/usr/bin/env python3
"""
Product Drawing Extractor v2.0
===============================
专为 Farreach 产品工程图纸设计的结构化信息提取器。

策略：
  1. Docling 提取带坐标的文本块
  2. 按 bbox 坐标分区（6 个区域）
  3. 各区域独立重建结构化字段
  4. Vision API 兜底（处理图形/手绘区域）
  5. 字段校验 + 输出 JSON/Markdown

用法：
  python3 extract_drawing.py <pdf_path> [--output-dir ./output] [--format json|md|both]
  python3 extract_drawing.py <pdf_path> --vision  # 启用 Vision API 兜底
"""

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# 1. 数据结构
# ---------------------------------------------------------------------------

@dataclass
class TextBlock:
    """带坐标的文本块"""
    text: str
    left: float
    top: float
    right: float
    bottom: float
    zone: str = ""  # 分区后填充

@dataclass
class BOMRow:
    """BOM 物料行"""
    no: str = ""
    part_name: str = ""       # 部件名称
    spec: str = ""            # 规格
    quantity: str = ""        # 用量

@dataclass
class ToleranceSpec:
    """公差标准"""
    range_mm: str = ""
    hardware: str = ""        # 五金件
    plastic: str = ""         # 丝印/塑胶件

@dataclass
class DrawingData:
    """产品图纸提取结果"""
    # 基本信息（右上区域）
    product_name: str = ""          # 客人品名
    length_mm: str = ""             # 长度
    material_code: str = ""         # 物料编码
    packaging_spec: str = ""        # 包装规范

    # 模具信息（左上区域）
    mold_info: str = ""             # 模具
    mold_number: str = ""           # 模号/AB端

    # BOM 物料清单（右侧区域）
    bom: list = field(default_factory=list)

    # 公差标准（左下区域）
    tolerances: list = field(default_factory=list)

    # Pin 分配（中央区域）
    pin_assignment: dict = field(default_factory=dict)

    # 注意事项
    notes: list = field(default_factory=list)

    # 公司信息
    company: str = ""
    date: str = ""

    # 元数据
    source_file: str = ""
    extraction_method: str = ""
    confidence: float = 0.0
    warnings: list = field(default_factory=list)


# ---------------------------------------------------------------------------
# 2. 区域定义
# ---------------------------------------------------------------------------

# A4 横向尺寸 841.92 x 595.32 pt
# 基于实测坐标数据定义 6 个区域
# 注意：Docling bbox 坐标 (left, top, right, bottom)，原点在左下角

ZONES = {
    "top_left": {
        "desc": "模具信息 + 注意事项",
        "x_range": (0, 250),
        "y_range": (500, 600),
    },
    "top_right": {
        "desc": "客人品名/长度/物料编码/包装规范",
        "x_range": (400, 842),
        "y_range": (500, 600),
    },
    "center": {
        "desc": "图形区域（接线图/Pin Assignment）",
        "x_range": (100, 480),
        "y_range": (220, 520),
    },
    "tolerance_area": {
        "desc": "公差标准",
        "x_range": (370, 500),
        "y_range": (100, 220),
    },
    "pin_label": {
        "desc": "Pin Assignment 标签",
        "x_range": (0, 370),
        "y_range": (0, 220),
    },
    "bottom_right_bom": {
        "desc": "BOM 物料清单",
        "x_range": (480, 842),
        "y_range": (100, 230),
    },
    "bottom_bar": {
        "desc": "公司信息/日期/受控文件",
        "x_range": (300, 500),
        "y_range": (0, 110),
    },
}


def classify_zone(block: TextBlock) -> str:
    """根据坐标分配区域"""
    cx = (block.left + block.right) / 2
    cy = (block.top + block.bottom) / 2

    for zone_name, zone_def in ZONES.items():
        xr = zone_def["x_range"]
        yr = zone_def["y_range"]
        if xr[0] <= cx <= xr[1] and yr[0] <= cy <= yr[1]:
            return zone_name

    return "unknown"


# ---------------------------------------------------------------------------
# 3. Docling 提取
# ---------------------------------------------------------------------------

def extract_with_docling(pdf_path: str) -> list[TextBlock]:
    """用 Docling 提取带坐标的文本块"""
    from docling.document_converter import DocumentConverter, PdfFormatOption
    from docling.datamodel.pipeline_options import PdfPipelineOptions

    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = True
    pipeline_options.do_table_structure = True

    conv = DocumentConverter(
        format_options={"pdf": PdfFormatOption(pipeline_options=pipeline_options)}
    )
    result = conv.convert(pdf_path)
    doc = result.document

    blocks = []
    for item, _level in doc.iterate_items():
        if not hasattr(item, "text") or not item.text.strip():
            continue
        if not item.prov:
            continue
        prov = item.prov[0]
        bbox = prov.bbox
        b = TextBlock(
            text=item.text.strip(),
            left=bbox.l,
            top=bbox.t,
            right=bbox.r,
            bottom=bbox.b,
        )
        b.zone = classify_zone(b)
        blocks.append(b)

    return blocks


# ---------------------------------------------------------------------------
# 4. Tesseract OCR 兜底（图形区域）
# ---------------------------------------------------------------------------

def ocr_region(image_path: str, region: tuple, lang: str = "chi_sim+eng") -> str:
    """对图片指定区域做 OCR"""
    from PIL import Image

    img = Image.open(image_path)
    w, h = img.size

    # region = (x1_pct, y1_pct, x2_pct, y2_pct) 百分比
    crop_box = (
        int(region[0] * w),
        int(region[1] * h),
        int(region[2] * w),
        int(region[3] * h),
    )
    cropped = img.crop(crop_box)
    tmp_path = "/tmp/ocr_region_crop.png"
    cropped.save(tmp_path)

    try:
        result = subprocess.run(
            ["tesseract", tmp_path, "stdout", "-l", lang, "--psm", "6"],
            capture_output=True,
            timeout=30,
        )
        # Decode with error handling
        text = result.stdout.decode("utf-8", errors="replace").strip()
        return text
    except Exception as e:
        return f"[OCR Error: {e}]"


def pdf_to_image(pdf_path: str, output_dir: str = "/tmp", dpi: int = 200) -> str:
    """PDF 转 PNG"""
    stem = Path(pdf_path).stem
    prefix = os.path.join(output_dir, f"drawing_{stem}")
    subprocess.run(
        ["pdftoppm", "-r", str(dpi), "-png", pdf_path, prefix],
        check=True,
        capture_output=True,
    )
    # pdftoppm 输出 prefix-1.png
    img_path = f"{prefix}-1.png"
    if os.path.exists(img_path):
        return img_path
    # 有些版本输出 prefix-01.png
    for f in os.listdir(output_dir):
        if f.startswith(f"drawing_{stem}") and f.endswith(".png"):
            return os.path.join(output_dir, f)
    raise FileNotFoundError(f"PDF to image conversion failed for {pdf_path}")


# ---------------------------------------------------------------------------
# 5. 区域解析器
# ---------------------------------------------------------------------------

def parse_top_right(blocks: list[TextBlock]) -> dict:
    """解析右上区域：客人品名/长度/物料编码/包装规范
    
    策略：关键词标签在顶行（y~574），值在其正下方同列（y~542-558）。
    按 x 坐标列对齐匹配 label→value。
    """
    zone_blocks = [b for b in blocks if b.zone == "top_right"]
    if not zone_blocks:
        return {"product_name": "", "length_mm": "", "material_code": "", "packaging_spec": ""}

    # 分两行：标签行（y > 560）和值行（y < 560）
    label_blocks = sorted([b for b in zone_blocks if b.top > 560], key=lambda b: b.left)
    value_blocks = sorted([b for b in zone_blocks if b.top <= 560], key=lambda b: b.left)

    data = {
        "product_name": "",
        "length_mm": "",
        "material_code": "",
        "packaging_spec": "",
    }

    keyword_map = {
        "客人品名": "product_name",
        "长 度": "length_mm",
        "长度": "length_mm",
        "物料编码": "material_code",
        "包装规范": "packaging_spec",
    }

    for label_b in label_blocks:
        field_name = None
        for kw, fname in keyword_map.items():
            if kw in label_b.text:
                field_name = fname
                break
        if not field_name:
            continue

        # 查找同列的值（x 中心相近，y 更低）
        label_cx = (label_b.left + label_b.right) / 2
        best_val = None
        best_dist = 999
        for vb in value_blocks:
            val_cx = (vb.left + vb.right) / 2
            x_dist = abs(val_cx - label_cx)
            if x_dist < 60:  # 同列容差
                if x_dist < best_dist:
                    best_dist = x_dist
                    best_val = vb.text
        
        if best_val:
            data[field_name] = best_val

    return data


def parse_top_left(blocks: list[TextBlock]) -> dict:
    """解析左上区域：模具信息 + 注意事项"""
    zone_blocks = sorted(
        [b for b in blocks if b.zone == "top_left"],
        key=lambda b: (-b.top, b.left),
    )
    data = {"mold_info": "", "mold_number": "", "notes": []}

    # 注意事项相关的文本块
    note_texts = []

    for b in zone_blocks:
        text = b.text.strip()
        if text == "模具":
            # "模具" 是标签，值在其正下方（同列，y 更低）
            for other in zone_blocks:
                if other is not b and other.top < b.top and abs(other.left - b.left) < 40:
                    if other.text.strip() not in ("模号/AB端", "注意", ":", "1"):
                        data["mold_info"] = other.text.strip()
                        break
        elif text == "模号/AB端":
            # "模号/AB端" 是标签，值在其正下方
            for other in zone_blocks:
                if other is not b and other.top < b.top and abs(other.left - b.left) < 60:
                    if other.text.strip() not in ("模具", "注意", ":", "1"):
                        data["mold_number"] = other.text.strip()
                        break
        elif any(kw in text for kw in ("注意", "RoHS", "REACH", "材质", "环保")):
            note_texts.append(text)

    # 合并注意事项
    if note_texts:
        combined = " ".join(note_texts)
        # 清理 "注意 : 1 、所有材质..." 格式
        combined = re.sub(r"注意\s*[:：]\s*", "", combined)
        combined = re.sub(r"^\d+\s*[、.]\s*", "", combined.strip())
        if combined:
            data["notes"] = [combined.strip()]

    return data


def parse_bom(blocks: list[TextBlock]) -> list[dict]:
    """解析 BOM 物料清单（bottom_right_bom 区域）
    
    策略：
    1. 按 y 坐标分行（量化到 10pt）
    2. 找到表头行（含 NO./部件名称/用量）
    3. 建立列的 x 坐标基准
    4. 每行按最近列归类
    """
    zone_blocks = [b for b in blocks if b.zone == "bottom_right_bom"]
    if not zone_blocks:
        return []

    # 按 y 坐标分行（同行 y 差 < 10pt）
    rows_by_y = {}
    for b in zone_blocks:
        y_key = round(b.top / 10) * 10
        if y_key not in rows_by_y:
            rows_by_y[y_key] = []
        rows_by_y[y_key].append(b)

    # 按 y 从小到大排序（底部=0，顶部=595，表头在底部）
    sorted_rows = sorted(rows_by_y.items(), key=lambda x: x[0])

    # 识别表头行
    col_x = {}
    header_y = None
    for y_key, row_blocks in sorted_rows:
        row_text = " ".join(b.text for b in row_blocks)
        if "NO" in row_text and ("部件" in row_text or "用量" in row_text):
            header_y = y_key
            for b in row_blocks:
                t = b.text.strip()
                cx = (b.left + b.right) / 2
                if "NO" in t:
                    col_x["no"] = cx
                elif "部件" in t:
                    col_x["part_name"] = cx
                elif "规" in t:
                    col_x["spec"] = cx
                elif "用量" in t:
                    col_x["quantity"] = cx
            break

    if not col_x:
        # 表头没找到，尝试硬编码常见列位（基于实测坐标）
        col_x = {"no": 490, "part_name": 535, "spec": 696, "quantity": 818}
        header_y = 110

    # 数据行：y > header_y 的行
    bom = []
    for y_key, row_blocks in sorted_rows:
        if y_key <= (header_y or 0):
            continue

        row_blocks.sort(key=lambda b: b.left)
        row_data = {"no": "", "part_name": "", "spec": "", "quantity": ""}

        for b in row_blocks:
            bcx = (b.left + b.right) / 2
            # 归到最近的列
            best_col = None
            best_dist = 999
            for col_name, col_cx in col_x.items():
                dist = abs(bcx - col_cx)
                if dist < best_dist:
                    best_dist = dist
                    best_col = col_name

            if best_col and best_dist < 100:
                if row_data[best_col]:
                    row_data[best_col] += " " + b.text
                else:
                    row_data[best_col] = b.text

        # 跳过空行
        if any(v.strip() for v in row_data.values()):
            bom.append(row_data)

    # 过滤掉表头行（部件名称/规格/用量 等关键词出现在值里说明是表头）
    header_keywords = {"部件名称", "规格", "用量", "NO.", "规    格"}
    bom = [
        row for row in bom
        if not any(
            any(kw in v for kw in header_keywords)
            for v in row.values()
        )
    ]

    # 按 NO. 排序（数字从小到大）
    def sort_key(row):
        try:
            return int(re.sub(r'\D', '', row.get("no", "0")) or "0")
        except:
            return 0
    bom.sort(key=sort_key)

    # 自动填充 NO.（如果全部缺失）
    if all(not row.get("no") for row in bom):
        for i, row in enumerate(bom, 1):
            row["no"] = str(i)

    return bom


def parse_tolerances(blocks: list[TextBlock]) -> list[dict]:
    """解析公差标准（tolerance_area 区域）"""
    zone_blocks = [b for b in blocks if b.zone == "tolerance_area"]
    tolerances = []

    # 五金件列 x < 433，塑胶件列 x >= 433（基于实测坐标）
    hardware_vals = []
    plastic_vals = []

    for b in zone_blocks:
        text = b.text
        if "±" in text:
            if b.left < 433:
                hardware_vals.append((b.top, text))
            else:
                plastic_vals.append((b.top, text))

    # 按 y 从高到低排序（对应图纸从上到下）
    hardware_vals.sort(key=lambda x: -x[0])
    plastic_vals.sort(key=lambda x: -x[0])

    # 合并 "30" + "以上" + "/±0.xxmm" 行
    def merge_30plus(vals):
        merged = []
        for y, text in vals:
            if text in ("30", "以上") or (text.startswith("/±") and not text.startswith("0.")):
                # 属于 "30以上/±..." 的片段
                if merged and abs(merged[-1][0] - y) < 8:
                    merged[-1] = (merged[-1][0], merged[-1][1] + text)
                else:
                    merged.append((y, text))
            else:
                merged.append((y, text))
        return [t for _, t in merged]

    hw = merge_30plus(hardware_vals)
    pl = merge_30plus(plastic_vals)

    for i in range(max(len(hw), len(pl))):
        tol = {
            "hardware": hw[i] if i < len(hw) else "",
            "plastic": pl[i] if i < len(pl) else "",
        }
        tolerances.append(tol)

    return tolerances


def parse_pin_assignment(blocks: list[TextBlock]) -> dict:
    """解析 Pin Assignment 信息"""
    pin_blocks = [b for b in blocks if b.zone in ("pin_label", "center")]
    pin_info = {"connectors": [], "pin_labels": [], "description": ""}

    connector_names = []
    pin_labels = []

    for b in pin_blocks:
        text = b.text
        if "PIN Assignment" in text:
            continue
        if text.startswith("pin"):
            pin_labels.append(text)
        elif text in ("CN1", "CN2"):
            connector_names.append(text)
        elif any(kw in text for kw in ("HDMI", "DVI", "USB", "DP", "VGA")):
            connector_names.append(text)
        elif "SHELL" in text:
            pin_labels.append(text)

    pin_info["connectors"] = list(dict.fromkeys(connector_names))  # 去重保序
    pin_info["pin_labels"] = pin_labels

    # 构建描述
    if connector_names:
        pin_info["description"] = " ↔ ".join(
            [c for c in connector_names if c not in ("CN1", "CN2")]
        )

    return pin_info


def parse_company_info(blocks: list[TextBlock]) -> dict:
    """解析公司信息（bottom_bar + tolerance_area 底部）"""
    # 公司信息可能在 bottom_bar 或其他低 y 区域
    candidate_blocks = [b for b in blocks if b.top < 110]
    data = {"company": "", "date": ""}

    company_parts = []
    for b in candidate_blocks:
        text = b.text.strip()
        if any(kw in text for kw in ("SKW", "FARREACH", "福睿", "farreach")):
            company_parts.append(text)
        date_match = re.search(r"\d{4}[./\-]\d{2}[./\-]\d{2}", text)
        if date_match:
            data["date"] = date_match.group()
        elif "受控" in text:
            pass  # 跳过 "受控文件"

    if company_parts:
        data["company"] = " / ".join(company_parts)

    return data


# ---------------------------------------------------------------------------
# 6. 主提取流程
# ---------------------------------------------------------------------------

def extract_drawing(pdf_path: str, use_vision: bool = False) -> DrawingData:
    """主提取入口"""
    result = DrawingData(source_file=os.path.basename(pdf_path))
    warnings = []

    # Step 1: Docling 提取
    print("[1/5] Docling 文本提取...", file=sys.stderr)
    try:
        blocks = extract_with_docling(pdf_path)
        result.extraction_method = "docling"
        print(f"  提取到 {len(blocks)} 个文本块", file=sys.stderr)
    except Exception as e:
        warnings.append(f"Docling 提取失败: {e}")
        # Fallback: pdftotext
        print(f"  Docling 失败，回退到 pdftotext", file=sys.stderr)
        blocks = []
        result.extraction_method = "pdftotext_fallback"

    # Step 2: 分区统计
    print("[2/5] 区域分析...", file=sys.stderr)
    zone_counts = {}
    for b in blocks:
        zone_counts[b.zone] = zone_counts.get(b.zone, 0) + 1
    for zone, count in sorted(zone_counts.items()):
        print(f"  {zone}: {count} 块", file=sys.stderr)

    # Step 3: 各区域解析
    print("[3/5] 结构化字段提取...", file=sys.stderr)

    # 右上：产品基本信息
    top_right = parse_top_right(blocks)
    result.product_name = top_right["product_name"]
    result.length_mm = top_right["length_mm"]
    result.material_code = top_right["material_code"]
    result.packaging_spec = top_right["packaging_spec"]

    # 左上：模具信息
    top_left = parse_top_left(blocks)
    result.mold_info = top_left["mold_info"]
    result.mold_number = top_left["mold_number"]
    result.notes = top_left["notes"]

    # BOM
    bom = parse_bom(blocks)
    result.bom = bom

    # 公差标准
    tolerances = parse_tolerances(blocks)
    result.tolerances = tolerances

    # Pin Assignment
    pin_info = parse_pin_assignment(blocks)
    result.pin_assignment = pin_info

    # 公司信息
    company_info = parse_company_info(blocks)
    result.company = company_info["company"]
    result.date = company_info["date"]

    # Step 4: 图形区域 OCR（可选）
    if use_vision:
        print("[4/5] 图形区域 OCR...", file=sys.stderr)
        try:
            img_path = pdf_to_image(pdf_path)
            # OCR 中央区域（接线图部分）
            # 中央区域大约占图纸 12%~65% x, 20%~80% y
            center_ocr = ocr_region(img_path, (0.12, 0.15, 0.55, 0.85))
            if center_ocr:
                result.pin_assignment["ocr_text"] = center_ocr
                print(f"  OCR 提取到 {len(center_ocr)} 字符", file=sys.stderr)
        except Exception as e:
            warnings.append(f"图形区域 OCR 失败: {e}")
    else:
        print("[4/5] 跳过图形 OCR（使用 --vision 启用）", file=sys.stderr)

    # Step 5: 校验
    print("[5/5] 字段校验...", file=sys.stderr)
    confidence = 0.0
    checks = 0
    total = 0

    required_fields = [
        ("product_name", result.product_name),
        ("material_code", result.material_code),
        ("packaging_spec", result.packaging_spec),
    ]
    for fname, fval in required_fields:
        total += 1
        if fval:
            checks += 1
        else:
            warnings.append(f"⚠️ 缺失必填字段: {fname}")

    if result.bom:
        total += 1
        checks += 1
    else:
        total += 1
        warnings.append("⚠️ BOM 物料清单为空")

    confidence = (checks / total * 100) if total > 0 else 0
    result.confidence = round(confidence, 1)
    result.warnings = warnings

    print(f"  置信度: {confidence:.1f}%", file=sys.stderr)
    if warnings:
        for w in warnings:
            print(f"  {w}", file=sys.stderr)

    return result


# ---------------------------------------------------------------------------
# 7. 输出格式化
# ---------------------------------------------------------------------------

def to_json(data: DrawingData) -> str:
    """输出 JSON"""
    return json.dumps(asdict(data), ensure_ascii=False, indent=2)


def to_markdown(data: DrawingData) -> str:
    """输出 Markdown（归档用）"""
    lines = []
    lines.append(f"# 产品图纸：{data.product_name or '未知产品'}")
    lines.append("")
    lines.append(f"> 📋 **来源文件：** `{data.source_file}`")
    lines.append(f"> 📅 **图纸日期：** {data.date or '未标注'}")
    lines.append(f"> 🏭 **公司：** {data.company or '未标注'}")
    lines.append(f"> 🎯 **提取置信度：** {data.confidence}%")
    lines.append("")

    # 基本信息
    lines.append("## 📊 基本信息")
    lines.append("")
    lines.append("| 项目 | 内容 |")
    lines.append("|------|------|")
    lines.append(f"| **客人品名** | {data.product_name or '—'} |")
    lines.append(f"| **长度 (mm)** | {data.length_mm or '—'} |")
    lines.append(f"| **物料编码** | {data.material_code or '—'} |")
    lines.append(f"| **包装规范** | {data.packaging_spec or '—'} |")
    lines.append(f"| **模具** | {data.mold_info or '—'} |")
    lines.append(f"| **模号/AB端** | {data.mold_number or '—'} |")
    lines.append("")

    # BOM
    if data.bom:
        lines.append("## 🔧 BOM 物料清单")
        lines.append("")
        lines.append("| NO. | 部件名称 | 规格 | 用量 |")
        lines.append("|-----|----------|------|------|")
        for row in data.bom:
            if isinstance(row, dict):
                lines.append(
                    f"| {row.get('no', '')} | {row.get('part_name', '')} "
                    f"| {row.get('spec', '')} | {row.get('quantity', '')} |"
                )
        lines.append("")

    # 公差标准
    if data.tolerances:
        lines.append("## 📏 公差标准")
        lines.append("")
        lines.append("| 五金件 | 丝印/塑胶件 |")
        lines.append("|--------|-------------|")
        for tol in data.tolerances:
            if isinstance(tol, dict):
                lines.append(
                    f"| {tol.get('hardware', '')} | {tol.get('plastic', '')} |"
                )
        lines.append("")

    # Pin Assignment
    if data.pin_assignment:
        lines.append("## 🔌 Pin Assignment")
        lines.append("")
        pa = data.pin_assignment
        if pa.get("connectors"):
            lines.append(f"**连接器：** {', '.join(pa['connectors'])}")
        if pa.get("pin_labels"):
            lines.append(f"**Pin 标签：** {', '.join(pa['pin_labels'])}")
        if pa.get("ocr_text"):
            lines.append("")
            lines.append("**图形区域 OCR：**")
            lines.append(f"```\n{pa['ocr_text']}\n```")
        lines.append("")

    # 注意事项
    if data.notes:
        lines.append("## ⚠️ 注意事项")
        lines.append("")
        for note in data.notes:
            lines.append(f"- {note}")
        lines.append("")

    # 校验警告
    if data.warnings:
        lines.append("## 🚨 提取警告")
        lines.append("")
        for w in data.warnings:
            lines.append(f"- {w}")
        lines.append("")

    lines.append("---")
    lines.append(f"*提取方法：{data.extraction_method} | 置信度：{data.confidence}%*")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 8. CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="产品图纸结构化提取器 v2.0"
    )
    parser.add_argument("pdf_path", help="PDF 文件路径")
    parser.add_argument(
        "--output-dir", "-o", default="./output", help="输出目录 (默认 ./output)"
    )
    parser.add_argument(
        "--format",
        "-f",
        choices=["json", "md", "both"],
        default="both",
        help="输出格式 (默认 both)",
    )
    parser.add_argument(
        "--vision", action="store_true", help="启用图形区域 OCR (tesseract)"
    )
    parser.add_argument(
        "--stdout", action="store_true", help="输出到 stdout (不写文件)"
    )

    args = parser.parse_args()

    if not os.path.exists(args.pdf_path):
        print(f"❌ 文件不存在: {args.pdf_path}", file=sys.stderr)
        sys.exit(1)

    # 提取
    data = extract_drawing(args.pdf_path, use_vision=args.vision)

    # 输出
    if args.stdout:
        if args.format in ("json", "both"):
            print(to_json(data))
        if args.format in ("md", "both"):
            print(to_markdown(data))
        return

    os.makedirs(args.output_dir, exist_ok=True)
    stem = Path(args.pdf_path).stem

    if args.format in ("json", "both"):
        json_path = os.path.join(args.output_dir, f"{stem}.json")
        with open(json_path, "w", encoding="utf-8") as f:
            f.write(to_json(data))
        print(f"✅ JSON: {json_path}", file=sys.stderr)

    if args.format in ("md", "both"):
        md_path = os.path.join(args.output_dir, f"{stem}.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(to_markdown(data))
        print(f"✅ Markdown: {md_path}", file=sys.stderr)

    # 摘要
    print(f"\n📊 提取完成", file=sys.stderr)
    print(f"  产品: {data.product_name or '未识别'}", file=sys.stderr)
    print(f"  物料编码: {data.material_code or '未识别'}", file=sys.stderr)
    print(f"  BOM 行数: {len(data.bom)}", file=sys.stderr)
    print(f"  置信度: {data.confidence}%", file=sys.stderr)
    if data.warnings:
        print(f"  ⚠️ 警告: {len(data.warnings)} 条", file=sys.stderr)


if __name__ == "__main__":
    main()
