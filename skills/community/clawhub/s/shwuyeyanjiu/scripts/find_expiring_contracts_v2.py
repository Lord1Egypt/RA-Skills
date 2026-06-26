#!/usr/bin/env python3
"""
改进版：基于上海住宅物业公告信息识别 2026 年内合同到期项目
改进点：
1. 更准确的中标日期提取
2. 更准确的服务期限提取
3. 更好的 OCR 错误处理
"""

import sys
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time

def search_projects_by_district(district: str, max_pages: int = 10) -> list:
    """搜索指定区域的公告"""
    base_url = 'https://962121.fgj.sh.gov.cn/wyweb/web/front/common/greenmorelist.jsp?id=A000000000000000&twoid=A000B00400000000&thrid=A000B004C0010000'
    
    all_results = []
    
    try:
        response = requests.get(base_url, timeout=30)
        response.encoding = 'GBK'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找所有链接
        links = soup.find_all('a')
        for link in links:
            text = link.get_text()
            # 筛选包含指定区域的公告
            if district in text and '中标公告' in text:
                href = link.get('href', '')
                match = re.search(r'infoid=(\d+)', href)
                if match:
                    infoid = match.group(1)
                    all_results.append({
                        'title': text.strip(),
                        'infoid': infoid,
                        'pdf_id': str(int(infoid) - 1),
                        'url': f"https://962121.fgj.sh.gov.cn{href}" if href.startswith('/') else href
                    })
    except Exception as e:
        print(f"搜索失败: {e}")
    
    return all_results

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
        for i, image in enumerate(images):
            text += pytesseract.image_to_string(image, lang='chi_sim+eng')
            text += "\n"
        
        return text
    except Exception as e:
        print(f"OCR 识别失败: {e}")
        return ""

