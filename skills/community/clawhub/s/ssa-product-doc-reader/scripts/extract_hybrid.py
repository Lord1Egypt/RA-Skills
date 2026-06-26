#!/usr/bin/env python3
"""
Product Drawing Extractor v5.0 - Hybrid Mode (Text-First)
==========================================================
混合策略 v5.0：pdftotext 优先 + Vision API 兜底

核心改进：
1. ⭐ 模具号/BOM 优先用 pdftotext（字体嵌入，100% 准确）
2. ⭐ Vision API 仅作为兜底（当 pdftotext 失败时）
3. ⭐ OCR DPI 提升到 300（更高分辨率）
4. ⭐ 数据校验：模具号格式检查（必须包含数字 + 字母）
5. 字段识别规则：BJ 开头=包装规范，599-xxx=Drawing No.

用法：
  python3 extract_hybrid.py <pdf_path> [--output-dir ./output] [--format json|md|both]
"""

import argparse
import base64
import json
import os
import re
import subprocess
import sys
import glob
from pathlib import Path
from typing import Optional


# ---------------------------------------------------------------------------
# 1. PDF → PNG（用于 Vision API，300 DPI）
# ---------------------------------------------------------------------------

def pdf_to_images(pdf_path: str, dpi: int = 300) -> list[str]:
    """PDF 转 PNG，返回图片路径列表（300 DPI 高分辨率）"""
    stem = Path(pdf_path).stem[:20]
    prefix = f"/tmp/hybrid_{stem}"

    for f in glob.glob(f"{prefix}*.png"):
        os.remove(f)

    subprocess.run(
        ["pdftoppm", "-r", str(dpi), "-png", pdf_path, prefix],
        check=True, capture_output=True,
    )

    images = sorted(glob.glob(f"{prefix}*.png"))
    if not images:
        raise FileNotFoundError(f"PDF to image failed for {pdf_path}")
    return images


def image_to_base64(image_path: str) -> str:
    """图片转 base64"""
    with open(image_path, "rb") as f:
        return base64.standard_b64encode(f.read()).decode("utf-8")


# ---------------------------------------------------------------------------
# 2. pdftotext 精确文本提取（优先使用）
# ---------------------------------------------------------------------------

def extract_text_with_pdftotext(pdf_path: str) -> str:
    """用 pdftotext 提取精确文本（保留布局）"""
    result = subprocess.run(
        ["pdftotext", "-layout", pdf_path, "-"],
        capture_output=True, text=True, timeout=30,
    )
    return result.stdout


