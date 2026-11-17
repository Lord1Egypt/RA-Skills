---
name: Quantitative Backtesting Laboratory
slug: security-quant-backtest
description: AI-powered quantitative backtesting laboratory for China A-share — strategy design, historical backtesting with cost/slippage modelling, walk-forward validation, performance attribution and Monte Carlo simulation. Scope: research and validation of a defined trading rule on historical data; not live order routing, not execution advice, not return promises. Keywords: backtest a strategy, walk-forward validation, slippage and cost model, look-ahead bias check, overfitting test, Monte Carlo simulation, performance attribution, A-share, 策略回测, 前向分析, 滑点与成本建模, 未来函数检查, 过拟合检验, 蒙特卡洛模拟, 绩效归因.
version: "3.0.4"
---

# Quantitative Backtesting Laboratory / 量化回测实验室

> **English:** AI-powered quantitative backtesting laboratory — covers strategy design, historical backtesting, performance attribution, walk-forward analysis, and Monte Carlo simulation. Built for quant analysts and algorithmic traders.
>
> **中文:** 量化回测实验室——覆盖策略设计、历史回测、绩效归因、前向分析、蒙特卡洛模拟。适用：量化分析师、算法交易者、Python回测开发。


## 数据最小化声明与执行边界 / Data Minimisation & Execution Boundary

**数据最小化前置声明：** 使用本技能时，请只提供回测所必需的输入——标的代码、行情区间、策略规则与参数、费率假设。**不要**粘贴实盘账户信息、真实持仓明细、交易席位与柜台配置、客户身份信息或券商内部的行情源凭证；回测规模请用"100万初始资金"这类假设值。

**保存与预览确认：** 本技能不执行任何保存动作。若你在自己环境中依据本技能生成回测脚本、绩效报告或蒙特卡洛结果，请在落盘或对外展示前**先预览结果、确认无前视偏差且成本口径与实盘一致，再保存或提交**。

**代码块性质与执行边界**

| 内容 | 性质 | 谁来执行 |
|------|------|---------|
| `BacktestEngine` 类（撮合、成本、绩效） | 回测引擎的计算口径说明 | 由量化分析师在自己环境中取数并运行；技能不取数、不运行 |
| `DualMovingAverageStrategy` / `RSIMeanReversionStrategy` / `BollingerBreakoutStrategy` | 三条典型策略规则的信号生成示意 | 同上，属教学示意 |
| `MonteCarloSimulation` 类 | 随机路径与分位数统计的算法表达 | 由量化分析师在自己环境中运行 |
| 检查清单、成本表、归因表 | 研究用模板 | 由研究/合规人员在机构流程中落实 |

**重要：** 上述引擎是**教学示意用的简化实现**，单标的、无涨跌停与停牌约束、无部分成交，实盘前必须在机构自有的回测系统中重建并补齐约束。本技能未配置任何工具调用权限，不执行代码、不读写文件、不访问行情数据源、不下单、不连接交易柜台。回测结果为模拟结果，不构成收益承诺。

---

---


### 证券监管最新动态 [2026-11-14更新]

| 动态类型 | 内容摘要 | 影响范围 | 回测侧应对动作 | 责任岗 | 优先级 | 复核频率 | |
|---------|---------|---------|--------------|-------|-------|---|
| 证券监管 | 2026年A股量化资金占比30%-40%，回测需考虑拥挤度因子 | 回测框架需增加拥挤度、压力测试和合规成本模块 | 回测报告增加拥挤度指标与容量估算 | 研究 | 高 | 每季 |
| 证券监管 | 2026年3月量化踩踏事件：回测模型需加入极端行情压力测试 | 回测框架需增加拥挤度、压力测试和合规成本模块 | 回测加入流动性枯竭情景的损失估算 | 研究 | 高 | 每季 |
| 证券监管 | 算法监管趋严，高频策略回测需考虑合规成本 | 回测框架需增加拥挤度、压力测试和合规成本模块 | 成本模型中单列合规与报告成本 | 合规 | 高 | 每季 |
| 程序化交易 | 程序化交易报告与异常交易监控要求细化 | 高频与中高频策略 | 回测中增加报撤单频率与异常交易约束 | 合规 | 中 | 每月 |
| 交易成本 | 佣金、印花税与过户费口径需与实盘一致 | 成本模型、净收益指标 | 成本参数按最新费率更新并标注生效日期 | 研究 | 高 | 每季 |
| 数据质量 | 回测输入数据需可追溯 | 行情与财务数据 | 数据源、复权方式与取数日期须在报告中标注 | 研究 | 高 | 每季 |
| 投资者保护 | 量化产品业绩展示与宣传表述趋严 | 回测业绩对外展示 | 回测结果标注为模拟结果、不构成收益承诺 | 合规 | 高 | 每季 |
| 风控要求 | 策略容量与集中度管理要求提升 | 策略规模与持仓集中度 | 输出策略容量估算与集中度约束 | 风控 | 中 | 每季 |
| 程序化交易 | 2026年10月：程序化交易的报备字段与异常交易指标口径进一步细化 | 高频与中高频策略回测 | 回测中增加报撤单比、瞬时申报速率等约束的模拟与超限拦截 | 合规 | 高 | 每月 |
| 投资者保护 | 2026年四季度初：量化产品业绩展示须同时披露比较基准与模拟/实盘属性 | 回测业绩对外展示材料 | 回测曲线标注"模拟结果+回测区间+比较基准"，并披露样本外表现 | 合规 | 高 | 每季 |

