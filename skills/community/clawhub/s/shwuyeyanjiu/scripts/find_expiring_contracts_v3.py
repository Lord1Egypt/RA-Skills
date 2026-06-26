#!/usr/bin/env python3
"""
综合版：基于上海住宅物业公告信息识别 2026 年内合同到期项目
改进点：
1. 同时搜索招标公告和中标公告
2. 综合两个公告的信息
3. 更准确地提取关键信息
"""

import sys
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time

def search_all_announcements(district: str) -> dict:
    """搜索指定区域的所有公告（招标公告、中标公告、评标结果公告）"""
    base_url = 'https://962121.fgj.sh.gov.cn/wyweb/web/front/common/greenmorelist.jsp?id=A000000000000000&twoid=A000B00400000000&thrid=A000B004C0010000'
    
    results = {
        '招标公告': [],
        '中标公告': [],
        '评标结果公告': []
    }
    
    try:
        response = requests.get(base_url, timeout=30)
        response.encoding = 'GBK'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找所有链接
        links = soup.find_all('a')
        for link in links:
            text = link.get_text()
            href = link.get('href', '')
            
            # 筛选包含指定区域的公告
            if district in text:
                match = re.search(r'infoid=(\d+)', href)
                if match:
                    infoid = match.group(1)
                    item = {
                        'title': text.strip(),
                        'infoid': infoid,
                        'pdf_id': str(int(infoid) - 1),
                        'url': f"https://962121.fgj.sh.gov.cn{href}" if href.startswith('/') else href
                    }
                    
                    # 分类
                    if '招标公告' in text and '中标' not in text:
                        results['招标公告'].append(item)
                    elif '中标公告' in text:
                        results['中标公告'].append(item)
                    elif '评标结果' in text:
                        results['评标结果公告'].append(item)
    except Exception as e:
        print(f"搜索失败: {e}")
    
    return results

def match_announcements(bid_announcements: list, tender_announcements: list) -> list:
    """匹配中标公告和招标公告"""
    matched = []
    
    for bid in bid_announcements:
        # 提取项目名称
        project_name = re.search(r'《([^》]+)》', bid['title'])
        if project_name:
            project_name = project_name.group(1)
        else:
            project_name = bid['title']
        
        # 查找对应的招标公告
        matching_tender = None
        for tender in tender_announcements:
            if project_name in tender['title']:
                matching_tender = tender
                break
        
        matched.append({
            '项目名称': project_name,
            '中标公告': bid,
            '招标公告': matching_tender
        })
    
    return matched

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
        print(f"下载失败: {e}")
    
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
        print(f"OCR 识别失败: {e}")
        return ""