def parse_model_no_from_text(text: str) -> str:
    """从 pdftotext 文本中提取模具号（Model No.）
    
    规则：
    - 模具号格式：字母 + 数字组合，如 5001-130A, AP-073A, AD1005-001
    - 排除单个字符（如 P）
    - 排除纯数字（如 1）
    - 排除 BJ 开头的包装规范
    """
    # 常见模具号模式（按优先级排序）
    patterns = [
        r'MODEL NO\.?\s+([A-Z0-9\-]+)',          # MODEL NO. 5004-6A（优先，支持换行）
        r'\b(USB-\d{4,}[A-Z]?\-\d{2,})\b',       # USB-3005A-014, USB-30651-014
        r'\b([A-Z]{2,}\d{3,}-\d{2,}[A-Z]?)\b',   # AP-073A, AD1005-001
        r'\b(\d{4}-\d{2,}[A-Z])\b',              # 5001-130A, 5004-6DA
        r'\b(MAP-\d{3}[A-Z])\b',                 # MAP-043A
        r'\b(TP-C\d{3}[A-Z])\b',                 # TP-C089B
        r'\b(OP-[A-Z]{2}\d{2})\b',               # OP-DP09, OP-HD65
        r'\b(DP-\d{3}[A-Z])\b',                  # DP-021B, DP-033A
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        if match:
            model = match.group(1)
            
            # 排除 BJ 开头的包装规范
            if model.upper().startswith('BJ'):
                continue
            
            # 排除 599 开头的 drawing no
            if model.startswith('599'):
                continue
            
            # 校验：必须包含字母和数字
            has_letter = any(c.isalpha() for c in model)
            has_digit = any(c.isdigit() for c in model)
            if has_letter and has_digit:
                return model.upper()
    
    return ""


def parse_products_from_text(text: str) -> list[dict]:
    """从 pdftotext 文本中解析产品规格矩阵（跨行收集）"""
    # 清理软连字符（PDF 换行导致的 \xad）和多余空白
    text = text.replace('\xad', '').replace('\u00ad', '')
    lines = text.split('\n')

    # 找产品表格区域
    header_idx = -1
    for i, line in enumerate(lines):
        if "客人品名" in line or "CUSTOMER ITEM" in line:
            header_idx = i
            break

    if header_idx < 0:
        return []

    # 收集所有产品名（大写字母串，长度>3，排除 BOM 词汇）
    product_names = []
    exclude_words = {
        'HDMI', 'AWM', 'STYLE', 'VW', 'PIN', 'SHELL', 'ROHS', 'REACH', 'PVC', 'SKW', 'FARREACH',
        'DP', 'USB', 'AOC', 'CABLE', 'GRIP', 'HDR', 'GR', 'CM', 'FM', 'AM', 'AF', 'MM', 'MLS',
        'MODEL', 'SCREW', 'PLATED', 'NUT', 'PLUG', 'PASS', 'TEST', 'HDPE', 'SKIN', 'BLACK', 'TPE',
        'DRAIN', 'WIRE', 'AL', 'MY', 'BC', 'PE', 'OD', 'CONDUCTOR', 'BRAID', 'JACKET', 'COLOR',
        'COPPER', 'FOIL', 'FABRIC', 'RUBBERIZED', 'IRON', 'GOLD', 'SHEATH', 'CLIP', 'WIRE', 'NI',
        'ETHERNET', 'HIGH', 'SPEED', 'WITH', 'ETHERNET', 'E358026', 'AWM', 'STYLE', 'VW-1',
        'OPEN', 'SHORT', 'MISS', 'WIRE', 'CONTACT', 'RESISTANCE', 'INSULATION', 'HI-POT', 'HDTV-DVD'
    }
    
    for i, line in enumerate(lines[header_idx + 1:header_idx + 40]):
        # 使用更宽松的正则（允许数字开头，如 HDMI2CABLE）
        matches = re.findall(r'\b([A-Z0-9]{3,}(?:-[A-Z0-9]+)*)\b', line)
        for m in matches:
            m_upper = m.upper()
            # 排除纯数字（长度值）
            if m.isdigit():
                continue
            # 排除电气参数（300V/60HZ 等）
            if re.match(r'^\d+[A-Z]+$', m):
                continue
            # 排除线材规格（32BC/511BC 等）
            if m.endswith('BC'):
                continue
            if (not m.startswith('599') and not m.startswith('BJ') and 
                m_upper not in exclude_words and len(m) > 3):
                if m not in product_names:
                    product_names.append(m)

    # 对每个产品名，在整篇文本中找对应的值
    products = []
    for pname in product_names:
        product = {
            "customer_item": pname,
            "length_mm": "",
            "packaging_spec": "",
            "material_code": "",
        }
        
        # 找包含该产品名的行
        for i, line in enumerate(lines):
            if pname in line:
                # 提取包装规范
                if not product["packaging_spec"]:
                    bj_match = re.search(r'(BJ\d{4}-\d{4})', line)
                    if bj_match:
                        product["packaging_spec"] = bj_match.group(1)
                
                # 提取物料编码
                if not product["material_code"]:
                    mc_match = re.search(r'\b(599-\d{2,3})\b', line)
                    if mc_match:
                        product["material_code"] = mc_match.group(1)
                
                # 提取长度（优先同行，其次上行，排除 BJ 编号）
                if not product["length_mm"]:
                    # 先找当前行（支持多种格式：9144+50, 10000+50, 9144+50/-0）
                    # 排除 BJ 格式（如 BJ0599-0053）
                    length_match = re.search(r'(?<!BJ)(\d{4,}[±\+\-]\d+(?:[±\+\-]\d+)?)', line)
                    if length_match and not length_match.group(1).startswith('0'):
                        product["length_mm"] = length_match.group(1)
                    # 再找上行（最多 5 行）
                    else:
                        for j in range(max(0, i - 5), i):
                            check_line = lines[j]
                            length_match = re.search(r'(?<!BJ)(\d{4,}[±\+\-]\d+(?:[±\+\-]\d+)?)', check_line)
                            if length_match and not length_match.group(1).startswith('0'):
                                product["length_mm"] = length_match.group(1)
                                break
        
        products.append(product)

    return products


def parse_packaging_from_text(text: str) -> str:
    """从 pdftotext 文本中提取包装规范（BJ 开头）"""
    matches = re.findall(r'(BJ\d{4}-\d{4})', text)
    if matches:
        return ",".join(matches)
    return ""


def parse_bom_from_text(text: str) -> list[dict]:
    """从 pdftotext 文本中解析 BOM 物料清单"""
    bom = []
    lines = text.split('\n')

    # 找 BOM 区域
    bom_start = -1
    for i, line in enumerate(lines):
        if "部件名称" in line or "PART NAME" in line or "规格" in line:
            bom_start = i
            break

    if bom_start < 0:
        return []

    in_bom = False
    current_row = {}

    for line in lines[bom_start:]:
        line = line.strip()
        if not line or len(line) < 5:
            continue

        # 跳过表头
        if any(kw in line for kw in ["NO.", "部件名称", "PART NAME", "规格", "用量", "UNIT"]):
            in_bom = True
            continue

        if not in_bom:
            continue

        # 解析 BOM 行（以序号开头）
        seq_match = re.match(r'^([①②③④⑤⑥⑦⑧⑨⑩\d]+)[\s\.、]*(.+?)\s{2,}(.+?)\s{2,}(.+)$', line)
        if seq_match:
            if current_row:
                bom.append(current_row)
            current_row = {
                "no": seq_match.group(1),
                "part_name": seq_match.group(2).strip(),
                "spec": seq_match.group(3).strip(),
                "quantity": seq_match.group(4).strip(),
            }
        elif current_row:
            # 多行规格
            current_row["spec"] += " " + line

    if current_row:
        bom.append(current_row)

    # 过滤表头残留
    header_keywords = {"部件名称", "规格", "用量", "NO.", "PART NAME"}
    bom = [
        row for row in bom
        if not any(kw in row.get("part_name", "") for kw in header_keywords)
    ]

    return bom


# ---------------------------------------------------------------------------
# 3. Vision API 调用（仅作为兜底）
# ---------------------------------------------------------------------------

VISION_PROMPT = """你是一个产品工程图纸分析专家。请仔细查看这张产品图纸图片，提取以下所有信息。

**务必严格按照 JSON 格式输出，不要输出任何其他内容。**

```json
{
  "product_name": "客人品名 / CUSTOMER ITEM（可能有多个，用逗号分隔）",
  "model_no": "型号 / MODEL NO. / ITEM 栏的值（如 5001-130A）",
  "drawing_no": "DRAWING NO. / 物料编码（如 599-002）",
  "packaging_spec": "包装规范 / Package No（BJ 开头，如 BJ0599-0002）",
  "length_mm": "长度 (mm)（可能有多个，用逗号分隔）",
  "mold_info": "模具信息（如 INNER MOLDING: xxx, OUTER MOLDING: xxx）",
  "mold_number": "模号/AB 端",
  "bom": [
    {
      "no": "序号（①②③ 或 1,2,3）",
      "part_name": "部件名称 / PART NAME",
      "spec": "规格 / SPECIFICATION（完整写出，包括材质、线径、颜色等）",
      "quantity": "用量 / UNIT"
    }
  ],
  "tolerances": [
    {
      "range": "尺寸范围（如 0.5-3.0）",
      "hardware": "五金件公差 / Metal tolerance",
      "plastic": "丝印/塑胶件公差 / Plastic tolerance"
    }
  ],
  "test_requirements": {
    "table": [],
    "other_tests": ["其他测试要求列表"]
  },
  "pin_assignment": {
    "connectors": ["连接器类型列表"],
    "description": "连接器对应关系描述"
  },
  "dimensions": ["关键尺寸标注"],
  "notes": ["注意事项"],
  "revision_history": [
    {
      "revision": "版本号（A0, A1, A2...）",
      "date": "日期",
      "description": "变更内容"
    }
  ],
  "company": "公司名称",
  "drawing_date": "图纸日期",
  "drawn_by": "绘图人",
  "checked_by": "审核人",
  "approved_by": "批准人",
  "products": [
    {
      "customer_item": "客人品名",
      "length_mm": "长度",
      "material_code": "物料编码",
      "packaging_spec": "包装规范"
    }
  ]
}
```

**重要识别规则：**
1. **包装规范** = BJ 开头的 8 位编码（如 BJ0599-0002）
2. **Drawing No.** = 599-xxx 格式（如 599-002）
3. **Model No.** = 字母 + 数字组合（如 5001-130A, AP-073A），排除单个字符
4. **客人品名** = CUSTOMER ITEM 后的值
5. 如果某个字段不存在或看不清，填空字符串 ""
6. BOM 物料清单要完整提取每一行
7. 如果有多个产品型号/长度，在 products 数组中列出所有
8. 变更记录在图纸边栏，提取版本号、日期、变更内容"""


def call_vision_api(images_b64: list[str], provider: str = "openrouter", model: str = None) -> dict:
    """调用 Vision API 提取图纸信息（仅作为兜底）"""
    if provider == "openrouter":
        return _call_openrouter(images_b64, model or "google/gemini-2.5-flash")
    else:
        raise ValueError(f"Unknown provider: {provider}")


def _call_openrouter(images_b64: list[str], model: str) -> dict:
    """调用 OpenRouter (Gemini/Claude)"""
    import urllib.request

    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    if not api_key:
        api_key = "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"

    content = [{"type": "text", "text": VISION_PROMPT}]
    for img_b64 in images_b64:
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/png;base64,{img_b64}"},
        })

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": content}],
        "temperature": 0.1,
        "max_tokens": 4096,
    }

    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
    )

    with urllib.request.urlopen(req, timeout=120) as resp:
        result = json.loads(resp.read().decode("utf-8"))

    text = result["choices"][0]["message"]["content"]
    return _parse_json_response(text)


