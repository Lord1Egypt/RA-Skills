#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF 产品目录提取脚本

从 PDF 产品目录（模具图纸）中自动提取产品信息，生成结构化知识库和 Excel 填充数据。

使用方法：
    python3 extract.py --pdf-dir "/path/to/pdfs" --output-dir "/path/to/output"

作者：IRON 💪
版本：1.0
日期：2026-03-23
"""

import argparse
import subprocess
import os
import re
import json
import shutil
from datetime import datetime

try:
    from docling.document_converter import DocumentConverter
    HAS_DOCLING = True
except ImportError:
    HAS_DOCLING = False
    print("⚠️  警告：docling 未安装，OCR 功能将不可用")
    print("   安装：pip3 install docling")

try:
    import openpyxl
    HAS_OPENPYXL = True
except ImportError:
    HAS_OPENPYXL = False
    print("⚠️  警告：openpyxl 未安装，Excel 填充功能将不可用")
    print("   安装：pip3 install openpyxl")


# ============== 已知映射表（fallback 用）=============
KNOWN_MAPPINGS = {
    # KVM 系列
    '599-031': {'model': 'DP-033A', 'pkg': 'BJ0599-0068', 'items': ['DDU1226-KVM-CABLE'], 'lengths': ['1830mm']},
    '599-032': {'model': 'DP-033B', 'pkg': 'BJ0599-0069', 'items': ['DU1226-KVM-CABLE'], 'lengths': ['1830mm']},
    '599-033': {'model': 'DP-034A', 'pkg': 'BJ0599-0070', 'items': ['DU12210-KVMCABLE'], 'lengths': ['3000mm']},
    '599-034': {'model': 'DP-035A', 'pkg': 'BJ0599-0071', 'items': ['HU1226-KVM-CABLE'], 'lengths': ['1830mm']},
    '599-035': {'model': 'DP-035B', 'pkg': 'BJ0599-0072', 'items': ['HU12210-KVM-CABLE'], 'lengths': ['3000mm']},
    # 其他系列...
}


def extract_text_from_pdf(pdf_path, ocr_threshold=300, use_ocr=False):
    """
    从 PDF 提取文本
    
    Args:
        pdf_path: PDF 文件路径
        ocr_threshold: 文本少于多少字符时启用 OCR
        use_ocr: 是否强制使用 OCR
    
    Returns:
        text: 提取的文本
        method: 提取方法 ('pdftotext' 或 'ocr')
    """
    # Method 1: pdftotext (矢量图 PDF)
    try:
        result = subprocess.run(['pdftotext', pdf_path, '-'], capture_output=True, text=True, timeout=30)
        text = result.stdout
        
        if len(text) >= ocr_threshold and not use_ocr:
            return text, 'pdftotext'
    except Exception as e:
        print(f"  pdftotext 失败：{e}")
    
    # Method 2: OCR (图片格式 PDF)
    if HAS_DOCLING:
        try:
            converter = DocumentConverter()
            ocr_result = converter.convert(pdf_path)
            text = ocr_result.document.export_to_markdown()
            return text, 'ocr'
        except Exception as e:
            print(f"  OCR 失败：{e}")
    
    return "", 'failed'


def extract_model_no(text):
    """
    提取模具号 (MODEL NO.)
    
    排除规则：
    1. BJ0599-XXXX 是包装规范，不是模具号
    2. 与客户品名完全相同的可能不是模具号
    3. 太短（<5 字符）的需要人工确认
    """
    # Pattern 1: MODEL NO. field
    match = re.search(r'MODEL\s+NO\.?\s*[:\|\s\n]*([A-Z]{2,}-\d+[A-Z0-9\-]*)', text, re.IGNORECASE)
    if match:
        model_no = match.group(1)
        # 排除 BJ 开头（包装规范）
        if not model_no.startswith('BJ'):
            return model_no
    
    # Pattern 2: XX-NNNA format (like DP-033A, OP-HD31)
    patterns = re.findall(r'\b([A-Z]{2,}-\d{2,}[A-Z]?)\b', text)
    for p in patterns:
        if not p.startswith('BJ') and len(p) >= 5:
            return p
    
    return None


def extract_package_specs(text):
    """提取包装规范 (BJ0599-XXXX)"""
    matches = re.findall(r'(BJ0599-\d{4})', text)
    return list(set(matches))[:3]


def extract_customer_items(text):
    """提取客户品名"""
    items = []
    
    # Pattern 1: CUSTOMER ITEM field
    ci_match = re.search(r'CUSTOMER ITEM\s*\n([A-Za-z0-9\-]+)', text, re.IGNORECASE)
    if ci_match:
        items.append(ci_match.group(1))
    
    # Pattern 2: 客人品名 section
    ci_idx = text.find('客人品名')
    if ci_idx >= 0:
        snippet = text[ci_idx:ci_idx+1500]
        lines = [l.strip() for l in snippet.split('\n') if l.strip()]
        for line in lines[1:15]:
            if re.match(r'^[A-Za-z][A-Za-z0-9\-\.]{4,}$', line):
                # 排除非产品名
                exclude = ['LENGTH', 'CABLE', 'TEST', 'ROHS', 'REACH', 'MODEL', 'DRAWING', 
                          'PACKAGE', 'SPECIFICATION', 'BJ0599']
                if line.upper() not in exclude and not line.startswith('BJ'):
                    if line not in items:
                        items.append(line)
    
    return items[:10]


def extract_lengths(text):
    """提取长度信息"""
    lengths = []
    
    # Pattern: number + mm/M/F
    matches = re.findall(r'(\d{2,4})\s*\+\d*\s*-\d*\s*(mm)?', text)
    for m in matches:
        length = f"{m[0]}mm"
        if int(m[0]) > 100 and length not in lengths:  # 合理的长度
            lengths.append(length)
    
    return lengths[:10]


def process_pdf(pdf_path, pdf_num, known_data=None, verbose=False):
    """
    处理单个 PDF 文件
    
    Returns:
        dict: 产品数据
    """
    pdf_file = os.path.basename(pdf_path)
    
    if verbose:
        print(f"  处理：{pdf_file}...", end=" ")
    
    # 1. 提取文本
    text, method = extract_text_from_pdf(pdf_path)
    
    # 2. 提取关键信息
    data = {
        'pdf_file': pdf_file,
        'pdf_number': pdf_num,
        'model_no': None,
        'package_specs': [],
        'customer_items': [],
        'lengths': [],
        'products': [],
        'extraction_method': method
    }
    
    # 3. 提取各字段
    data['model_no'] = extract_model_no(text)
    data['package_specs'] = extract_package_specs(text)
    data['customer_items'] = extract_customer_items(text)
    data['lengths'] = extract_lengths(text)
    
    # 4. Fallback 到已知映射
    pdf_key = f"599-{pdf_num:03d}"
    if known_data and pdf_key in known_data:
        known = known_data[pdf_key]
        if not data['model_no'] and known.get('model'):
            data['model_no'] = known['model']
        if not data['package_specs'] and known.get('pkg'):
            data['package_specs'] = [known['pkg']]
        if not data['customer_items'] and known.get('items'):
            data['customer_items'] = known['items']
        if not data['lengths'] and known.get('lengths'):
            data['lengths'] = known['lengths']
    
    # 5. 构建产品列表
    for i, item in enumerate(data['customer_items'][:10]):
        prod = {
            'customer_item': item,
            'length': data['lengths'][i] if i < len(data['lengths']) else None,
            'package_spec': data['package_specs'][0] if data['package_specs'] else None
        }
        data['products'].append(prod)
    
    if verbose:
        print(f"✓ Model={data['model_no'] or 'N/A'}, Items={len(data['customer_items'])}")
    
    return data


def generate_markdown_index(products, output_path):
    """生成产品索引 Markdown"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# 产品知识库索引\n\n")
        f.write(f"**总计：** {len(products)} 个产品\n\n")
        f.write(f"**更新时间：** {datetime.now().strftime('%Y-%m-%d')}\n\n")
        f.write("**数据结构：** 模具号 → 客户品名 → 长度 + 包装规范\n\n")
        f.write("## 产品列表\n\n")
        f.write("| 序号 | PDF 文件 | 模具号 (MODEL NO.) | 包装规范 | 客户品名 | 长度 |\n")
        f.write("|------|----------|-------------------|----------|----------|------|\n")
        
        for p in products:
            model = p['model_no'] or '❌ 未找到'
            pkg = ', '.join(p['package_specs']) if p['package_specs'] else 'N/A'
            items = ', '.join(p['customer_items'][:3]) if p['customer_items'] else '❌ 未找到'
            lengths = ', '.join(p['lengths'][:3]) if p['lengths'] else 'N/A'
            
            f.write(f"| {p['pdf_number']} | {p['pdf_file']} | {model} | {pkg} | {items} | {lengths} |\n")
        
        f.write("\n---\n\n## 详细数据\n\n")
        f.write("完整的产品数据已保存在：`产品详细数据.json`\n")


