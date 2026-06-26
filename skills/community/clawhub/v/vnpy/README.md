# vn.py 量化交易框架 Skill

[![Version](https://img.shields.io/badge/version-1.2.0-blue.svg)](https://www.vnpy.com)
[![License](https://img.shields.io/badge/license-Apache--2.0-green.svg)](LICENSE)
[![ClawHub](https://img.shields.io/badge/ClawHub-BossQuant-purple.svg)](https://clawhub.com)

vn.py开源量化交易框架，支持CTA、套利、期权策略，20+券商网关。

## ✨ 特性

- 🏆 **中国最流行开源框架** - 量化交易领域最活跃的开源社区
- 📈 **CTA/套利/期权** - 内置多种策略模板，快速开发
- 🔌 **20+券商网关** - 支持CTP、飞马、恒生等主流交易接口
- 🖥️ **GUI界面** - 提供完整的图形化交易和监控界面

## 📥 安装

```bash
pip install vnpy vnpy-ctp vnpy-ctastrategy
```

## 🚀 快速开始

```python
from vnpy_ctastrategy import CtaTemplate, BarGenerator, ArrayManager

class MyStrategy(CtaTemplate):
    """自定义CTA策略"""
    author = "量化开发者"

    fast_window = 10
    slow_window = 20

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)
        self.bg = BarGenerator(self.on_bar)
        self.am = ArrayManager()

    def on_bar(self, bar):
        self.am.update_bar(bar)
        if not self.am.inited:
            return

        fast_ma = self.am.sma(self.fast_window)
        slow_ma = self.am.sma(self.slow_window)

        if fast_ma > slow_ma:
            self.buy(bar.close_price, 1)
        elif fast_ma < slow_ma:
            self.sell(bar.close_price, 1)
```

## 📊 支持的策略类型

| 类别 | 说明 | 模板 |
|------|------|------|
| CTA策略 | 趋势/均值回归 | `CtaTemplate` |
| 套利策略 | 跨期/跨品种 | `SpreadStrategyTemplate` |
| 期权策略 | Delta对冲等 | `ElectronicEyeEngine` |
| 算法交易 | TWAP/VWAP | `AlgoTemplate` |

## 📖 更多示例

```python
from vnpy_ctastrategy import ArrayManager

am = ArrayManager()

# 技术指标计算
sma = am.sma(20)
ema = am.ema(20)
macd_value, signal, hist = am.macd(12, 26, 9)
rsi = am.rsi(14)

# 下单接口
self.buy(price, volume)       # 买入开仓
self.sell(price, volume)      # 卖出平仓
self.short(price, volume)     # 卖出开仓
self.cover(price, volume)     # 买入平仓
```

## 📄 许可证

Apache License 2.0

## 📊 更新日志

### v1.2.0 (2026-03-23)
- 🎉 增加更丰富的AI Agent演示和高阶使用指南
- 🔄 更新版本号并清理失效链接


### v1.1.0 (2026-03-15)
- 🎉 初始版本发布
- 📊 支持CTA、套利、期权策略开发

---

## 🤝 社区与支持

- **维护者**：大佬量化 (Boss Quant)
- **主页**：https://www.vnpy.com
- **ClawHub**：https://clawhub.com
