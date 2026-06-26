#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from datetime import datetime

# 读取 canon_bible.json
with open('C:/Users/huang/.openclaw/workspace/story/meta/canon_bible.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 添加第4章的铺垫
new_setups = [
    {
        'id': 'setup_ch4_001',
        'type': 'short',
        'setup': '东陆金控将在2021年Q2资金链断裂，73%概率',
        'chapter': 4,
        'expected_payoff_range': [5, 15],
        'priority': 'high',
        'status': 'active'
    },
    {
        'id': 'setup_ch4_002',
        'type': 'medium',
        'setup': '林晚晴被系统标记为隐藏变量，她在这个时间线上已存在',
        'chapter': 4,
        'expected_payoff_range': [5, 20],
        'priority': 'medium',
        'status': 'active'
    },
    {
        'id': 'setup_ch4_003',
        'type': 'short',
        'setup': '赵家与东陆金控的关联开始显现',
        'chapter': 4,
        'expected_payoff_range': [5, 10],
        'priority': 'high',
        'status': 'active'
    }
]

# 添加第4章的兑现
new_payoffs = [
    {
        'id': 'payoff_ch4_001',
        'original_setup': 'setup_ch2_002',
        'payoff': '陈安开始追踪赵家的商业布局',
        'chapter': 4,
        'type': 'partial'
    },
    {
        'id': 'payoff_ch4_002',
        'original_setup': 'setup_ch2_003',
        'payoff': '系统功能部分恢复',
        'chapter': 4,
        'type': 'partial'
    }
]

# 更新数据
data['continuity']['setups'].extend(new_setups)
data['continuity']['payoffs'].extend(new_payoffs)

# 重新计算 pending_setups
paid_ids = {p.get('original_setup') for p in data['continuity']['payoffs']}
pending = [s for s in data['continuity']['setups'] if s['id'] not in paid_ids and s.get('status') == 'active']
data['continuity']['pending_setups'] = pending

# 更新 setup_health
by_type = {'short': 0, 'medium': 0, 'long': 0, 'ongoing': 0}
for s in pending:
    t = s.get('type', 'medium')
    by_type[t] = by_type.get(t, 0) + 1

data['continuity']['setup_health'] = {
    'short': by_type['short'],
    'medium': by_type['medium'],
    'long': by_type['long'],
    'ongoing': by_type['ongoing'],
    'total': len(pending),
    'expired': 0,
    'last_check_chapter': 4
}

# 更新 _meta
data['_meta']['last_chapter'] = 4
data['_meta']['updated_at'] = datetime.now().isoformat()
data['_meta']['source'] = '第4章归档'

# 保存
with open('C:/Users/huang/.openclaw/workspace/story/meta/canon_bible.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('Canon bible updated for chapter 4')
print('Total setups:', len(data['continuity']['setups']))
print('Total payoffs:', len(data['continuity']['payoffs']))
print('Pending setups:', len(pending))
print('Setup health:', data['continuity']['setup_health'])
