# Tavily 搜索命令（联网验证用）

在 WildIdea Step 7.5 联网验证循环中使用。
`web_search` 不是工具函数，用以下 curl 命令替代。

## 基础用法

```bash
# 读取 API key
KEY=$(grep TAVILY_API_KEY ~/.openclaw/.env | cut -d'=' -f2)

# 单条搜索
curl -s "https://api.tavily.com/search" \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "'"$KEY"'",
    "query": "手机 场景意图识别 AI 自动识别",
    "search_depth": "basic",
    "max_results": 3
  }' | python3 -c "
import sys, json
d = json.load(sys.stdin)
for r in d.get('results', []):
    print(r['title'] + ' | ' + r['url'][:60])
"
```

## 批量搜索（多条一起跑）

```python
import json
from hermes_tools import terminal

key = terminal("grep TAVI ~/.openclaw/.env | cut -d'=' -f2", timeout=5)['output'].strip()

queries = [
    "候选建议1",
    "候选建议2",
]

for q in queries:
    r = terminal(
        f'''curl -s "https://api.tavily.com/search" -H "Content-Type: application/json" -d '{{
            "api_key": "{key}",
            "query": "{q}",
            "search_depth": "basic",
            "max_results": 3
        }}' | python3 -c "import sys,json; d=json.load(sys.stdin); [print(r['title']+' | '+r['url'][:60]) for r in d.get('results',[])]"''',
        timeout=15
    )
    status = "🚫" if r['output'].strip() else "✅"
    print(f"{status} | {q}")
    if r['output'].strip():
        for line in r['output'].strip().split('\n')[:2]:
            print(f"  {line}")
```

## 判断标准

| 搜索返回 | 判定 | 例子 |
|----------|------|------|
| 产品发布/功能公布/专利/论文/品牌案例 | 🚫 已存在，ban | "vivo 发布蓝图色彩风格" |
| 用户反馈/论坛讨论/理论研究/无关结果 | ✅ 通过 | "ADHD 手机成瘾"（不是 camera near-miss） |
| 无结果 | ✅ 通过 | — |
| 搜索错误/超时 | ⚠️ 标记"需人工验证" | — |
