# 智能仓位管理系统 - Intelligent Position Sizing System

## 📋 项目概述

基于信号强度和风险的智能仓位推荐系统，为 A 股投资提供科学的仓位管理方案。

### 核心特性

- ✅ **多维度信号评估** (技术指标、形态识别、多周期共振)
- ✅ **全面风险管理** (波动率、回撤、Beta 系数)
- ✅ **市场环境适应** (大盘趋势、行业景气、市场情绪)
- ✅ **资金规模优化** (账户资金、可用资金、风险承受能力)
- ✅ **智能止损止盈** (基于 ATR 和支撑阻力位)
- ✅ **完整回测框架** (历史验证、绩效评估)

---

## 🏗️ 系统架构

```
position_sizer.py    # 仓位计算核心
├── SignalStrength   # 信号强度计算
├── RiskMetrics      # 风险指标计算
├── MarketEnvironment # 市场环境评估
├── CapitalInfo      # 资金信息管理
└── PositionSizer    # 仓位管理器

risk_model.py        # 风险模型模块
├── RiskCalculator   # 风险计算器
├── StressTester     # 压力测试器
└── RiskAnalysisResult # 风险分析结果

backtester.py        # 回测验证模块
├── Backtester       # 回测引擎
├── SignalGenerator  # 信号生成器
└── BacktestResult   # 回测结果
```

---

## 📐 仓位计算公式

### 权重分配

| 因子 | 权重 | 说明 |
|------|------|------|
| 信号强度 | 40% | 技术指标 + 形态识别 + 多周期共振 |
| 风险水平 | 30% | 波动率 + 最大回撤 + Beta 系数 |
| 市场环境 | 20% | 大盘趋势 + 行业景气 + 市场情绪 |
| 资金规模 | 10% | 账户总资金 + 可用资金 + 风险承受能力 |

### 计算流程

```python
基础仓位 = 信号强度 × 0.4
风险调整 = (1 - 风险水平) × 0.3
环境调整 = 市场环境 × 0.2
资金调整 = 资金充足度 × 0.1

建议仓位 = 基础仓位 + 风险调整 + 环境调整 + 资金调整
最终仓位 = min(建议仓位，80%)  # 最大仓位限制 80%
```

---

## 🚀 快速开始

### 1. 基本使用

```python
from position_sizer import (
    PositionSizerBuilder, 
    MarketTrend
)

# 使用构建器创建仓位管理器
sizer = (PositionSizerBuilder()
    .with_signal(technical=75, pattern=80, multi_period=70)
    .with_risk(volatility=0.15, max_drawdown=0.25, beta=1.1)
    .with_market(
        trend=MarketTrend.BULLISH,
        industry_health=0.7,
        sentiment=0.6
    )
    .with_capital(
        total=1000000,
        available=800000,
        risk_tolerance=0.6
    )
    .build()
)

# 生成仓位推荐
recommendation = sizer.generate_recommendation(
    current_price=540.0,
    atr=12.5,
    support_level=520.0,
    resistance_level=580.0
)

# 输出结果
print(recommendation.to_dict())
```

### 2. 输出格式

```python
{
    "recommended_shares": 1200,      # 推荐股数
    "position_value": 648000,        # 仓位价值
    "position_pct": 64.8,            # 仓位百分比 (%)
    "stop_loss": 520.00,             # 止损价
    "take_profit": 580.00,           # 止盈价
    "risk_amount": 26400,            # 风险金额
    "risk_pct": 2.6,                 # 风险百分比 (%)
    "sharpe_ratio": 1.85,            # 夏普比率
    "signal_strength": 75.0,         # 信号强度得分
    "risk_level": 49.0,              # 风险水平得分
    "environment_score": 79.0,       # 环境得分
    "capital_adequacy": 72.0         # 资金充足度
}
```

---

## 📊 风险模型

### 风险指标

- **历史波动率**: 年化波动率计算
- **ATR**: 平均真实波幅
- **最大回撤**: 历史最大亏损幅度
- **VaR (95%/99%)**: 风险价值
- **CVaR**: 条件风险价值 (预期亏损)
- **夏普比率**: 风险调整收益
- **索提诺比率**: 下行风险调整收益
- **卡玛比率**: 收益/回撤比
- **Beta 系数**: 市场相关性
- **Alpha**: 超额收益

