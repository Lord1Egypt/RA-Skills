---
name: 股票交易监控系统
description: 股票交易监控系统，通过新浪财经 API 获取 A 股实时行情。支持盘前盘后自动跳过，异常触发即时告警（无需消耗模型 token），支持价格日志自动记录。适用场景：(1) 定时盘中检查，价格触高/触低/涨跌幅超标即时推送 (2) 实时查询股价 (3) 查看每日价格日志与历史日志 (4) 盘前盘后自动过滤无效行情。版本 3.0，新增规则：每日仅报一次 + 无异常静默 + 即时推送 + 价格日志自动记录。
slug: stock-monitor-v3
version: 3.0.0
---

# 股票交易监控系统 v3.0

A 股实时行情监控，基于新浪财经 API，支持价格/涨跌幅预警、日志记录，零 AI token 消耗。

## 更新日志

**v3.0.0 (2026-06-02)**
- 新增监控规则系统（alert_once_per_day / no_alert_silent / alert_pushes_immediately / price_log_auto_record）
- 驱动方式升级为 `clawdbot_internal_cron` + Linux crontab 双保险
- 告警推送切换至小艺通道（绕过 token 消耗模型）
- 新增数据库建表脚本（MySQL），支持持久化行情日志与预警记录
- 新增无 token 模式检查脚本 `stock_monitor_check.sh`
- 优化价格日志：记录 API 返回的当日真实最高/最低价，避免快照遗漏极值

## 运行模式

| 指令 | 说明 |
|------|------|
| `check` | 执行一轮检查，触发预警则返回告警消息 |
| `query` | 返回所有监控股票实时价格 |
| `log` | 查看今日价格日志 |
| `log_history` | 查看最近 7 天日志摘要 |

### 命令行调用

```bash
cd scripts/
python3 stock_monitor_skill.py check
python3 stock_monitor_skill.py query
python3 stock_monitor_skill.py log
python3 stock_monitor_skill.py log_history
```

## 配置文件

`scripts/stock_config.json`：

```json
{
  "meta": { "name": "股票交易监控系统配置", "version": "3.0.0" },
  "driver": {
    "type": "clawdbot_internal_cron",
    "cron_expr": "*/10 9-15 * * 1-5",
    "timezone": "Asia/Shanghai",
    "delivery_channel": "xiaoyi"
  },
  "trading_hours": {
    "morning": "09:30-11:30",
    "afternoon": "13:00-15:00"
  },
  "rules": {
    "alert_once_per_day": true,
    "no_alert_silent": true,
    "alert_pushes_immediately": true,
    "price_log_auto_record": true
  },
  "stocks": [
    { "code": "688599", "name": "天合光能", "price_high": 17, "price_low": 15 },
    { "code": "600000", "name": "浦发银行", "price_high": 10, "price_low": 8 },
    { "code": "000785", "name": "居然智家", "price_high": 2.6, "price_low": 2.25 }
  ]
}
```

## 系统规则

| 规则 | 说明 |
|------|------|
| alert_once_per_day | 同条件当日仅提醒一次，避免重复轰炸 |
| no_alert_silent | 无异常时保持静默，不推送消息 |
| alert_pushes_immediately | 触发预警即时推送，不攒批 |
| price_log_auto_record | 每次 check/query 自动记录价格日志 |

## 文件结构

```
stock-monitor-v3.skill/
├── SKILL.md
└── scripts/
    ├── stock_config.json
    └── stock_monitor_skill.py
```
