---
name: zdat-crawl-skill
description: ZDAT零缺陷情报抓取技能。关键词监测+多平台情报采集+自动归档分类+负面预警。封装 smart-search-reader、crawl4ai-search、blogwatcher 进行定时抓取。
---

# 🕷️ ZDAT 零缺陷情报抓取技能

## 身份定位
ZDAT博士军团情报中枢。定时全网抓取零缺陷相关情报，自动分类归档，触发预警。

## 触发关键词
`抓取情报`、`全网监控`、`关键词监听`、`舆情`、`情报采集`、`竞品监控`

## 依赖技能
- `smart-search-reader` — 元搜索引擎，聚合200+引擎搜索
- `crawl4ai-search` — 全站深度抓取
- `blogwatcher` — RSS/博客监控
- `cron` — 定时执行
- `xlsx` — 竞品台账写入

## 配置文件
- `skill_config/zd_keyword.yaml` — 关键词词库
- `skill_config/zd_crawl_schedule.yaml` — 抓取调度规则
- `skill_config/zd_publish_rule.yaml` — 归档分类规则

## 执行流程

### 步骤1：关键词检索（多引擎并行）
```bash
# 多关键词并行搜索（按 keyword 类型分组）
python scripts/zd_crawl_search.py --type core
python scripts/zd_crawl_search.py --type industry
python scripts/zd_crawl_search.py --type intent
```

### 步骤2：内容判断与归档
命中关键词后：
- 用户提问内容 → 输出标记为 `【选题备用】`
- 行业落地案例 → 输出标记为 `【工厂案例】`
- 竞品讲师发文 → 写入竞品台账Excel
- 行业政策新规 → 输出标记为 `【政策】`

### 步骤3：负面预警检查
- 统计负面关键词日出现次数
- 单关键词单日≥15条 → 自动推送预警到企业微信
- 头部行业博主大量发布 → 推送简报

### 步骤4：输出格式
```
📡 ZDAT抓取简报 YYYY-MM-DD HH:MM
━━━━━━━━━━━━━━━━━━━━━━
🟢 核心关键词：N条
  ├ 零缺陷：X条
  ├ PONC：Y条
  └ ...
🟡 行业拓展：N条
🔴 预警：N条
  ├ 负面关键词触发：XX
  └ 头部博主动态：XX
```

## 定时调度（通过 cron skill 注册）
| 时段 | 类型 | 范围 |
|:----|:----|:----|
| 08:00/14:00/20:00 | 全量抓取 | 所有关键词+全平台 |
| 02:00/08:00/14:00/20:00 | 增量巡检 | 小众论坛 |

## 示例命令
```bash
# 执行一次全量抓取
python active_skills/zdat-crawl-skill/scripts/zd_crawl_search.py --type all

# 仅抓取竞品监控
python active_skills/zdat-crawl-skill/scripts/zd_crawl_search.py --type competitor

# 检查预警
python active_skills/zdat-crawl-skill/scripts/zd_crawl_alert.py
```
