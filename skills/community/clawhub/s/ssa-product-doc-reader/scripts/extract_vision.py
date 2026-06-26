#!/usr/bin/env python3
"""
Product Drawing Extractor v3.0 - Vision Mode
=============================================
用 Vision API（Claude/GPT-4V）直接理解产品图纸，提取结构化数据。

不依赖 Docling 坐标分区——直接把图片发给 Vision 模型，让模型理解布局。
这是最通用的方案，适用于所有模板类型。

用法：
  python3 extract_vision.py <pdf_path> [--output-dir ./output] [--format json|md|both]
  python3 extract_vision.py <pdf_path> --provider openrouter  # 指定 API
  python3 extract_vision.py <pdf_path> --dry-run              # 只生成图片不调API
"""

import argparse
import base64
import json
import os
import re
import subprocess
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# 1. PDF → PNG
# ---------------------------------------------------------------------------

def pdf_to_images(pdf_path: str, dpi: int = 200) -> list[str]:
    """PDF 转 PNG，返回图片路径列表"""
    stem = Path(pdf_path).stem[:20]  # 截断避免路径过长
    prefix = f"/tmp/vision_{stem}"

    # 清理旧文件
    import glob
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
# 2. Vision API 调用
# ---------------------------------------------------------------------------

EXTRACTION_PROMPT = """你是一个产品工程图纸分析专家。请仔细查看这张产品图纸图片，提取以下所有信息。

**务必严格按照 JSON 格式输出，不要输出任何其他内容。**

```json
{
  "product_name": "客人品名 / CUSTOMER ITEM（可能有多个，用逗号分隔）",
  "length_mm": "长度(mm)（可能有多个，用逗号分隔）",
  "material_code": "物料编码 / DRAWING NO.",
  "packaging_spec": "包装规范 / Package No（可能有多个，用逗号分隔）",
  "model_no": "型号 / MODEL NO.（如有）",
  "mold_info": "模具信息",
  "mold_number": "模号/AB端",
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
  "pin_assignment": {
    "connectors": ["连接器类型列表（如 HDMI AF, DVI(24+1)F, DP M）"],
    "description": "连接器对应关系描述"
  },
  "test_requirements": [
    "测试要求列表（如 100% 开路短路测试、PASS 8K@60Hz 等）"
  ],
  "dimensions": [
    "关键尺寸标注（如 11.1±0.3, 50.1±0.5 等）"
  ],
  "notes": [
    "注意事项（如 RoHS 2.0、REACH、加州 65 等）"
  ],
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

注意事项：
1. 如果某个字段在图纸上不存在或看不清，填空字符串 ""
2. BOM 物料清单要完整提取每一行，序号可能是 ①②③ 或数字
3. 规格字段要完整，包括材质、颜色、尺寸、镀层等所有信息
4. 如果有多个产品型号/长度，在 products 数组中列出所有
5. 测试要求可能在图纸不同位置，全部收集
6. 公差标准分五金件和塑胶件两列
7. 尺寸标注提取图纸上的所有关键尺寸（带公差的优先）
8. 变更记录在图纸边栏，提取版本号、日期、变更内容"""


def call_vision_api(
    images_b64: list[str],
    provider: str = "bailian",
    model: str = None,
) -> dict:
    """调用 Vision API 提取图纸信息"""

    if provider == "bailian":
        return _call_bailian(images_b64, model or "qwen-vl-max")
    elif provider == "openrouter":
        return _call_openrouter(images_b64, model or "google/gemini-2.5-flash")
    else:
        raise ValueError(f"Unknown provider: {provider}")


def _call_bailian(images_b64: list[str], model: str) -> dict:
    """调用百炼 Qwen-VL"""
    import urllib.request

    api_key = os.environ.get("DASHSCOPE_API_KEY", "")
    if not api_key:
        # Try reading from config
        config_path = os.path.expanduser("~/.openclaw/config.yaml")
        if os.path.exists(config_path):
            with open(config_path) as f:
                for line in f:
                    if "DASHSCOPE_API_KEY" in line or "dashscope" in line.lower():
                        # Simple extraction
                        if ":" in line:
                            api_key = line.split(":", 1)[1].strip().strip("'\"")
                            break

    if not api_key:
        raise RuntimeError("DASHSCOPE_API_KEY not found. Set env or pass --provider openrouter")

    content = [{"type": "text", "text": EXTRACTION_PROMPT}]
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
        "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
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