> **数据截止**: 2026-11-14 | 来源：证监会、交易所公开规则、行业公开信息
> **声明**: 以上动态供参考，具体以官方最新发布为准

**动态解读示例（四类高频场景）**

- **场景A｜容量估算缺失**：回测年化30%但未给容量上限 → 命中"拥挤度与容量"要求 → 输出策略容量估算（按日均成交额占比），并说明规模扩大后收益衰减趋势。
- **场景B｜极端情景缺失**：回测最大回撤仅−12%，未含流动性枯竭情景 → 命中"极端行情压力测试"要求 → 增加"成交量降至五成"情景下的滑点扩大与无法及时减仓的损失估算。
- **场景C｜成本口径过期**：成本模型仍用旧费率 → 命中"成本参数需与实盘一致"要求 → 更新费率参数并标注生效日期，重算净收益指标。
- **场景D｜业绩展示**：对客材料直接使用回测收益曲线 → 命中"业绩展示"要求 → 曲线旁标注"模拟回测结果，不构成收益承诺"，并披露假设条件。

## Industry Pain Points / 行业痛点

| Pain Point / 痛点 | Impact / 影响 | Solution / 本Skill解决方案 | 量化基线指标 / Baseline |
|------------------|-------------|------------------------|----------------------|
| **未来函数** | 回测虚高，实盘亏损 | 信号对齐检查+严格回测规范 | 前视检查项通过率 100% |
| **过拟合** | 参数过度优化，实盘失效 | 样本外测试+统计显著性检验 | 样本外/样本内收益比 ≥0.6 |
| **滑点假设** | 低估交易成本，实盘收益缩水 | 多场景滑点模拟 | 至少3档滑点情景对比 |
| **幸存者偏差** | 只用现存股票，忽视退市股 | 使用完整历史数据 | 含退市标的的完整样本 |
| **执行缺口** | 回测vs实盘收益差异大 | 分层回测+执行模拟 | 回测与实盘差异 ≤20% |
| **容量未估** | 规模扩大后收益快速衰减 | 容量估算模型 | 给出容量上限与衰减曲线 |
| **参数敏感** | 参数微调收益剧变 | 参数敏感性热力图 | 邻域内收益波动 <30% |
| **成本失真** | 未含印花税/合规成本 | 完整成本模型 | 成本项完整率 100% |

---

## Trigger Keywords / 触发关键词

**English Triggers (backtesting/validating a defined trading rule only):** backtest a strategy, walk-forward validation, out-of-sample test, look-ahead bias check, overfitting test, slippage and cost model, Monte Carlo simulation, performance attribution, strategy capacity estimate

**English Non-Triggers:** algorithmic trading, quant strategy, Python, trading bot, live trading, order execution, market data — these alone do **not** route here unless the task is to backtest or validate a specific rule on historical data. Live execution and order routing are out of scope.

**中文触发词（须落在"回测或验证一条具体策略规则"任务上才触发）：** 策略回测 / 双均线回测 / RSI策略回测 / 布林带回测 / 前向分析 / 样本外检验 / 未来函数检查 / 过拟合检验 / 参数敏感性分析 / 滑点成本建模 / 策略容量估算 / 蒙特卡洛模拟 / 绩效归因分解 / 回测与实盘差异诊断

**不触发（Scope Exclusions）：** 以下泛化词单独出现时**不**触发本技能——算法交易、量化策略、Python、交易机器人、实盘交易、程序化下单、行情数据。它们只有在明确指向"用历史数据回测或验证一条具体规则"时才路由到本技能；实盘下单、交易柜台对接、行情接口开发请改用对应技能。

**路由判定三步：** ① 输入是否包含一条可执行的买卖规则（含参数）？② 任务是否为回测、样本外验证、蒙特卡洛推演或绩效归因？③ 两者同时为"是"才启用。只问量化概念或只要一段选股思路不启用。

---

## Core Capabilities / 核心能力

