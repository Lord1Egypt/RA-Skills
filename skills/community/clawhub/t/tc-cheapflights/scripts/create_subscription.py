#!/usr/bin/env python3
"""
订阅管理脚本 - 简化版
创建、管理价格订阅任务
"""

import json
import os
import logging
from datetime import datetime
import uuid

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_subscription(params: dict) -> dict:
    """
    创建订阅（简化版）
    
    Args:
        params: 查询参数
        
    Returns:
        创建的订阅信息
    """
    # 生成订阅ID
    subscription_id = f"sub_{uuid.uuid4().hex[:8]}"
    
    # 创建订阅对象
    subscription = {
        'subscription_id': subscription_id,
        'from_city': params.get('from_city'),
        'to_city': params.get('to_city'),
        'date': params.get('date'),
        'type': params.get('type', 'flight'),
        'status': 'active',
        'created_at': datetime.now().isoformat(),
        'check_interval_hours': 6,
        'price_drop_threshold': 5.0
    }
    
    # 保存到文件
    data_file = 'subscriptions.json'
    subscriptions = []
    
    if os.path.exists(data_file):
        with open(data_file, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                subscriptions = data.get('subscriptions', [])
            except:
                subscriptions = []
    
    subscriptions.append(subscription)
    
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump({'subscriptions': subscriptions}, f, ensure_ascii=False, indent=2)
    
    logger.info(f"创建订阅成功: {subscription_id}")
    return subscription

def list_subscriptions() -> list:
    """
    列出所有订阅
    
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

def main():
    """主函数"""
    import sys
    
    if len(sys.argv) < 2:
        print("用法:")
        print("  python create_subscription.py create '查询参数JSON'")
        print("  python create_subscription.py list")
        print("示例:")
        print('  python create_subscription.py create \'{"from_city": "北京", "to_city": "上海", "date": "2026-03-16"}\'')
        sys.exit(1)
    
    action = sys.argv[1]
    
    if action == 'create':
        if len(sys.argv) < 3:
            print("错误: 需要查询参数JSON")
            sys.exit(1)
        
        try:
            params = json.loads(sys.argv[2])
            subscription = create_subscription(params)
            print(f"创建订阅成功:")
            print(json.dumps(subscription, ensure_ascii=False, indent=2))
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
            sys.exit(1)
    
    elif action == 'list':
        subscriptions = list_subscriptions()
        print(f"当前订阅 ({len(subscriptions)} 个):")
        for sub in subscriptions:
            print(f"  {sub['subscription_id']}: {sub['from_city']}→{sub['to_city']} ({sub['date']})")
    
    else:
        print(f"未知操作: {action}")
        sys.exit(1)

if __name__ == '__main__':
    main()