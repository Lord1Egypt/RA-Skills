---
name: "trading-execution"
description: "交易执行工具：看盘效率/自动化执行/资产配置/Upbit自动交易/快捷键效率提升"
user-invocable: true
metadata:
  openclaw:
    emoji: "⚡"
    tags: ["trading", "execution", "automation", "portfolio"]
---

# Trading Execution v2.0

## 看盘效率
快捷键切换/多屏联动/预警条件快速设置

## Upbit 自动交易
```bash
python scripts/upbit_breakout.py --mode top_volume --budget 1000
```
突破策略/cron友好/回测+实盘模式

## 资产配置
保守(60%指数+30%债券+10%现金)/均衡(40%+30%+20%+10%)/进取(50%个股+20%加密+15%指数+10%现金+5%投机)
季度再平衡，偏离>10%调整

## 定时任务
```
25 9 * * 1-5  market_open.py       # 开盘
30 10,13,14 * * 1-5 intraday_check.py  # 盘中
30 15 * * 1-5  daily_summary.py    # 收盘
```

## 安全
实盘需确认/单日最大亏损限制/Key安全存储/不做高频杠杆