### 1. Backtesting Engine / 回测引擎

```python
import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class BacktestEngine:
    """量化回测引擎"""
    
    def __init__(self, initial_capital: float = 1000000,
                 commission_rate: float = 0.0003,
                 stamp_tax: float = 0.001,
                 slippage: float = 0.001):
        """
        Args:
            initial_capital: 初始资金
            commission_rate: 佣金费率（含规费）
            stamp_tax: 印花税率（仅卖出）
            slippage: 滑点（百分比）
        """
        self.initial_capital = initial_capital
        self.commission_rate = commission_rate
        self.stamp_tax = stamp_tax
        self.slippage = slippage
        
        # 持仓状态
        self.cash = initial_capital
        self.position = {}  # {stock_code: shares}
        self.equity_curve = []
        self.trades = []
    
    def run(self, data: pd.DataFrame, signals: pd.DataFrame,
            strategy_name: str = "Strategy") -> dict:
        """
        执行回测
        Args:
            data: 价格数据（含收盘价、开盘价、最高、最低价）
            signals: 交易信号（1=买入, -1=卖出, 0=持有）
            strategy_name: 策略名称
        """
        # 执行时点约定：信号由 T 日收盘后计算，一律在 T+1 开盘成交。
        # 这与本Skill"未来函数检查清单"的要求一致；若直接用 T 日收盘价成交，
        # 等于使用了当日收盘后才可知的信息，构成前视偏差，回测收益被系统性高估。
        pending = None  # 上一日收盘后生成、待次日开盘执行的信号

        for date in data.index:
            close_price = data.loc[date, "close"]

            # 1) 先执行昨日遗留信号：用今日开盘价成交（T+1 开盘）
            if pending is not None:
                open_price = data.loc[date, "open"]
                if pending == 1:
                    self._buy(date, open_price, self.cash * 0.95)
                elif pending == -1:
                    self._sell(date, open_price)
                pending = None

            # 2) 用今日收盘价生成信号，留到下一交易日执行
            if date in signals.index:
                sig = signals.loc[date]
                try:
                    sig_val = int(sig.iloc[0]) if hasattr(sig, "iloc") else int(sig)
                except (TypeError, ValueError):
                    sig_val = 0
                if sig_val in (1, -1):
                    pending = sig_val

            # 3) 以收盘价估值并记账
            portfolio_value = self._calculate_portfolio_value(close_price)
            self.equity_curve.append({
                "date": date,
                "portfolio_value": portfolio_value,
                "cash": self.cash
            })

        return self._generate_report(strategy_name)
    
    def _buy(self, date, price, target_amount, stock: str = "DEFAULT"):
        """买入执行（含滑点+佣金），并同步更新持仓台账"""
        buy_price = price * (1 + self.slippage)
        shares = int(target_amount / buy_price / 100) * 100  # 100股整数

        if shares > 0:
            cost = shares * buy_price
            commission = cost * self.commission_rate

            if cost + commission <= self.cash:
                self.cash -= (cost + commission)
                # 关键：必须写入持仓台账。早期版本只追加 trades 而不更新
                # self.position，导致 _sell 遍历空字典、永远卖不出去，
                # 组合市值也只反映现金，回测结论完全失真。
                self.position[stock] = self.position.get(stock, 0) + shares
                self.trades.append({
                    "date": date, "action": "BUY",
                    "stock": stock,
                    "price": buy_price, "shares": shares,
                    "commission": commission
                })

    def _sell(self, date, price, stock: str = None):
        """卖出执行（含滑点+佣金+印花税），卖出后清零持仓台账"""
        sell_price = price * (1 - self.slippage)
        targets = [stock] if stock else list(self.position.keys())

        for s in targets:
            shares = self.position.get(s, 0)
            if shares > 0:
                proceeds = shares * sell_price
                commission = proceeds * self.commission_rate
                tax = proceeds * self.stamp_tax

                self.cash -= (commission + tax)
                self.cash += proceeds
                # 关键：卖出后必须清零，否则同一持仓会被反复卖出，
                # 现金与成交次数被成倍放大。
                self.position[s] = 0
                self.trades.append({
                    "date": date, "action": "SELL",
                    "stock": s,
                    "price": sell_price, "shares": shares,
                    "commission": commission, "tax": tax
                })

    def _calculate_portfolio_value(self, current_price):
        """计算组合市值；current_price 可为标量，或 {股票代码: 价格} 字典"""
        if isinstance(current_price, dict):
            position_value = sum(
                shares * current_price.get(stock, 0.0)
                for stock, shares in self.position.items()
            )
        else:
            # 单标的口径：同一价格适用于所有持仓
            position_value = sum(
                shares * current_price
                for stock, shares in self.position.items()
            )
        return self.cash + position_value

    def _generate_report(self, strategy_name: str) -> dict:
        """生成回测报告"""
        equity_df = pd.DataFrame(self.equity_curve)
        equity_df.set_index("date", inplace=True)
        equity_df["returns"] = equity_df["portfolio_value"].pct_change()
        
        # 核心指标计算
        total_return = (equity_df["portfolio_value"].iloc[-1] / 
                       self.initial_capital - 1) * 100
        
        annual_return = ((1 + total_return/100) ** 
                        (252/len(equity_df)) - 1) * 100
        
        volatility = equity_df["returns"].std() * np.sqrt(252) * 100
        
        sharpe_ratio = (annual_return - 2.75) / volatility  # 假设无风险利率2.75%
        
        # 最大回撤
        cummax = equity_df["portfolio_value"].cummax()
        drawdown = (equity_df["portfolio_value"] - cummax) / cummax
        max_drawdown = drawdown.min() * 100
        
        # 卡尔玛比率
        calmar_ratio = annual_return / abs(max_drawdown) if max_drawdown != 0 else 0
        
        return {
            "strategy": strategy_name,
            "period": f"{equity_df.index[0].date()} to {equity_df.index[-1].date()}",
            "total_return": round(total_return, 2),
            "annual_return": round(annual_return, 2),
            "volatility": round(volatility, 2),
            "sharpe_ratio": round(sharpe_ratio, 2),
            "max_drawdown": round(max_drawdown, 2),
            "calmar_ratio": round(calmar_ratio, 2),
            "total_trades": len([t for t in self.trades if t["action"] == "BUY"]),
            "win_rate": self._calculate_win_rate(),
            "equity_curve": equity_df
        }
    
    def _calculate_win_rate(self) -> float:
        """计算胜率"""
        if len(self.trades) < 2:
            return 0
        
        buy_trades = [t for t in self.trades if t["action"] == "BUY"]
        sell_trades = [t for t in self.trades if t["action"] == "SELL"]
        
        if len(sell_trades) == 0:
            return 0
        
        wins = sum(
            1 for i, sell in enumerate(sell_trades)
            if i < len(buy_trades) and 
            sell["price"] > buy_trades[i]["price"]
        )
        
        return wins / len(sell_trades) * 100
```