def extract_info_from_tender(text: str) -> dict:
    """从招标公告中提取信息"""
    info = {}
    
    # 服务期限
    patterns = [
        r'(?:服务期限|合同期限|物业服务合同期限)[：:]?\s*(\d+)\s*年',
        r'服务期限.*?(\d+)\s*年',
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            info['服务期限'] = f"{match.group(1)}年"
            info['折算服务年限'] = int(match.group(1))
            break
    
    # 如果没有找到，尝试分段服务期限
    if '服务期限' not in info:
        match = re.search(r'服务期限.*?(\d+)\s*\+\s*(\d+)(?:\s*\+\s*(\d+))?', text)
        if match:
            total = int(match.group(1)) + int(match.group(2))
            if match.group(3):
                total += int(match.group(3))
            info['服务期限'] = f"{match.group(0)}"
            info['折算服务年限'] = total
    
    # 收费方式
    if '包干制' in text:
        info['收费方式'] = '包干制'
    elif '酬金制' in text:
        info['收费方式'] = '酬金制'
    
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
    patterns = [
        r'商品房高层[^物业]*物业费标准\s*(\d+[.,]?\d*)\s*元/平方米',
        r'住宅.*?物业费标准\s*(\d+[.,]?\d*)\s*元',
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            new_fee = float(match.group(1).replace(',', '.'))
            if new_fee > 10:
                new_fee = new_fee / 100
            if '住宅物业费' not in info or new_fee > info.get('住宅物业费', 0):
                info['住宅物业费'] = new_fee
                break
    
    # 商业物业费
    patterns = [
        r'商业[^物业]*物业费标准\s*(\d+[.,]?\d*)\s*元/平方米',
        r'商业.*?物业费\s*(\d+[.,]?\d*)\s*元',
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            new_fee = float(match.group(1).replace(',', '.'))
            if new_fee > 20:
                new_fee = new_fee / 100
            info['商业物业费'] = new_fee
            break
    
    # 地下停车位
    match = re.search(r'地下停车位\s*(\d+)\s*个', text)
    if match:
        info['地下停车位'] = int(match.group(1))
    
    # 容积率
    match = re.search(r'容积率\s*(\d+[.,]?\d*)', text)
    if match:
        info['容积率'] = float(match.group(1).replace(',', '.'))
    
    return info

def extract_info_from_bid(text: str) -> dict:
    """从中标公告中提取信息"""
    info = {}
    
    # 项目名称
    patterns = [
        r'项目名称[：:]\s*["«《]?([^"»》\n]+)["»》]?',
        r'《([^》]+)》',
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            info['项目名称'] = match.group(1).strip()
            break
    
    # 招标人
    match = re.search(r'招标人[：:]\s*([^\n]+)', text)
    if match:
        info['招标人'] = match.group(1).strip()
    
    # 中标企业
    patterns = [
        r'(?:中标企业|中标单位)[：:]\s*([^\n]+)',
        r'中标人[：:]\s*([^\n]+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            info['中标企业'] = match.group(1).strip()
            break
    
    # 中标日期
    patterns = [
        r'(\d{4})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日',
        r'(\d{4})[年\-./](\d{1,2})[月\-./](\d{1,2})',
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            year = match.group(1)
            month = match.group(2).zfill(2)
            day = match.group(3).zfill(2)
            info['中标日期'] = f"{year}-{month}-{day}"
            break
    
    return info

def merge_info(tender_info: dict, bid_info: dict) -> dict:
    """合并招标公告和中标公告的信息"""
    merged = {}
    
    # 优先使用中标公告的信息
    for key, value in bid_info.items():
        merged[key] = value
    
    # 补充招标公告的信息
    for key, value in tender_info.items():
        if key not in merged:
            merged[key] = value
    
    return merged

def calculate_contract_dates(info: dict) -> dict:
    """计算合同开始和结束时间"""
    result = {}
    
    if '中标日期' in info and '折算服务年限' in info:
        try:
            bid_date = datetime.strptime(info['中标日期'], '%Y-%m-%d')
            contract_start = (bid_date + relativedelta(months=1)).replace(day=1)
            result['合同开始时间'] = contract_start.strftime('%Y-%m-%d')
            
            contract_end = contract_start + relativedelta(years=info['折算服务年限']) - timedelta(days=1)
            result['合同结束时间'] = contract_end.strftime('%Y-%m-%d')
            
            target_start = datetime(2026, 1, 1)
            target_end = datetime(2026, 12, 31)
            
            if target_start <= contract_end <= target_end:
                result['是否2026年内到期'] = '是'
                result['到期类型'] = '明确2026年内到期'
            elif contract_end < target_start:
                result['是否2026年内到期'] = '否（已过期）'
                result['到期类型'] = '已过期'
            else:
                result['是否2026年内到期'] = '否'
                result['到期类型'] = '未到期'
            
            result['判断依据'] = f"中标公告日期为 {info['中标日期']}，按次月 1 日起算，{info['折算服务年限']} 年期至 {result['合同结束时间']} 到期"
            
        except Exception as e:
            result['判断依据'] = f"计算失败: {e}"
    else:
        result['判断依据'] = '缺少中标日期或服务期限'
    
    return result

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
    print("综合版：基于上海住宅物业公告信息识别 2026 年内合同到期项目")
    print("任务：识别静安区 2026 年内合同到期的项目")
    print("=" * 80)
    print()
    
    district = "静安区"
    print(f"正在搜索 {district} 的所有公告...\n")
    
    # 搜索所有公告
    all_announcements = search_all_announcements(district)
    
    print(f"找到:")
    print(f"  - 招标公告: {len(all_announcements['招标公告'])} 个")
    print(f"  - 中标公告: {len(all_announcements['中标公告'])} 个")
    print(f"  - 评标结果公告: {len(all_announcements['评标结果公告'])} 个")
    print()
    
    # 匹配中标公告和招标公告
    matched = match_announcements(all_announcements['中标公告'], all_announcements['招标公告'])
    
    print(f"匹配到 {len(matched)} 个项目\n")
    
    # 处理每个项目
    all_projects = []
    
    for i, item in enumerate(matched, 1):
        print(f"[{i}/{len(matched)}] 正在处理: {item['项目名称']}")
        
        # 下载并识别中标公告
        bid_pdf_path = f"/tmp/bid_{item['中标公告']['pdf_id']}.pdf"
        bid_text = ""
        if download_pdf(item['中标公告']['pdf_id'], bid_pdf_path):
            bid_text = ocr_pdf(bid_pdf_path)
        
        # 下载并识别招标公告
        tender_text = ""
        if item['招标公告']:
            tender_pdf_path = f"/tmp/tender_{item['招标公告']['pdf_id']}.pdf"
            if download_pdf(item['招标公告']['pdf_id'], tender_pdf_path):
                tender_text = ocr_pdf(tender_pdf_path)
        
        # 提取信息
        bid_info = extract_info_from_bid(bid_text)
        tender_info = extract_info_from_tender(tender_text)
        
        # 合并信息
        merged_info = merge_info(tender_info, bid_info)
        merged_info['项目名称'] = item['项目名称']
        
        # 计算合同时间
        contract_dates = calculate_contract_dates(merged_info)
        
        # 计算饱和收入
        revenue = calculate_saturation_revenue(merged_info)
        
        # 合并所有信息
        project = {
            '区域': district,
            '项目名称': merged_info.get('项目名称', '待核实'),
            '招标人': merged_info.get('招标人', '待核实'),
            '中标人': merged_info.get('中标企业', '待核实'),
            '中标公告日期': merged_info.get('中标日期', '待核实'),
            '服务期限': merged_info.get('服务期限', '待核实'),
            '折算服务年限': merged_info.get('折算服务年限', '待核实'),
            '收费方式': merged_info.get('收费方式', '待核实'),
            '物业费标准': merged_info.get('住宅物业费', '待核实'),
            '合同开始时间': contract_dates.get('合同开始时间', '待核实'),
            '合同结束时间': contract_dates.get('合同结束时间', '待核实'),
            '是否2026年内到期': contract_dates.get('是否2026年内到期', '待核实'),
            '到期类型': contract_dates.get('到期类型', '待核实'),
            '判断依据': contract_dates.get('判断依据', '待核实'),
            '可收费面积': merged_info.get('总建筑面积', '待核实'),
            '月度饱和收入': revenue.get('月度饱和收入', '待核实'),
            '年度饱和收入': revenue.get('年度饱和收入', '待核实'),
        }
        
        all_projects.append(project)
        
        # 如果找到 2026 年内到期的项目，立即输出
        if project['是否2026年内到期'] == '是':
            print(f"  ✅ 找到 2026 年内到期项目！")
            print(f"     合同结束时间: {project['合同结束时间']}")
        
        print()
    
    # 输出结果汇总
    print("=" * 80)
    print("搜索结果汇总")
    print("=" * 80)
    print()
    
    clear_projects = [p for p in all_projects if p['到期类型'] == '明确2026年内到期']
    suspected_projects = [p for p in all_projects if '疑似' in p.get('到期类型', '')]
    unknown_projects = [p for p in all_projects if '待核实' in p.get('判断依据', '') or '缺少' in p.get('判断依据', '')]
    
    print(f"总计: {len(all_projects)} 个项目")
    print(f"  - 明确 2026 年内到期: {len(clear_projects)} 个")
    print(f"  - 疑似 2026 年内到期: {len(suspected_projects)} 个")
    print(f"  - 信息不足: {len(unknown_projects)} 个")
    print()
    
    if clear_projects:
        print("【第一部分：明确属于 2026 年内到期项目】")
        print("-" * 80)
        for p in clear_projects:
            print(f"项目名称: {p['项目名称']}")
            print(f"中标人: {p['中标人']}")
            print(f"合同结束时间: {p['合同结束时间']}")
            print(f"年度饱和收入: {p['年度饱和收入']}")
            print(f"判断依据: {p['判断依据']}")
            print()

if __name__ == '__main__':
    main()
