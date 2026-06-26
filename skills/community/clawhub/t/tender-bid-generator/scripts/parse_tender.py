#!/usr/bin/env python3
"""
招标文件解析脚本
支持PDF、DOCX、TXT格式
输出JSON格式的关键信息
"""

import sys
import json
import re
from pathlib import Path

def parse_pdf(file_path):
    """解析PDF文件"""
    try:
        import PyPDF2
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text
    except ImportError:
        print("错误：未安装PyPDF2，请运行 pip install PyPDF2")
        sys.exit(1)

def parse_docx(file_path):
    """解析DOCX文件"""
    try:
        from docx import Document
        doc = Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    except ImportError:
        print("错误：未安装python-docx，请运行 pip install python-docx")
        sys.exit(1)

def parse_txt(file_path):
    """解析TXT文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_info(text):
    """提取关键信息"""
    info = {
        "项目基本信息": {},
        "资质要求": [],
        "技术规格": [],
        "商务条款": {},
        "评分标准": [],
        "投标文件要求": {}
    }
    
    # 提取项目名称
    project_name_patterns = [
        r'项目名称[：:]\s*([^\n]+)',
        r'招标项目名称[：:]\s*([^\n]+)',
        r'采购项目名称[：:]\s*([^\n]+)'
    ]
    for pattern in project_name_patterns:
        match = re.search(pattern, text)
        if match:
            info["项目基本信息"]["项目名称"] = match.group(1).strip()
            break
    
    # 提取项目编号
    project_code_patterns = [
        r'项目编号[：:]\s*([^\n]+)',
        r'招标编号[：:]\s*([^\n]+)',
        r'采购编号[：:]\s*([^\n]+)'
    ]
    for pattern in project_code_patterns:
        match = re.search(pattern, text)
        if match:
            info["项目基本信息"]["项目编号"] = match.group(1).strip()
            break
    
    # 提取采购单位
    buyer_patterns = [
        r'采购人[：:]\s*([^\n]+)',
        r'采购单位[：:]\s*([^\n]+)',
        r'招标人[：:]\s*([^\n]+)'
    ]
    for pattern in buyer_patterns:
        match = re.search(pattern, text)
        if match:
            info["项目基本信息"]["采购单位"] = match.group(1).strip()
            break
    
    # 提取预算金额
    budget_patterns = [
        r'预算金额[：:]\s*([^\n]+)',
        r'采购预算[：:]\s*([^\n]+)',
        r'最高限价[：:]\s*([^\n]+)'
    ]
    for pattern in budget_patterns:
        match = re.search(pattern, text)
        if match:
            info["项目基本信息"]["预算金额"] = match.group(1).strip()
            break
    
    # 提取资质要求（简化版，提取包含"资质"、"资格"的段落）
    qualification_keywords = ['资质', '资格', '认证', '证书', '业绩', '经验']
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if any(kw in line for kw in qualification_keywords):
            # 获取上下文
            context = []
            for j in range(max(0, i-1), min(len(lines), i+3)):
                if lines[j].strip():
                    context.append(lines[j].strip())
            if context:
                info["资质要求"].append(' '.join(context))
    
    # 去重并限制数量
    info["资质要求"] = list(set(info["资质要求"]))[:20]
    
    # 提取技术规格要求
    tech_keywords = ['技术参数', '技术指标', '技术要求', '规格', '性能', '功能']
    for i, line in enumerate(lines):
        if any(kw in line for kw in tech_keywords):
            context = []
            for j in range(max(0, i-1), min(len(lines), i+3)):
                if lines[j].strip():
                    context.append(lines[j].strip())
            if context:
                info["技术规格"].append(' '.join(context))
    
    info["技术规格"] = list(set(info["技术规格"]))[:20]
    
    # 提取商务条款
    business_keywords = ['交货', '付款', '质保', '售后', '服务期']
    for i, line in enumerate(lines):
        if any(kw in line for kw in business_keywords):
            if '交货' in line or '交付' in line:
                match = re.search(r'交货期[：:]\s*([^\n]+)', line)
                if match:
                    info["商务条款"]["交货期"] = match.group(1).strip()
            if '付款' in line:
                match = re.search(r'付款方式[：:]\s*([^\n]+)', line)
                if match:
                    info["商务条款"]["付款方式"] = match.group(1).strip()
            if '质保' in line or '保修' in line:
                match = re.search(r'质保期[：:]\s*([^\n]+)', line)
                if match:
                    info["商务条款"]["质保期"] = match.group(1).strip()
    
    # 提取评分标准
    score_section = False
    score_lines = []
    for line in lines:
        if '评分' in line or '评标' in line:
            score_section = True
        if score_section:
            score_lines.append(line)
            if len(score_lines) > 50:  # 限制评分部分长度
                break
    info["评分标准"] = score_lines[:30]
    
    return info

def main():
    if len(sys.argv) < 2:
        print("用法: python3 parse_tender.py <招标文件路径>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    file_ext = Path(file_path).suffix.lower()
    
    # 根据扩展名选择解析器
    if file_ext == '.pdf':
        text = parse_pdf(file_path)
    elif file_ext in ['.docx', '.doc']:
        text = parse_docx(file_path)
    elif file_ext == '.txt':
        text = parse_txt(file_path)
    else:
        print(f"不支持的文件格式: {file_ext}")
        print("支持的格式: PDF, DOCX, TXT")
        sys.exit(1)
    
    # 提取信息
    info = extract_info(text)
    
    # 输出JSON
    print(json.dumps(info, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
