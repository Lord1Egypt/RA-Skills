#!/usr/bin/env python3
"""
简历解析工具
支持PDF、Word(.doc/.docx)、图片格式简历的文本提取和结构化解析
"""
import os
import sys
from pathlib import Path
from typing import Dict, Any

# 依赖安装说明：
# pip install pdfplumber python-docx pytesseract pillow python-magic-bin
# 安装Tesseract OCR引擎：https://github.com/UB-Mannheim/tesseract/wiki

try:
    import pdfplumber
except ImportError:
    print("⚠️  缺少pdfplumber依赖，PDF解析功能不可用，执行：pip install pdfplumber")
try:
    from docx import Document
except ImportError:
    print("⚠️  缺少python-docx依赖，Word解析功能不可用，执行：pip install python-docx")
try:
    from PIL import Image
    import pytesseract
    # Windows下需要指定tesseract安装路径
    if sys.platform == 'win32':
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
except ImportError:
    print("⚠️  缺少pytesseract/Pillow依赖，图片解析功能不可用，执行：pip install pytesseract pillow")

def extract_text_from_pdf(pdf_path: str) -> str:
    """从PDF文件提取文本"""
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    except Exception as e:
        print(f"PDF解析失败: {str(e)}")
        return ""

def extract_text_from_docx(docx_path: str) -> str:
    """从docx文件提取文本"""
    try:
        doc = Document(docx_path)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])
    except Exception as e:
        print(f"Word解析失败: {str(e)}")
        return ""

def extract_text_from_image(image_path: str) -> str:
    """从图片文件提取文本（OCR）"""
    try:
        image = Image.open(image_path)
        # 支持中英文识别
        return pytesseract.image_to_string(image, lang='chi_sim+eng')
    except Exception as e:
        print(f"图片OCR解析失败: {str(e)}")
        return ""

def parse_resume(file_path: str) -> Dict[str, Any]:
    """
    解析简历文件，返回结构化信息
    """
    if not os.path.exists(file_path):
        return {"error": "文件不存在"}
    
    file_ext = Path(file_path).suffix.lower()
    text = ""
    
    # 根据文件类型提取文本
    if file_ext == '.pdf':
        text = extract_text_from_pdf(file_path)
    elif file_ext in ['.docx', '.doc']:
        text = extract_text_from_docx(file_path)
    elif file_ext in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']:
        text = extract_text_from_image(file_path)
    else:
        return {"error": f"不支持的文件格式: {file_ext}"}
    
    if not text:
        return {"error": "未能从文件中提取到文本内容"}
    
    return {
        "raw_text": text,
        "file_type": file_ext,
        "file_path": file_path
    }

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python resume_parser.py <简历文件路径>")
        sys.exit(1)
    
    result = parse_resume(sys.argv[1])
    # 输出到文件避免编码问题
    import json
    output_path = "resume_parsed_result.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"解析结果已保存到: {output_path}")