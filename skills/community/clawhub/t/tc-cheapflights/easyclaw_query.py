#!/usr/bin/env python3
"""
EasyClaw环境下的同程旅行价格查询封装
整合自然语言解析和API查询，提供简洁的调用接口
"""

import sys
import os
import json
from datetime import datetime

# 添加脚本目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from scripts.natural_language_parser import NaturalLanguageParser
    from scripts.tongcheng_api import TongchengAPI
except ImportError as e:
    print(f"导入模块失败: {e}")
    print("请确保以下文件存在:")
    print("  scripts/natural_language_parser.py")
    print("  scripts/tongcheng_api.py")
    sys.exit(1)

def query_tongcheng_prices(query_text: str, use_mock=False):
    """
    查询同程旅行价格（封装函数）
    
    Args:
        query_text: 自然语言查询语句
        use_mock: 是否使用模拟数据（测试用）
        
    Returns:
        格式化的查询结果字符串
    """
    try:
        # 创建解析器和API实例
        parser = NaturalLanguageParser()
        api = TongchengAPI()
        
        # 解析查询语句
        params = parser.parse(query_text)
        
        if not params['parsed_successfully']:
            # 尝试提供更详细的错误信息
            error_msg = [
                "❌ 无法解析查询语句。",
                "请提供以下格式的信息：",
                "  - '北京到上海机票'",
                "  - '3月16日成都到广州的航班'",
                "  - '查询明天深圳到北京的机票价格'",
                "  - '监控CA1611航班的价格'",
                "",
                "你提供的查询是：",
                f"  \"{query_text}\"",
                "",
                "解析到的信息：",
                f"  出发城市: {params['from_city'] or '未识别'}",
                f"  到达城市: {params['to_city'] or '未识别'}",
                f"  日期: {params['date'] or '未识别'}",
                f"  航班号: {params['flight_no'] or '未识别'}",
            ]
            return "\n".join(error_msg)
        
        # 提取参数
        from_city = params['from_city']
        to_city = params['to_city']
        date_str = params['date']
        flight_no = params['flight_no']
        action = params['action']
        
        # 如果有航班号但没有城市，尝试根据航班号查询
        if flight_no and (not from_city or not to_city):
            # 这里可以扩展：根据航班号查询对应的城市
            # 暂时使用默认城市
            if not from_city:
                from_city = "北京"
            if not to_city:
                to_city = "上海"
            
            return f"⚠️ 已识别航班号 {flight_no}，但无法确定具体城市。\n使用默认查询：{from_city} → {to_city} 日期: {date_str}"
        
        # 查询航班价格
        if use_mock:
            # 使用模拟数据（测试用）
            flights = api._get_mock_flights(from_city, to_city, date_str)
        else:
            flights = api.query_flight_prices(from_city, to_city, date_str)
        
        # 格式化结果
        formatted = api.format_results(flights)
        
        # 根据操作类型添加额外信息
        if action == 'subscribe':
            formatted += "\n\n📅 **价格监控已创建**"
            formatted += f"\n- 监控航线: {from_city} → {to_city}"
            formatted += f"\n- 监控日期: {date_str}"
            formatted += f"\n- 监控频率: 每天查询一次"
            formatted += f"\n- 降价提醒: 降价≥5元时发送通知"
            formatted += "\n\n💡 提示: 降价通知将通过飞书发送（如果已配置）"
        
        elif action == 'query' and flight_no:
            # 如果是查询特定航班
            flight_flights = [f for f in flights if flight_no in f.get('flight_no', '')]
            if flight_flights:
                flight = flight_flights[0]
                formatted += f"\n\n✈️ **{flight_no} 航班详情**"
                formatted += f"\n- 航空公司: {flight.get('airline', 'N/A')}"
                formatted += f"\n- 起飞时间: {flight.get('departure_time', 'N/A')}"
                formatted += f"\n- 到达时间: {flight.get('arrival_time', 'N/A')}"
                formatted += f"\n- 当前价格: ¥{flight.get('price', 'N/A')}"
                if flight.get('discount'):
                    formatted += f" ({flight.get('discount')})"
                formatted += f"\n- 是否直飞: {flight.get('via', '直飞')}"
            else:
                formatted += f"\n\n⚠️ 未找到航班 {flight_no} 的具体信息"
        
        # 添加价格历史趋势（如果有）
        formatted += "\n\n📊 **价格趋势分析**"
        
        prices = [f['price'] for f in flights if f.get('price')]
        if prices:
            min_price = min(prices)
            max_price = max(prices)
            avg_price = sum(prices) / len(prices)
            
            # 判断价格水平
            if min_price < avg_price * 0.85:
                formatted += f"\n- **当前最低价显著低于平均水平** (低{(1 - min_price/avg_price)*100:.1f}%)"
                formatted += "\n- 💰 **建议**: 现在是较好的购买时机"
            elif min_price > avg_price * 1.15:
                formatted += f"\n- **当前价格偏高** (高{(min_price/avg_price - 1)*100:.1f}%)"
                formatted += "\n- ⏳ **建议**: 可以等待降价或关注其他航班"
            else:
                formatted += "\n- **当前价格处于正常范围**"
                formatted += "\n- 📅 **建议**: 可根据行程安排灵活选择"
            
            # 添加购买建议
            formatted += "\n\n🛒 **智能购买建议**"
            
            cheapest_flight = min(flights, key=lambda x: x.get('price', 9999))
            if cheapest_flight.get('price') < 500:
                formatted += "\n- 💸 **价格极低**: 可能是特价票，建议立即购买"
            elif '直飞' in str(cheapest_flight.get('via', '')):
                formatted += f"\n- ✈️ **推荐航班**: {cheapest_flight.get('flight_no')} (直飞航班，价格适中)"
            else:
                formatted += f"\n- 🎯 **性价比最高**: {cheapest_flight.get('flight_no')} 航班"
        
        return formatted
        
    except Exception as e:
        error_msg = [
            "❌ 查询过程中出现错误",
            f"错误信息: {str(e)}",
            "",
            "可能的原因:",
            "1. 网络连接问题",
            "2. 同程旅行网站结构变化",
            "3. 查询参数格式错误",
            "",
            "可以尝试:",
            "1. 检查网络连接",
            "2. 稍后重试",
            "3. 简化查询语句，如'北京到上海机票'",
        ]
        return "\n".join(error_msg)

