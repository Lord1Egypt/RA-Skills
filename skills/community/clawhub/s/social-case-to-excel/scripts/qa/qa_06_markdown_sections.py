# -*- coding: utf-8 -*-
import re
md = open('/tmp/social-case-to-excel-example/跨境电商案例研究_42条_20260916.md', encoding='utf-8').read()
print('标题候选', md.count('### 标题候选'), '故事', md.count('### 故事'), '结论', md.count('### 一句话结论'))
print(md[:1200])
print('...')
i = md.find('\n## 案例 42')
print(md[i:i+900])
