#!/usr/bin/env python3
"""
通知发送脚本 - 简化版
发送降价通知到飞书等平台
"""

import json
import logging
import requests

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_config():
    """
    加载配置文件
    
    Returns:
        配置字典
    """
    config_file = 'config.json'
    
    if not os.path.exists(config_file):
        return {}
    
    with open(config_file, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except:
            return {}

def send_feishu_notification(webhook_url: str, message: dict) -> bool:
    """
    发送飞书通知
    
    Args:
        webhook_url: 飞书webhook地址
        message: 消息内容
        
    Returns:
        是否发送成功
    """
    try:
        headers = {
            'Content-Type': 'application/json'
        }
        
        response = requests.post(
            webhook_url,
            json=message,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            logger.info("飞书通知发送成功")
            return True
        else:
            logger.error(f"飞书通知发送失败: {response.status_code}, {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"飞书通知发送异常: {e}")
        return False

def create_price_drop_message(subscription: dict, old_price: float, new_price: float) -> dict:
    """
    创建降价通知消息
    
    Args:
        subscription: 订阅信息
        old_price: 原价
        new_price: 现价
        
    Returns:
        飞书消息格式
    """
    price_drop = old_price - new_price
    drop_percentage = (price_drop / old_price) * 100
    
    message = {
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": "🎉 机票降价提醒"
                },
                "template": "green"
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": f"**航线**: {subscription['from_city']} → {subscription['to_city']}\n"
                                   f"**日期**: {subscription['date']}\n"
                                   f"**航班类型**: {subscription.get('type', '机票')}"
                    }
                },
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": f"**原价**: ¥{old_price:.2f}\n"
                                   f"**现价**: ¥{new_price:.2f}\n"
                                   f"**降价**: ¥{price_drop:.2f} ({drop_percentage:.1f}%)"
                    }
                },
                {
                    "tag": "action",
                    "actions": [
                        {
                            "tag": "button",
                            "text": {
                                "tag": "plain_text",
                                "content": "立即查询"
                            },
                            "type": "primary",
                            "url": f"https://www.ly.com/flights/itinerary/oneway/{subscription['from_city']}-{subscription['to_city']}?date={subscription['date']}"
                        }
                    ]
                }
            ]
        }
    }
    
    return message

def send_price_drop_alert(subscription: dict, old_price: float, new_price: float) -> bool:
    """
    发送降价提醒
    
    Args:
        subscription: 订阅信息
        old_price: 原价
        new_price: 现价
        
    Returns:
        是否发送成功
    """
    config = load_config()
    webhook_url = config.get('feishu_webhook')
    
    if not webhook_url:
        logger.warning("未配置飞书webhook，跳过通知发送")
        return False
    
    # 创建消息
    message = create_price_drop_message(subscription, old_price, new_price)
    
    # 发送通知
    return send_feishu_notification(webhook_url, message)

def send_query_result_notification(query: str, results: list) -> bool:
    """
    发送查询结果通知
    
    Args:
        query: 查询语句
        results: 查询结果
        
    Returns:
        是否发送成功
    """
    config = load_config()
    webhook_url = config.get('feishu_webhook')
    
    if not webhook_url:
        logger.warning("未配置飞书webhook，跳过通知发送")
        return False
    
    if not results:
        message = {
            "msg_type": "text",
            "content": {
                "text": f"📊 查询结果\n查询: {query}\n结果: 未找到相关航班"
            }
        }
    else:
        # 取前3个航班
        top_flights = results[:3]
        flights_text = "\n".join([
            f"{i+1}. {f.get('flight_no', 'N/A')}: ¥{f.get('price', 'N/A')} ({f.get('departure_time', 'N/A')}→{f.get('arrival_time', 'N/A')})"
            for i, f in enumerate(top_flights)
        ])
        
        message = {
            "msg_type": "text",
            "content": {
                "text": f"📊 机票查询结果\n查询: {query}\n\n**推荐航班**:\n{flights_text}\n\n共找到 {len(results)} 个航班"
            }
        }
    
    return send_feishu_notification(webhook_url, message)

def main():
    """主函数"""
    import sys
    import os
    
    if len(sys.argv) < 2:
        print("用法:")
        print("  python send_notification.py price-drop '订阅JSON' 原价 现价")
        print("  python send_notification.py query-result '查询语句' '结果JSON'")
        print("示例:")
        print('  python send_notification.py price-drop \'{"from_city":"北京","to_city":"上海","date":"2026-03-16"}\' 800 750')
        print('  python send_notification.py query-result "北京到上海机票" \'[{"flight_no":"CA1501","price":680}]\'')
        sys.exit(1)
    
    action = sys.argv[1]
    
    if action == 'price-drop':
        if len(sys.argv) < 5:
            print("错误: 需要订阅JSON、原价和现价")
            sys.exit(1)
        
        try:
            subscription = json.loads(sys.argv[2])
            old_price = float(sys.argv[3])
            new_price = float(sys.argv[4])
            
            success = send_price_drop_alert(subscription, old_price, new_price)
            if success:
                print("降价通知发送成功")
            else:
                print("降价通知发送失败")
                
        except (json.JSONDecodeError, ValueError) as e:
            print(f"参数错误: {e}")
            sys.exit(1)
    
    elif action == 'query-result':
        if len(sys.argv) < 4:
            print("错误: 需要查询语句和结果JSON")
            sys.exit(1)
        
        try:
            query = sys.argv[2]
            results = json.loads(sys.argv[3])
            
            success = send_query_result_notification(query, results)
            if success:
                print("查询结果通知发送成功")
            else:
                print("查询结果通知发送失败")
                
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
            sys.exit(1)
    
    else:
        print(f"未知操作: {action}")
        sys.exit(1)

if __name__ == '__main__':
    main()