---
name: yinghuo-grid
description: 萤火网格1.0（YingHuo Grid v1.0）——加密货币永续合约的「手工锚仓 + 马丁加仓 + ATR 间距」网格交易系统，全自动闭环执行（自动扫描接管持仓、马丁加仓、单格止盈、两档总止盈止损、趋势过滤器、仓位流水记录）。用于部署、运维或回测一套网格量化交易策略时使用。
---

# 萤火网格1.0 (YingHuo Grid v1.0)

针对手工锚仓的永续合约网格系统。锚仓由用户手动开（系统只识别、永不自动动），系统负责在锚仓基础上做 ATR 动态网格的全自动加仓/减仓/止盈止损。

## 核心规则

| 环节 | 规则 |
|---|---|
| 网格间距 | 基于 ATR 动态计算，跟随波动 |
| 马丁加仓 | 递增加仓摊薄成本，封顶控敞口 |
| 单格止盈 | 反弹减仓锁利（LIFO） |
| 总止盈 | 分批止盈，利润落袋 |
| 总止损 | 分批止损兜底，防深套 |
| 趋势过滤 | 单边行情自动暂停加仓 |
| 账户熔断 | 总浮亏超标全局暂停 |
| 防踏空 | 单边行情自动跟随上移基准 |
| 仓位流水 | 每次操作自动落 `.manual_grid_journal.jsonl` |

多空镜像：做多与做空同一套规则、方向相反。

## 快速开始

```bash
# 依赖
pip install ccxt

# 配置参数（复制示例配置，填入真实参数；付费订阅版提供回测调优参数）
cp strategy_params.example.json strategy_params.json

# 查看状态（自动从交易所同步持仓）
python3 scripts/manual_grid_atr.py status

# 登记锚仓
python3 scripts/manual_grid_atr.py add BTC/USDT long 0.003 84277.5 fixed

# 常驻自动扫描（每 60s，接管持仓 + 检查触发 + 自动下单）
python3 scripts/manual_grid_atr.py watch 60
```

常用命令：`status` / `add` / `remove` / `unignore` / `atrmult <SYM> <乘数>` / `trendfilter <SYM> on|off` / `sync` / `journal [SYM]` / `run` / `watch [秒]`。

## 详细文档

- **策略规则与参数详解**：见 [references/strategy.md](references/strategy.md)
- **回测与实盘绩效数据**：见 [references/performance.md](references/performance.md)
- **趋势过滤器回测**：`scripts/grid_trend_filter_backtest.py`（对比「趋势时停加仓」vs「一直加仓」的回撤与收益）
