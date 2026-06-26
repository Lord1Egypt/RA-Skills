#!/usr/bin/env python3
"""修复 pairing-server.js 的 req.url → urlPath 问题"""

import re

FILE = '/var/www/hermesai/pairing-server/pairing-server.js'

with open(FILE, 'r') as f:
    content = f.read()

# 修复1: urlPath.startsWith(http) → urlPath.startsWith('http')
old1 = 'urlPath.startsWith(http)'
new1 = "urlPath.startsWith('http')"
if old1 in content:
    content = content.replace(old1, new1, 1)
    print('✅ 修复1: 补全引号')
else:
    print('⚠️  修复1: 未找到模式（可能已修复）')

# 修复2: req.url.split(?) → urlPath.split('?') （在 urlPath 赋值行）
old2 = 'let urlPath = req.url.split(?)[0];'
new2 = "let urlPath = req.url.split('?')[0];"
if old2 in content:
    content = content.replace(old2, new2, 1)
    print('✅ 修复2: urlPath 赋值补全引号')
else:
    print('⚠️  修复2: 未找到模式')

# 修复3: 把所有 req.url === 替换成 urlPath ===
count3 = content.count("req.url === ")
if count3 > 0:
    content = content.replace("req.url === ", "urlPath === ")
    print(f'✅ 修复3: 替换 {count3} 处 req.url ===')
else:
    print('⚠️  修复3: 无 req.url ===')

# 修复4: 把所有 req.url.startsWith( 替换成 urlPath.startsWith(
count4 = content.count("req.url.startsWith(")
if count4 > 0:
    content = content.replace("req.url.startsWith(", "urlPath.startsWith(")
    print(f'✅ 修复4: 替换 {count4} 处 req.url.startsWith(')
else:
    print('⚠️  修复4: 无 req.url.startsWith(')

# 检查语法（简单检查成对花括号）
opens = content.count('{')
closes = content.count('}')
if opens == closes:
    print(f'✅ 花括号匹配: {{ {opens} === }} {closes}')
else:
    print(f'⚠️  花括号可能不匹配: {{ {opens} vs }} {closes}')

with open(FILE, 'w') as f:
    f.write(content)

print(f'\n✅ 修复完成，文件已写入 {FILE}')
print(f'   文件大小: {len(content)} 字符')