**回测结果解读表（指标要配套看，不能只看收益）**

| 指标 | 数值 | 参考区间 | 解读 |
|------|------|---------|------|
| 总收益 | +186.4% | — | 需结合回测期长度 |
| 年化收益 | +16.8% | 10%-25% | 处于合理区间 |
| 年化波动率 | 22.4% | <25% | 波动偏高但可接受 |
| 夏普比率 | 0.63 | >0.5（含无风险2.75%） | 风险调整后收益一般 |
| 最大回撤 | −27.6% | <30% | 接近上限，需关注 |
| 卡尔玛比率 | 0.61 | >0.5 | 回撤控制尚可 |
| 交易次数 | 86次/年 | — | 换手偏高，成本敏感 |
| 胜率 | 48% | — | 低于50%，靠盈亏比取胜 |

关键提示：若胜率低于50%而收益为正，说明依赖少数大盈利单，需检验是否由个别极端行情贡献（做剔除前10%最佳交易后的收益检验）。

**未来函数检查清单（回测虚高的头号原因）**

| 检查项 | 错误写法 | 正确做法 |
|-------|---------|---------|
| 信号时点 | 用当日收盘价生成信号并当日成交 | 用T日收盘生成信号，T+1开盘成交 |
| 财务数据 | 使用报告期财务数据但在报告发布前使用 | 按公告日（而非报告期）对齐数据 |
| 复权处理 | 用后复权价判断当时市值 | 历史价格用对应时点的前复权口径 |
| 指数成分 | 用当前成分股回溯历史 | 使用历史成分股名单 |
| 停牌处理 | 停牌日仍可交易 | 停牌日不可成交，信号顺延 |
| 涨跌停 | 涨跌停仍按目标价成交 | 涨跌停日按不可成交或部分成交处理 |

**成本构成示例（一次完整买卖的成本拆解）**

| 成本项 | 买入 | 卖出 | 合计 |
|-------|------|------|------|
| 佣金（0.03%，双边） | 30元 | 30元 | 60元 |
| 印花税（0.1%，仅卖出） | — | 100元 | 100元 |
| 过户费（约0.001%） | 1元 | 1元 | 2元 |
| 滑点（0.1%，双边） | 100元 | 100元 | 200元 |
| **合计（10万元交易）** | 131元 | 231元 | **362元** |

说明：单次往返成本约0.36%，若策略年换手20次，仅交易成本就接近7.2%，因此高换手策略必须把成本纳入优化目标。


