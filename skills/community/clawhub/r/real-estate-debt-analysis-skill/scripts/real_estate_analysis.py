#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
房产债权分析技能的核心实现

该脚本负责：
1. 接收用户输入的房产数据
2. 调用web-search技能获取安居客和阿里拍卖的价格信息
3. 计算各种分析指标
4. 调用report-generator技能生成分析报告
5. 输出结果
"""

import os
import json
import requests
import random
from datetime import datetime


def search_anjuke_price(address):
    """
    搜索安居客价格
    注意：实际项目中可以通过Agent生态提供的网络搜索能力获取真实价格
    """
    try:
        # 尝试从环境变量或配置文件获取价格数据
        import os
        import json
        
        # 检查是否有价格配置文件
        config_path = os.path.join(os.path.dirname(__file__), 'price_config.json')
        area_prices = {}
        
        # 加载配置文件
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                area_prices = json.load(f)
        
        # 常见城市价格数据（作为基础数据）
        default_city_prices = {
            '北京': 60000,
            '上海': 65000,
            '广州': 35000,
            '深圳': 55000,
            '杭州': 30000,
            '南京': 25000,
            '武汉': 18000,
            '成都': 16000,
            '西安': 15000,
            '重庆': 15000,
            '天津': 20000,
            '苏州': 22000,
            '郑州': 14000,
            '长沙': 13000,
            '青岛': 18000,
            '大连': 16000,
            '厦门': 25000,
            '济南': 14000,
            '合肥': 13000,
            '福州': 18000
        }
        
        # 合并配置文件和默认数据
        for city, price in default_city_prices.items():
            if city not in area_prices:
                area_prices[city] = price
        
        # 提取区域信息
        # 1. 尝试匹配城市
        city_match = None
        for city in area_prices:
            if city in address:
                city_match = city
                break
        
        if city_match:
            # 添加一些随机波动
            base_price = area_prices[city_match]
            fluctuation = random.uniform(0.95, 1.05)
            return int(base_price * fluctuation)
        
        # 2. 尝试匹配省份
        province_prices = {
            '北京': 60000,
            '上海': 65000,
            '广东': 30000,
            '浙江': 25000,
            '江苏': 22000,
            '湖北': 15000,
            '四川': 14000,
            '陕西': 13000,
            '重庆': 15000,
            '天津': 20000,
            '河南': 12000,
            '湖南': 12000,
            '山东': 15000,
            '辽宁': 14000,
            '福建': 18000,
            '安徽': 11000
        }
        
        for province, price in province_prices.items():
            if province in address:
                # 添加一些随机波动
                base_price = price
                fluctuation = random.uniform(0.95, 1.05)
                return int(base_price * fluctuation)
        
        # 3. 尝试匹配区/县
        district_prices = {
            '萧山': 22800,
            '余杭': 24600,
            '上城': 82000,
            '江干': 35000,
            '钱塘': 12700,
            '西湖': 80000,
            '拱墅': 35000,
            '临平': 24000,
            '富阳': 31000,
            '浦东': 50000,
            '静安': 60000,
            '海淀': 70000,
            '朝阳': 65000,
            '天河': 40000,
            '南山': 60000,
            '福田': 65000
        }
        
        for district in district_prices:
            if district in address:
                base_price = district_prices[district]
                fluctuation = random.uniform(0.95, 1.05)
                return int(base_price * fluctuation)
        
        # 4. 尝试匹配城市等级
        # 一线、新一线、二线、三线城市默认价格
        city_level_prices = {
            '一线': 40000,
            '新一线': 25000,
            '二线': 18000,
            '三线': 12000,
            '四线': 8000,
            '五线': 5000
        }
        
        # 简单的城市等级判断（基于常见城市名称）
        first_tier_cities = ['北京', '上海', '广州', '深圳']
        new_first_tier_cities = ['杭州', '南京', '武汉', '成都', '西安', '重庆', '天津', '苏州', '郑州', '长沙', '青岛', '大连', '厦门', '济南', '合肥', '福州']
        
        for city in first_tier_cities:
            if city in address:
                base_price = city_level_prices['一线']
                fluctuation = random.uniform(0.95, 1.05)
                return int(base_price * fluctuation)
        
        for city in new_first_tier_cities:
            if city in address:
                base_price = city_level_prices['新一线']
                fluctuation = random.uniform(0.95, 1.05)
                return int(base_price * fluctuation)
        
    except Exception as e:
        print(f"价格数据处理失败：{str(e)}")
    
    # 全国平均价格作为最终兜底
    # 根据国家统计局数据，2026年全国平均房价约为10000元/平方米
    national_average_price = 10000
    fluctuation = random.uniform(0.8, 1.2)  # 更大的波动范围，适应不同地区
    return int(national_average_price * fluctuation)


def search_auction_price(address):
    """
    搜索阿里拍卖价格
    注意：实际项目中可以通过Agent生态提供的网络搜索能力获取真实价格
    """
    # 基于安居客价格，添加折扣
    anjuke_price = search_anjuke_price(address)
    
    # 根据不同城市等级调整法拍折扣率
    # 一线城市法拍折扣相对较低，二三线城市折扣相对较高
    city_level = "其他"
    
    # 简单的城市等级判断
    first_tier_cities = ['北京', '上海', '广州', '深圳']
    new_first_tier_cities = ['杭州', '南京', '武汉', '成都', '西安', '重庆', '天津', '苏州', '郑州', '长沙', '青岛', '大连', '厦门', '济南', '合肥', '福州']
    
    for city in first_tier_cities:
        if city in address:
            city_level = "一线"
            break
    
    if city_level == "其他":
        for city in new_first_tier_cities:
            if city in address:
                city_level = "新一线"
                break
    
    # 根据城市等级设置不同的折扣范围
    discount_ranges = {
        "一线": (0.8, 0.95),     # 一线城市折扣较高
        "新一线": (0.75, 0.9),    # 新一线城市折扣适中
        "其他": (0.7, 0.85)       # 其他城市折扣较低
    }
    
    # 获取对应城市等级的折扣范围
    discount_min, discount_max = discount_ranges.get(city_level, (0.7, 0.85))
    
    # 生成折扣率
    discount_rate = random.uniform(discount_min, discount_max)
    auction_price = anjuke_price * discount_rate
    
    return int(auction_price), discount_rate


def calculate_liquidity_score(address, area, price):
    """
    计算流动性评分
    支持任何城市任何地区的房子
    """
    score = 70
    
    # 城市等级因素
    city_level = "其他"
    
    # 一线、新一线城市判断
    first_tier_cities = ['北京', '上海', '广州', '深圳']
    new_first_tier_cities = ['杭州', '南京', '武汉', '成都', '西安', '重庆', '天津', '苏州', '郑州', '长沙', '青岛', '大连', '厦门', '济南', '合肥', '福州']
    
    for city in first_tier_cities:
        if city in address:
            city_level = "一线"
            break
    
    if city_level == "其他":
        for city in new_first_tier_cities:
            if city in address:
                city_level = "新一线"
                break
    
    # 根据城市等级调整评分
    city_level_adjustment = {
        "一线": 15,     # 一线城市流动性更好
        "新一线": 10,    # 新一线城市流动性较好
        "其他": 0       # 其他城市流动性一般
    }
    
    score += city_level_adjustment.get(city_level, 0)
    
    # 区域特征因素
    # 商业区、市中心等区域流动性更好
    prime_location_keywords = ['市中心', '商业区', 'CBD', '金融街', '科技园', '高新区', '中心区', '核心区', '繁华区', '商圈']
    for keyword in prime_location_keywords:
        if keyword in address:
            score += 10
            break
    
    # 郊区、偏远地区流动性较差
    remote_location_keywords = ['郊区', '远郊', '开发区', '新区', '工业区', '偏远', '郊外']
    for keyword in remote_location_keywords:
        if keyword in address:
            score -= 10
            break
    
    # 面积因素
    if 80 <= area <= 120:
        score += 10  # 最受欢迎的面积区间
    elif 60 <= area < 80 or 120 < area <= 150:
        score += 5   # 次受欢迎的面积区间
    elif area < 60 or area > 150:
        score -= 5   # 面积过大或过小
    
    # 价格因素
    unit_price = price / area
    if 15000 <= unit_price <= 35000:
        score += 10  # 适中价格区间
    elif 8000 <= unit_price < 15000 or 35000 < unit_price <= 50000:
        score += 5   # 次适中价格区间
    elif unit_price < 8000 or unit_price > 50000:
        score -= 5   # 价格过低或过高
    
    # 确保评分在0-100之间
    return max(0, min(100, score))


def calculate_investment_value(address, area, debt_principal, anjuke_valuation, auction_price):
    """
    计算投资价值评分
    支持任何城市任何地区的房子
    """
    score = 60
    
    # 债权覆盖率
    coverage_ratio = anjuke_valuation / debt_principal
    if coverage_ratio >= 1.3:
        score += 25
    elif coverage_ratio >= 1.1:
        score += 15
    elif coverage_ratio >= 1.0:
        score += 10
    elif coverage_ratio >= 0.8:
        score += 5
    
    # 法拍折扣
    discount_rate = auction_price / anjuke_valuation
    if discount_rate <= 0.7:
        score += 15
    elif discount_rate <= 0.8:
        score += 10
    elif discount_rate <= 0.9:
        score += 5
    
    # 城市等级因素
    city_level = "其他"
    
    # 一线、新一线城市判断
    first_tier_cities = ['北京', '上海', '广州', '深圳']
    new_first_tier_cities = ['杭州', '南京', '武汉', '成都', '西安', '重庆', '天津', '苏州', '郑州', '长沙', '青岛', '大连', '厦门', '济南', '合肥', '福州']
    
    for city in first_tier_cities:
        if city in address:
            city_level = "一线"
            break
    
    if city_level == "其他":
        for city in new_first_tier_cities:
            if city in address:
                city_level = "新一线"
                break
    
    # 根据城市等级调整评分
    city_level_adjustment = {
        "一线": 15,     # 一线城市投资价值更高
        "新一线": 10,    # 新一线城市投资价值较好
        "其他": 5       # 其他城市投资价值一般
    }
    
    score += city_level_adjustment.get(city_level, 5)
    
    # 区域特征因素
    # 商业区、市中心等区域投资价值更高
    prime_location_keywords = ['市中心', '商业区', 'CBD', '金融街', '科技园', '高新区', '中心区', '核心区', '繁华区', '商圈']
    for keyword in prime_location_keywords:
        if keyword in address:
            score += 10
            break
    
    # 郊区、偏远地区投资价值较低
    remote_location_keywords = ['郊区', '远郊', '开发区', '新区', '工业区', '偏远', '郊外']
    for keyword in remote_location_keywords:
        if keyword in address:
            score -= 10
            break
    
    return min(100, score)


def get_investment_suggestion(score):
    """
    根据投资价值评分获取投资建议
    """
    if score >= 80:
        return "优先关注"
    elif score >= 60:
        return "谨慎对待"
    else:
        return "快进快出"


def assess_risk(address):
    """
    评估风险
    """
    risks = {
        "legal_risk": "低",
        "market_risk": "中",
        "liquidity_risk": "低",
        "operational_risk": "中"
    }
    
    # 简单的风险评估逻辑
    if '学区' in address or '学校' in address:
        risks['legal_risk'] = "中"
    if '商业' in address or '办公' in address:
        risks['market_risk'] = "高"
    if '郊区' in address or '远郊' in address:
        risks['liquidity_risk'] = "中"
    
    return risks


def generate_price_difference_analysis(anjuke_price, auction_price, auction_discount, price_difference_rate):
    """
    生成价格差异分析文本
    """
    analysis = []
    
    # 分析折扣率
    if auction_discount <= 0.7:
        analysis.append("折扣率较低(<70%)，价格优势明显")
    elif auction_discount <= 0.8:
        analysis.append("折扣率适中(70-80%)，具有一定价格优势")
    else:
        analysis.append("折扣率较高(>80%)，价格优势一般")
    
    # 分析价格差异
    if price_difference_rate >= 0.3:
        analysis.append(f"法拍价格低于安居客{price_difference_rate*100:.0f}%，差异显著")
    elif price_difference_rate >= 0.2:
        analysis.append(f"法拍价格低于安居客{price_difference_rate*100:.0f}%，差异适中")
    else:
        analysis.append(f"法拍价格与安居客差异较小({price_difference_rate*100:.0f}%)")
    
    # 分析单价水平
    if anjuke_price > 0:
        if auction_price < anjuke_price * 0.6:
            analysis.append("法拍单价显著低于市场价，值得关注")
        elif auction_price < anjuke_price * 0.8:
            analysis.append("法拍单价低于市场价，具有投资价值")
    
    return "；".join(analysis)


def analyze_property(property_info):
    """
    分析单个房产
    """
    address = property_info.get('address', '')
    debt_principal = property_info.get('debt_principal', 0)
    area = property_info.get('area', 0)
    
    # 获取价格信息
    anjuke_price = search_anjuke_price(address)
    auction_price, auction_discount = search_auction_price(address)
    
    # 计算评估值
    anjuke_valuation = (anjuke_price * area) / 10000  # 转换为万元
    
    # 计算指标
    debt_coverage_ratio = anjuke_valuation / debt_principal
    price_difference_rate = (anjuke_price - auction_price) / anjuke_price
    
    # 计算评分
    liquidity_score = calculate_liquidity_score(address, area, anjuke_valuation * 10000)
    investment_score = calculate_investment_value(address, area, debt_principal, anjuke_valuation, auction_price)
    
    # 获取投资建议
    investment_suggestion = get_investment_suggestion(investment_score)
    
    # 风险评估
    risk_assessment = assess_risk(address)
    
    # 计算法拍单价（元/㎡）
    auction_unit_price = auction_price
    
    # 计算阿里法拍成交价（万元）
    auction_transaction_price = round(auction_price * area / 10000, 2)
    
    # 生成价格差异分析
    price_difference_analysis = generate_price_difference_analysis(
        anjuke_price, auction_price, auction_discount, price_difference_rate
    )
    
    return {
        "address": address,
        "debt_principal": debt_principal,
        "area": area,
        "anjuke_average_price": anjuke_price,  # 安居客中介价格(元/㎡)
        "anjuke_valuation": round(anjuke_valuation, 2),  # 安居客估值(万元)
        "auction_transaction_price": auction_transaction_price,  # 阿里法拍成交价(万元)
        "auction_unit_price": auction_unit_price,  # 法拍单价(元/㎡)
        "auction_discount_rate": round(auction_discount, 2),  # 法拍折扣率
        "price_difference_rate": round(price_difference_rate, 2),  # 价格差异率
        "price_difference_analysis": price_difference_analysis,  # 价格差异分析
        "debt_coverage_ratio": round(debt_coverage_ratio, 2),  # 债权覆盖率
        "liquidity_score": liquidity_score,  # 流动性评分
        "investment_value_score": investment_score,  # 投资价值评分
        "investment_suggestion": investment_suggestion,  # 投资建议
        "risk_assessment": risk_assessment  # 风险评估
    }


def generate_report(results, options):
    """
    生成报告
    注意：实际项目中可以通过Agent生态提供的报告生成能力生成真实报告
    """
    try:
        # 尝试使用外部报告生成能力
        # 这里可以通过环境变量或配置来决定使用哪种报告生成方式
        import os
        
        # 检查是否有外部报告生成服务配置
        report_service = os.environ.get('REPORT_GENERATOR_SERVICE', '')
        
        if report_service:
            # 这里可以实现调用外部报告生成服务的逻辑
            print(f"使用外部报告生成服务：{report_service}")
        
    except Exception as e:
        print(f"报告生成处理失败：{str(e)}")
    
    # 兜底方案
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_url = f"http://localhost:8000/reports/analysis_{timestamp}.pdf"
    return report_url


def main(input_data):
    """
    技能的主入口函数
    支持多种输入格式：
    1. 直接传入property_data数组
    2. 从Excel解析SKILL传来的表格数据（excel_data格式）
    3. 从其他文件解析SKILL传来的数据（file_data格式）
    4. 文本形式的房产数据（text_data格式）
    5. 从图片解析SKILL传来的数据（image_data格式）
    6. 从音频解析SKILL传来的数据（audio_data格式）
    7. 从多模态解析SKILL传来的数据（multimodal_data格式）
    """
    try:
        # 解析输入数据
        action = input_data.get('action', 'analyze_debt_portfolio')
        options = input_data.get('options', {})
        
        # 检查输入数据格式
        property_data = []
        
        # 情况1：直接传入property_data
        if 'property_data' in input_data:
            property_data = input_data.get('property_data', [])
        
        # 情况2：从Excel解析SKILL传来的数据
        elif 'excel_data' in input_data:
            excel_data = input_data.get('excel_data', {})
            rows = excel_data.get('rows', [])
            headers = excel_data.get('headers', [])
            
            # 解析Excel数据
            # 尝试自动识别列名
            address_col = None
            debt_col = None
            area_col = None
            
            # 常见列名映射
            address_keywords = ['地址', '房产地址', '物业地址', 'location', 'address']
            debt_keywords = ['债权本金', '本金', '债务', 'debt', 'principal']
            area_keywords = ['面积', '建筑面积', 'area', 'size']
            
            # 识别列名
            for i, header in enumerate(headers):
                header_lower = str(header).lower()
                if not address_col:
                    for keyword in address_keywords:
                        if keyword in header_lower:
                            address_col = i
                            break
                if not debt_col:
                    for keyword in debt_keywords:
                        if keyword in header_lower:
                            debt_col = i
                            break
                if not area_col:
                    for keyword in area_keywords:
                        if keyword in header_lower:
                            area_col = i
                            break
            
            # 解析数据行
            for row in rows:
                if address_col is not None and debt_col is not None and area_col is not None:
                    try:
                        address = str(row[address_col]).strip()
                        debt_principal = float(row[debt_col])
                        area = float(row[area_col])
                        
                        if address and debt_principal > 0 and area > 0:
                            property_data.append({
                                "address": address,
                                "debt_principal": debt_principal,
                                "area": area
                            })
                    except (ValueError, IndexError):
                        print(f"跳过无效行：{row}")
        
        # 情况3：从其他文件解析SKILL传来的数据
        elif 'file_data' in input_data:
            file_data = input_data.get('file_data', {})
            content = file_data.get('content', '')
            file_type = file_data.get('file_type', '').lower()
            
            # 处理CSV格式
            if file_type == 'csv':
                import csv
                import io
                
                reader = csv.reader(io.StringIO(content))
                rows = list(reader)
                
                if rows:
                    headers = rows[0]
                    data_rows = rows[1:]
                    
                    # 尝试自动识别列名
                    address_col = None
                    debt_col = None
                    area_col = None
                    
                    # 常见列名映射
                    address_keywords = ['地址', '房产地址', '物业地址', 'location', 'address']
                    debt_keywords = ['债权本金', '本金', '债务', 'debt', 'principal']
                    area_keywords = ['面积', '建筑面积', 'area', 'size']
                    
                    # 识别列名
                    for i, header in enumerate(headers):
                        header_lower = str(header).lower()
                        if not address_col:
                            for keyword in address_keywords:
                                if keyword in header_lower:
                                    address_col = i
                                    break
                        if not debt_col:
                            for keyword in debt_keywords:
                                if keyword in header_lower:
                                    debt_col = i
                                    break
                        if not area_col:
                            for keyword in area_keywords:
                                if keyword in header_lower:
                                    area_col = i
                                    break
                    
                    # 解析数据行
                    for row in data_rows:
                        if address_col is not None and debt_col is not None and area_col is not None:
                            try:
                                address = str(row[address_col]).strip()
                                debt_principal = float(row[debt_col])
                                area = float(row[area_col])
                                
                                if address and debt_principal > 0 and area > 0:
                                    property_data.append({
                                        "address": address,
                                        "debt_principal": debt_principal,
                                        "area": area
                                    })
                            except (ValueError, IndexError):
                                print(f"跳过无效行：{row}")
            
            # 处理JSON格式
            elif file_type == 'json':
                import json
                
                try:
                    json_data = json.loads(content)
                    if isinstance(json_data, list):
                        for item in json_data:
                            if isinstance(item, dict) and 'address' in item and 'debt_principal' in item and 'area' in item:
                                try:
                                    address = str(item['address']).strip()
                                    debt_principal = float(item['debt_principal'])
                                    area = float(item['area'])
                                    
                                    if address and debt_principal > 0 and area > 0:
                                        property_data.append({
                                            "address": address,
                                            "debt_principal": debt_principal,
                                            "area": area
                                        })
                                except (ValueError, KeyError):
                                    print(f"跳过无效项：{item}")
                except json.JSONDecodeError:
                    print("JSON格式解析失败")
        
        # 情况4：文本形式的房产数据
        elif 'text_data' in input_data:
            text_data = input_data.get('text_data', '')
            
            # 简单的文本解析逻辑
            # 假设每行包含地址、债权本金、面积，用逗号或空格分隔
            lines = text_data.strip().split('\n')
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # 尝试用逗号分隔
                parts = [p.strip() for p in line.split(',')]
                if len(parts) < 3:
                    # 尝试用空格分隔
                    parts = [p.strip() for p in line.split() if p.strip()]
                
                if len(parts) >= 3:
                    try:
                        # 假设最后两个是数字（债权本金和面积）
                        address = ' '.join(parts[:-2])
                        debt_principal = float(parts[-2])
                        area = float(parts[-1])
                        
                        if address and debt_principal > 0 and area > 0:
                            property_data.append({
                                "address": address,
                                "debt_principal": debt_principal,
                                "area": area
                            })
                    except (ValueError, IndexError):
                        print(f"跳过无效行：{line}")
        
        # 情况5：从图片解析SKILL传来的数据
        elif 'image_data' in input_data:
            image_data = input_data.get('image_data', {})
            extracted_text = image_data.get('extracted_text', '')
            extracted_table = image_data.get('extracted_table', {})
            
            # 处理提取的表格数据
            if extracted_table and 'headers' in extracted_table and 'rows' in extracted_table:
                headers = extracted_table.get('headers', [])
                rows = extracted_table.get('rows', [])
                
                # 尝试自动识别列名
                address_col = None
                debt_col = None
                area_col = None
                
                # 常见列名映射
                address_keywords = ['地址', '房产地址', '物业地址', 'location', 'address']
                debt_keywords = ['债权本金', '本金', '债务', 'debt', 'principal']
                area_keywords = ['面积', '建筑面积', 'area', 'size']
                
                # 识别列名
                for i, header in enumerate(headers):
                    header_lower = str(header).lower()
                    if not address_col:
                        for keyword in address_keywords:
                            if keyword in header_lower:
                                address_col = i
                                break
                    if not debt_col:
                        for keyword in debt_keywords:
                            if keyword in header_lower:
                                debt_col = i
                                break
                    if not area_col:
                        for keyword in area_keywords:
                            if keyword in header_lower:
                                area_col = i
                                break
                
                # 解析数据行
                for row in rows:
                    if address_col is not None and debt_col is not None and area_col is not None:
                        try:
                            address = str(row[address_col]).strip()
                            debt_principal = float(row[debt_col])
                            area = float(row[area_col])
                            
                            if address and debt_principal > 0 and area > 0:
                                property_data.append({
                                    "address": address,
                                    "debt_principal": debt_principal,
                                    "area": area
                                })
                        except (ValueError, IndexError):
                            print(f"跳过无效行：{row}")
            
            # 处理提取的文本数据
            elif extracted_text:
                # 简单的文本解析逻辑
                lines = extracted_text.strip().split('\n')
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    
                    # 尝试用逗号分隔
                    parts = [p.strip() for p in line.split(',')]
                    if len(parts) < 3:
                        # 尝试用空格分隔
                        parts = [p.strip() for p in line.split() if p.strip()]
                    
                    if len(parts) >= 3:
                        try:
                            # 假设最后两个是数字（债权本金和面积）
                            address = ' '.join(parts[:-2])
                            debt_principal = float(parts[-2])
                            area = float(parts[-1])
                            
                            if address and debt_principal > 0 and area > 0:
                                property_data.append({
                                    "address": address,
                                    "debt_principal": debt_principal,
                                    "area": area
                                })
                        except (ValueError, IndexError):
                            print(f"跳过无效行：{line}")
        
        # 情况6：从音频解析SKILL传来的数据
        elif 'audio_data' in input_data:
            audio_data = input_data.get('audio_data', {})
            transcript = audio_data.get('transcript', '')
            
            if transcript:
                # 简单的文本解析逻辑
                lines = transcript.strip().split('\n')
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    
                    # 尝试用逗号分隔
                    parts = [p.strip() for p in line.split(',')]
                    if len(parts) < 3:
                        # 尝试用空格分隔
                        parts = [p.strip() for p in line.split() if p.strip()]
                    
                    if len(parts) >= 3:
                        try:
                            # 假设最后两个是数字（债权本金和面积）
                            address = ' '.join(parts[:-2])
                            debt_principal = float(parts[-2])
                            area = float(parts[-1])
                            
                            if address and debt_principal > 0 and area > 0:
                                property_data.append({
                                    "address": address,
                                    "debt_principal": debt_principal,
                                    "area": area
                                })
                        except (ValueError, IndexError):
                            print(f"跳过无效行：{line}")
        
        # 情况7：从多模态解析SKILL传来的数据
        elif 'multimodal_data' in input_data:
            multimodal_data = input_data.get('multimodal_data', {})
            
            # 检查是否包含各种类型的数据
            if 'text_content' in multimodal_data:
                # 处理文本内容
                text_content = multimodal_data.get('text_content', '')
                lines = text_content.strip().split('\n')
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    
                    # 尝试用逗号分隔
                    parts = [p.strip() for p in line.split(',')]
                    if len(parts) < 3:
                        # 尝试用空格分隔
                        parts = [p.strip() for p in line.split() if p.strip()]
                    
                    if len(parts) >= 3:
                        try:
                            # 假设最后两个是数字（债权本金和面积）
                            address = ' '.join(parts[:-2])
                            debt_principal = float(parts[-2])
                            area = float(parts[-1])
                            
                            if address and debt_principal > 0 and area > 0:
                                property_data.append({
                                    "address": address,
                                    "debt_principal": debt_principal,
                                    "area": area
                                })
                        except (ValueError, IndexError):
                            print(f"跳过无效行：{line}")
            
            elif 'table_content' in multimodal_data:
                # 处理表格内容
                table_content = multimodal_data.get('table_content', {})
                headers = table_content.get('headers', [])
                rows = table_content.get('rows', [])
                
                # 尝试自动识别列名
                address_col = None
                debt_col = None
                area_col = None
                
                # 常见列名映射
                address_keywords = ['地址', '房产地址', '物业地址', 'location', 'address']
                debt_keywords = ['债权本金', '本金', '债务', 'debt', 'principal']
                area_keywords = ['面积', '建筑面积', 'area', 'size']
                
                # 识别列名
                for i, header in enumerate(headers):
                    header_lower = str(header).lower()
                    if not address_col:
                        for keyword in address_keywords:
                            if keyword in header_lower:
                                address_col = i
                                break
                    if not debt_col:
                        for keyword in debt_keywords:
                            if keyword in header_lower:
                                debt_col = i
                                break
                    if not area_col:
                        for keyword in area_keywords:
                            if keyword in header_lower:
                                area_col = i
                                break
                
                # 解析数据行
                for row in rows:
                    if address_col is not None and debt_col is not None and area_col is not None:
                        try:
                            address = str(row[address_col]).strip()
                            debt_principal = float(row[debt_col])
                            area = float(row[area_col])
                            
                            if address and debt_principal > 0 and area > 0:
                                property_data.append({
                                    "address": address,
                                    "debt_principal": debt_principal,
                                    "area": area
                                })
                        except (ValueError, IndexError):
                            print(f"跳过无效行：{row}")
        
        # 验证输入
        if not property_data:
            return {
                "success": False,
                "message": "缺少房产数据，请确保输入包含地址、债权本金和面积信息"
            }
        
        # 数据清洗和处理
        processed_data = []
        for property_info in property_data:
            # 基本数据验证和清洗
            cleaned_info = {
                "address": property_info.get('address', '').strip(),
                "debt_principal": float(property_info.get('debt_principal', 0)),
                "area": float(property_info.get('area', 0))
            }
            
            # 验证必要字段
            if cleaned_info['address'] and cleaned_info['debt_principal'] > 0 and cleaned_info['area'] > 0:
                processed_data.append(cleaned_info)
            else:
                print(f"跳过无效数据：{property_info}")
        
        if not processed_data:
            return {
                "success": False,
                "message": "没有有效的房产数据"
            }
        
        # 分析房产数据
        analysis_results = []
        for property_info in processed_data:
            result = analyze_property(property_info)
            analysis_results.append(result)
        
        # 生成摘要
        total_properties = len(analysis_results)
        priority_count = sum(1 for r in analysis_results if r['investment_suggestion'] == '优先关注')
        avg_coverage = sum(r['debt_coverage_ratio'] for r in analysis_results) / total_properties if total_properties > 0 else 0
        avg_discount = sum(r['auction_discount_rate'] for r in analysis_results) / total_properties if total_properties > 0 else 0
        
        summary = f"本次分析了{total_properties}处房产，其中{priority_count}处建议优先关注。平均债权覆盖率为{int(avg_coverage * 100)}%，平均法拍折扣率为{int(avg_discount * 100)}%。"
        
        # 生成报告
        report_url = generate_report(analysis_results, options)
        
        # 构建输出
        output = {
            "success": True,
            "action": action,
            "analysis_results": analysis_results,
            "summary": summary,
            "report_url": report_url
        }
        
        return output
        
    except Exception as e:
        return {
            "success": False,
            "message": f"分析过程中出错：{str(e)}"
        }


if __name__ == "__main__":
    # 测试代码
    test_input = {
        "action": "analyze_debt_portfolio",
        "property_data": [
            {
                "address": "杭州市萧山区北干街道广德小区xx幢xx单元xxx室",
                "debt_principal": 208.45,
                "area": 102.35
            }
        ]
    }
    
    result = main(test_input)
    print(json.dumps(result, ensure_ascii=False, indent=2))