def generate_product_cards(products, output_dir):
    """生成单个产品词条"""
    cards_dir = os.path.join(output_dir, '类目词条')
    os.makedirs(cards_dir, exist_ok=True)
    
    for p in products:
        pdf_base = p['pdf_file'].replace('.pdf', '')
        card_path = os.path.join(cards_dir, f"{pdf_base}-类目词条.md")
        
        with open(card_path, 'w', encoding='utf-8') as f:
            f.write(f"# {p['pdf_file']} 产品类目词条\n\n")
            f.write("## 基础信息\n\n")
            f.write(f"- **模具号 (MODEL NO.):** {p['model_no'] or '未找到'}\n")
            f.write(f"- **包装规范:** {', '.join(p['package_specs']) if p['package_specs'] else '未找到'}\n")
            f.write(f"- **客户品名:** {', '.join(p['customer_items']) if p['customer_items'] else '未找到'}\n")
            f.write(f"- **长度:** {', '.join(p['lengths']) if p['lengths'] else '未找到'}\n\n")
            
            f.write("## 产品列表\n\n")
            f.write("| 客户品名 | 长度 | 包装规范 |\n")
            f.write("|----------|------|----------|\n")
            for prod in p['products']:
                f.write(f"| {prod['customer_item']} | {prod['length'] or 'N/A'} | {prod['package_spec'] or 'N/A'} |\n")
            
            f.write(f"\n---\n\n**数据来源：** {p['extraction_method']}\n")