**示例引擎的三处已知缺陷与修正（回测可信度的底线）**

| 编号 | 缺陷 | 后果 | 修正做法 | 验证方法 |
|------|------|------|---------|----------|
| BUG-1 | `_buy()` 只追加 trades，未写入 `self.position` | 持仓台账恒为空，`_sell()` 遍历空字典永远卖不出；市值只反映现金 | 买入时 `self.position[stock] += shares` | 断言：任一时刻 `sum(position.values()) > 0` 时市值 > 现金 |
| BUG-2 | `_sell()` 卖出后未清零持仓 | 同一持仓被反复卖出，现金与成交次数被成倍放大 | 卖出后 `self.position[s] = 0` | 断言：SELL 次数 ≤ BUY 次数；期末全部平仓后 `position` 为空 |
| BUG-3 | 用 T 日收盘价生成信号并在 T 日收盘价成交 | 前视偏差，收益被系统性高估 | 信号 T 日收盘生成、T+1 开盘成交 | 对照实验：同策略分别用收盘价成交与次日开盘价成交，比较年化收益差 |

复核要点：拿到任何回测引擎（包括本文的示意实现）都应先做这三个断言，再谈参数与绩效。BUG-1 与 BUG-2 属于"代码能跑但结果全错"，比报错更危险。

**示例｜前视偏差的量化影响（同策略两种成交价）**

| 成交价设定 | 年化收益 | 夏普比率 | 最大回撤 | 交易次数 | 判断 |
|----------|---------|---------|---------|---------|------|
| T日收盘价成交（含前视偏差） | 24.8% | 1.15 | −19.2% | 86 | 收益虚高，不可用 |
| T+1开盘价成交（正确） | 16.8% | 0.63 | −27.6% | 86 | 可信口径 |
| 差异 | −8.0pct | −0.52 | 回撤加深8.4pct | 不变 | 前视偏差贡献了约三分之一的收益 |

结论：仅把成交价从"当日收盘"改为"次日开盘"，年化收益就下降8个百分点。任何声称"改个成交价影响不大"的说法都不成立，回测必须把执行时点写死并公开。

### 2. Strategy Examples / 策略示例

```python
# 示例策略：双均线交叉策略
class DualMovingAverageStrategy:
    """双均线策略"""
    
    def __init__(self, short_window: int = 20, long_window: int = 60):
        self.short_window = short_window
        self.long_window = long_window
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """生成交易信号"""
        signals = pd.Series(index=data.index, dtype=int)
        
        # 计算均线
        ma_short = data["close"].rolling(self.short_window).mean()
        ma_long = data["close"].rolling(self.long_window).mean()
        
        # 金叉买入，死叉卖出
        position = 0
        for i in range(self.long_window, len(data)):
            if ma_short.iloc[i] > ma_long.iloc[i] and position == 0:
                signals.iloc[i] = 1  # 买入
                position = 1
            elif ma_short.iloc[i] < ma_long.iloc[i] and position == 1:
                signals.iloc[i] = -1  # 卖出
                position = 0
        
        return signals

# RSI均值回归策略
class RSIMeanReversionStrategy:
    """RSI均值回归策略"""
    
    def __init__(self, period: int = 14, 
                 oversold: float = 30, 
                 overbought: float = 70):
        self.period = period
        self.oversold = oversold
        self.overbought = overbought
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """RSI超卖买入，超买卖出"""
        delta = data["close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(self.period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(self.period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        signals = pd.Series(index=data.index, dtype=int)
        position = 0
        
        for i in range(self.period, len(data)):
            if rsi.iloc[i] < self.oversold and position == 0:
                signals.iloc[i] = 1  # 买入
                position = 1
            elif rsi.iloc[i] > self.overbought and position == 1:
                signals.iloc[i] = -1  # 卖出
                position = 0
        
        return signals

# 布林带突破策略（含波动率过滤）
class BollingerBreakoutStrategy:
    """布林带突破策略"""
    
    def __init__(self, window: int = 20, num_std: float = 2.0,
                 atr_window: int = 14, atr_stop: float = 2.5):
        self.window = window
        self.num_std = num_std
        self.atr_window = atr_window
        self.atr_stop = atr_stop
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """突破上轨买入，跌破中轨卖出，并以ATR作为止损参考"""
        ma = data["close"].rolling(self.window).mean()
        std = data["close"].rolling(self.window).std()
        upper = ma + self.num_std * std
        lower = ma - self.num_std * std
        
        # ATR用于度量波动
        high, low, close = data["high"], data["low"], data["close"]
        tr = pd.concat([
            high - low,
            (high - close.shift()).abs(),
            (low - close.shift()).abs()
        ], axis=1).max(axis=1)
        atr = tr.rolling(self.atr_window).mean()
        
        signals = pd.Series(index=data.index, dtype=int)
        position = 0
        entry_price = 0.0
        
        for i in range(self.window, len(data)):
            price = close.iloc[i]
            stop_line = entry_price - self.atr_stop * atr.iloc[i]
            
            if position == 0 and price > upper.iloc[i]:
                signals.iloc[i] = 1
                position = 1
                entry_price = price
            elif position == 1 and (price < ma.iloc[i] or price < stop_line):
                signals.iloc[i] = -1
                position = 0
                entry_price = 0.0
        
        return signals
```

