---
name: tzzb-analyzer
description: 同花顺投资账本持仓分析工具。自动从同花顺投资账本读取持仓、自选股、交易记录，结合市场行情生成深度分析报告，支持板块分布、风险监控和阈值报警。
version: 2.0.0
homepage: https://tzzb.10jqka.com.cn
tags: ["portfolio", "analyzer", "stock", "tzzb", "chinese-market"]
commands:
  - /tzzb analyze   - 生成持仓分析报告
  - /tzzb positions - 获取当前持仓数据
  - /tzzb watchlist - 获取自选股列表
  - /tzzb trades    - 获取近期交易记录
  - /tzzb monitor   - 运行持仓风险监控
  - /tzzb status    - 检查 Chrome 连接状态
metadata: {"clawdbot":{"emoji":"📊","requires":{"bins":["python","uv"],"env":["CHROME_DEBUG_URL"]}}}
---

# 同花顺投资账本持仓分析器

自动从同花顺投资账本读取持仓数据，结合市场行情生成深度分析报告，支持板块分布、风险监控和阈值报警。

## 安装

### 1. 安装依赖

```bash
# 安装 Chromium 浏览器（Playwright）
playwright install chromium
```

### 2. 配置（可选）

```bash
# Chrome 远程调试端口（默认: http://127.0.0.1:9222）
export CHROME_DEBUG_URL=http://127.0.0.1:9222
```

## 快速开始

### 生成持仓分析报告

```bash
python -m uv run scripts/analyze.py analyze
```

### 生成定时报告（早盘/午盘/收盘，新闻由 MCP web_search 注入）

```bash
# 早盘
python -m uv run scripts/report.py morning --news '[{"title":"...","snippet":"..."}]'

# 午盘
python -m uv run scripts/report.py midday --news '[{"title":"...","snippet":"..."}]'

# 收盘
python -m uv run scripts/report.py close --news '[{"title":"...","snippet":"..."}]'
```

> 新闻数据通过 `--news` 参数（JSON 数组）注入，格式：`{"title":"标题","snippet":"摘要"}`。
> 定时任务中，agent 先调用 `web_search` 获取新闻，再调用 report.py 时传入。

### 查看各模块

```bash
python -m uv run scripts/analyze.py positions   # 持仓数据
python -m uv run scripts/analyze.py watchlist  # 自选股
python -m uv run scripts/analyze.py trades     # 交易记录
python -m uv run scripts/analyze.py status     # 连接状态
```

### 运行风险监控

```bash
python -m uv run scripts/monitor.py            # 检查并报警
python -m uv run scripts/monitor.py --dry-run # 仅预览不写状态
```

## 配置文件

配置文件位于 `memory/` 目录，首次运行自动创建：

### memory/positions_config.json

```json
{
  "report": {
    "show_sector_detail": true,
    "show_risk_alerts": true,
    "show_suggestions": true,
    "price_source": "tzzb+yahoo",
    "sort_by": "profit_pct"
  }
}
```

### memory/monitor_config.json

```json
{
  "enabled": true,
  "alerts": [
    {"name": "单股仓位过重", "condition": "position_rate_above", "threshold": 30, "message": "...", "cooldown_hours": 24},
    {"name": "亏损超20%", "condition": "profit_rate_below", "threshold": -20, "message": "...", "cooldown_hours": 24},
    {"name": "持仓超1年", "condition": "hold_days_above", "threshold": 365, "message": "...", "cooldown_hours": 168},
    {"name": "总仓位过高", "condition": "total_position_above", "threshold": 80, "message": "...", "cooldown_hours": 24}
  ]
}
```

支持的监控条件：

- `position_rate_above` - 单股仓位占比超过 X%
- `profit_rate_below` - 单股亏损率超过 X%
- `hold_days_above` - 持仓天数超过 X 天
- `total_position_above` - 总仓位超过 X%

## 分析报告内容

1. **账户概览** - 总资产、持仓市值、可用资金、仓位、整体盈亏
2. **持仓明细** - 持仓量、成本、现价、市值、盈亏、收益率、持股天数
3. **板块分布** - 按行业/概念分类的持仓市值
4. **风险提示** - 仓位过重、连续亏损、持仓过长等
5. **优化建议** - 减仓、换股、仓位管理建议

## 定时任务

```bash
# 每天收盘后自动分析
openclaw cron add --name "持仓分析" \
  --cron "0 16 * * 1-5" --tz "Asia/Shanghai" \
  --message "运行 python -m uv run scripts/analyze.py analyze"

# 每天 16:05 风险监控
openclaw cron add --name "持仓监控" \
  --cron "5 16 * * 1-5" --tz "Asia/Shanghai" \
  --message "运行 python -m uv run scripts/monitor.py"
```

## 数据来源

- 持仓/自选股/交易：同花顺投资账本（Playwright CDP 提取）
- 行情数据：Yahoo Finance

## 注意事项

1. Chrome 远程调试端口由 Playwright 自动管理（自动启动/连接）
2. 分析建议仅供参考，不构成投资建议
3. 监控状态每日重置（跟随交易日）
4. 数据缓存位于 `data/` 目录（可手动清理）
