#!/usr/bin/env python3
"""
价格监控脚本 - 简化版
定时检查订阅的价格变化
"""

import json
import os
import logging
from datetime import datetime
import time

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_subscriptions() -> list:
    """
    加载订阅列表
    
    Returns:
        订阅列表
    """
    data_file = 'subscriptions.json'
    
    if not os.path.exists(data_file):
        return []
    
    with open(data_file, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            return data.get('subscriptions', [])
        except:
            return []

def check_subscription(subscription: dict):
    """
    检查单个订阅的价格
    
    Args:
        subscription: 订阅信息
        
    Returns:
        价格检查结果
    """
    from natural_language_parser import NaturalLanguageParser
    from tongcheng_api import TongchengAPI
    
    try:
        # 解析查询参数
        query_text = f"{subscription['from_city']}到{subscription['to_city']}的机票"
        if subscription.get('date'):
            query_text += f"，{subscription['date']}"
        
        parser = NaturalLanguageParser()
        params = parser.parse(query_text)
        
        # 查询价格
        api = TongchengAPI()
        flights = api.query_flights(
            from_city=params['from_city'],
            to_city=params['to_city'],
            date=params['date']
        )
        
        if not flights:
            logger.warning(f"订阅 {subscription['subscription_id']} 未查询到航班")
            return None
        
        # 获取最低价格
        prices = [f['price'] for f in flights if 'price' in f]
        if not prices:
            return None
        
        min_price = min(prices)
        
        # 记录价格历史
        record_price_history(
            subscription['subscription_id'],
            min_price,
            subscription['from_city'],
            subscription['to_city']
        )
        
        # 检查降价
        check_price_drop(subscription, min_price)
        
        return {
            'subscription_id': subscription['subscription_id'],
            'min_price': min_price,
            'flight_count': len(flights),
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"检查订阅 {subscription['subscription_id']} 失败: {e}")
        return None

def record_price_history(subscription_id: str, price: float, from_city: str, to_city: str):
    """
    记录价格历史
    
    Args:
        subscription_id: 订阅ID
        price: 价格
        from_city: 出发城市
        to_city: 到达城市
    """
    history_file = 'price_history.json'
    
    # 加载现有历史
    history_data = {}
    if os.path.exists(history_file):
        with open(history_file, 'r', encoding='utf-8') as f:
            try:
                history_data = json.load(f)
            except:
                history_data = {}
    
    # 初始化订阅历史
    if subscription_id not in history_data:
        history_data[subscription_id] = []
    
    # 添加历史记录
    history_entry = {
        'timestamp': datetime.now().isoformat(),
        'price': price,
        'from_city': from_city,
        'to_city': to_city
    }
    
    history_data[subscription_id].append(history_entry)
    
    # 只保留最近50条记录
    if len(history_data[subscription_id]) > 50:
        history_data[subscription_id] = history_data[subscription_id][-50:]
    
    # 保存
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(history_data, f, ensure_ascii=False, indent=2)

def check_price_drop(subscription: dict, current_price: float):
    """
    检查价格下降
    
    Args:
        subscription: 订阅信息
        current_price: 当前价格
    """
    # 这里可以添加价格下降检查逻辑
    # 例如：比较历史最低价，发送通知等
    pass

def check_all_subscriptions():
    """
    检查所有订阅
    """
    subscriptions = load_subscriptions()
    
    if not subscriptions:
        logger.info("没有需要检查的订阅")
        return
    
    logger.info(f"开始检查 {len(subscriptions)} 个订阅")
    
    for sub in subscriptions:
        if sub.get('status') != 'active':
            continue
        
        result = check_subscription(sub)
        if result:
            logger.info(f"订阅 {sub['subscription_id']}: 最低价格 ¥{result['min_price']}")
        
        # 避免请求过于频繁
        time.sleep(1)
    
    logger.info("所有订阅检查完成")

def main():
    """主函数"""
    import sys
    
    if len(sys.argv) < 2:
        print("用法:")
        print("  python monitor_prices.py check-all   # 检查所有订阅")
        print("  python monitor_prices.py check <subscription_id>  # 检查单个订阅")
        print("  python monitor_prices.py history <subscription_id>  # 查看价格历史")
        sys.exit(1)
    
    action = sys.argv[1]
    
    if action == 'check-all':
        check_all_subscriptions()
    
    elif action == 'check':
        if len(sys.argv) < 3:
            print("错误: 需要订阅ID")
            sys.exit(1)
        
        subscription_id = sys.argv[2]
        subscriptions = load_subscriptions()
        
        subscription = None
        for sub in subscriptions:
            if sub['subscription_id'] == subscription_id:
                subscription = sub
                break
        
        if not subscription:
            print(f"订阅不存在: {subscription_id}")
            sys.exit(1)
        
        result = check_subscription(subscription)
        if result:
            print(f"检查结果:")
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print("检查失败")
    
    elif action == 'history':
        if len(sys.argv) < 3:
            print("错误: 需要订阅ID")
            sys.exit(1)
        
        subscription_id = sys.argv[2]
        history_file = 'price_history.json'
        
        if not os.path.exists(history_file):
            print("没有价格历史记录")
            sys.exit(0)
        
        with open(history_file, 'r', encoding='utf-8') as f:
            try:
                history_data = json.load(f)
            except:
                history_data = {}
        
        history = history_data.get(subscription_id, [])
        
        if not history:
            print(f"订阅 {subscription_id} 没有价格历史")
        else:
            print(f"订阅 {subscription_id} 价格历史 ({len(history)} 条):")
            for entry in history[-10:]:  # 显示最近10条
                print(f"  {entry['timestamp']}: ¥{entry['price']} ({entry['from_city']}→{entry['to_city']})")
    
    else:
        print(f"未知操作: {action}")
        sys.exit(1)

if __name__ == '__main__':
    main()