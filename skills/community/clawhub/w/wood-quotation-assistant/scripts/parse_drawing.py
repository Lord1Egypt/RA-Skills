"""
parse_drawing.py - 图纸解析脚本
支持：CAD (DWG) / PDF / 图片 (JPG/PNG)
提取：尺寸数据、工艺要求、材料说明
"""

import os
import sys
import json
from pathlib import Path


def parse_dwg(file_path: str) -> dict:
    """解析 DWG CAD 图纸"""
    # TODO: 接入 LibreCAD / ODA File Converter 或 ezdxf 库
    # 现阶段返回占位结构，等待接入真实解析引擎
    return {
        "format": "dwg",
        "file": file_path,
        "status": "pending",
        "dimensions": {},
        "materials": [],
        "processes": [],
        "note": "请补充 CAD 图纸解析实现"
    }


def parse_pdf(file_path: str) -> dict:
    """解析 PDF 图纸（文字+尺寸提取）"""
    try:
        import pdfplumber
    except ImportError:
        return {
            "format": "pdf",
            "file": file_path,
            "status": "error",
            "error": "pdfplumber 未安装，执行: pip install pdfplumber"
        }

    result = {
        "format": "pdf",
        "file": file_path,
        "status": "success",
        "dimensions": {},
        "materials": [],
        "processes": [],
        "raw_text": ""
    }

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            result["raw_text"] += text + "\n"
            # 尺寸正则：识别 "W1200*D600*H800" / "1200×600×800" 等格式
            import re
            dim_pattern = re.findall(r'(\d+[\*×x]\d+[\*×x]\d+)', text)
            for d in dim_pattern:
                parts = re.split(r'[\*×x]', d)
                if len(parts) == 3:
                    w, d_h, h = parts
                    result["dimensions"][f"W{w}_D{d_h}_H{h}"] = {
                        "width": int(w), "depth": int(d_h), "height": int(h)
                    }
            # 工艺关键词
            keywords = ["喷漆", "烤漆", "贴皮", "封边", "CNC", "雕刻", "打磨", "组装"]
            for kw in keywords:
                if kw in text:
                    if kw not in result["processes"]:
                        result["processes"].append(kw)
            # 材料关键词
            mat_keywords = ["密度板", "颗粒板", "多层板", "实木", "欧松板", "刨花板"]
            for m in mat_keywords:
                if m in text:
                    if m not in result["materials"]:
                        result["materials"].append(m)

    return result


def parse_image(file_path: str, description: str = "") -> dict:
    """解析图片图纸 + 文字描述"""
    # TODO: 接入 OCR（pytesseract）或视觉模型识别尺寸/工艺
    # 现阶段依赖 description 字段作为主要输入
    result = {
        "format": "image",
        "file": file_path,
        "status": "partial",
        "dimensions": {},
        "materials": [],
        "processes": [],
        "raw_description": description
    }

    import re
    # 从 description 中解析尺寸
    dim_pattern = re.findall(r'(\d+[\*×x]\d+[\*×x]\d+)', description)
    for d in dim_pattern:
        parts = re.split(r'[\*×x]', d)
        if len(parts) == 3:
            w, d_h, h = parts
            result["dimensions"][f"W{w}_D{d_h}_H{h}"] = {
                "width": int(w), "depth": int(d_h), "height": int(h)
            }

    keywords = ["喷漆", "烤漆", "贴皮", "封边", "CNC", "雕刻", "打磨", "组装"]
    for kw in keywords:
        if kw in description and kw not in result["processes"]:
            result["processes"].append(kw)

    mat_keywords = ["密度板", "颗粒板", "多层板", "实木", "欧松板", "刨花板"]
    for m in mat_keywords:
        if m in description and m not in result["materials"]:
            result["materials"].append(m)

    return result


def parse_drawing(file_path: str, description: str = "") -> dict:
    """
    主入口：根据文件扩展名自动路由解析器
    Args:
        file_path: 图纸文件路径
        description: 用户提供的文字描述（图片场景补充用）
    Returns:
        dict: 解析结果，含 dimensions / materials / processes
    """
    ext = Path(file_path).suffix.lower()
    if ext in [".dwg", ".dxf"]:
        return parse_dwg(file_path)
    elif ext == ".pdf":
        return parse_pdf(file_path)
    elif ext in [".jpg", ".jpeg", ".png", ".bmp"]:
        return parse_image(file_path, description)
    else:
        return {
            "format": "unknown",
            "file": file_path,
            "status": "error",
            "error": f"不支持的图纸格式: {ext}，支持: DWG/DXF/PDF/JPG/PNG"
        }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python parse_drawing.py <图纸路径> [文字描述]")
        sys.exit(1)
    file_path = sys.argv[1]
    description = sys.argv[2] if len(sys.argv) > 2 else ""
    result = parse_drawing(file_path, description)
    print(json.dumps(result, ensure_ascii=False, indent=2))
