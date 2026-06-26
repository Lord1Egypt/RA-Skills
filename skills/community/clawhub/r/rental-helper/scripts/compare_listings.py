#!/usr/bin/env python3
"""
生成房源对比表格
用法: python compare_listings.py --ids L001 L002 L003 [--format markdown|feishu] [--company "公司地址"]
"""

import json
import os
import argparse
import re

DATA_DIR = os.path.expanduser("~/.openclaw/workspace/rental-data")
DATA_FILE = os.path.join(DATA_DIR, "listings.json")
VIEWINGS_FILE = os.path.join(DATA_DIR, "viewings.json")

def load_listings():
    """加载房源列表"""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_viewings():
    """加载看房记录"""
    if not os.path.exists(VIEWINGS_FILE):
        return []
    with open(VIEWINGS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def format_value(value, max_len=20):
    """格式化值，限制长度"""
    if not value or value == "-":
        return "-"
    value = str(value).replace('\n', ' ').replace('|', '｜')
    if len(value) > max_len:
        return value[:max_len-1] + "…"
    return value

def get_cell_width(text, min_width=12):
    """计算单元格宽度（考虑中文字符）"""
    width = 0
    for char in str(text):
        if ord(char) > 127:  # 中文字符
            width += 2
        else:
            width += 1
    return max(width, min_width)

def print_markdown_table(headers, rows):
    """打印整齐的Markdown表格"""
    # 计算每列宽度
    col_widths = []
    for i, header in enumerate(headers):
        width = get_cell_width(header)
        for row in rows:
            if i < len(row):
                width = max(width, get_cell_width(row[i]))
        col_widths.append(width + 2)  # 加padding
    
    # 打印表头
    header_line = "|"
    for i, header in enumerate(headers):
        header_line += f" {header:<{col_widths[i]-2}} |"
    print(header_line)
    
    # 打印分隔线
    sep_line = "|"
    for width in col_widths:
        sep_line += "-" * width + "|"
    print(sep_line)
    
    # 打印数据行
    for row in rows:
        row_line = "|"
        for i, cell in enumerate(row):
            if i < len(col_widths):
                # 计算padding
                cell_str = str(cell)
                cell_width = get_cell_width(cell_str)
                padding = col_widths[i] - cell_width - 2
                row_line += f" {cell_str}{' ' * padding} |"
        print(row_line)

def extract_metro_distance(transport_text):
    """提取地铁距离信息"""
    if not transport_text:
        return None
    
    # 匹配模式：距地铁x号线xx站xx米 或 步行x分钟
    patterns = [
        r'距地铁[\d\u4e00-\u9fa5]*线[\d\u4e00-\u9fa5]*站(\d+)米',
        r'步行(\d+)分钟',
        r'地铁[\d\u4e00-\u9fa5]*线.*?距离.*?(\d+)米',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, transport_text)
        if match:
            return int(match.group(1))
    return None

def extract_pois(facilities_text):
    """提取周边POI信息"""
    if not facilities_text:
        return []
    
    # 常见POI关键词
    poi_keywords = {
        '公园': ['公园', '绿地', '广场'],
        '商场': ['商场', '购物中心', '超市', '便利店'],
        '医院': ['医院', '诊所', '卫生院'],
        '学校': ['学校', '幼儿园', '小学', '中学', '大学'],
        '餐饮': ['餐厅', '饭店', '美食', '小吃'],
        '运动': ['健身房', '体育馆', '游泳馆', '球场'],
    }
    
    found_pois = []
    text = facilities_text.lower()
    
    for category, keywords in poi_keywords.items():
        for keyword in keywords:
            if keyword in text:
                found_pois.append(category)
                break
    
    return found_pois

def analyze_pros_cons(listing, all_listings, company_location=None):
    """分析房源的优缺点"""
    pros = []
    cons = []
    
    # 1. 价格分析
    rents = [l.get('rent', 0) for l in all_listings if l.get('rent', 0) > 0]
    if rents:
        avg_rent = sum(rents) / len(rents)
        rent = listing.get('rent', 0)
        if rent < avg_rent * 0.9:
            pros.append(f"💰 价格低于平均{((avg_rent-rent)/avg_rent*100):.0f}%")
        elif rent > avg_rent * 1.1:
            cons.append(f"💰 价格高于平均{((rent-avg_rent)/avg_rent*100):.0f}%")
    
    # 2. 面积分析
    areas = [l.get('area', 0) for l in all_listings if l.get('area', 0) > 0]
    if areas:
        avg_area = sum(areas) / len(areas)
        area = listing.get('area', 0)
        if area > avg_area * 1.1:
            pros.append(f"📐 面积大于平均{area-avg_area:.0f}㎡")
        elif area < avg_area * 0.9:
            cons.append(f"📐 面积小于平均{avg_area-area:.0f}㎡")
    
    # 3. 交通分析
    transport = listing.get('transport', '')
    metro_dist = extract_metro_distance(transport)
    
    if metro_dist:
        all_dists = [extract_metro_distance(l.get('transport', '')) for l in all_listings]
        all_dists = [d for d in all_dists if d is not None]
        
        if all_dists:
            min_dist = min(all_dists)
            if metro_dist == min_dist:
                pros.append(f"🚇 离地铁最近({metro_dist}米)")
            elif metro_dist <= 500:
                pros.append(f"🚇 距地铁近({metro_dist}米)")
            elif metro_dist > 1000:
                cons.append(f"🚇 距地铁较远({metro_dist}米)")
    
    # 4. 公交分析
    if transport:
        if '公交' in transport or '车站' in transport:
            # 提取公交距离
            bus_match = re.search(r'公交.*?距.*?(\d+)米', transport)
            if bus_match:
                bus_dist = int(bus_match.group(1))
                if bus_dist <= 300:
                    pros.append(f"🚌 距公交站近({bus_dist}米)")
    
    # 5. 周边配套分析
    facilities = listing.get('facilities', '')
    pois = extract_pois(facilities)
    
    if pois:
        # 统计所有房源的POI
        all_pois = []
        for l in all_listings:
            all_pois.extend(extract_pois(l.get('facilities', '')))
        
        poi_count = len(pois)
        avg_poi_count = len(all_pois) / len(all_listings) if all_listings else 0
        
        if poi_count > avg_poi_count:
            pros.append(f"🏪 配套丰富({', '.join(pois[:3])})")
        
        # 特殊配套
        if '公园' in pois:
            pros.append("🌳 近公园，环境好")
        if '商场' in pois:
            pros.append("🛍️ 近商场，购物方便")
        if '医院' in pois:
            pros.append("🏥 近医院，就医方便")
        if '学校' in pois:
            pros.append("📚 近学校，教育资源好")
    
    # 6. 装修分析
    decoration = listing.get('decoration', '')
    if decoration:
        if '精装' in decoration or '新装' in decoration:
            pros.append("✨ 精装修，拎包入住")
        elif '简装' in decoration or '老' in decoration:
            cons.append("🔧 装修较旧")
    
    # 7. 楼层分析
    floor = listing.get('floor', '')
    if floor:
        # 提取楼层数字
        floor_match = re.search(r'(\d+)层', floor)
        if floor_match:
            floor_num = int(floor_match.group(1))
            if '电梯' in floor:
                if floor_num >= 10:
                    pros.append("🏢 高层有电梯，视野好")
                else:
                    pros.append("🛗 有电梯，方便")
            else:
                if floor_num >= 5:
                    cons.append("🏃 楼层较高无电梯")
                elif floor_num <= 2:
                    pros.append("🏠 低楼层，方便")
    
    # 8. 朝向分析
    orientation = listing.get('orientation', '')
    if orientation:
        if '南北' in orientation:
            pros.append("☀️ 南北通透，采光好")
        elif '南' in orientation:
            pros.append("☀️ 朝南，采光好")
        elif '北' in orientation:
            cons.append("🌑 朝北，采光较差")
    
    return pros, cons

def compare_listings(args):
    """生成对比表格"""
    listings = load_listings()
    viewings = load_viewings()
    
    if not args.ids:
        print("请指定要对比的房源ID")
        return
    
    # 获取指定房源
    selected = []
    for id in args.ids:
        listing = next((l for l in listings if l.get("id") == id), None)
        if listing:
            # 查找看房记录
            listing_viewings = [v for v in viewings if v.get("listing_id") == id]
            if listing_viewings:
                latest_viewing = max(listing_viewings, key=lambda x: x.get("viewing_time", ""))
                listing["viewing_score"] = latest_viewing.get("overall_score", "-")
            else:
                listing["viewing_score"] = "-"
            selected.append(listing)
        else:
            print(f"⚠️ 未找到房源: {id}")
    
    if len(selected) < 2:
        print("至少需要2个房源才能对比")
        return
    
    # 为每个房源分析优缺点
    for listing in selected:
        auto_pros, auto_cons = analyze_pros_cons(listing, selected, args.company)
        
        # 合并原有的优缺点
        original_pros = listing.get('pros', '')
        original_cons = listing.get('cons', '')
        
        all_pros = auto_pros + ([original_pros] if original_pros else [])
        all_cons = auto_cons + ([original_cons] if original_cons else [])
        
        listing['analyzed_pros'] = all_pros
        listing['analyzed_cons'] = all_cons
    
    # 生成对比表
    format_type = args.format or "markdown"
    
    if format_type == "markdown":
        print("\n" + "="*70)
        print("🏠 房源对比表")
        print("="*70)
        
        # 表头
        headers = ["对比项"] + [format_value(l.get("name", l.get("id", "")), 18) for l in selected]
        
        # 对比数据
        rows = [
            ["💰 租金"] + [f"{l.get('rent', 0)}元/月" for l in selected],
            ["💳 押金"] + [format_value(l.get("deposit", "-")) for l in selected],
            ["🏢 户型"] + [format_value(l.get("room_type", "-")) for l in selected],
            ["📐 面积"] + [f"{l.get('area', 0)}㎡" if l.get('area') else "-" for l in selected],
            ["🔢 单价"] + [f"{l.get('rent', 0)/l.get('area', 1):.1f}元/㎡" if l.get('area') else "-" for l in selected],
            ["🏠 楼层"] + [format_value(l.get("floor", "-")) for l in selected],
            ["🧭 朝向"] + [format_value(l.get("orientation", "-")) for l in selected],
            ["✨ 装修"] + [format_value(l.get("decoration", "-")) for l in selected],
            ["🚇 交通"] + [format_value(l.get("transport", "-"), 28) for l in selected],
            ["🏪 配套"] + [format_value(l.get("facilities", "-"), 25) for l in selected],
            ["🔗 房源链接"] + [format_value(l.get("url", "-"), 30) for l in selected],
            ["⭐ 看房评分"] + [str(l.get("viewing_score", "-")) for l in selected],
            ["📊 状态"] + [format_value(l.get("status", "-")) for l in selected],
        ]
        
        print_markdown_table(headers, rows)
        
        # 智能优缺点分析
        print("\n" + "="*70)
        print("🎯 智能优缺点分析")
        print("="*70)
        
        for listing in selected:
            print(f"\n【{listing.get('name')}】")
            
            pros = listing.get('analyzed_pros', [])
            cons = listing.get('analyzed_cons', [])
            
            if pros:
                print("  ✅ 优点:")
                for pro in pros[:5]:  # 最多显示5条
                    print(f"     • {pro}")
            
            if cons:
                print("  ❌ 缺点:")
                for con in cons[:3]:  # 最多显示3条
                    print(f"     • {con}")
            
            if not pros and not cons:
                print("  ℹ️ 暂无分析数据")
        
        # 汇总分析
        print("\n" + "="*70)
        print("📈 汇总分析")
        print("="*70)
        
        rents = [l.get('rent', 0) for l in selected if l.get('rent', 0) > 0]
        areas = [l.get('area', 0) for l in selected if l.get('area', 0) > 0]
        scores = [l.get('viewing_score') for l in selected if l.get('viewing_score') != "-"]
        
        if rents:
            min_rent = min(rents)
            max_rent = max(rents)
            avg_rent = sum(rents) / len(rents)
            print(f"💰 租金范围: {min_rent} - {max_rent} 元/月  (平均: {avg_rent:.0f}元)")
        
        if areas:
            min_area = min(areas)
            max_area = max(areas)
            avg_area = sum(areas) / len(areas)
            print(f"📐 面积范围: {min_area} - {max_area} ㎡  (平均: {avg_area:.1f}㎡)")
        
        if scores:
            max_score = max(scores)
            best_listing = next((l for l in selected if l.get('viewing_score') == max_score), None)
            if best_listing:
                print(f"⭐ 最高评分: {best_listing.get('name')} ({max_score}分)")
        
        # 性价比分析
        if rents and areas:
            print(f"\n💡 性价比分析:")
            unit_prices = [(l.get('rent', 0)/l.get('area', 1), l) for l in selected if l.get('area', 0) > 0]
            unit_prices.sort(key=lambda x: x[0])
            print(f"   最低单价: {unit_prices[0][1].get('name')} ({unit_prices[0][0]:.1f}元/㎡·月)")
            print(f"   最高单价: {unit_prices[-1][1].get('name')} ({unit_prices[-1][0]:.1f}元/㎡·月)")
        
        # 交通对比
        metro_listings = [(extract_metro_distance(l.get('transport', '')), l) for l in selected]
        metro_listings = [(d, l) for d, l in metro_listings if d is not None]
        if metro_listings:
            metro_listings.sort(key=lambda x: x[0])
            print(f"\n🚇 交通对比:")
            print(f"   距地铁最近: {metro_listings[0][1].get('name')} ({metro_listings[0][0]}米)")
        
        print("="*70)
    
    else:
        # 飞书格式（文本形式，可手动复制到飞书表格）
        print("\n飞书表格格式（可复制到飞书多维表格）：\n")
        
        # CSV格式
        print("房源名称,租金,押金,户型,面积,单价,楼层,朝向,装修,交通,配套,房源链接,智能优点,智能缺点,看房评分,状态")
        for l in selected:
            rent = l.get('rent', 0)
            area = l.get('area', 0)
            unit_price = f"{rent/area:.1f}" if area > 0 else "-"
            pros = ";".join(l.get('analyzed_pros', []))
            cons = ";".join(l.get('analyzed_cons', []))
            row = [
                l.get("name", ""),
                f"{rent}元",
                l.get("deposit", ""),
                l.get("room_type", ""),
                f"{area}㎡" if area else "",
                unit_price,
                l.get("floor", ""),
                l.get("orientation", ""),
                l.get("decoration", ""),
                l.get("transport", ""),
                l.get("facilities", ""),
                l.get("url", ""),
                pros,
                cons,
                str(l.get("viewing_score", "-")),
                l.get("status", "")
            ]
            print(",".join(row))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="生成房源对比表")
    parser.add_argument("--ids", nargs="+", help="要对比的房源ID列表")
    parser.add_argument("--format", choices=["markdown", "feishu"], default="markdown", help="输出格式")
    parser.add_argument("--company", help="公司地址（用于计算通勤）")
    
    args = parser.parse_args()
    compare_listings(args)
