#!/usr/bin/env python3
"""
批量提取静安区项目的合同到期时间
"""

import sys
import re
import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
import csv

def search_district_projects(district: str) -> dict:
    """搜索指定区域的所有项目"""
    url = 'https://962121.fgj.sh.gov.cn/wyweb/web/front/common/greenmorelist.jsp?id=A000000000000000&twoid=A000B00400000000&thrid=A000B004C0010000'
    
    response = requests.get(url, timeout=30)
    response.encoding = 'GBK'
    soup = BeautifulSoup(response.text, 'html.parser')
    
    projects = {}
    
    links = soup.find_all('a')
    for link in links:
        text = link.get_text()
        if district in text:
            href = link.get('href', '')
            match = re.search(r'infoid=(\d+)', href)
            if match:
                infoid = match.group(1)
                pdf_id = str(int(infoid) - 1)
                
                # 提取项目名称
                name_match = re.search(r'《([^》]+)》', text)
                if name_match:
                    project_name = name_match.group(1)
                else:
                    continue
                
                if project_name not in projects:
                    projects[project_name] = {
                        '招标公告': [],
                        '中标公告': []
                    }
                
                # 判断公告类型
                if '招标公告' in text and '中标' not in text:
                    projects[project_name]['招标公告'].append({
                        'title': text.strip(),
                        'infoid': infoid,
                        'pdf_id': pdf_id
                    })
                elif '中标公告' in text:
                    projects[project_name]['中标公告'].append({
                        'title': text.strip(),
                        'infoid': infoid,
                        'pdf_id': pdf_id
                    })
    
    return projects

def download_pdf(pdf_id: str, output_path: str) -> bool:
    """下载 PDF 文件"""
    url = f"https://962121.fgj.sh.gov.cn/wyweb//web/UploadFiles/pdf/{pdf_id}.pdf"
    
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.content)
            return True
    except Exception as e:
        print(f"    下载失败: {e}")
    
    return False

def ocr_pdf(pdf_path: str) -> str:
    """OCR 识别 PDF 文件"""
    try:
        from pdf2image import convert_from_path
        import pytesseract
        
        images = convert_from_path(pdf_path, dpi=200)
        text = ""
        for image in images:
            text += pytesseract.image_to_string(image, lang='chi_sim+eng')
            text += "\n"
        
        return text
    except Exception as e:
        print(f"    OCR 识别失败: {e}")
        return ""

