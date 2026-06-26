#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""更新 canon_bible.json 的 pending_setups 字段"""

import json
from pathlib import Path

canon_file = Path("C:/Users/huang/.openclaw/workspace/story/meta/canon_bible.json")

# 读取 canon_bible
with open(canon_file, 'r', encoding='utf-8-sig') as f:
    canon = json.load(f)

continuity = canon.get('continuity', {})
setups = continuity.get('setups', [])
payoffs = continuity.get('payoffs', [])

# 计算已兑现的铺垫 ID
paid_ids = set()
for p in payoffs:
    setup_id = p.get('original_setup') or p.get('id', '')
    if setup_id:
        paid_ids.add(setup_id)

# 计算 pending_setups：未兑现 + 活跃状态
pending_setups = [
    s for s in setups 
    if s.get('id') not in paid_ids 
    and s.get('status', 'active') == 'active'
]

# 添加到 continuity
continuity['pending_setups'] = pending_setups

# 更新 setup_health
continuity['setup_health'] = {
    'short': len([s for s in pending_setups if s.get('type') == 'short']),
    'medium': len([s for s in pending_setups if s.get('type') == 'medium']),
    'long': len([s for s in pending_setups if s.get('type') == 'long']),
    'ongoing': len([s for s in pending_setups if s.get('type') == 'ongoing']),
    'total': len(pending_setups),
    'expired': 0,
    'last_check_chapter': canon.get('_meta', {}).get('last_chapter', 0)
}

# 保存
with open(canon_file, 'w', encoding='utf-8') as f:
    json.dump(canon, f, ensure_ascii=False, indent=2)

print(f"[OK] Updated pending_setups: {len(pending_setups)} items")
print(f"  - short: {continuity['setup_health']['short']}")
print(f"  - medium: {continuity['setup_health']['medium']}")
print(f"  - long: {continuity['setup_health']['long']}")
print(f"  - ongoing: {continuity['setup_health']['ongoing']}")
