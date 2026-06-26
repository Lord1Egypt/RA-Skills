#!/usr/bin/env python3
"""
上海物业招标公告研究工具
从上海住宅物业网获取招标公告、中标公告，使用 OCR 提取项目信息，计算饱和收入
"""

import sys
import re
import requests
from bs4 import BeautifulSoup

def search_project(project_name: str) -> list:
    """搜索项目公告"""
    url = 'https://962121.fgj.sh.gov.cn/wyweb/web/front/common/greenmorelist.jsp?id=A000000000000000&twoid=A000B00400000000&thrid=A000B004C0010000'
    
    response = requests.get(url)
    response.encoding = 'GBK'
    soup = BeautifulSoup(response.text, 'html.parser')
    
    results = []
    links = soup.find_all('a')
    for link in links:
        text = link.get_text()
        if project_name in text:
            href = link.get('href', '')
            # 提取 infoid
            match = re.search(r'infoid=(\d+)', href)
            if match:
                infoid = match.group(1)
                results.append({
                    'title': text.strip(),
                    'infoid': infoid,
                    'pdf_id': str(int(infoid) - 1),  # PDF ID 通常是 infoid - 1
                    'url': f"https://962121.fgj.sh.gov.cn{href}" if href.startswith('/') else href
                })
    
    return results

