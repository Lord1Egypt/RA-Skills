#!/usr/bin/env python3
"""
处理静安区的 PDF 文件，提取关键信息并判断是否 2026 年内到期
"""

import os
import re
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def ocr_pdf(pdf_path: str) -> str:
    """OCR 识别 PDF 文件"""
    try:
        from pdf2image import convert_from_path
        import pytesseract
        
        print(f"  正在 OCR 识别: {os.path.basename(pdf_path)}")
        images = convert_from_path(pdf_path, dpi=200)
        text = ""
        for i, image in enumerate(images, 1):
            print(f"    处理第 {i}/{len(images)} 页...")
            text += pytesseract.image_to_string(image, lang='chi_sim+eng')
            text += "\n"
        
        return text
    except Exception as e:
        print(f"  OCR 识别失败: {e}")
        return ""

def extract_info(text: str) -> dict:
    """从 OCR 文本中提取关键信息"""
    info = {}
    
    # 项目名称
    match = re.search(r'项目名称[：:]\s*["«《]?([^"»》\n]+)["»》]?', text)
    if match:
        info['项目名称'] = match.group(1).strip()
    
    # 总建筑面积
    match = re.search(r'总建筑面积\s*(\d+[.,]?\d*)\s*平方米', text)
    if match:
        info['总建筑面积'] = float(match.group(1).replace(',', '.'))
    
    # 住宅建筑面积
    match = re.search(r'住宅建筑面积\s*(\d+[.,]?\d*)\s*平方米', text)
    if match:
        info['住宅建筑面积'] = float(match.group(1).replace(',', '.'))
    
    # 非住宅建筑面积
    match = re.search(r'非住宅建筑面积\s*(\d+[.,]?\d*)\s*平方米', text)
    if match:
        info['非住宅建筑面积'] = float(match.group(1).replace(',', '.'))
    else:
        match = re.search(r'非住宅建筑面积\s*(\d+[.,]?\d*)\s*\n\s*(\d+[.,]?\d*)\s*平方米', text)
        if match:
            num1 = match.group(1).replace(',', '.')
            num2 = match.group(2).replace(',', '.')
            if '.' in num1:
                info['非住宅建筑面积'] = float(num1)
            else:
                info['非住宅建筑面积'] = float(num1 + num2)
    
    # 住宅物业费
    match = re.search(r'商品房高层[^物业]*物业费标准\s*(\d+[.,]?\d*)\s*元/平方米', text)
    if match:
        new_fee = float(match.group(1).replace(',', '.'))
        if new_fee > 10:
            new_fee = new_fee / 100
        if '住宅物业费' not in info or new_fee > info.get('住宅物业费', 0):
            info['住宅物业费'] = new_fee
    
    # 商业物业费
    match = re.search(r'商业[^物业]*物业费标准\s*(\d+[.,]?\d*)\s*元/平方米', text)
    if match:
        new_fee = float(match.group(1).replace(',', '.'))
        if new_fee > 20:
            new_fee = new_fee / 100
        info['商业物业费'] = new_fee
    
    # 地下停车位
    match = re.search(r'地下停车位\s*(\d+)\s*个', text)
    if match:
        info['地下停车位'] = int(match.group(1))
    
    # 中标企业
    match = re.search(r'(?:中标企业|评标结果排序)[：:]\s*([^\n]+)', text)
    if match:
        info['中标企业'] = match.group(1).strip()
    
    # 招标人
    match = re.search(r'招标人[：:]\s*([^\n]+)', text)
    if match:
        info['招标人'] = match.group(1).strip()
    
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
    
    return info

def calculate_saturation_revenue(info: dict, parking_fee: float = 100.0) -> dict:
    """计算饱和收入"""
    result = {}
    
    residential_revenue = 0
    commercial_revenue = 0
    parking_revenue = 0
    
    if '住宅建筑面积' in info and '住宅物业费' in info:
        residential_revenue = info['住宅建筑面积'] * info['住宅物业费']
        result['住宅物业费收入'] = residential_revenue
    
    if '非住宅建筑面积' in info and '商业物业费' in info:
        commercial_revenue = info['非住宅建筑面积'] * info['商业物业费']
        result['商业物业费收入'] = commercial_revenue
    
    if '地下停车位' in info:
        parking_revenue = info['地下停车位'] * parking_fee
        result['停车管理费收入'] = parking_revenue
    
    total_monthly = residential_revenue + commercial_revenue + parking_revenue
    result['月度饱和收入'] = total_monthly
    result['年度饱和收入'] = total_monthly * 12
    
    return result