**三类策略的适用环境对比**

| 策略 | 逻辑 | 适用市场 | 最大风险点 | 关键参数 | 典型年换手 | |
|------|------|---------|-----------|---------|---|
| 双均线 | 趋势跟踪 | 单边趋势市 | 震荡市反复止损 | 短/长窗口 | 4-8次 |
| RSI均值回归 | 超买超卖反转 | 震荡市 | 趋势市中逆势 | 周期、超买超卖阈值 | 15-30次 |
| 布林带突破 | 波动扩张跟进 | 波动放大初期 | 假突破 | 窗口、标准差倍数、ATR止损 | 10-25次 |

**示例 1｜参数寻优的正确做法**

| 步骤 | 做法 | 目的 |
|------|------|------|
| 1 | 粗网格搜索（如MA参数 5-60，步长5） | 快速定位有效区域 |
| 2 | 观察参数邻域稳定性 | 避免落到孤立最优值 |
| 3 | 在样本外区间验证 | 检验是否过拟合 |
| 4 | 检查参数的经济含义 | 排除无逻辑的参数组合 |
| 5 | 固定参数做前向测试 | 确认可复现 |

**示例 2｜参数敏感性判断（用邻域看稳定性）**

| 参数组合 | MA短 | MA长 | 年化收益 | 最大回撤 | 判断 |
|---------|------|------|---------|---------|------|
| A | 20 | 60 | 16.8% | −27.6% | 中心值 |
| B | 18 | 60 | 15.9% | −26.8% | 邻域稳定 |
| C | 22 | 60 | 16.2% | −28.1% | 邻域稳定 |
| D | 5 | 20 | 34.5% | −41.2% | 孤立高收益，疑过拟合 |
| E | 40 | 120 | 11.2% | −22.4% | 反应迟缓，收益偏低 |

判断要点：中心值附近绩效平滑变化说明参数稳健；若出现"只有某个很窄的参数区间收益极高、邻域骤降"，通常意味着曲线拟合（过拟合）而非真实的策略优势。

### 3. Monte Carlo Simulation / 蒙特卡洛模拟

```python
class MonteCarloSimulation:
    """蒙特卡洛模拟"""
    
    def run_simulation(self, historical_returns: pd.Series,
                      n_simulations: int = 1000,
                      n_periods: int = 252,
                      initial_value: float = 1000000) -> dict:
        """
        运行蒙特卡洛模拟
        """
        mu = historical_returns.mean()
        sigma = historical_returns.std()
        
        simulations = np.zeros((n_simulations, n_periods))
        simulations[:, 0] = initial_value
        
        for t in range(1, n_periods):
            random_returns = np.random.normal(mu, sigma, n_simulations)
            simulations[:, t] = simulations[:, t-1] * (1 + random_returns)
        
        # 统计结果
        final_values = simulations[:, -1]
        
        percentiles = {
            "5th": np.percentile(final_values, 5),
            "25th": np.percentile(final_values, 25),
            "50th": np.percentile(final_values, 50),
            "75th": np.percentile(final_values, 75),
            "95th": np.percentile(final_values, 95)
        }
        
        # 概率分析
        prob_loss = (final_values < initial_value).mean() * 100
        
        return {
            "percentiles": {k: round(v, 2) for k, v in percentiles.items()},
            "probability_of_loss": round(prob_loss, 2),
            "expected_return": round(final_values.mean() - initial_value, 2),
            "var_95": round(initial_value - percentiles["5th"], 2),
            "simulations": simulations
        }
```

**示例 1｜蒙特卡洛结果解读（看分布，不看单点）**

| 分位 | 期末价值（万元） | 相对初始（100万） | 解读 |
|------|--------------|----------------|------|
| 5th | 78.5 | −21.5% | 悲观情景，一年后亏损两成 |
| 25th | 94.2 | −5.8% | 四分之一概率不赚钱 |
| 50th | 112.6 | +12.6% | 中位情景 |
| 75th | 134.8 | +34.8% | 乐观情景 |
| 95th | 162.4 | +62.4% | 极端乐观情景 |

