#!/usr/bin/env python3
"""
WeFlow JSON 数据解析器
提取微信聊天记录中的关键信息生成知识卡片
"""

import json
import sys
from datetime import datetime
from collections import Counter

def parse_weflow_json(file_path):
    """解析WeFlow导出的JSON文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def extract_knowledge(data):
    """从聊天数据中提取知识"""
    messages = data if isinstance(data, list) else [data]
    
    # 统计信息
    stats = {
        'total_messages': len(messages),
        'senders': Counter(),
        'keywords': Counter(),
        'time_range': {'start': None, 'end': None}
    }
    
    # 关键词列表（可根据业务调整）
    business_keywords = [
        '价格', '报价', '成本', '优惠', '折扣',
        '发货', '物流', '快递', '到货',
        '质量', '规格', '型号', '参数',
        '合同', '协议', '条款', '签字',
        '付款', '转账', '发票', '结算',
        '需求', '方案', '定制', '开发'
    ]
    
    knowledge = {
        '客户画像': [],
        '业务要点': [],
        '常用话术': [],
        '关键决策': []
    }
    
    # 简单统计
    for msg in messages:
        if 'talker' in msg:
            stats['senders'][msg['talker']] += 1
        
        content = msg.get('content', '')
        for keyword in business_keywords:
            if keyword in content:
                stats['keywords'][keyword] += 1
    
    return stats, knowledge

def generate_knowledge_card(data, output_path='knowledge_card.md'):
    """生成知识卡片"""
    stats, knowledge = extract_knowledge(data)
    
    card = f"""# 微信聊天知识卡片

## 📊 基本统计

| 指标 | 数值 |
|------|------|
| 总消息数 | {stats['total_messages']} |
| 参与人数 | {len(stats['senders'])} |

## 👥 活跃用户

{chr(10).join([f"- {name}: {count}条消息" for name, count in stats['senders'].most_common(10)])}

## 🔑 高频关键词

{chr(10).join([f"- **{keyword}**: {count}次" for keyword, count in stats['keywords'].most_common(15)])}

## 📝 知识摘要

（请根据实际聊天内容手动补充）

### 客户需求
-

### 关键约定
-

### 跟进事项
-

---
*由 wechat-knowledge-builder 自动生成 | {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(card)
    
    print(f"✅ 知识卡片已生成: {output_path}")
    return output_path

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python parse_weflow.py <weflow_json_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    data = parse_weflow_json(file_path)
    generate_knowledge_card(data)