def main():
    print("=" * 80)
    print("处理静安区的 PDF 文件")
    print("=" * 80)
    print()
    
    # 获取所有静安区的 PDF 文件
    pdf_files = []
    for filename in os.listdir('/tmp'):
        if filename.startswith('静安') and filename.endswith('.pdf'):
            pdf_files.append(os.path.join('/tmp', filename))
    
    print(f"找到 {len(pdf_files)} 个静安区的 PDF 文件")
    print()
    
    # 按项目名称分组
    projects = {}
    for pdf_path in pdf_files:
        # 提取项目名称
        basename = os.path.basename(pdf_path)
        match = re.match(r'(.+)_(\d+)\.pdf', basename)
        if match:
            project_name = match.group(1)
            if project_name not in projects:
                projects[project_name] = []
            projects[project_name].append(pdf_path)
    
    print(f"涉及 {len(projects)} 个项目")
    print()
    
    # 处理每个项目
    all_results = []
    
    for i, (project_name, pdf_paths) in enumerate(projects.items(), 1):
        print(f"[{i}/{len(projects)}] 正在处理: {project_name}")
        
        # 处理该项目的所有 PDF 文件
        all_info = {}
        for pdf_path in pdf_paths:
            text = ocr_pdf(pdf_path)
            if text:
                info = extract_info(text)
                # 智能合并：住宅物业费取最大值，其他字段直接覆盖
                for key, value in info.items():
                    if key == '住宅物业费':
                        if key not in all_info or value > all_info.get(key, 0):
                            all_info[key] = value
                    else:
                        all_info[key] = value
        
        # 计算合同到期时间
        if '中标日期' in all_info and '合同期限' in all_info:
            try:
                start_date = datetime.strptime(all_info['中标日期'], '%Y-%m-%d')
                years = int(all_info['合同期限'].replace('年', ''))
                # 合同开始时间 = 中标公告发布日期后一个月的 1 日
                contract_start = (start_date + relativedelta(months=1)).replace(day=1)
                # 合同结束时间 = 合同开始时间 + 服务年限 - 1 天
                contract_end = contract_start + relativedelta(years=years) - timedelta(days=1)
                
                all_info['合同开始时间'] = contract_start.strftime('%Y-%m-%d')
                all_info['合同结束时间'] = contract_end.strftime('%Y-%m-%d')
                
                # 判断是否 2026 年内到期
                target_start = datetime(2026, 1, 1)
                target_end = datetime(2026, 12, 31)
                
                if target_start <= contract_end <= target_end:
                    all_info['是否2026年内到期'] = '是'
                    all_info['到期类型'] = '明确2026年内到期'
                    print(f"  ✅ 找到 2026 年内到期项目！合同结束时间: {all_info['合同结束时间']}")
                elif contract_end < target_start:
                    all_info['是否2026年内到期'] = '否（已过期）'
                    all_info['到期类型'] = '已过期'
                else:
                    all_info['是否2026年内到期'] = '否'
                    all_info['到期类型'] = '未到期'
            except Exception as e:
                all_info['判断依据'] = f"计算失败: {e}"
        else:
            all_info['判断依据'] = '缺少中标日期或合同期限'
        
        # 计算饱和收入
        revenue = calculate_saturation_revenue(all_info)
        all_info['年度饱和收入'] = revenue.get('年度饱和收入', '待核实')
        
        all_results.append(all_info)
        print()
    
    # 输出结果汇总
    print("=" * 80)
    print("搜索结果汇总")
    print("=" * 80)
    print()
    
    clear_projects = [p for p in all_results if p.get('到期类型') == '明确2026年内到期']
    unknown_projects = [p for p in all_results if '判断依据' in p]
    
    print(f"总计: {len(all_results)} 个项目")
    print(f"  - 明确 2026 年内到期: {len(clear_projects)} 个")
    print(f"  - 信息不足: {len(unknown_projects)} 个")
    print()
    
    if clear_projects:
        print("【第一部分：明确属于 2026 年内到期项目】")
        print("-" * 80)
        for p in clear_projects:
            print(f"项目名称: {p.get('项目名称', '待核实')}")
            print(f"中标人: {p.get('中标企业', '待核实')}")
            print(f"合同结束时间: {p.get('合同结束时间', '待核实')}")
            if isinstance(p.get('年度饱和收入'), (int, float)):
                print(f"年度饱和收入: {p.get('年度饱和收入'):,.2f} 元/年")
            else:
                print(f"年度饱和收入: {p.get('年度饱和收入', '待核实')}")
            print()

if __name__ == '__main__':
    main()
