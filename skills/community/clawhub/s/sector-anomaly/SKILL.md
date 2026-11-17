---
name: sector-anomaly
description: 分析A股板块异动（放量、资金流入、涨停潮、个股联动），输出板块异动评分、强势/出货判断和操作建议。用于"看看哪些板块异动""分析XX板块是不是异动""今天资金流向哪些板块""哪些板块有异动信号"等场景。可接入本地 SQLite 行情库和 stock-pool-v2.json 板块映射。
---

# 板块异动分析

## 数据源与工作目录

- 项目根目录: 通过环境变量 `STOCK_ANALYZER_ROOT` 指定；未设置时默认取脚本上三级目录
- 板块映射: `data/stock-pool-v2.json`（`code -> sector`）
- 行情库: `data/stock_analyzer.db` 的 `daily_quotes` 表
- 资金流: `fundflow_cache` 表（JSON 字段，含 `mainForce`、`history` 5日序列）
- 龙虎榜: `longhubang_daily` 表（可选增强）

运行前如数据过期，先刷新：

```bash
cd "${STOCK_ANALYZER_ROOT:-.}"
node src/cli/refresh-all.mjs
node src/cli/fetch-fundflow.js --all
```

## 快速开始

运行板块异动分析：

```bash
STOCK_ANALYZER_ROOT=/path/to/project node skills/sector-anomaly/scripts/analyze-sector-anomaly.mjs
```

若 skill 与行情库同目录部署，可直接运行（脚本自动定位上级目录）。

常用参数：

```bash
# 指定分析日期（默认最新有效交易日）
node skills/sector-anomaly/scripts/analyze-sector-anomaly.mjs --date=2026-08-07

# 板块最少成分股数（默认3，过滤样本过小的板块）
node skills/sector-anomaly/scripts/analyze-sector-anomaly.mjs --min-members=5

# 只看前 N 个板块（默认15）
node skills/sector-anomaly/scripts/analyze-sector-anomaly.mjs --top=10
```

## 输出解读

脚本输出板块排行榜和评分前5板块详情，字段含义见 `references/indicators.md`。

判断要点：

- **评分 >= 60**：强势异动，需确认是否有龙头封板 + 资金延续，可重点跟踪
- **评分 40-59**：温和异动，观察资金能否持续，不急于参与
- **评分 < 40**：弱异动或资金背离，暂不参与
- **量价背离**：板块涨幅为正但主力净流出，警惕冲高出货
- **资金流基准日**：盘前运行时资金流滞后一日（如 8/7 盘中看到的是 8/6 资金流），报告会自动标注

## 手工补充分析

脚本输出基础排行榜后，如需深度分析，查询数据库补充：

```bash
# 查看某板块成分股（从 JSON 提取）
python3 -c "import json; pool=json.load(open('data/stock-pool-v2.json')); print([s['name'] for s in pool if s.get('sector')=='半导体'])"

# 查看个股资金流明细
/usr/bin/sqlite3 data/stock_analyzer.db "SELECT stock_code, data FROM fundflow_cache WHERE fetch_date='2026-08-07' AND stock_code='300308.SZ';"

# 查看龙虎榜
/usr/bin/sqlite3 data/stock_analyzer.db "SELECT * FROM longhubang_daily WHERE trade_date='2026-08-07';"
```

## 注意事项

- 历史 K 线中 `volume/amount` 多为 0（项目数据源限制），脚本已自动降级为"成交占比 + 5日资金流趋势"，不显示量比
- 板块映射来自 `stock-pool-v2.json`，数据库 `stocks.sector` 字段为空，勿直接查该字段
- 涨停判定：主板 >= 9.5%，创业板/科创板 >= 19.5%

## 合规与免责

- 本 skill 仅基于公开行情数据和本地数据库做统计整理，输出用于研究、复盘与个人交易系统优化。
- 所有评分、判断和操作含义均为数据统计结果，**不构成任何投资建议**，不承诺收益。
- 脚本输出末尾自带免责声明，引用输出时应保留。
- 本地数据库如含个人持仓等敏感信息，请勿随 skill 打包上传；上传版本应仅含脚本、文档与演示数据。
