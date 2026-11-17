---
name: yanlin-report-gen
description: 研林Skill — 产业投研日报生成器，将采集数据合成为完整券商级日报（Markdown格式）
---
# 研林 · 日报生成器 (yanlin-report-gen)
> **⚠️ 数据来源与限制（重要披露）：**
> 默认模式：基于传入的4个数据JSON（market/macro/news/filings）生成日报；另有 `--standalone` 独立模式：自动调用本课程配套的采集Skill（yanlin-market-data 等）拉取数据，该模式仅适用于已完整安装课程全部Skill的环境，且数据来源同样遵循各采集Skill的实时优先/内置兜底策略。
> 日报仅用于课程教学演示，不构成投资建议。



## 功能
将前序Skill采集的结构化数据，按固定模板生成完整的产业投研日报。

## 输入依赖（必须）
前序4个Skill的输出JSON必须全部提供，缺一不可：
1. `yanlin-market-data` → 市场行情数据
2. `yanlin-macro-data` → 宏观指标数据
3. `yanlin-news-filter` → 过滤后的关键事件
4. `yanlin-company-filings` → 有效公告列表

## 处理流程
```
market_data.json ───────┐
macro_data.json ─────────┤
news_filter.json ────────┤──→ 日报模板引擎 → 产业投研日报.md
filings_data.json ───────┘         │
                                   ├── 一致性校验
                                   └── 格式化输出
```

## 模板结构（7大板块，固定输出顺序）
| 板块 | 输入数据源 | 核心逻辑 |
|------|-----------|---------|
| 一、今日核心投研结论 | 全量数据 | AI提取TOP 1-3条最重要边际变化 |
| 二、宏观&流动性观察 | macro_data | 表格+文字解读，判断对权益市场影响 |
| 三、行业产业动态深度解读 | news_filter | 事件→边际变化→供需→业绩→预期差 |
| 四、重点公司公告速览 | filings_data | 过滤后的有效公告表格 |
| 五、市场情绪&资金复盘 | market_data | 指数复盘+轮动归因+估值分位 |
| 六、明日前瞻&跟踪清单 | 全量+历史 | 事件日历+赛道增量更新+催化 |
| 七、核心风险提示 | 全量 | 五大维度风险评估矩阵 |

## 调用方式
```bash
python3 {baseDir}/scripts/generate_report.py \
  --market-data <market_data.json> \
  --macro-data <macro_data.json> \
  --news-data <news_filter.json> \
  --filings-data <filings_data.json> \
  --output <output_dir> \
  --date YYYY-MM-DD
```

## 输出
- 文件：`研林产业投研日报_YYYY-MM-DD.md`
- 可额外指定 `--format pdf` 或 `--format docx` 按需输出

## 日报文件命名规范
```
研林产业投研日报_2026-07-03.md
```
存放路径：`{output_dir}/{date}/`
