#!/usr/bin/env python3
"""
verify.py — 验证下载的中考真题文件的真实性和完整性
用法: python3 verify.py <file_path> <expected_year> [expected_region] [expected_subject]
返回: JSON格式的验证结果
"""

import sys
import os
import json
import re
import zipfile

def verify_file(file_path, year, region="", subject="英语"):
    """验证文件的真实性和完整性"""
    result = {
        "pass": True,
        "file": file_path,
        "issues": [],
        "checks": [],
        "content_detail": None
    }
    
    # 检查1: 文件是否存在
    if not os.path.exists(file_path):
        result["pass"] = False
        result["error"] = "文件不存在"
        return result
    
    # 检查2: 文件大小
    file_size = os.path.getsize(file_path)
    min_size = 51200  # 50KB
    size_ok = file_size >= min_size
    result["checks"].append(f"文件大小: {file_size} bytes {'✅' if size_ok else '❌'}")
    if not size_ok:
        result["pass"] = False
        result["issues"].append(f"文件过小 ({file_size} bytes < {min_size} bytes)")
    result["file_size"] = file_size
    
    # 检查3: 文件格式与扩展名一致
    file_ext = os.path.splitext(file_path)[1].lower().lstrip(".")
    
    # 用magic bytes检测实际格式
    actual_format = detect_format(file_path)
    format_ok = True
    
    format_map = {
        "pdf": ["pdf"],
        "docx": ["zip", "docx"],  # docx实际是zip格式
        "doc": ["ole2", "doc"],
        "zip": ["zip"],
        "rar": ["rar"],
        "png": ["png"],
        "jpg": ["jpeg"],
    }
    
    if file_ext in format_map:
        if actual_format not in format_map[file_ext]:
            format_ok = False
            result["pass"] = False
            result["issues"].append(f"扩展名.{file_ext}但实际格式为{actual_format}")
    
    result["checks"].append(f"文件格式一致性: {actual_format} {'✅' if format_ok else '❌'}")
    result["actual_format"] = actual_format
    
    # 检查4: HTML重定向检测
    if actual_format == "html":
        result["pass"] = False
        result["issues"].append("文件是HTML页面而非真实试卷文件，可能是下载被重定向到登录页")
    
    # 检查5: 内容关键词验证
    if file_ext == "docx" and actual_format in ["zip", "docx"]:
        content_result = verify_docx(file_path, subject)
        result["content_detail"] = content_result
        
        if not content_result.get("has_content", False):
            result["pass"] = False
            result["issues"].append("docx内容为空或过短")
        
        if content_result.get("issues"):
            for issue in content_result["issues"]:
                if "必需关键词" in issue:
                    result["pass"] = False
                    result["issues"].append(issue)
        
        is_scan = content_result.get("is_scan", False)
        result["checks"].append(
            f"内容检查: has_content={content_result.get('has_content')}, "
            f"is_scan={is_scan} {'✅' if content_result.get('has_content') else '❌'}"
        )
    
    elif file_ext == "pdf" and actual_format == "pdf":
        pdf_result = verify_pdf(file_path)
        result["content_detail"] = pdf_result
        if not pdf_result.get("valid", False):
            result["pass"] = False
            result["issues"].append("PDF文件无效")
        result["checks"].append(f"PDF有效性: {pdf_result.get('valid')} {'✅' if pdf_result.get('valid') else '❌'}")
    
    return result


def detect_format(file_path):
    """通过magic bytes检测文件实际格式"""
    try:
        with open(file_path, "rb") as f:
            header = f.read(16)
        
        if header[:4] == b'%PDF':
            return "pdf"
        elif header[:4] == b'PK\x03\x04':
            # ZIP或DOCX（DOCX也是ZIP格式）
            return "zip"
        elif header[:7] == b'Rar!\x1a\x07':
            return "rar"
        elif header[:8] == b'\x89PNG\r\n\x1a\n':
            return "png"
        elif header[:2] == b'\xff\xd8':
            return "jpeg"
        elif header[:4] == b'\xd0\xcf\x11\xe0':
            return "ole2"  # MS Office 97-2003
        elif header[:5] == b'<?xml' or header[:1] == b'<':
            return "html"
        elif b'<!DOCTYPE' in header or b'<html' in header.lower():
            return "html"
        else:
            # 尝试检测HTML
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read(500).lower()
                    if '<html' in content or '<!doctype' in content:
                        return "html"
            except:
                pass
            return "unknown"
    except:
        return "unknown"


