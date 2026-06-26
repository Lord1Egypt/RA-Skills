#!/usr/bin/env python3
"""
轻量版处理静安区的 PDF 文件，分批处理以避免资源限制
"""

import os
import re
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def process_single_pdf(pdf_path: str) -> dict:
    """处理单个 PDF 文件"""
    print(f"处理: {os.path.basename(pdf_path)}")
    
    info = {}
    
    # 检查文件名模式
    basename = os.path.basename(pdf_path)
    match = re.match(r'(.+)_(\d+)\.pdf', basename)
    if match:
        info['项目名称'] = match.group(1)
    
    # 使用简单的 OCR 识别（简化版）
    try:
        import pytesseract
        from pdf2image import convert_from_path
        
        # 只处理前 2 页，减少资源消耗
        print(f"  OCR 识别中...")
        images = convert_from_path(pdf_path, dpi=150, first_page=1, last_page=2)
        text = ""
        for i, image in enumerate(images, 1):
            text += pytesseract.image_to_string(image, lang='chi_sim+eng')
            text += "\n"
        
        print(f"  文本长度: {len(text)} 字符")
        
        # 提取关键信息
        # 项目名称
        match = re.search(r'项目名称[：:]\s*["«《]?([^"»》\n]+)["»》]?', text)
        if match:
            info['项目名称'] = match.group(1).strip()
        
        # 住宅物业费
        match = re.search(r'商品房高层[^物业]*物业费标准\s*(\d+[.,]?\d*)\s*元/平方米', text)
        if match:
            new_fee = float(match.group(1).replace(',', '.'))
            if new_fee > 10:
                new_fee = new_fee / 100
            info['住宅物业费'] = new_fee
        
        # 商业物业费
        match = re.search(r'商业[^物业]*物业费标准\s*(\d+[.,]?\d*)\s*元/平方米', text)
        if match:
            new_fee = float(match.group(1).replace(',', '.'))
            if new_fee > 20:
                new_fee = new_fee / 100
            info['商业物业费'] = new_fee
        
        # 中标日期
        match = re.search(r'(\d{4})年(\d{1,2})月(\d{1,2})日?\s*$', text, re.MULTILINE)
        if match:
            year = match.group(1)
            month = match.group(2).zfill(2)
            day = match.group(3).zfill(2)
            info['中标日期'] = f"{year}-{month}-{day}"
        
        # 合同期限
        match = re.search(r'物业服务合同期限\s*(\d+)\s*年', text)
        if match:
            info['合同期限'] = f"{match.group(1)}年"
        
    except Exception as e:
        info['处理错误'] = str(e)
    
    return info

def is_contract_expiring_in_2026(info: dict) -> bool:
    """判断合同是否在 2026 年内到期"""
    if '中标日期' not in info or '合同期限' not in info:
        return False
    
    try:
        start_date = datetime.strptime(info['中标日期'], '%Y-%m-%d')
        years = int(info['合同期限'].replace('年', ''))
        # 合同开始时间 = 中标公告发布日期后一个月的 1 日
        contract_start = (start_date + relativedelta(months=1)).replace(day=1)
        # 合同结束时间 = 合同开始时间 + 服务年限 - 1 天
        contract_end = contract_start + relativedelta(years=years) - timedelta(days=1)
        
        # 判断是否 2026 年内到期
        target_start = datetime(2026, 1, 1)
        target_end = datetime(2026, 12, 31)
        
        return target_start <= contract_end <= target_end
    except Exception:
        return False

def main():
    print("=" * 60)
    print("轻量版处理静安区的 PDF 文件")
    print("=" * 60)
    print()
    
    # 获取所有静安区的 PDF 文件
    pdf_files = []
    for filename in os.listdir('/tmp'):
        if filename.startswith('静安') and filename.endswith('.pdf'):
            pdf_files.append(os.path.join('/tmp', filename))
    
    print(f"找到 {len(pdf_files)} 个静安区的 PDF 文件")
    print()
    
    # 分批处理，每批 10 个文件
    batch_size = 10
    all_results = []
    expiring_projects = []
    
    for batch in range(0, len(pdf_files), batch_size):
        batch_files = pdf_files[batch:batch + batch_size]
        batch_num = batch // batch_size + 1
        total_batches = (len(pdf_files) + batch_size - 1) // batch_size
        
        print(f"[{batch_num}/{total_batches}] 处理批 {batch_num} ({len(batch_files)} 个文件)")
        print("-" * 40)
        
        batch_results = []
        for pdf_path in batch_files:
            info = process_single_pdf(pdf_path)
            batch_results.append(info)
            
            # 检查是否在 2026 年内到期
            if is_contract_expiring_in_2026(info):
                expiring_projects.append(info)
                print(f"  ✅ 找到 2026 年内到期项目！")
        
        all_results.extend(batch_results)
        print(f"批 {batch_num} 完成，共处理 {len(batch_files)} 个文件")
        print()
    
    # 输出结果汇总
    print("=" * 60)
    print("结果汇总")
    print("=" * 60)
    print()
    
    print(f"总计处理: {len(all_results)} 个文件")
    print(f"明确 2026 年内到期: {len(expiring_projects)} 个项目")
    print()
    
    if expiring_projects:
        print("【2026 年内到期项目】")
        print("-" * 40)
        for i, project in enumerate(expiring_projects, 1):
            print(f"{i}. 项目名称: {project.get('项目名称', '待核实')}")
            print(f"   中标日期: {project.get('中标日期', '待核实')}")
            print(f"   合同期限: {project.get('合同期限', '待核实')}")
            print()
    
    return expiring_projects

if __name__ == '__main__':
    main()