---
name: wechat-report
description: Generate a structured comparison report for multiple WeChat Official Account articles under one topic. Use this when the user wants several公众号文章 collected into one local report with article metadata, engagement status, content structure tables,爆款写法标签, and a later optional Feishu sync step.
---

# wechat-report

输入文件使用 Markdown + frontmatter，至少提供 `topic`，也可以直接给 `seed_urls`。

示例：

```markdown
---
topic: Harness Engineering
max_articles: 5
collect_engagement: true
seed_urls:
  - https://mp.weixin.qq.com/s?__biz=...
---

优先围绕中文 AI / Agent 语境收集公众号原文。
```

运行：

```bash
.venv/bin/python -m skill_runtime.cli run-skill wechat-report --input content-production/inbox/20260406-wechat-report-request.md
```

输出：

- `content-production/inbox/YYYYMMDD-{slug}-wechat-report.md`
- `content-production/inbox/raw/wechat-report/YYYY-MM-DD/{slug}.json`

报告除文章总表、互动对比表、内容结构表外，还会补：

- 爆款写法标签表
- 标题与开头拆解
- 结尾与转发钩子
- 共性写法总结

注意：

- 本 skill 不会自动发送飞书。
- 报告生成后，若用户确认同步，再运行 `feishu-bitable-sync`。
