---
name: xhs-feedback-analyzer
description: 小红书跑腿类帖子监控与用户反馈分析工具。多关键词搜索（美团跑腿/跑腿/帮买/帮送等），按发帖日期过滤，相关性筛选，深度分类（服务类型/情感/反馈类型），输出 Markdown 报告写入 KM 学城文档。当用户需要分析跑腿产品在小红书的用户口碑、定期舆情监控、竞品用户反馈时使用。触发词：小红书反馈分析、跑腿帖子监控、抓小红书、分析用户评价、舆情。
---

# 小红书跑腿帖子监控工具

## 工作流

### Step 1：抓取数据

```bash
node scripts/xhs_search_scraper.mjs \
  --keywords "美团跑腿,跑腿,跑腿帮忙,美团帮忙,美团帮送,跑腿帮送,帮买" \
  --days 3 \
  --limit 50 \
  --out ./output
```

输出：`output/xhs_paotui_<昨天日期>.json`

### Step 2：分析并生成报告

```bash
python3 scripts/analyze_feedback.py output/xhs_paotui_<日期>.json --out ./output
```

输出：`output/report_<日期>.md`（同时打印到 stdout）

### Step 3：写入 KM 文档

报告写入：https://km.sankuai.com/collabpage/2751219981  
**新结果放在文档最前面**（用 CDP insertText 插入到文档顶部）

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--keywords` | 逗号分隔关键词 | 7个预设关键词 |
| `--days` | 往前几天（不含今天） | 3 |
| `--limit` | 总帖子数上限 | 50 |
| `--out` | 输出目录 | ./output |
| `--cdp` | Chrome CDP URL | http://127.0.0.1:9222 |

## 分析维度

1. **服务类型**：帮送/配送、帮买/代购、帮办/跑腿通用
2. **情感**：正面、中立、负面
3. **反馈类型**：价格问题、配送速度、骑手态度、客服、App体验、丢失损坏、好评、攻略、测评
4. **内容提炼**：每篇摘要
5. **帖子链接**：全量
6. **精选帖**：3篇有产品价值的代表帖

## 依赖

- playwright（已在全局 node_modules）
- Python 3（系统内置）

## 定期运行

用 daxiang-scheduled-message skill 设置定时任务，每天早上跑前一天数据：
> "每天早上9点帮我运行一次小红书跑腿帖子分析"
