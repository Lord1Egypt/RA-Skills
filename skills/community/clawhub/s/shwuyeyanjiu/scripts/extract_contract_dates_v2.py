#!/usr/bin/env python3
"""
提取合同到期时间 - 改进版
策略：同时下载招标公告和中标公告的 PDF，使用 OCR 提取合同期限和中标日期
"""

import sys
import re
import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta

def search_project_announcements(project_name: str) -> dict:
    """搜索项目的所有公告（招标公告、中标公告）"""
    url = 'https://962121.fgj.sh.gov.cn/wyweb/web/front/common/greenmorelist.jsp?id=A000000000000000&twoid=A000B00400000000&thrid=A000B004C0010000'
    
    response = requests.get(url, timeout=30)
    response.encoding = 'GBK'
    soup = BeautifulSoup(response.text, 'html.parser')
    
    announcements = {
        '招标公告': [],
        '中标公告': []
    }
    
    links = soup.find_all('a')
    for link in links:
        text = link.get_text()
        if project_name in text:
            href = link.get('href', '')
            match = re.search(r'infoid=(\d+)', href)
            if match:
                infoid = match.group(1)
                pdf_id = str(int(infoid) - 1)
                
                # 判断公告类型
                if '招标公告' in text and '中标' not in text:
                    announcements['招标公告'].append({
                        'title': text.strip(),
                        'infoid': infoid,
                        'pdf_id': pdf_id
                    })
                elif '中标公告' in text:
                    announcements['中标公告'].append({
                        'title': text.strip(),
                        'infoid': infoid,
                        'pdf_id': pdf_id
                    })
    
    return announcements

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
        print(f"  下载失败: {e}")
    
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
        print(f"  OCR 识别失败: {e}")
        return ""

def extract_contract_period(text: str) -> int:
    """从文本中提取合同期限（年）"""
    # 尝试多种格式
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
    
    # 尝试分段服务期限（1+1+1, 1+2, 2+1）
    match = re.search(r'服务期限.*?(\d+)\s*\+\s*(\d+)(?:\s*\+\s*(\d+))?', text)
    if match:
        total = int(match.group(1)) + int(match.group(2))
        if match.group(3):
            total += int(match.group(3))
        return total
    
    # 尝试匹配"五、投标条件"和"七、申请投标的地点"之间的单独"X年"
    # 这是针对 OCR 识别漏掉标题的情况
    match = re.search(r'五、投标条件.*?(\d+)\s*年.*?七、申请投标的地点', text, re.DOTALL)
    if match:
        return int(match.group(1))
    
    return 0

def extract_bidding_date(text: str) -> str:
    """从文本中提取中标日期"""
    # 查找公告底部的日期
    patterns = [
        r'(\d{4})年(\d{1,2})月(\d{1,2})日?\s*$',
        r'发布日期[：:]?\s*(\d{4})年(\d{1,2})月(\d{1,2})日',
        r'(\d{4})[.-](\d{1,2})[.-](\d{1,2})',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.MULTILINE)
        if matches:
            # 取最后一个日期（通常是公告发布日期）
            year, month, day = matches[-1]
            return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
    
    return ""

def calculate_contract_expiry(bidding_date: str, contract_period: int) -> str:
    """计算合同到期时间"""
    if not bidding_date or contract_period == 0:
        return ""
    
    try:
        # 解析中标日期
        year, month, day = map(int, bidding_date.split('-'))
        
        # 合同开始时间通常是中标日期后一个月的1日
        start_date = datetime(year, month, 1) + relativedelta(months=1)
        
        # 合同结束时间 = 合同开始时间 + 合同期限
        end_date = start_date + relativedelta(years=contract_period) - relativedelta(days=1)
        
        return end_date.strftime('%Y-%m-%d')
    except Exception as e:
        print(f"  计算失败: {e}")
        return ""

def process_project(project_name: str, output_dir: str = '/tmp') -> dict:
    """处理单个项目"""
    print(f"\n正在处理: {project_name}")
    
    # 搜索公告
    announcements = search_project_announcements(project_name)
    
    if not announcements['招标公告'] and not announcements['中标公告']:
        print(f"  未找到公告")
        return {}
    
    print(f"  找到 {len(announcements['招标公告'])} 个招标公告, {len(announcements['中标公告'])} 个中标公告")
    
    result = {
        '项目名称': project_name,
        '合同期限': 0,
        '中标日期': '',
        '合同到期时间': ''
    }
    
    # 下载并处理招标公告（提取合同期限）
    for ann in announcements['招标公告'][:1]:  # 只处理最新的一个
        pdf_path = f"{output_dir}/{project_name}_招标_{ann['pdf_id']}.pdf"
        print(f"  下载招标公告: {ann['title']}")
        
        if download_pdf(ann['pdf_id'], pdf_path):
            print(f"  OCR 识别中...")
            text = ocr_pdf(pdf_path)
            if text:
                contract_period = extract_contract_period(text)
                if contract_period > 0:
                    result['合同期限'] = contract_period
                    print(f"    合同期限: {contract_period} 年")
    
    # 下载并处理中标公告（提取中标日期）
    for ann in announcements['中标公告'][:1]:  # 只处理最新的一个
        pdf_path = f"{output_dir}/{project_name}_中标_{ann['pdf_id']}.pdf"
        print(f"  下载中标公告: {ann['title']}")
        
        if download_pdf(ann['pdf_id'], pdf_path):
            print(f"  OCR 识别中...")
            text = ocr_pdf(pdf_path)
            if text:
                bidding_date = extract_bidding_date(text)
                if bidding_date:
                    result['中标日期'] = bidding_date
                    print(f"    中标日期: {bidding_date}")
    
    # 计算合同到期时间
    if result['合同期限'] > 0 and result['中标日期']:
        result['合同到期时间'] = calculate_contract_expiry(result['中标日期'], result['合同期限'])
        print(f"  合同到期时间: {result['合同到期时间']}")
    
    return result

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python extract_contract_dates_v2.py <项目名称>")
        sys.exit(1)
    
    project_name = sys.argv[1]
    result = process_project(project_name)
    
    if result:
        print("\n" + "="*60)
        print(f"项目名称: {result['项目名称']}")
        print(f"合同期限: {result['合同期限']} 年")
        print(f"中标日期: {result['中标日期']}")
        print(f"合同到期时间: {result['合同到期时间']}")
        print("="*60)

if __name__ == '__main__':
    main()