def _call_openrouter(images_b64: list[str], model: str) -> dict:
    """调用 OpenRouter (Claude/GPT-4V)"""
    import urllib.request

    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    if not api_key:
        api_key = "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"

    content = [{"type": "text", "text": EXTRACTION_PROMPT}]
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
    # 尝试直接解析
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # 尝试提取 ```json ... ``` 块
    match = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass

    # 尝试提取 { ... } 块
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    # 全部失败
    return {"error": "Failed to parse JSON", "raw_response": text[:2000]}


# ---------------------------------------------------------------------------
# 3. 输出格式化
# ---------------------------------------------------------------------------

def to_markdown(data: dict, source_file: str = "") -> str:
    """输出 Markdown"""
    lines = []

    product_name = data.get("product_name", "") or "未知产品"
    lines.append(f"# 产品图纸：{product_name}")
    lines.append("")
    lines.append(f"> 📋 **来源文件：** `{source_file}`")
    lines.append(f"> 📅 **图纸日期：** {data.get('drawing_date', '—')}")
    lines.append(f"> 🏭 **公司：** {data.get('company', '—')}")
    lines.append(f"> 📐 **型号：** {data.get('model_no', '—')}")
    if data.get("drawn_by") or data.get("checked_by") or data.get("approved_by"):
        lines.append(
            f"> 👤 **绘图/审核/批准：** "
            f"{data.get('drawn_by', '—')} / {data.get('checked_by', '—')} / {data.get('approved_by', '—')}"
        )
    lines.append("")

    # 产品列表
    products = data.get("products", [])
    if products and len(products) > 0:
        lines.append("## 📊 产品规格")
        lines.append("")
        lines.append("| 客人品名 | 长度(mm) | 物料编码 | 包装规范 |")
        lines.append("|----------|----------|----------|----------|")
        for p in products:
            lines.append(
                f"| {p.get('customer_item', '')} "
                f"| {p.get('length_mm', '')} "
                f"| {p.get('material_code', '')} "
                f"| {p.get('packaging_spec', '')} |"
            )
        lines.append("")
    else:
        # 单产品
        lines.append("## 📊 基本信息")
        lines.append("")
        lines.append("| 项目 | 内容 |")
        lines.append("|------|------|")
        lines.append(f"| **客人品名** | {data.get('product_name', '—')} |")
        lines.append(f"| **长度 (mm)** | {data.get('length_mm', '—')} |")
        lines.append(f"| **物料编码** | {data.get('material_code', '—')} |")
        lines.append(f"| **包装规范** | {data.get('packaging_spec', '—')} |")
        lines.append(f"| **模具** | {data.get('mold_info', '—')} |")
        lines.append(f"| **模号/AB端** | {data.get('mold_number', '—')} |")
        lines.append("")

    # BOM
    bom = data.get("bom", [])
    if bom:
        lines.append("## 🔧 BOM 物料清单")
        lines.append("")
        lines.append("| NO. | 部件名称 | 规格 | 用量 |")
        lines.append("|-----|----------|------|------|")
        for row in bom:
            lines.append(
                f"| {row.get('no', '')} "
                f"| {row.get('part_name', '')} "
                f"| {row.get('spec', '')} "
                f"| {row.get('quantity', '')} |"
            )
        lines.append("")

    # 公差
    tolerances = data.get("tolerances", [])
    if tolerances:
        lines.append("## 📏 公差标准")
        lines.append("")
        lines.append("| 范围 | 五金件 | 丝印/塑胶件 |")
        lines.append("|------|--------|-------------|")
        for tol in tolerances:
            lines.append(
                f"| {tol.get('range', '')} "
                f"| {tol.get('hardware', '')} "
                f"| {tol.get('plastic', '')} |"
            )
        lines.append("")

    # 测试要求
    tests = data.get("test_requirements", [])
    if tests:
        lines.append("## 🧪 测试要求")
        lines.append("")
        for t in tests:
            lines.append(f"- {t}")
        lines.append("")

    # 尺寸标注
    dims = data.get("dimensions", [])
    if dims:
        lines.append("## 📐 关键尺寸")
        lines.append("")
        for d in dims:
            lines.append(f"- {d}")
        lines.append("")

    # Pin Assignment
    pa = data.get("pin_assignment", {})
    if pa and pa.get("connectors"):
        lines.append("## 🔌 Pin Assignment")
        lines.append("")
        lines.append(f"**连接器：** {', '.join(pa['connectors'])}")
        if pa.get("description"):
            lines.append(f"**描述：** {pa['description']}")
        lines.append("")

    # 注意事项
    notes = data.get("notes", [])
    if notes:
        lines.append("## ⚠️ 注意事项")
        lines.append("")
        for n in notes:
            lines.append(f"- {n}")
        lines.append("")

    # 变更记录
    revs = data.get("revision_history", [])
    if revs:
        lines.append("## 📝 变更记录")
        lines.append("")
        lines.append("| 版本 | 日期 | 内容 |")
        lines.append("|------|------|------|")
        for r in revs:
            lines.append(
                f"| {r.get('revision', '')} "
                f"| {r.get('date', '')} "
                f"| {r.get('description', '')} |"
            )
        lines.append("")

    lines.append("---")
    lines.append("*提取方法：Vision API*")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 4. CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="产品图纸 Vision 提取器 v3.0")
    parser.add_argument("pdf_path", help="PDF 文件路径")
    parser.add_argument("-o", "--output-dir", default="./output")
    parser.add_argument("-f", "--format", choices=["json", "md", "both"], default="both")
    parser.add_argument("--provider", choices=["bailian", "openrouter"], default="openrouter")
    parser.add_argument("--model", default=None)
    parser.add_argument("--dpi", type=int, default=200)
    parser.add_argument("--stdout", action="store_true")
    parser.add_argument("--dry-run", action="store_true", help="只转图片不调 API")

    args = parser.parse_args()

    if not os.path.exists(args.pdf_path):
        print(f"❌ 文件不存在: {args.pdf_path}", file=sys.stderr)
        sys.exit(1)

    # Step 1: PDF → PNG
    print("[1/3] PDF 转图片...", file=sys.stderr)
    images = pdf_to_images(args.pdf_path, dpi=args.dpi)
    print(f"  生成 {len(images)} 张图片", file=sys.stderr)

    if args.dry_run:
        print("  [dry-run] 跳过 API 调用", file=sys.stderr)
        for img in images:
            print(f"  📷 {img}", file=sys.stderr)
        return

    # Step 2: 调用 Vision API
    print(f"[2/3] 调用 Vision API ({args.provider})...", file=sys.stderr)
    images_b64 = [image_to_base64(img) for img in images]
    data = call_vision_api(images_b64, provider=args.provider, model=args.model)

    if "error" in data:
        print(f"  ❌ API 错误: {data['error']}", file=sys.stderr)
        if "raw_response" in data:
            print(f"  原始回复: {data['raw_response'][:500]}", file=sys.stderr)
        sys.exit(1)

    # 补充元数据
    data["source_file"] = os.path.basename(args.pdf_path)
    data["extraction_method"] = f"vision_{args.provider}"
    data["pages"] = len(images)

    # Step 3: 输出
    print("[3/3] 生成输出...", file=sys.stderr)

    if args.stdout:
        if args.format in ("json", "both"):
            print(json.dumps(data, ensure_ascii=False, indent=2))
        if args.format in ("md", "both"):
            print(to_markdown(data, os.path.basename(args.pdf_path)))
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
            f.write(to_markdown(data, os.path.basename(args.pdf_path)))
        print(f"✅ Markdown: {md_path}", file=sys.stderr)

    # 摘要
    bom_count = len(data.get("bom", []))
    products_count = len(data.get("products", []))
    print(f"\n📊 提取完成", file=sys.stderr)
    print(f"  产品: {data.get('product_name', '未识别')}", file=sys.stderr)
    print(f"  物料编码: {data.get('material_code', '未识别')}", file=sys.stderr)
    print(f"  BOM 行数: {bom_count}", file=sys.stderr)
    if products_count > 1:
        print(f"  产品型号数: {products_count}", file=sys.stderr)


if __name__ == "__main__":
    main()