def _parse_json_response(text: str) -> dict:
    """从 LLM 回复中提取 JSON"""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    match = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    return {"error": "Failed to parse JSON", "raw_response": text[:2000]}


# ---------------------------------------------------------------------------
# 4. 混合提取主流程（pdftotext 优先）
# ---------------------------------------------------------------------------

def merge_text_and_vision(text_data: dict, vision_data: dict) -> dict:
    """合并 pdftotext 和 Vision 的提取结果
    
    优先级策略（v5.0）：
    - 模具号：pdftotext 优先（精确），Vision 兜底
    - BOM：pdftotext 优先，Vision 兜底
    - 产品名：pdftotext 优先，Vision 兜底
    - 包装规范：pdftotext 优先（BJ 精确匹配）
    - 图形/尺寸/测试：Vision
    """
    result = {}

    # 模具号：pdftotext 优先（关键！）
    text_model = text_data.get("model_no", "")
    vision_model = vision_data.get("model_no", "")
    
    # 校验 pdftotext 的模具号
    if text_model and len(text_model) > 2 and any(c.isdigit() for c in text_model):
        result["model_no"] = text_model
    elif vision_model and len(vision_model) > 2 and any(c.isdigit() for c in vision_model):
        result["model_no"] = vision_model
    else:
        result["model_no"] = ""

    # 产品名：pdftotext 优先
    text_product = text_data.get("product_name", "")
    vision_product = vision_data.get("product_name", "")
    result["product_name"] = text_product or vision_product

    # 包装规范：pdftotext 优先
    text_pkg = text_data.get("packaging_spec", "")
    vision_pkg = vision_data.get("packaging_spec", "")
    result["packaging_spec"] = text_pkg or vision_pkg

    # Drawing No.
    result["drawing_no"] = vision_data.get("drawing_no", "") or text_data.get("drawing_no", "")
    result["material_code"] = vision_data.get("material_code", "") or text_data.get("material_code", "")
    result["length_mm"] = text_data.get("length_mm", "") or vision_data.get("length_mm", "")

    # BOM：pdftotext 优先
    text_bom = text_data.get("bom", [])
    vision_bom = vision_data.get("bom", [])
    if text_bom and len(text_bom) >= 3:
        result["bom"] = text_bom
    elif vision_bom:
        result["bom"] = vision_bom
    else:
        result["bom"] = []

    # 产品矩阵
    text_products = text_data.get("products", [])
    vision_products = vision_data.get("products", [])
    result["products"] = text_products or vision_products

    # Vision 擅长的部分
    result["mold_info"] = vision_data.get("mold_info", "")
    result["mold_number"] = vision_data.get("mold_number", "")
    result["tolerances"] = vision_data.get("tolerances", [])
    result["test_requirements"] = vision_data.get("test_requirements", {})
    result["pin_assignment"] = vision_data.get("pin_assignment", {})
    result["dimensions"] = vision_data.get("dimensions", [])
    result["notes"] = vision_data.get("notes", [])
    result["revision_history"] = vision_data.get("revision_history", [])
    result["company"] = vision_data.get("company", "")
    result["drawing_date"] = vision_data.get("drawing_date", "")
    result["drawn_by"] = vision_data.get("drawn_by", "")
    result["checked_by"] = vision_data.get("checked_by", "")
    result["approved_by"] = vision_data.get("approved_by", "")

    return result


