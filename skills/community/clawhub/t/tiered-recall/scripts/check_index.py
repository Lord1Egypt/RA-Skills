import json
from pathlib import Path

index_file = Path('C:/Windows/System32/UsersAdministrator.openclawworkspace/.tiered-recall/index.json')
with open(index_file, 'r', encoding='utf-8') as f:
    index = json.load(f)

# 显示索引大小
print('=== 索引信息 ===')
print('文件大小:', round(index_file.stat().st_size/1024, 1), 'KB')
print('主题数:', len(index['topics']))
print()

# 显示一个主题的示例（带标题和摘要）
print('=== 示例：搞钱特战队（前5条）===')
for entry in index['topics']['搞钱特战队'][:5]:
    print('  文件:', entry['f'])
    print('  行号:', entry['l'])
    print('  标题:', entry['t'])
    print('  摘要:', entry.get('s', '无'))
    print()