def fill_excel(excel_path, products):
    """填充 Excel 文件"""
    if not HAS_OPENPYXL:
        print("⚠️  openpyxl 未安装，跳过 Excel 填充")
        return
    
    # 建立 SKU→模具号映射
    sku_to_model = {}
    for p in products:
        if p['model_no']:
            for item in p['customer_items']:
                sku_to_model[item] = p['model_no']
    
    # 加载 Excel
    wb = openpyxl.load_workbook(excel_path)
    ws = wb.active
    
    # 填充 Model 列
    filled = 0
    for row in ws.iter_rows(min_row=4):
        sku_cell = row[3]  # SKU 列
        model_cell = row[2]  # Model 列
        
        if sku_cell.value and sku_cell.value in sku_to_model:
            model_cell.value = sku_to_model[sku_cell.value]
            filled += 1
    
    wb.save(excel_path)
    print(f"✅ Excel 已填充：{filled} 行")


def main():
    parser = argparse.ArgumentParser(description='PDF 产品目录提取工具')
    parser.add_argument('--pdf-dir', required=True, help='PDF 文件目录')
    parser.add_argument('--output-dir', required=True, help='输出目录')
    parser.add_argument('--excel-path', help='Excel 文件路径（可选）')
    parser.add_argument('--ocr-threshold', type=int, default=300, help='OCR 触发阈值（默认 300 字符）')
    parser.add_argument('--verbose', action='store_true', help='详细输出模式')
    
    args = parser.parse_args()
    
    # 创建输出目录
    os.makedirs(args.output_dir, exist_ok=True)
    
    print("="*60)
    print("PDF 产品目录提取工具 v1.0")
    print("="*60)
    print(f"\n输入目录：{args.pdf_dir}")
    print(f"输出目录：{args.output_dir}")
    print()
    
    # 获取 PDF 文件列表
    pdf_files = sorted([f for f in os.listdir(args.pdf_dir) if f.endswith('.pdf')])
    print(f"找到 {len(pdf_files)} 个 PDF 文件\n")
    
    # 处理所有 PDF
    all_products = []
    for i, pdf_file in enumerate(pdf_files, 1):
        pdf_path = os.path.join(args.pdf_dir, pdf_file)
        pdf_num = i
        
        product = process_pdf(pdf_path, pdf_num, known_data=KNOWN_MAPPINGS, verbose=args.verbose)
        all_products.append(product)
    
    # 生成输出
    print(f"\n{'='*60}")
    print("生成输出文件...")
    print(f"{'='*60}\n")
    
    # 1. 产品索引 Markdown
    index_path = os.path.join(args.output_dir, '产品索引.md')
    generate_markdown_index(all_products, index_path)
    print(f"✅ 产品索引：{index_path}")
    
    # 2. 产品词条
    generate_product_cards(all_products, args.output_dir)
    print(f"✅ 产品词条：{args.output_dir}/类目词条/")
    
    # 3. JSON 数据
    json_path = os.path.join(args.output_dir, '产品详细数据.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(all_products, f, ensure_ascii=False, indent=2)
    print(f"✅ 详细数据：{json_path}")
    
    # 4. Excel 填充（可选）
    if args.excel_path and os.path.exists(args.excel_path):
        fill_excel(args.excel_path, all_products)
    
    # 统计
    with_model = sum(1 for p in all_products if p['model_no'])
    with_items = sum(1 for p in all_products if p['customer_items'])
    
    print(f"\n{'='*60}")
    print("📊 处理统计")
    print(f"{'='*60}")
    print(f"总 PDF 数：{len(all_products)}")
    print(f"有模具号：{with_model}/{len(all_products)} ({with_model*100//len(all_products)}%)")
    print(f"有客户品名：{with_items}/{len(all_products)} ({with_items*100//len(all_products)}%)")
    print(f"\n✅ 处理完成！")


if __name__ == '__main__':
    main()