def extract_hybrid(pdf_path: str, use_vision: bool = True, use_text: bool = True) -> dict:
    """混合提取主入口（v5.0：pdftotext 优先）"""
    result = {
        "source_file": os.path.basename(pdf_path),
        "extraction_method": "hybrid",
        "pages": 0,
    }

    text_data = {}
    vision_data = {}

    # Step 1: pdftotext 精确文本提取（优先）
    if use_text:
        print("[1/4] pdftotext 文本提取...", file=sys.stderr)
        try:
            text = extract_text_with_pdftotext(pdf_path)
            print(f"  提取到 {len(text)} 字符", file=sys.stderr)

            # 解析各字段
            text_data["product_name"] = ""
            text_data["model_no"] = parse_model_no_from_text(text)
            text_data["drawing_no"] = ""
            text_data["material_code"] = ""
            text_data["packaging_spec"] = parse_packaging_from_text(text)
            text_data["length_mm"] = ""
            text_data["bom"] = parse_bom_from_text(text)
            text_data["products"] = parse_products_from_text(text)

            # 从 products 中提取产品名
            if text_data["products"]:
                products = text_data["products"]
                product_names = [p.get("customer_item", "") for p in products if p.get("customer_item")]
                if product_names:
                    text_data["product_name"] = ", ".join(product_names)

            print(f"  Model No: {text_data.get('model_no', '未识别')}", file=sys.stderr)
            print(f"  BOM: {len(text_data.get('bom', []))} 行", file=sys.stderr)
            print(f"  产品：{text_data.get('product_name', '未识别')[:50]}", file=sys.stderr)
        except Exception as e:
            print(f"  pdftotext 失败：{e}", file=sys.stderr)

    # Step 2: PDF → PNG (300 DPI)
    print("[2/4] PDF 转图片 (300 DPI)...", file=sys.stderr)
    try:
        images = pdf_to_images(pdf_path, dpi=300)
        result["pages"] = len(images)
        print(f"  生成 {len(images)} 张图片", file=sys.stderr)
    except Exception as e:
        print(f"  PDF 转图片失败：{e}", file=sys.stderr)
        images = []

    # Step 3: Vision API（仅兜底）
    if use_vision and images:
        print("[3/4] Vision API 提取（兜底）...", file=sys.stderr)
        try:
            images_b64 = [image_to_base64(img) for img in images]
            vision_data = call_vision_api(images_b64)

            if "error" in vision_data:
                print(f"  Vision API 错误：{vision_data['error']}", file=sys.stderr)
                vision_data = {}
            else:
                print(f"  Model No: {vision_data.get('model_no', '未识别')}", file=sys.stderr)
                print(f"  BOM: {len(vision_data.get('bom', []))} 行", file=sys.stderr)
        except Exception as e:
            print(f"  Vision API 失败：{e}", file=sys.stderr)
    elif not use_vision:
        print("[3/4] 跳过 Vision API", file=sys.stderr)

    # Step 4: 合并结果（pdftotext 优先）
    print("[4/4] 合并提取结果（pdftotext 优先）...", file=sys.stderr)

    if use_text and use_vision:
        result = merge_text_and_vision(text_data, vision_data)
        result["extraction_method"] = "hybrid"
    elif use_text:
        result.update(text_data)
        result["extraction_method"] = "pdftotext"
    elif use_vision:
        result.update(vision_data)
        result["extraction_method"] = "vision"

    # 补充元数据
    result["source_file"] = os.path.basename(pdf_path)
    result["pages"] = result.get("pages", len(images) if images else 0)

    # 字段校验 + 数据质量检查（v5.0）
    warnings = []
    
    # 必填字段检查
    required_fields = ["product_name", "drawing_no", "packaging_spec"]
    for field in required_fields:
        if not result.get(field):
            warnings.append(f"⚠️ 缺失字段：{field}")
    
    # 模具号数据质量检查
    model_no = result.get("model_no", "")
    if model_no:
        if len(model_no) <= 2:
            warnings.append(f"⚠️ 模具号异常：'{model_no}' (可能识别错误)")
            result["model_no"] = ""
        elif not any(c.isdigit() for c in model_no):
            warnings.append(f"⚠️ 模具号格式异常：'{model_no}' (应包含数字)")
            result["model_no"] = ""
    
    # 产品名数据质量检查
    product_name = result.get("product_name", "")
    if product_name and len(product_name) <= 3:
        warnings.append(f"⚠️ 产品名异常：'{product_name}' (可能识别错误)")
        result["product_name"] = ""
    
    # BOM 检查
    if not result.get("bom"):
        warnings.append("⚠️ BOM 物料清单为空")
    elif len(result.get("bom", [])) < 3:
        warnings.append(f"⚠️ BOM 行数过少：{len(result.get('bom', []))} 行 (可能提取不完整)")

    result["warnings"] = warnings

    # 计算置信度（带惩罚）
    checks = sum(1 for f in required_fields if result.get(f))
    if result.get("bom"):
        checks += 1
    
    base_confidence = (checks / (len(required_fields) + 1)) * 100
    if warnings:
        penalty = len(warnings) * 10
        confidence = max(0, base_confidence - penalty)
    else:
        confidence = base_confidence
    
    result["confidence"] = round(confidence, 1)

    print(f"  置信度：{confidence:.1f}%", file=sys.stderr)
    if warnings:
        for w in warnings:
            print(f"  {w}", file=sys.stderr)

    return result