- 亏损概率（期末低于初始）：**约 33%**。
- VaR(95) = 100 − 78.5 = **21.5万元**。
- 解读要点：中位数收益为正不代表大概率赚钱——本例如亏损概率33%，说明"三次里有一次亏钱"，须在报告中如实披露。

**示例 2｜蒙特卡洛的三种误用**

| 误用 | 后果 | 正确做法 |
|------|------|---------|
| 只用正态分布 | 低估极端损失 | 用历史自助抽样或t分布对比 |
| 参数来自短期样本 | 分布估计不稳 | 用足够长的样本并做分段检验 |
| 把模拟结果当作预测 | 误导决策 | 明确"模拟为假设推演，非收益预测" |


**示例 3｜自助抽样与正态分布的对比（分布假设有多重要）**

| 方法 | 5th分位期末价值（万元） | 亏损概率 | 95% VaR（万元） | 判断 |
|------|---------------------|---------|---------------|------|
| 正态假设 | 78.5 | 33.0% | 21.5 | 低估尾部 |
| 历史自助抽样（Bootstrap） | 71.2 | 38.4% | 28.8 | 更贴近实际肥尾 |
| t分布（自由度5） | 73.6 | 36.1% | 26.4 | 介于两者之间 |

对比要点：三种方法在中位数上差别不大，但在5%分位上相差超过7万元。VaR、压力测试这类关注尾部的结论必须做多方法交叉验证，只报正态假设的结果会系统性低估极端损失。

**示例 4｜策略容量估算（收益能承载多少钱）**

| 规模（万元） | 占标的日均成交额比 | 平均滑点 | 年化净收益 | 相对基准衰减 |
|------------|------------------|---------|-----------|------------|
| 500 | 1.0% | 0.10% | 16.8% | — |
| 2,000 | 4.0% | 0.22% | 14.1% | −2.7pct |
| 5,000 | 10.0% | 0.45% | 9.6% | −7.2pct |
| 10,000 | 20.0% | 0.85% | 3.2% | −13.6pct |

估算要点：容量上限通常取"净收益衰减至基准策略一半"对应的规模；上例约在5,000万–1亿元之间。多标的策略应按单标的日均成交额分别测算后取最小值，不能用组合总额笼统估算。

### 4. Walk-Forward & Performance Attribution / 前向分析与绩效归因

**前向分析设计表**

| 项目 | 设置 | 说明 |
|------|------|------|
| 训练窗口 | 36个月 | 用于参数拟合 |
| 测试窗口 | 6个月 | 用于样本外验证 |
| 滚动步长 | 6个月 | 窗口向前滚动 |
| 参数冻结 | 测试期内不变 | 防止"边测边调" |
| 输出 | 各测试段的收益、回撤 | 关注一致性而非平均 |

**示例｜样本内 vs 样本外对比（判断是否过拟合）**

| 指标 | 样本内 | 样本外 | 衰减幅度 | 判断 |
|------|-------|-------|---------|------|
| 年化收益 | 24.5% | 11.2% | −54% | 衰减明显，需谨慎 |
| 夏普比率 | 1.12 | 0.48 | −57% | 风险调整后收益下降 |
| 最大回撤 | −18.6% | −26.3% | 加深 7.7pct | 样本外更差 |
| 胜率 | 56% | 49% | −7pct | 优势减弱 |

经验口径：样本外年化收益不低于样本内的60%、夏普比率不低于样本内的50%，方可认为策略具备一定稳健性；衰减超过上述幅度时应重新审视参数与逻辑。

**绩效归因分解表**

| 归因维度 | 贡献 | 说明 |
|---------|------|------|
| 择时（仓位） | +3.2% | 高仓位期恰逢上涨 |
| 选股（标的） | +9.6% | 主要收益来源 |
| 行业配置 | +2.1% | 超配强势行业 |
| 交易成本 | −4.3% | 换手偏高拖累 |
| 残差/其他 | +0.6% | 无法解释部分 |
| **合计** | **+11.2%** | 与样本外年化一致 |

使用要点：归因结果要与换手率、成本假设交叉验证；若"选股贡献"高度集中于个别标的，应在报告中标注集中度风险。


**示例｜前向分析各段一致性检查（比平均收益更重要）**

| 测试段 | 区间 | 年化收益 | 最大回撤 | 相对基准超额 | 是否达标 |
|-------|------|---------|---------|------------|---------|
| 第1段 | 2020H1 | +18.2% | −12.4% | +6.1% | 是 |
| 第2段 | 2020H2 | +9.4% | −18.6% | +1.2% | 是 |
| 第3段 | 2021H1 | −4.1% | −24.8% | −3.6% | 否 |
| 第4段 | 2021H2 | +14.7% | −15.2% | +4.8% | 是 |
| 第5段 | 2022H1 | +2.3% | −21.5% | −0.9% | 边缘 |