def verify_docx(file_path, subject="英语"):
    """验证DOCX文件内容"""
    result = {
        "type": "docx",
        "is_scan": False,
        "text_length": 0,
        "media_count": 0,
        "media_total_size": 0,
        "found_keywords": [],
        "issues": [],
        "has_content": False
    }
    
    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            # 提取文本
            try:
                with z.open('word/document.xml') as f:
                    content = f.read().decode('utf-8')
                    text = re.sub(r'<[^>]+>', ' ', content)
                    text = re.sub(r'\s+', ' ', text).strip()
                    result["text_length"] = len(text)
            except KeyError:
                text = ""
            
            # 检查媒体文件
            media_files = [n for n in z.namelist() if 'media' in n.lower()]
            result["media_count"] = len(media_files)
            total_media_size = sum(z.getinfo(n).file_size for n in media_files)
            result["media_total_size"] = total_media_size
            
            # 判断是否为扫描嵌入版
            result["is_scan"] = total_media_size > 1000000 and len(text) < 500
            
            # 关键词检查（扫描版跳过，因为文本在图片中无法提取）
            if not result["is_scan"] and len(text) > 50:
                # 检查必需关键词
                required_keywords = ['考试', '注意事项']
                for kw in required_keywords:
                    if kw in text:
                        result["found_keywords"].append(kw)
                    else:
                        result["issues"].append(f'缺少必需关键词: {kw}')
                
                # 检查学科关键词
                subject_keywords_map = {
                    "英语": ['听力', '阅读', '完形', '填空', '写作', '翻译'],
                    "数学": ['选择题', '填空题', '解答题', '计算', '证明'],
                    "语文": ['阅读', '作文', '文言文', '默写', '名著'],
                    "物理": ['选择题', '填空题', '实验', '计算'],
                    "化学": ['选择题', '填空题', '实验', '计算'],
                }
                
                subject_keywords = subject_keywords_map.get(subject, ['选择题', '填空题'])
                found_subject = [kw for kw in subject_keywords if kw in text]
                
                if len(found_subject) < 2:
                    result["issues"].append(f'学科关键词过少(仅{len(found_subject)}个): {found_subject}')
                else:
                    result["found_keywords"].extend(found_subject)
            elif result["is_scan"]:
                result["found_keywords"] = ["(扫描嵌入版，无法提取文本关键词)"]
            
            # 判断是否有实质内容
            result["has_content"] = len(text) > 200 or result["is_scan"]
    
    except Exception as e:
        result["error"] = str(e)
        result["issues"].append(str(e))
    
    return result


def verify_pdf(file_path):
    """验证PDF文件"""
    result = {"type": "pdf", "valid": False, "issues": []}
    try:
        with open(file_path, 'rb') as f:
            header = f.read(10)
            if header[:4] == b'%PDF':
                result["valid"] = True
            else:
                result["issues"].append('非有效PDF文件')
    except Exception as e:
        result["error"] = str(e)
        result["issues"].append(str(e))
    return result


def main():
    if len(sys.argv) < 3:
        print(json.dumps({
            "pass": False,
            "error": "用法: verify.py <file_path> <expected_year> [expected_region] [expected_subject]"
        }, ensure_ascii=False))
        sys.exit(1)
    
    file_path = sys.argv[1]
    year = sys.argv[2]
    region = sys.argv[3] if len(sys.argv) > 3 else ""
    subject = sys.argv[4] if len(sys.argv) > 4 else "英语"
    
    result = verify_file(file_path, year, region, subject)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 返回非零退出码表示验证失败
    sys.exit(0 if result["pass"] else 1)


if __name__ == "__main__":
    main()