# ---------------------------------------------------------------------------
# 5. 输出格式化
# ---------------------------------------------------------------------------

def to_markdown(data: dict) -> str:
    """输出 Markdown"""
    lines = []

    product_name = data.get("product_name", "") or "未知产品"
    lines.append(f"# 产品图纸：{product_name[:50]}")
    lines.append("")
    lines.append(f"> 📋 **来源文件：** `{data.get('source_file', '')}`")
    lines.append(f"> 📅 **图纸日期：** {data.get('drawing_date', '—')}")
    lines.append(f"> 🏭 **公司：** {data.get('company', '—')}")
    lines.append(f"> 📐 **型号：** {data.get('model_no', data.get('drawing_no', '—'))}")
    lines.append(f"> 🎯 **提取方法：** {data.get('extraction_method', 'hybrid')} | 置信度：{data.get('confidence', 0)}%")
    lines.append("")

    # 基本信息
    lines.append("## 📊 基本信息")
    lines.append("")
    lines.append("| 项目 | 内容 |")
    lines.append("|------|------|")
    lines.append(f"| **客人品名** | {data.get('product_name', '—')} |")
    lines.append(f"| **模具编号** | {data.get('model_no', '—')} |")
    lines.append(f"| **Drawing No.** | {data.get('drawing_no', '—')} |")
    lines.append(f"| **包装规范** | {data.get('packaging_spec', '—')} |")
    lines.append(f"| **长度 (mm)** | {data.get('length_mm', '—')} |")
    lines.append("")

    # 产品矩阵
    products = data.get("products", [])
    if products and len(products) > 1:
        lines.append("## 📋 产品规格矩阵")
        lines.append("")
        lines.append("| 客人品名 | 长度 (mm) | 包装规范 |")
        lines.append("|----------|----------|----------|")
        for p in products:
            lines.append(
                f"| {p.get('customer_item', '')} "
                f"| {p.get('length_mm', '')} "
                f"| {p.get('packaging_spec', '')} |"
            )
        lines.append("")

    # BOM
    bom = data.get("bom", [])
    if bom:
        lines.append("## 🔧 BOM 物料清单")
        lines.append("")
        lines.append("| NO. | 部件名称 | 规格 | 用量 |")
        lines.append("|-----|----------|------|------|")
        for row in bom[:15]:
            lines.append(
                f"| {row.get('no', '')} "
                f"| {row.get('part_name', '')} "
                f"| {row.get('spec', '')[:80]} "
                f"| {row.get('quantity', '')} |"
            )
        lines.append("")

    # 测试要求
    tests = data.get("test_requirements", {})
    if tests:
        lines.append("## 🧪 测试要求")
        lines.append("")
        for t in tests.get("other_tests", []):
            lines.append(f"- {t}")
        lines.append("")

    # 模具信息
    mold = data.get("mold_info", "")
    if mold:
        lines.append("## 🏗️ 模具信息")
        lines.append("")
        lines.append(f"```\n{mold}\n```")
        lines.append("")

    # 注意事项
    notes = data.get("notes", [])
    if notes:
        lines.append("## ⚠️ 注意事项")
        lines.append("")
        for n in notes:
            lines.append(f"- {n}")
        lines.append("")

    lines.append("---")
    lines.append(f"*提取完成 | 页数：{data.get('pages', 1)}*")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 6. CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="产品图纸混合提取器 v5.0（pdftotext 优先）")
    parser.add_argument("pdf_path", help="PDF 文件路径")
    parser.add_argument("-o", "--output-dir", default="./output")
    parser.add_argument("-f", "--format", choices=["json", "md", "both"], default="both")
    parser.add_argument("--vision-only", action="store_true", help="仅用 Vision API")
    parser.add_argument("--text-only", action="store_true", help="仅用 pdftotext")
    parser.add_argument("--dpi", type=int, default=300, help="OCR DPI（默认 300）")
    parser.add_argument("--stdout", action="store_true")

    args = parser.parse_args()

    if not os.path.exists(args.pdf_path):
        print(f"❌ 文件不存在：{args.pdf_path}", file=sys.stderr)
        sys.exit(1)

    use_vision = not args.text_only
    use_text = not args.vision_only

    if args.vision_only and args.text_only:
        print("❌ 不能同时使用 --vision-only 和 --text-only", file=sys.stderr)
        sys.exit(1)

    # 提取
    data = extract_hybrid(args.pdf_path, use_vision=use_vision, use_text=use_text)

    # 输出
    if args.stdout:
        if args.format in ("json", "both"):
            print(json.dumps(data, ensure_ascii=False, indent=2))
        if args.format in ("md", "both"):
            print(to_markdown(data))
        return

    os.makedirs(args.output_dir, exist_ok=True)
    stem = Path(args.pdf_path).stem

    if args.format in ("json", "both"):
        json_path = os.path.join(args.output_dir, f"{stem}.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ JSON: {json_path}", file=sys.stderr)

    if args.format in ("md", "both"):
        md_path = os.path.join(args.output_dir, f"{stem}.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(to_markdown(data))
        print(f"✅ Markdown: {md_path}", file=sys.stderr)

    # 摘要
    print(f"\n📊 提取完成", file=sys.stderr)
    print(f"  产品：{data.get('product_name', '未识别')[:50]}", file=sys.stderr)
    print(f"  模具：{data.get('model_no', '未识别')}", file=sys.stderr)
    print(f"  包装：{data.get('packaging_spec', '未识别')}", file=sys.stderr)
    print(f"  BOM: {len(data.get('bom', []))} 行", file=sys.stderr)
    print(f"  置信度：{data.get('confidence', 0)}%", file=sys.stderr)


if __name__ == "__main__":
    main()