def extract_contract_period(text: str) -> int:
    """从文本中提取合同期限（年）"""
    patterns = [
        r'物业服务合同期限[：:]?\s*(\d+)\s*年',
        r'合同期限[：:]?\s*(\d+)\s*年',
        r'服务期限[：:]?\s*(\d+)\s*年',
        r'合同期[：:]?\s*(\d+)\s*年',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return int(match.group(1))
    
    # 尝试分段服务期限
    match = re.search(r'服务期限.*?(\d+)\s*\+\s*(\d+)(?:\s*\+\s*(\d+))?', text)
    if match:
        total = int(match.group(1)) + int(match.group(2))
        if match.group(3):
            total += int(match.group(3))
        return total
    
    # 尝试匹配"五、投标条件"和"七、申请投标的地点"之间的单独"X年"
    match = re.search(r'五、投标条件.*?(\d+)\s*年.*?七、申请投标的地点', text, re.DOTALL)
    if match:
        return int(match.group(1))
    
    return 0

def extract_bidding_date(text: str) -> str:
    """从文本中提取中标日期"""
    patterns = [
        # 匹配文件末尾的日期（最常见）
        r'(\d{4})年(\d{1,2})月(\d{1,2})日?\s*$',
        # 匹配"发布日期：XXXX年XX月XX日"
        r'发布日期[：:]?\s*(\d{4})年(\d{1,2})月(\d{1,2})日',
        # 匹配"XXXX年XX月XX日"（任意位置）
        r'(\d{4})年(\d{1,2})月(\d{1,2})日',
        # 匹配"XXXX-XX-XX"格式
        r'(\d{4})[.-](\d{1,2})[.-](\d{1,2})',
        # 匹配"XX月XX日"格式（假设当前年份）
        r'(\d{1,2})月(\d{1,2})日',
    ]
    
    # 优先尝试从文件末尾提取（通常是发布日期）
    for pattern in patterns[:3]:
        matches = re.findall(pattern, text, re.MULTILINE)
        if matches:
            year, month, day = matches[-1]
            # 如果是"XX月XX日"格式，假设是当前年份
            if len(year) == 2:
                year = "2026"
            return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
    
    # 如果前面都没找到，尝试其他格式
    for pattern in patterns[3:]:
        matches = re.findall(pattern, text, re.MULTILINE)
        if matches:
            year, month, day = matches[-1]
            # 如果是"XX月XX日"格式，假设是当前年份
            if len(year) == 2:
                year = "2026"
            return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
    
    return ""

def calculate_contract_expiry(bidding_date: str, contract_period: int) -> str:
    """计算合同到期时间"""
    if not bidding_date or contract_period == 0:
        return ""
    
    try:
        year, month, day = map(int, bidding_date.split('-'))
        start_date = datetime(year, month, 1) + relativedelta(months=1)
        end_date = start_date + relativedelta(years=contract_period) - relativedelta(days=1)
        return end_date.strftime('%Y-%m-%d')
    except Exception as e:
        return ""

def process_projects(district: str, output_csv: str):
    """批量处理项目"""
    print(f"搜索 {district} 的所有项目...")
    projects = search_district_projects(district)
    print(f"找到 {len(projects)} 个项目")
    
    results = []
    
    for i, (project_name, announcements) in enumerate(projects.items()):
        print(f"\n[{i+1}/{len(projects)}] 处理: {project_name}")
        
        result = {
            '项目名称': project_name,
            '合同期限': 0,
            '中标日期': '',
            '合同到期时间': '',
            '备注': ''
        }
        
        # 处理招标公告（提取合同期限）
        if announcements['招标公告']:
            ann = announcements['招标公告'][0]  # 只处理最新的一个
            pdf_path = f"/tmp/{project_name}_招标_{ann['pdf_id']}.pdf"
            print(f"  下载招标公告: {ann['title']}")
            
            if download_pdf(ann['pdf_id'], pdf_path):
                print(f"  OCR 识别中...")
                text = ocr_pdf(pdf_path)
                if text:
                    contract_period = extract_contract_period(text)
                    if contract_period > 0:
                        result['合同期限'] = contract_period
                        print(f"    合同期限: {contract_period} 年")
                else:
                    result['备注'] = '招标公告 OCR 识别失败'
            else:
                result['备注'] = '招标公告 PDF 下载失败'
        else:
            result['备注'] = '未找到招标公告'
        
        # 处理中标公告（提取中标日期）
        if announcements['中标公告']:
            ann = announcements['中标公告'][0]  # 只处理最新的一个
            pdf_path = f"/tmp/{project_name}_中标_{ann['pdf_id']}.pdf"
            print(f"  下载中标公告: {ann['title']}")
            
            if download_pdf(ann['pdf_id'], pdf_path):
                print(f"  OCR 识别中...")
                text = ocr_pdf(pdf_path)
                if text:
                    bidding_date = extract_bidding_date(text)
                    if bidding_date:
                        result['中标日期'] = bidding_date
                        print(f"    中标日期: {bidding_date}")
            else:
                if result['备注']:
                    result['备注'] += '; 中标公告 PDF 下载失败'
                else:
                    result['备注'] = '中标公告 PDF 下载失败'
        
        # 计算合同到期时间
        if result['合同期限'] > 0 and result['中标日期']:
            result['合同到期时间'] = calculate_contract_expiry(result['中标日期'], result['合同期限'])
            print(f"  合同到期时间: {result['合同到期时间']}")
        
        results.append(result)
    
    # 保存结果到 CSV
    with open(output_csv, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=['项目名称', '合同期限', '中标日期', '合同到期时间', '备注'])
        writer.writeheader()
        writer.writerows(results)
    
    print(f"\n结果已保存到: {output_csv}")
    
    # 统计 2026 年内到期的项目
    expiring_2026 = [r for r in results if r['合同到期时间'].startswith('2026')]
    print(f"\n2026 年内到期项目: {len(expiring_2026)} 个")
    for r in expiring_2026:
        print(f"  - {r['项目名称']}: {r['合同到期时间']}")

def main():
    """主函数"""
    district = '静安区'
    output_csv = '/Users/yujunwang/.openclaw/workspace/jingan_contract_dates.csv'
    
    process_projects(district, output_csv)

if __name__ == '__main__':
    main()
