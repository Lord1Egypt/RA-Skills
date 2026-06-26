#!/usr/bin/env python3
import json
import re
import sys

text = sys.stdin.read().strip() if not sys.argv[1:] else ' '.join(sys.argv[1:]).strip()

patterns = [
    ('price', [r'最低', r'便宜', r'少点', r'多少钱出', r'包邮', r'刀不刀', r'砍价']),
    ('tech', [r'成色', r'划痕', r'电池', r'维修', r'拆修', r'配件', r'功能', r'型号', r'尺寸', r'参数']),
    ('delivery', [r'发货', r'自提', r'同城', r'快递', r'什么时候发']),
    ('after-sales', [r'退', r'换', r'保修', r'售后', r'有问题怎么办']),
]

intent = 'default'
for name, regs in patterns:
    if any(re.search(p, text, re.I) for p in regs):
        intent = name
        break

print(json.dumps({'intent': intent, 'text': text}, ensure_ascii=False))