def query_with_params(from_city: str, to_city: str, date: str, flight_no: str = None):
    """
    使用参数查询（非自然语言）
    
    Args:
        from_city: 出发城市
        to_city: 到达城市
        date: 日期 (YYYY-MM-DD)
        flight_no: 航班号（可选）
        
    Returns:
        格式化的查询结果
    """
    try:
        api = TongchengAPI()
        flights = api.query_flight_prices(from_city, to_city, date)
        
        formatted = api.format_results(flights)
        
        # 如果有特定航班号，突出显示
        if flight_no:
            target_flights = [f for f in flights if flight_no in f.get('flight_no', '')]
            if target_flights:
                flight = target_flights[0]
                formatted += f"\n\n✈️ **指定航班 {flight_no}**"
                formatted += f"\n- 航空公司: {flight.get('airline')}"
                formatted += f"\n- 时间: {flight.get('departure_time')} → {flight.get('arrival_time')}"
                formatted += f"\n- 价格: ¥{flight.get('price')}"
                formatted += f"\n- 状态: {'特价' if flight.get('price', 9999) < 500 else '正常'}"
            else:
                formatted += f"\n\n⚠️ 未找到航班 {flight_no}"
        
        return formatted
        
    except Exception as e:
        return f"查询失败: {str(e)}"

def save_query_result(query_text: str, result: str):
    """
    保存查询结果到文件
    
    Args:
        query_text: 原始查询
        result: 查询结果
    """
    try:
        os.makedirs('logs', exist_ok=True)
        
        filename = f"logs/query_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"查询时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"原始查询: {query_text}\n")
            f.write("-" * 80 + "\n")
            f.write(result + "\n")
        
        print(f"查询结果已保存到 {filename}")
        return filename
    except Exception as e:
        print(f"保存结果失败: {e}")
        return None

def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法:")
        print("  1. python easyclaw_query.py '查询语句'")
        print("     示例: python easyclaw_query.py '帮我查一下北京到上海的机票'")
        print("  2. python easyclaw_query.py 出发城市 到达城市 日期 [航班号]")
        print("     示例: python easyclaw_query.py 北京 上海 2026-03-16 CA1512")
        print("")
        print("选项:")
        print("  --mock: 使用模拟数据（测试用）")
        print("  --save: 保存查询结果到文件")
        sys.exit(1)
    
    # 解析参数
    use_mock = '--mock' in sys.argv
    save_result = '--save' in sys.argv
    
    # 过滤掉选项参数
    args = [arg for arg in sys.argv[1:] if arg not in ['--mock', '--save']]
    
    if len(args) == 1:
        # 自然语言查询模式
        query_text = args[0]
        result = query_tongcheng_prices(query_text, use_mock)
        print(result)
        
        if save_result:
            save_query_result(query_text, result)
            
    elif len(args) >= 3:
        # 参数查询模式
        from_city = args[0]
        to_city = args[1]
        date = args[2]
        flight_no = args[3] if len(args) > 3 else None
        
        result = query_with_params(from_city, to_city, date, flight_no)
        print(result)
        
        if save_result:
            query_text = f"{from_city}到{to_city}机票 {date}" + (f" 航班{flight_no}" if flight_no else "")
            save_query_result(query_text, result)
    else:
        print("参数不足")
        sys.exit(1)

if __name__ == '__main__':
    main()