def download_pdf(pdf_id: str, output_path: str) -> bool:
    """下载 PDF 文件"""
    url = f"https://962121.fgj.sh.gov.cn/wyweb//web/UploadFiles/pdf/{pdf_id}.pdf"
    
    try:
        response = requests.get(url)
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
            text += f"=== 第 {i+1} 页 ===\n"
            text += pytesseract.image_to_string(image, lang='chi_sim+eng')
            text += "\n\n"
        
        return text
    except Exception as e:
        print(f"OCR 识别失败: {e}")
        print("提示: 请确保已安装 poppler (macOS: brew install poppler)")
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
    
    # 非住宅建筑面积（重要：必须提取，OCR 可能分行）
    # 尝试多种格式匹配
    match = re.search(r'非住宅建筑面积\s*(\d+[.,]?\d*)\s*平方米', text)
    if match:
        info['非住宅建筑面积'] = float(match.group(1).replace(',', '.'))
    else:
        # 尝试跨行匹配：数字在行尾，小数部分在下一行
        match = re.search(r'非住宅建筑面积\s*(\d+[.,]?\d*)\s*\n\s*(\d+[.,]?\d*)\s*平方米', text)
        if match:
            # 合并两部分数字
            num1 = match.group(1).replace(',', '.')
            num2 = match.group(2).replace(',', '.')
            # 如果第一部分有小数点，说明是完整的数字，直接使用
            if '.' in num1:
                info['非住宅建筑面积'] = float(num1)
            else:
                # 否则，第一部分是整数部分，第二部分是小数部分
                info['非住宅建筑面积'] = float(num1 + num2)
    
    # 住宅物业费（优先使用中标公告的价格，而不是招标公告的上限）
    # 注意：中标公告的价格是最终价格，招标公告的价格是上限
    match = re.search(r'商品房高层[^物业]*物业费标准\s*(\d+[.,]?\d*)\s*元/平方米', text)
    if match:
        # 只有当新值比现有值大时才更新（中标公告的价格通常更高或等于招标公告的上限）
        new_fee = float(match.group(1).replace(',', '.'))
        # OCR 可能错误地把 "2.40" 识别成 "240"，需要修正
        if new_fee > 10:
            new_fee = new_fee / 100
        if '住宅物业费' not in info or new_fee > info.get('住宅物业费', 0):
            info['住宅物业费'] = new_fee
    
    # 商业物业费
    match = re.search(r'商业[^物业]*物业费标准\s*(\d+[.,]?\d*)\s*元/平方米', text)
    if match:
        new_fee = float(match.group(1).replace(',', '.'))
        # OCR 可能错误地把 "4.00" 识别成 "400"，需要修正
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
    
    # 中标日期（从公告底部提取）
    match = re.search(r'(\d{4})年(\d{1,2})月(\d{1,2})日?\s*$', text, re.MULTILINE)
    if match:
        year = match.group(1)
        month = match.group(2).zfill(2)
        day = match.group(3).zfill(2)
        info['中标日期'] = f"{year}-{month}-{day}"
    
    # 合同期限（从招标公告提取）
    match = re.search(r'物业服务合同期限\s*(\d+)\s*年', text)
    if match:
        info['合同期限'] = f"{match.group(1)}年"
    
    return info

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
    if len(sys.argv) < 2:
        print("用法: python fetch_project.py <项目名称> [--parking-fee <停车管理费>]")
        print("示例: python fetch_project.py 协和城 --parking-fee 100")
        sys.exit(1)
    
    project_name = sys.argv[1]
    parking_fee = 100.0  # 默认停车管理费
    
    # 解析参数
    if '--parking-fee' in sys.argv:
        idx = sys.argv.index('--parking-fee')
        if idx + 1 < len(sys.argv):
            parking_fee = float(sys.argv[idx + 1])
    
    print(f"正在搜索项目: {project_name}\n")
    
    # 搜索公告
    results = search_project(project_name)
    
    if not results:
        print(f"未找到包含 '{project_name}' 的公告")
        sys.exit(1)
    
    print(f"找到 {len(results)} 个相关公告:\n")
    for i, r in enumerate(results, 1):
        print(f"{i}. {r['title']}")
        print(f"   PDF ID: {r['pdf_id']}")
    
    print()
    
    # 下载并识别每个公告
    all_info = {}
    for r in results:
        pdf_path = f"/tmp/{project_name}_{r['pdf_id']}.pdf"
        print(f"正在下载: {r['title']}")
        
        if download_pdf(r['pdf_id'], pdf_path):
            print(f"正在 OCR 识别...")
            text = ocr_pdf(pdf_path)
            if text:
                info = extract_info(text)
                # 智能合并：住宅物业费取最大值（中标公告 > 招标公告上限）
                for key, value in info.items():
                    if key == '住宅物业费':
                        # 住宅物业费：取最大值（中标公告的最终价格通常更高）
                        if key not in all_info or value > all_info[key]:
                            all_info[key] = value
                    else:
                        # 其他字段：直接覆盖（后处理的公告信息更完整）
                        all_info[key] = value
        else:
            print(f"下载失败，跳过")
        
        print()
    
    # 输出提取的信息
    print("=" * 60)
    print("项目信息:")
    print("=" * 60)
    for key, value in all_info.items():
        print(f"{key}: {value}")
    
    # 计算合同到期时间
    if '中标日期' in all_info and '合同期限' in all_info:
        from datetime import datetime
        from dateutil.relativedelta import relativedelta
        
        try:
            start_date = datetime.strptime(all_info['中标日期'], '%Y-%m-%d')
            years = int(all_info['合同期限'].replace('年', ''))
            end_date = start_date + relativedelta(years=years)
            all_info['合同到期时间'] = end_date.strftime('%Y-%m-%d')
            print(f"合同到期时间: {all_info['合同到期时间']}")
        except:
            pass
    
    print()
    
    # 计算饱和收入
    print("=" * 60)
    print("饱和收入计算:")
    print("=" * 60)
    
    if parking_fee:
        print(f"停车管理费: {parking_fee} 元/月/个\n")
    
    revenue = calculate_saturation_revenue(all_info, parking_fee)
    
    for key, value in revenue.items():
        if '收入' in key:
            if '年度' in key:
                print(f"{key}: {value:,.2f} 元/年")
            else:
                print(f"{key}: {value:,.2f} 元/月")
    
    print()

if __name__ == '__main__':
    main()