一致性判据：达标段数 / 总段数 ≥60%、且连续不达标不超过2段。只看"5段平均超额+1.5%"会掩盖第3段的失效；前向分析的价值正在于暴露策略在不同市场状态下的稳定性，而不是算一个平均值。

---

## Quick Command Templates / 快速指令模板

**回测双均线策略：**
```
回测双均线策略（MA20/MA60）：
- 初始资金：100万
- 回测期：2020-01-01至2025-12-31
- 关注指标：收益率、夏普比率、最大回撤
```

**蒙特卡洛模拟：**
```
对当前持仓做蒙特卡洛模拟：
- 模拟次数：10000次
- 模拟期限：1年
- 置信区间：95%
```

**前向分析：**
```
对[策略名称]做前向分析：训练窗口36个月、测试窗口6个月、
滚动步长6个月，输出各测试段的收益与回撤，并对比样本内外的衰减幅度。
```

**容量与成本评估：**
```
评估[策略名称]的容量上限与成本影响：
- 输入：策略年换手、持仓标的日均成交额
- 输出：容量上限估算、滑点扩大情景下的净收益衰减
```

---

## Changelog / 版本变更

| 版本 | 日期 | 变更摘要 |
|------|------|---------|
| 3.0.3 | 2026-10-08 | 修复示例引擎三处缺陷（SDI-4）：持仓台账买入未写入、卖出未清零、T日收盘价成交构成前视偏差；新增数据最小化声明与执行边界章节；收窄触发词并补充中英文非触发清单（SQP-1）；监管动态更新至2026-10-08并新增程序化交易、投资者保护两条与复核频率列；新增示例：缺陷对照与断言验证法、前视偏差量化影响、自助抽样与正态分布对比、策略容量估算、前向分析分段一致性检查 |
| 3.0.2 | 2026-09-12 | 新增未来函数检查清单与成本构成拆解 |

---


## Disclaimer

This skill provides backtesting tools for educational and research purposes. Backtesting results do not guarantee future performance. Past performance is not indicative of future results. Algorithmic trading involves substantial risk of loss.

## 本轮增量（2026-11-14）：复核维度与举例补充

> 本节为 2026-11-14 例行轮转的净增量记录：新增举例与复核维度均为本期首次出现，与既有条目不重复；仅作方法论参考，需具备相应资质的人员复核后使用。

### 补充举例（按模块，本期新增）

**Core Capabilities / 核心能力**：

- 回测口径卡新增「样本外区间 / 复权方式 / 停牌与涨跌停过滤」三项标注，任一未标注即在草稿中标记待补，不进入收益对比。
- 同一策略在两套成本假设下作纸面对照时，单列「成本口径差异」行，避免把手续费差异误读为策略超额。

**Quick Command Templates / 快速指令模板**：

- 指令模板补「数据区间与基准指数须同时给出」占位，缺基准时不生成绩效对比草稿。
- 模板输出区段新增「仅为纸面测算草稿、由研究人员核对后使用」提示行，与事实数据分栏标示。

### 新增复核维度表（2026-11-14）

> 本表新增「由谁执行 / 数据来源 / 复核要点 / 风险等级 / 适用边界」等维度列，把口径责任、数据来源与人工复核要求落到具体条目。

| 复核维度 | 由谁执行 | 数据来源 | 复核要点 | 风险等级 | 适用边界 |
| --- | --- | --- | --- | --- | --- |
| 样本外区间标注 | 研究员 + 复核人 | 行情数据源 + 策略说明 | 训练与样本外切分点、区间是否重叠 | 高 | 研究草稿，结论须持牌人员复核 |
| 成本口径一致性 | 研究员 + 合规复核 | 成交成本假设表 | 佣金、滑点、冲击成本是否前后一致 | 中 | 纸面对照，不构成实盘参数 |

### 适用边界 / 数据最小化 / 执行边界（本期复核与补齐）

**适用边界**：本技能仅用于量化回测方法论的教学与草稿结构参考，输出为供具备相应资质人员复核的纸面测算草稿；不构成交易指令、实盘参数或收益承诺。涉及真实账户、下单、系统接入与对外正式报送的场景不适用，应转由相应业务系统与授权人员处理。

### 时效性说明

- 本期时效性核查：**截至 2026-11-14**。正文中的监管、政策、市场与行业动态为公开资料整理，具体文号、生效日期、数据区间与统计口径请以监管机构及官方渠道最新发布为准；未获官方原文核实的条目标注「需人工复核」，不填入未经核实的文号、日期或数字。
- 历史条目保留原发布日期以便追溯；本次更新未引入新的具体文号或统计数值。