### 压力测试

```python
from risk_model import RiskCalculator, StressTester, PriceData

# 创建风险计算器
calculator = RiskCalculator(price_data, benchmark_data)
analysis = calculator.full_analysis()

# 压力测试
tester = StressTester(price_data, beta=analysis.beta)

# 运行场景测试
scenarios = tester.run_all_scenarios()
for scenario in scenarios:
    print(f"{scenario['scenario']}: {scenario['loss_pct']:.2%}")

# 蒙特卡洛模拟
mc_result = tester.monte_carlo_simulation(days=30, simulations=10000)
```

---

## 🔬 回测验证

### 运行回测

```python
from backtester import Backtester, SignalGenerator

# 创建回测引擎
backtester = Backtester(
    prices=price_list,
    dates=date_list,
    initial_capital=1000000,
    commission_rate=0.001,
    slippage=0.001
)

# 运行回测
result = backtester.run_backtest(
    position_sizer_class=PositionSizer,
    signal_generator=signal_gen.generate_signal,
    risk_calculator=risk_calc
)

# 查看结果
print(f"总收益：{result.total_return:.2%}")
print(f"年化收益：{result.annualized_return:.2%}")
print(f"最大回撤：{result.max_drawdown:.2%}")
print(f"夏普比率：{result.sharpe_ratio:.2f}")
print(f"胜率：{result.win_rate:.1f}%")
```

### 回测指标

| 指标 | 说明 |
|------|------|
| Total Return | 总收益率 |
| Annualized Return | 年化收益率 |
| Max Drawdown | 最大回撤 |
| Sharpe Ratio | 夏普比率 |
| Sortino Ratio | 索提诺比率 |
| Calmar Ratio | 卡玛比率 |
| Win Rate | 胜率 |
| Profit Factor | 盈利因子 |
| Avg Holding Period | 平均持仓期 |

---

## 📁 文件说明

```
skills/technical-indicators/
├── position_sizer.py    # 仓位计算核心 (23:30 交付 ✅)
├── risk_model.py        # 风险模型模块 (24:00 交付 ✅)
├── backtester.py        # 回测验证模块 (01:00 交付 ✅)
└── README.md            # 本文档
```

---

## 🎯 使用场景

### 1. 个股仓位推荐

```python
# 针对单只股票计算最优仓位
sizer = PositionSizerBuilder()...build()
recommendation = sizer.generate_recommendation(
    current_price=current_price,
    atr=atr,
    support_level=support,
    resistance_level=resistance
)
```

### 2. 投资组合仓位分配

```python
# 对多只股票分别计算仓位
for stock in portfolio:
    sizer = create_sizer_for_stock(stock)
    rec = sizer.generate_recommendation(...)
    allocate_position(stock, rec)
```

### 3. 风险评估与压力测试

```python
# 评估持仓风险
analysis = risk_calculator.full_analysis()
stress_results = stress_tester.run_all_scenarios()
```

### 4. 策略回测与优化

```python
# 回测历史表现
result = backtester.run_backtest(...)

# 参数优化
best_params = optimize_strategy(backtester, param_grid)
```

---

## ⚠️ 风险提示

1. **模型风险**: 所有模型都是对现实的简化，存在假设局限
2. **历史数据**: 历史表现不代表未来收益
3. **市场风险**: 极端市场条件下模型可能失效
4. **流动性风险**: 大仓位可能面临流动性问题
5. **执行风险**: 实际交易存在滑点和手续费

---

## 📝 依赖项

```
numpy>=1.20.0
pandas>=1.3.0
scipy>=1.7.0
```

---

## 👥 开发团队

- **开发时间**: 2026-03-14
- **交付期限**: 
  - ✅ 23:30 - 仓位计算框架
  - ✅ 24:00 - 风险模型
  - ✅ 01:00 - 回测验证

---

## 📞 使用支持

如有问题或建议，请联系 AIBoss 团队。
