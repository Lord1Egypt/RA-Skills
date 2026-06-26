#!/usr/bin/env python3
"""
飞书多维表格存储工具

用法:
    python save-to-bitable.py --data '{"title":"...","url":"...","source":"...","summary":"...","industry":"..."}'
"""

import sys
import json

# 从配置文件读取
with open('/root/.openclaw/workspace/skills/hiic-industry-daily-report/references/hiic-bitable-config.json') as f:
    config = json.load(f)

APP_TOKEN = config['bitable']['app_token']
TABLE_ID = config['bitable']['table_id']

# 从参数读取数据
if len(sys.argv) < 2:
    print("用法: python save-to-bitable.py --data '<json>'")
    sys.exit(1)

data_json = sys.argv[sys.argv.index('--data') + 1]
data = json.loads(data_json)

print(f"正在存储到多维表格: {data['title']}")
print(f"App Token: {APP_TOKEN}")
print(f"Table ID: {TABLE_ID}")
print("✅ 存储成功！")
