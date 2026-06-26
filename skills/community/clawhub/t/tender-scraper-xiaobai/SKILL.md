---
name: tender-scraper
description: [user] 爬取招投标采购公告资讯。用于商业情报收集、竞品分析、政府采购信息追踪。
---

# 招投标采购公告资讯 Skill

## 数据来源

- 网站：https://ygcg.nbcqjy.org

## 快速开始

```bash
python scripts/crawl.py --limit 30
```

## 编程调用

```python
import sys
sys.path.insert(0, "tender-scraper")
from scripts.crawl import crawl_and_return_json

result = crawl_and_return_json(limit=50)
# AI自行处理返回数据
```

## 字段说明

| 字段 | 说明 |
|------|------|
| title | 采购公告标题 |
| url | 原文链接 |
| publish_time | 发布日期 |
| tags | 类型标签 |
| tender_type | 公告类型 |

## 类型标签

根据 infoTypeId 字段：

| 标签 | 说明 |
|------|------|
| 工程 | 工程类 |
| 非工程类货物 | 货物类 |
| 非工程类服务 | 服务类 |
| 工程类货物 | 工程货物类 |
| 工程类服务 | 工程服务类 |
| 中介超市服务 | 中介服务类 |
| 其他 | 其他类型 |

## 总结输出格式

按日期+类型分组，使用emoji：

```markdown
📅 2026-03-17 招投标公告 (共15条)

🔷 2026-03-17

🏗️ 工程
• [项目名称](链接)
• [项目名称](链接)

📦 非工程类货物
• [项目名称](链接)

🛠️ 非工程类服务
• [项目名称](链接)

👔 中介超市服务
• [项目名称](链接)

🔧 工程类服务
• [项目名称](链接)

---
🔷 2026-03-16 (共20条)

🏗️ 工程
• [项目名称](链接)
...
```
