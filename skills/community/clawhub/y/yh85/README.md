# YH8.5 双引擎量化信号系统

> 纯规则化双引擎：**ST 趋势 + BB20 震荡**，Playbook 路由 + 市场状态自适应，信号直通可回测。

YH8.5 用 ST 抓趋势、BB20 抓均值回归，由 Playbook 按 ATR 波动状态自动路由到对应引擎，牛/基/熊三场景自适应参数。无黑箱 ML，全部规则可回测、可证伪。

## ✨ 特性

- **双引擎**：SuperTrend 趋势跟随 + 布林带均值回归
- **Playbook 路由**：波动状态自动切换引擎
- **市场状态自适应**：牛/基/熊三场景调参数
- **纯规则信号直通**：可回测、可证伪
- **多层过滤器**：量比放量、ACF/PACF 自相关、收盘确认、做空回落确认

## 📐 架构

| 引擎 | 定位 | 行情 |
|---|---|---|
| ST 趋势引擎 | 趋势跟随 | 高波动/趋势市 |
| BB20 震荡引擎 | 均值回归 | 低波动/震荡市 |

## 🚀 快速开始

```bash
# 依赖
pip install numpy pandas ccxt

# 配置参数（复制示例，填入真实参数）
cp strategy_params.example.json strategy_params.json

# 生成信号
python3 scripts/backtest.py --days 30 --coins BTC/USDT,ETH/USDT
```

## 📁 目录结构

```
yh85/
├── SKILL.md
├── strategies/
│   ├── yh8_engine.py        # 核心引擎（ST + BB20）
│   ├── playbook.json        # 策略配置（双引擎参数 + 币种分配）
│   └── playbook_manager.py  # 配置热加载
├── market_regime.py         # 市场状态分型
├── scripts/
│   └── backtest.py          # 回测脚本
└── references/
    ├── strategy.md
    └── performance.md
```

## ⚠️ 免责声明

本项目仅供学习与研究用途。加密货币合约交易具有高风险（含杠杆爆仓风险），历史回测不代表未来收益。使用本策略产生的任何盈亏由使用者自行承担。