def extract_contract_info_improved(text: str) -> dict:
    """改进版：从 OCR 文本中提取合同关键信息"""
    info = {}
    
    # 项目名称 - 改进匹配
    patterns = [
        r'项目名称[：:]\s*["«《]?([^"»》\n]+)["»》]?',
        r'《([^》]+)》',
        r'["「]([^"」\n]+)["」]',
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
    
    # 中标企业 - 改进匹配
    patterns = [
        r'(?:中标企业|中标单位)[：:]\s*([^\n]+)',
        r'中标人[：:]\s*([^\n]+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            info['中标企业'] = match.group(1).strip()
            break
    
    # 中标日期 - 改进匹配，更灵活的格式
    patterns = [
        r'(\d{4})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日',  # 2026年01月22日
        r'(\d{4})[年\-./](\d{1,2})[月\-./](\d{1,2})',  # 2026-01-22 或 2026.01.22
        r'(\d{4})\s*年\s*(\d{1,2})\s*月',  # 2026年01月（缺少日）
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            year = match.group(1)
            month = match.group(2).zfill(2)
            if len(match.groups()) >= 3:
                day = match.group(3).zfill(2)
            else:
                day = '01'  # 默认为 1 日
            info['中标日期'] = f"{year}-{month}-{day}"
            break
    
    # 服务期限 - 改进匹配
    patterns = [
        r'(?:服务期限|合同期限|物业服务合同期限)[：:]?\s*(\d+)\s*年',
        r'服务期限.*?(\d+)\s*年',
        r'合同期限.*?(\d+)\s*年',
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            info['服务期限'] = f"{match.group(1)}年"
            info['折算服务年限'] = int(match.group(1))
            break
    
    # 如果没有找到服务期限，尝试分段服务期限
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
    
    # 非住宅建筑面积 - 改进跨行匹配
    match = re.search(r'非住宅建筑面积\s*(\d+[.,]?\d*)\s*平方米', text)
    if match:
        info['非住宅建筑面积'] = float(match.group(1).replace(',', '.'))
    else:
        # 跨行匹配
        match = re.search(r'非住宅建筑面积\s*(\d+[.,]?\d*)\s*\n\s*(\d+[.,]?\d*)\s*平方米', text)
        if match:
            num1 = match.group(1).replace(',', '.')
            num2 = match.group(2).replace(',', '.')
            if '.' in num1:
                info['非住宅建筑面积'] = float(num1)
            else:
                info['非住宅建筑面积'] = float(num1 + num2)
    
    # 住宅物业费 - 改进匹配
    patterns = [
        r'商品房高层[^物业]*物业费标准\s*(\d+[.,]?\d*)\s*元/平方米',
        r'住宅.*?物业费标准\s*(\d+[.,]?\d*)\s*元',
        r'高层.*?物业费\s*(\d+[.,]?\d*)\s*元',
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            new_fee = float(match.group(1).replace(',', '.'))
            # OCR 错误修正
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
            # OCR 错误修正
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

def calculate_contract_dates(info: dict) -> dict:
    """计算合同开始和结束时间"""
    result = {}
    
    # 如果有中标日期和服务期限，计算合同时间
    if '中标日期' in info and '折算服务年限' in info:
        try:
            # 合同开始时间 = 中标公告发布日期后一个月的 1 日
            bid_date = datetime.strptime(info['中标日期'], '%Y-%m-%d')
            contract_start = (bid_date + relativedelta(months=1)).replace(day=1)
            result['合同开始时间'] = contract_start.strftime('%Y-%m-%d')
            
            # 合同结束时间 = 合同开始时间 + 服务年限 - 1 天
            contract_end = contract_start + relativedelta(years=info['折算服务年限']) - timedelta(days=1)
            result['合同结束时间'] = contract_end.strftime('%Y-%m-%d')
            
            # 判断是否属于 2026 年内到期
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
            
            # 判断依据
            result['判断依据'] = f"中标公告日期为 {info['中标日期']}，公告未明示合同起止时间，按次月 1 日起算，{info['折算服务年限']} 年期至 {result['合同结束时间']} 到期"
            
        except Exception as e:
            result['合同开始时间'] = '待核实'
            result['合同结束时间'] = '待核实'
            result['是否2026年内到期'] = '待核实'
            result['判断依据'] = f"计算失败: {e}"
    else:
        result['合同开始时间'] = '待核实'
        result['合同结束时间'] = '待核实'
        result['是否2026年内到期'] = '待核实'
        result['判断依据'] = '缺少中标日期或服务期限'
    
    return result

def calculate_saturation_revenue(info: dict, parking_fee: float = 100.0) -> dict:
    """计算饱和收入"""
    result = {}
    
    # 住宅物业费收入
    if '住宅建筑面积' in info and '住宅物业费' in info:
        residential_revenue = info['住宅建筑面积'] * info['住宅物业费']
        result['住宅物业费收入'] = residential_revenue
    else:
        residential_revenue = 0
    
    # 商业物业费收入
    if '非住宅建筑面积' in info and '商业物业费' in info:
        commercial_revenue = info['非住宅建筑面积'] * info['商业物业费']
        result['商业物业费收入'] = commercial_revenue
    else:
        commercial_revenue = 0
    
    # 停车管理费收入
    if '地下停车位' in info:
        parking_revenue = info['地下停车位'] * parking_fee
        result['停车管理费收入'] = parking_revenue
    else:
        parking_revenue = 0
    
    # 总收入
    total_monthly = residential_revenue + commercial_revenue + parking_revenue
    result['月度饱和收入'] = total_monthly
    result['年度饱和收入'] = total_monthly * 12
    
    return result

def main():
    print("=" * 80)
    print("改进版：基于上海住宅物业公告信息识别 2026 年内合同到期项目")
    print("任务：识别静安区 2026 年内合同到期的项目")
    print("=" * 80)
    print()
    
    # 搜索静安区的公告
    district = "静安区"
    print(f"正在搜索 {district} 的公告...\n")
    
    results = search_projects_by_district(district)
    
    if not results:
        print(f"未找到包含 '{district}' 的公告")
        return
    
    print(f"找到 {len(results)} 个相关公告:\n")
    
    # 下载并分析每个公告
    all_projects = []
    
    for i, r in enumerate(results, 1):
        pdf_path = f"/tmp/{district}_{r['pdf_id']}.pdf"
        print(f"[{i}/{len(results)}] 正在处理: {r['title']}")
        
        if download_pdf(r['pdf_id'], pdf_path):
            text = ocr_pdf(pdf_path)
            if text:
                info = extract_contract_info_improved(text)
                contract_dates = calculate_contract_dates(info)
                revenue = calculate_saturation_revenue(info)
                
                # 合并信息
                project = {
                    '区域': district,
                    '项目名称': info.get('项目名称', '待核实'),
                    '招标人': info.get('招标人', '待核实'),
                    '中标人': info.get('中标企业', '待核实'),
                    '中标公告日期': info.get('中标日期', '待核实'),
                    '服务期限': info.get('服务期限', '待核实'),
                    '折算服务年限': info.get('折算服务年限', '待核实'),
                    '收费方式': info.get('收费方式', '待核实'),
                    '物业费标准': info.get('住宅物业费', '待核实'),
                    '合同开始时间': contract_dates.get('合同开始时间', '待核实'),
                    '合同结束时间': contract_dates.get('合同结束时间', '待核实'),
                    '是否2026年内到期': contract_dates.get('是否2026年内到期', '待核实'),
                    '到期类型': contract_dates.get('到期类型', '待核实'),
                    '判断依据': contract_dates.get('判断依据', '待核实'),
                    '可收费面积': info.get('总建筑面积', '待核实'),
                    '月度饱和收入': revenue.get('月度饱和收入', '待核实'),
                    '年度饱和收入': revenue.get('年度饱和收入', '待核实'),
                }
                
                all_projects.append(project)
                
                # 如果找到 2026 年内到期的项目，立即输出
                if project['是否2026年内到期'] == '是':
                    print(f"  ✅ 找到 2026 年内到期项目！")
                    print(f"     合同结束时间: {project['合同结束时间']}")
        else:
            print(f"  ❌ 下载失败")
        
        print()
    
    # 输出结果
    print("=" * 80)
    print("搜索结果汇总")
    print("=" * 80)
    print()
    
    # 分类输出
    clear_projects = [p for p in all_projects if p['到期类型'] == '明确2026年内到期']
    suspected_projects = [p for p in all_projects if '疑似' in p.get('到期类型', '')]
    unknown_projects = [p for p in all_projects if p['到期类型'] not in ['明确2026年内到期', '已过期', '未到期'] and '疑似' not in p.get('到期类型', '')]
    
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
    
    if unknown_projects:
        print("【第三部分：信息不足，暂不能判断】")
        print("-" * 80)
        for p in unknown_projects[:10]:  # 只显示前 10 个
            print(f"项目名称: {p['项目名称']}")
            print(f"中标人: {p['中标人']}")
            print(f"判断依据: {p['判断依据']}")
            print()
        if len(unknown_projects) > 10:
            print(f"... 还有 {len(unknown_projects) - 10} 个项目")

if __name__ == '__main__':
    main()
