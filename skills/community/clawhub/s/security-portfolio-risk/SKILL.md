---
name: Portfolio Risk Analysis Expert
slug: security-portfolio-risk
description: AI-powered portfolio risk analysis expert for China market — quantifies risk on a given holdings portfolio: VaR/CVaR, stress testing, tail risk, factor exposure and risk-contribution decomposition. Scope: portfolio-level quantitative risk measurement only; not general risk-management consultancy, not single-name research, not asset-allocation theory. Keywords: portfolio VaR, CVaR, stress testing, risk contribution, risk decomposition, factor exposure, tail risk, China A-share, 组合风险分析, 组合VaR, CVaR计算, 组合压力测试, 风险归因, 风险贡献分解, 因子敞口, 尾部风险, 集中度风险检查, 风险预算.
version: "3.0.5"
---

# Portfolio Risk Analysis Expert / 组合风险分析专家

> **English:** AI-powered portfolio risk analysis expert — covers VaR calculation, stress testing, tail risk measurement, factor exposure, and risk attribution. Built for fund managers and risk analysts.
>
> **中文:** 组合风险分析专家——覆盖VaR计算、压力测试、尾部风险度量、因子敞口分析、风险归因。适用：基金经理、风险分析师、机构投资者。


---

## 数据最小化声明与执行边界 / Data Minimisation & Execution Boundary

**数据最小化前置声明：** 使用本技能时，请只提供风险测算所必需的输入——标的代码、权重、收益率或净值序列、已脱敏的组合规模（可用“1000万”这类量级，无需精确金额）。**不要**粘贴账户号、身份证号、实际成交明细、客户身份信息或未公开的持仓数据；个人持仓请用“标的+权重”的脱敏形式提供。

**保存与预览确认：** 本技能不执行任何保存动作。若你在自己环境中依据本技能生成风险报告、压力测试结论或风险预算表，请在落盘或对外报送前**先预览结果、确认口径与阈值无误，再保存或提交**。

**代码块性质与执行边界**

| 内容 | 性质 | 谁来执行 |
|------|------|---------|
| `PortfolioRiskAnalyzer` 类（VaR/CVaR/回撤/因子归因） | 风险指标的计算口径说明 | 由风险分析师在自有风控系统中取数复现；技能不取数、不运行 |
| `StressTestScenarios` 情景库与 `run_stress_test` | 情景参数与冲击传导的示意 | 由风险分析师在自有系统中配置并运行 |
| `risk_contribution_by_asset` | 边际风险贡献（MCTR）的算法表达 | 同上，属教学示意 |
| 口径登记表、阈值表、处置清单 | 管理用模板 | 由风控人员在机构流程中落实 |

本技能未配置任何工具调用权限，不执行代码、不读写文件、不访问行情或持仓数据源，也不生成可直接报送的监管报表。文中代码块均为指标口径的教学示意，读者可在自己环境中参考实现；风险测算结果须经独立复核后方可用于决策。

---


### 证券监管最新动态 [2026-11-13更新]

| 动态类型 | 内容摘要 | 影响范围 | 风险侧应对动作 | 责任岗 | 优先级 | 复核频率 | |
|---------|---------|---------|--------------|-------|-------|---|
| 证券监管 | 2026年Q1：市场波动加剧，组合风险管理要求提升 | 组合风险模型需增加量化冲击和ESG风险维度 | 风险报告增设极端情景专项说明 | 风控 | 高 | 每季 |
| 证券监管 | 量化资金共振风险增加，极端行情止损策略需更新 | 组合风险模型需增加量化冲击和ESG风险维度 | 压力测试新增流动性枯竭情景 | 风控 | 高 | 每季 |
| 证券监管 | ESG投资分析要求扩大，组合风险需纳入ESG因素 | 组合风险模型需增加量化冲击和ESG风险维度 | 风险分解单列ESG敞口维度 | 风控 | 中 | 每季 |
| 程序化交易 | 程序化交易报告与异常交易监控要求细化 | 极端行情下的流动性与波动归因 | 压力测试中区分程序化交易影响部分 | 风控 | 中 | 每月 |
| 信息披露 | 上市公司信息披露质量监管强化 | 风险模型的财务输入数据 | 模型输入须标注报告期与数据来源 | 风控 | 高 | 每季 |
| 估值与净值 | 净值化管理要求下风险指标披露趋严 | 产品风险报告与定期披露 | 波动率、回撤、VaR口径固定并留档 | 合规 | 高 | 每月 |
| 投资者保护 | 风险揭示与适当性匹配要求提升 | 产品风险等级与客户匹配 | 风险报告附适当性匹配说明 | 合规 | 高 | 每季 |
| 集中度管理 | 单一标的与单一行业集中度关注度提升 | 组合集中度指标 | 集中度阈值纳入日常监控与预警 | 风控 | 高 | 日 |
| 估值与净值 | 2026年9月下旬：净值化产品的风险指标披露口径一致性要求进一步强化 | 定期报告、产品风险揭示书 | 波动率/回撤/VaR三项口径写进口径登记表并随报告留档 | 合规 | 高 | 每月 |
| 集中度管理 | 2026年三季度：单一标的与单一行业集中度的日常监控要求细化 | 组合集中度指标 | 集中度监控改为日频，超限当日报送投资经理 | 风控 | 高 | 日 |
| 风险揭示 | 2026年10月上旬：净值型产品风险指标与业绩展示口径的一致性检查趋严，报告值与宣传值须同源 | 风险报告、产品宣传材料 | 波动率/回撤/VaR的报告数值与对外展示数值差异须书面说明 | 合规 | 高 | 每月 |
| 模型风险管理 | 2026年四季度初：机构风险模型的验证与留痕要求细化，模型版本与参数来源须可追溯 | 风险模型、参数与情景库 | 建立模型台账，登记模型版本、参数来源、情景设定依据并按季复核 | 风控 | 高 | 每季 |

> **数据截止**: 2026-11-13 | 来源：证监会、交易所公开规则、行业公开信息
> **声明**: 以上动态供参考，具体以官方最新发布为准

**动态解读示例（四类高频场景）**

- **场景A｜流动性枯竭情景**：压力测试仅覆盖价格冲击，未考虑成交量萎缩 → 命中"量化共振风险"要求 → 新增"流动性降至50%+价格下跌20%"的复合情景，输出无法顺利减仓的敞口估算。
- **场景B｜ESG敞口单列**：风险分解仅按行业与因子拆分 → 命中"ESG风险维度"要求 → 在风险分解中增加ESG评级分布与高碳敞口占比。
- **场景C｜口径固定留档**：不同报告的波动率口径时而日频、时而月频 → 命中"口径固定披露"要求 → 统一为日频年化并在报告中标注计算口径与样本区间。
- **场景D｜集中度预警**：单标的市值占比升至18%未触发任何预警 → 命中"集中度监控"要求 → 设置单标的15%、单行业35%的预警线，超限自动进入整改流程。

- **场景E｜口径不一致被问询**：同一产品季报用日频波动率、月报用月频波动率，数值无法比对 → 命中“口径一致性要求强化” → 建立口径登记表，把频率、样本窗口、无风险利率基准三项写死，每次出报告先对照登记表，改口径须留变更记录。
- **场景F｜集中度监控滞后**：集中度按周监控，超限后已持仓三天 → 命中“日常监控细化” → 改为日频自动计算，超限当日推送投资经理与风控，并在T+1前给出减仓或冻结新增买入的处置结论。

监控自检：口径看“是否跨报告一致”，集中度看“是否当日发现当日处置”。两条决定风险报告能否经得起复核。


## Industry Pain Points / 行业痛点

| Pain Point / 痛点 | Impact / 影响 | Solution / 本Skill解决方案 | 量化基线指标 / Baseline |
|------------------|-------------|------------------------|----------------------|
| **系统风险难预测** | 黑天鹅事件导致大幅回撤 | 极端情景压力测试+尾部风险分析 | 压力测试情景覆盖 ≥6类 |
| **因子敞口不清晰** | 不知道组合暴露在哪些风险上 | 因子归因模型+敞口分解 | 因子解释度 R² ≥0.7 |
| **回撤控制困难** | 持有人体验差，资金赎回压力 | 动态回撤监控+预警机制 | 最大回撤控制在预设阈值内 |
| **相关性突变** | 平时低相关的资产大跌时齐跌 | 相关性压力测试+分散化效果评估 | 压力情景下相关性假设上浮至0.7+ |
| **合规要求高** | 资管新规净值化要求 | 标准风险指标+监管报告 | 风险指标披露完整率 100% |
| **集中度超标** | 单一标的/行业权重过高 | 集中度监控阈值+预警 | 单标的≤15%、单行业≤35% |
| **尾部风险低估** | VaR未反映肥尾特征 | CVaR与修正VaR双口径 | 同时披露VaR与CVaR |
| **口径不一致** | 跨报告指标不可比 | 计算口径登记表 | 口径一致率 100% |

---

## Trigger Keywords / 触发关键词

**English Triggers (portfolio-level quantitative measurement only):** portfolio VaR, portfolio CVaR, stress test a portfolio, risk contribution, risk decomposition, factor exposure of a portfolio, tail risk measurement, correlation stress test, concentration check

**English Non-Triggers:** risk management, asset allocation, diversification, volatility, Sharpe ratio, risk-adjusted return, drawdown control — these alone do **not** route here; they must be scoped to "measure or decompose risk for a specific holdings portfolio".

**中文触发词（须落在“计算/分解一个组合的风险”任务上才触发）：** 组合风险分析 / 组合VaR / CVaR计算 / 组合压力测试 / 组合回撤分析 / 风险归因 / 因子敞口分解 / 尾部风险度量 / 风险贡献分析 / 风险预算分配 / 集中度风险检查 / 分散化效果评估 / 相关性压力测试

**不触发（Scope Exclusions）：** 以下泛化词单独出现时**不**触发本技能——风险分析、风险管理、资产配置、分散化、波动率、夏普比率、风险调整收益、回撤控制。它们只有在明确指向“对某个持仓组合做量化风险测算或分解”时才路由到本技能；单只证券的风险特征、通用资产配置理论、泛化的风险管理咨询请改用对应技能。

**路由判定三步：** ① 输入是否为一组持仓（标的+权重）？② 任务是否为计算VaR/CVaR、跑压力情景、分解风险贡献或检查集中度？③ 两者同时为“是”才启用。只问概念定义不启用。

---

## Core Capabilities / 核心能力

### 1. VaR & Risk Metrics / VaR与风险指标

```python
import numpy as np
import pandas as pd
from scipy import stats

class PortfolioRiskAnalyzer:
    """组合风险分析引擎"""
    
    def __init__(self, returns: pd.DataFrame, weights: np.ndarray):
        """
        Args:
            returns: 收益率序列（列=资产，行=日期）
            weights: 资产权重向量
        """
        self.returns = returns
        self.weights = weights
        self.n_assets = len(weights)
    
    def calculate_var(self, confidence: float = 0.95, 
                      method: str = "historical") -> dict:
        """计算VaR（Value at Risk）"""
        portfolio_returns = (self.returns * self.weights).sum(axis=1)
        
        if method == "historical":
            var = np.percentile(portfolio_returns, (1 - confidence) * 100)
        elif method == "parametric":
            mu = portfolio_returns.mean
            sigma = portfolio_returns.std
            var = stats.norm.ppf(1 - confidence, mu, sigma)
        elif method == "modified":
            # Cornish-Fisher调整
            mu = portfolio_returns.mean
            sigma = portfolio_returns.std
            skew = stats.skew(portfolio_returns)
            kurt = stats.kurtosis(portfolio_returns)
            z = stats.norm.ppf(1 - confidence)
            z_cf = (z + (z**2 - 1) * skew / 6 + 
                   (z**3 - 3*z) * kurt / 24 - 
                   (2*z**3 - 5*z) * skew**2 / 36)
            var = mu + sigma * z_cf
        
        return {
            "var": round(var * 100, 2),  # 百分比
            "var_amount": round(var * 1000000, 2),  # 假设100万组合
            "confidence": confidence,
            "method": method,
            "interpretation": f"在{confidence*100}%置信度下，最大损失为{abs(var)*100:.2f}%"
        }
    
    def calculate_cvar(self, confidence: float = 0.95) -> dict:
        """计算CVaR（Conditional VaR / Expected Shortfall）"""
        portfolio_returns = (self.returns * self.weights).sum(axis=1)
        var = np.percentile(portfolio_returns, (1 - confidence) * 100)
        
        cvar = portfolio_returns[portfolio_returns <= var].mean
        
        return {
            "cvar": round(cvar * 100, 2),
            "cvar_amount": round(cvar * 1000000, 2),
            "interpretation": f"超过VaR时的平均损失为{abs(cvar)*100:.2f}%"
        }
    
    def calculate_max_drawdown(self) -> dict:
        """计算最大回撤"""
        cumulative = (1 + self.returns @ self.weights).cumprod
        running_max = cumulative.expanding.max
        drawdown = (cumulative - running_max) / running_max
        
        max_dd = drawdown.min
        max_dd_end = drawdown.idxmin
        max_dd_start = cumulative[:max_dd_end].idxmax
        
        return {
            "max_drawdown": round(max_dd * 100, 2),
            "peak_date": str(max_dd_start.date),
            "trough_date": str(max_dd_end.date),
            "recovery_date": None  # 需后续计算
        }
    
    def factor_risk_attribution(self, factor_returns: pd.DataFrame) -> dict:
        """因子风险归因"""
        portfolio_returns = self.returns @ self.weights
        
        # 回归分析
        X = factor_returns.values
        X = np.column_stack([np.ones(len(X)), X])
        y = portfolio_returns.values
        
        coeffs = np.linalg.lstsq(X, y, rcond=None)[0]
        residuals = y - X @ coeffs
        
        # 分解方差
        total_var = np.var(y)
        factor_var = np.var(X[:, 1:] @ coeffs[1:])
        specific_var = np.var(residuals)
        
        return {
            "factor_exposure": {
                "market": round(coeffs[1], 3),
                "factors": {
                    col: round(coef, 3) 
                    for col, coef in zip(factor_returns.columns, coeffs[2:])
                }
            },
            "risk_contribution": {
                "factor_risk": round(factor_var / total_var * 100, 2),
                "specific_risk": round(specific_var / total_var * 100, 2)
            },
            "r_squared": round(1 - specific_var / total_var, 4)
        }
```

**VaR 三种方法对比（同一组合结果可能差异明显）**

| 方法 | 假设 | 适用场景 | 优点 | 局限 | 报告披露要求 |
|------|------|---------|------|------|---|
| 历史模拟法 | 未来分布与历史一致 | 样本充足、分布未知 | 不依赖分布假设 | 依赖历史窗口，肥尾可能漏估 | 须注明样本窗口 |
| 参数法（正态） | 收益率服从正态分布 | 快速估算、常规监控 | 计算快、易解释 | 低估极端损失 | 须提示低估风险 |
| 修正VaR（Cornish-Fisher） | 引入偏度与峰度 | 收益率非正态的市场 | 能反映肥尾特征 | 参数估计误差敏感 | 须同时披露CVaR |

实践建议：日常监控用历史模拟法，风险报告同时披露修正VaR与CVaR；若三者差异超过30%，须在报告中说明原因。

**示例 1｜组合VaR手算与解读**

- 输入：组合日收益率序列近250个交易日，95%置信度。
- 历史模拟法：取第5百分位收益 = **−2.35%**，即"95%置信度下，单日最大损失约2.35%"。
- 组合规模1000万元 → VaR金额 = 1000万 × 2.35% = **23.5万元**。
- CVaR（超过VaR部分的均值）= **−3.62%** → 金额 **36.2万元**，说明极端日的平均损失比VaR更深。
- 解读要点：VaR回答"最多亏多少（在95%情形下）"，CVaR回答"突破之后平均亏多少"，二者必须同时披露。

**示例 2｜最大回撤解读与恢复期**

| 项目 | 数值 | 说明 | 口径 |
|------|------|------|---|
| 最大回撤 | −18.6% | 峰值到谷底跌幅 | 复权净值口径 |
| 峰值日期 | 2026-03-12 | 回撤起点 | 峰值日 |
| 谷底日期 | 2026-05-28 | 回撤最深日 | 谷底日 |
| 回撤持续天数 | 77天 | 下跌过程时长 | 自然日 |
| 是否已恢复 | 否（当前−9.4%） | 尚未回到前高 | 相对峰值 |
| 恢复所需时间 | 待观察 | 不应假设"必然恢复" | 不做恢复假设 |

解读要点：回撤分析要给出三件事——多深、多久、是否恢复；只报"最大回撤−18.6%"而不说恢复状态会误导持有人。

**风险指标口径登记表（避免跨报告不可比）**

| 指标 | 计算口径 | 频率 | 样本窗口 | 备注 | 责任人 |
|------|---------|------|---------|------|---|
| 年化波动率 | 日收益率标准差×√244 | 日 | 近1年 | 采用交易日244天 | 风控 |
| 最大回撤 | 复权净值峰值到谷底 | 日 | 成立以来 | 标注峰值与谷底日期 | 风控 |
| 夏普比率 | (年化收益−无风险利率)/年化波动率 | 月 | 近1年 | 无风险利率用1年期国债 | 风控 |
| VaR | 历史模拟法，95% | 日 | 近250日 | 同时披露CVaR | 风控 |
| 跟踪误差 | 相对基准超额收益标准差 | 周 | 近1年 | 标注基准指数 | 风控 |

**示例 3｜三种VaR差异过大时的排查（差异>30%即须说明）**

| 排查项 | 检查内容 | 常见原因 |
|-------|---------|---------|
| 样本窗口 | 历史模拟法是否覆盖了极端区间 | 窗口过短，未包含大跌样本 |
| 分布假设 | 参数法是否低估肥尾 | 收益率峰度显著高于正态 |
| 偏度方向 | 修正VaR的方向是否合理 | 极端偏度导致Cornish-Fisher不稳定 |
| 单位与频率 | 三种方法是否同频同年化 | 日VaR与年化VaR混用 |

处置原则：三者差异超过30%时，报告中采用“修正VaR或CVaR”作为保守口径，并说明历史模拟法为何偏低；不得只披露数值最低的一种。

**示例 4｜置信度与持有期的VaR换算（跨报告最易出错）**

| 置信度 | 1日VaR | 10日VaR（√10 换算） | 1000万组合10日VaR金额 | 适用场景 |
|--------|--------|-------------------|---------------------|----------|
| 90% | −1.72% | −5.44% | 54.4万元 | 内部日常监控 |
| 95% | −2.35% | −7.43% | 74.3万元 | 标准风险报告披露 |
| 99% | −4.10% | −12.97% | 129.7万元 | 极端情形专项说明 |

换算前提：√t 外推仅在收益率独立同分布、无波动率集聚的假设下成立。若样本期内存在明显的波动率集聚（大涨大跌连续出现），√t 会低估持有期风险，此时应直接用重叠区间的历史收益计算多日VaR，并在报告中写明所用方法。常见错误是把95%的1日VaR当作10日VaR填报，损失被低估约3倍。

**示例 5｜VaR回退测试（Kupiec检验口径）**

| 检验项 | 数值 | 判断 | 处置 |
|-------|------|------|------|
| 检验样本天数 | 250 | 一年交易日 | — |
| 95% VaR被突破次数 | 18 | 期望约12.5次 | 突破偏多 |
| 实际突破率 | 7.2% | 高于5%的理论水平 | 模型低估风险 |
| 结论 | 未通过 | 需重估样本窗口或改用修正VaR | 调宽窗口至500日并重跑 |

回退测试要点：突破次数显著高于理论值说明模型低估风险，应拉长样本窗口或改用能反映肥尾的口径；突破次数远低于理论值则说明模型过于保守，会不必要地占用风险额度。回退测试应至少每季度做一次并留档。



### 2. Stress Testing / 压力测试

```python
class StressTestScenarios:
    """压力测试情景库"""
    
    SCENARIOS = {
        "2015股灾重演": {
            "description": "假设上证指数单周下跌20%",
            "market_shock": -0.20,
            "sector_impacts": {
                "金融": -0.25,
                "房地产": -0.30,
                "消费": -0.15,
                "科技": -0.20,
                "医药": -0.10
            },
            "liquidity_shock": 0.5  # 流动性降至50%
        },
        
        "利率急升": {
            "description": "假设基准利率上调100bp",
            "rate_shock": 0.01,
            "bond_impact": -0.08,
            "equity_impact": -0.10,
            "bank_impact": -0.05
        },
        
        "人民币急贬": {
            "description": "假设USD/CNY一日升值5%",
            "fx_shock": 0.05,
            "export_related": -0.15,
            "import_related": 0.05,
            "domestic_consumer": -0.08
        },
        
        "黑天鹅-新冠": {
            "description": "类似2020年初疫情冲击",
            "market_shock": -0.12,
            "travel": -0.30,
            "retail": -0.20,
            "healthcare": 0.10,
            "online": 0.05
        },
        
        "流动性枯竭-量化踩踏": {
            "description": "成交额萎缩至五成，程序化交易减仓放大波动",
            "market_shock": -0.18,
            "liquidity_shock": 0.5,
            "sector_impacts": {
                "小市值": -0.28,
                "高换手": -0.32,
                "大盘蓝筹": -0.12,
                "红利低波": -0.08
            },
            "correlation_shift": 0.85,
            "notes": "分散化效果在此情景下显著减弱"
        },
        
        "利率下行-资产重定价": {
            "description": "基准利率下调50bp，利率敏感资产重估",
            "rate_shock": -0.005,
            "bond_impact": 0.04,
            "equity_impact": 0.06,
            "bank_impact": -0.03,
            "notes": "债券与红利资产受益，银行净息差承压"
        }
    }
    
    def run_stress_test(self, portfolio: dict, scenario: str) -> dict:
        """执行压力测试"""
        if scenario not in self.SCENARIOS:
            raise ValueError(f"Unknown scenario: {scenario}")
        
        s = self.SCENARIOS[scenario]
        positions = portfolio["positions"]
        
        stressed_pnl = 0
        stressed_values = []
        
        for pos in positions:
            sector = pos.get("sector", "general")
            weight = pos["weight"]
            
            # 根据情景调整
            if "sector_impacts" in s and sector in s["sector_impacts"]:
                shock = s["sector_impacts"][sector]
            else:
                shock = s.get("market_shock", -0.10)
            
            pos_stressed = weight * (1 + shock)
            stressed_values.append(pos_stressed)
            stressed_pnl += weight * shock
        
        total_value = sum(stressed_values)
        portfolio_stress_loss = total_value - 1  # 假设初始为1
        
        return {
            "scenario": scenario,
            "description": s["description"],
            "portfolio_loss": round(portfolio_stress_loss * 100, 2),
            "portfolio_value_after": round(total_value * 100, 2),
            "position_impacts": [
                {"name": pos["name"], "weight": pos["weight"], 
                 "shock": round(shock * 100, 2), "impact": "loss" if shock < 0 else "gain"}
                for pos, shock in zip(positions, 
                    [s.get("sector_impacts", {}).get(pos.get("sector", ""), 
                     s.get("market_shock", -0.10)) for pos in positions])
            ]
        }
```

**情景结果对照表（一次跑完所有情景，横向比较）**

| 情景 | 组合冲击 | 最受伤资产 | 相对受益资产 | 触发动作 | 复核频率 | 流动性假设 | |
|------|---------|-----------|------------|---------|---|---|
| 2015股灾重演 | −21.5% | 房地产、金融 | 医药 | 降仓、暂停加仓 | 每季 | 降至50% |
| 利率急升100bp | −9.2% | 债券、权益、银行 | 现金类 | 缩短久期 | 每月 | 正常 |
| 人民币急贬5% | −7.8% | 进口相关、消费 | 出口相关 | 核查外汇敞口 | 每月 | 正常 |
| 黑天鹅-新冠 | −12.6% | 交运、零售 | 医药、线上 | 按行业再平衡 | 每季 | 正常 |
| 流动性枯竭-量化踩踏 | −19.4% | 小市值、高换手 | 红利低波 | 优先减仓低流动性标的 | 每月 | 降至50% |
| 利率下行50bp | +4.1% | 银行 | 债券、红利资产 | 适度提升久期 | 每季 | 正常 |

**示例 1｜压力测试后的处置清单**

| 优先级 | 处置动作 | 触发条件 | 责任人 | 时限 | 留痕要求 |
|-------|---------|---------|-------|------|---|
| 1 | 降低整体仓位至60%以下 | 任一情景损失>15% | 投资经理 | T+1 | 调仓记录+审批 |
| 2 | 减仓流动性最差标的 | 流动性情景损失>威胁阈值 | 交易 | T+1 | 成交明细 |
| 3 | 暂停同向新增买入 | 集中度超限 | 投资经理 | 即时 | 冻结记录 |
| 4 | 补充现金缓冲 | 组合现金<5% | 投资经理 | T+2 | 现金台账 |
| 5 | 出具情景专项说明 | 任一情景损失>10% | 风控 | T+3 | 专项说明归档 |

**示例 2｜压力测试阈值设定（把结果变成规则）**

| 指标 | 正常区间 | 预警线 | 处置线 | 超限后果 |
|------|---------|-------|-------|---|
| 单情景最大损失 | <10% | 10%-15% | >15% | 启动降仓预案 |
| 组合年化波动率 | <18% | 18%-25% | >25% | 提交风险说明 |
| 单标的权重 | <10% | 10%-15% | >15% | 暂停新增买入 |
| 单一行业权重 | <25% | 25%-35% | >35% | 暂停新增买入 |
| 前三大标的合计 | <30% | 30%-40% | >40% | 提交集中度说明 |
| 压力情景下相关性 | <0.5 | 0.5-0.7 | >0.7 | 重估分散化假设 |

**示例 3｜自建情景与历史情景的差异（两种都要有）**

| 维度 | 历史情景（如2015股灾） | 自建情景（如量化踩踏） |
|------|---------------------|---------------------|
| 参数来源 | 真实历史区间 | 假设参数设定 |
| 优点 | 有事实依据，易被接受 | 可覆盖历史上未发生的风险 |
| 局限 | 难以覆盖新风险形态 | 参数设定主观，需说明依据 |
| 使用方式 | 作为基准情景 | 至少保留2个自建极端情景 |

配置建议：情景库至少6个，其中历史情景与自建情景各占一半；自建情景必须写明参数设定依据，避免“拍脑袋”设定导致结论不可复现。

**示例 4｜自建情景的参数设定依据留痕表（应对模型复核）**

| 情景 | 关键参数 | 设定依据 | 上次复核结论 | 复核频率 |
|------|---------|---------|------------|----------|
| 流动性枯竭-量化踩踏 | 成交额降至50%、相关性升至0.85 | 参照历史极端区间成交额萎缩幅度与相关性上浮观测值 | 参数合理，保留 | 每季 |
| 利率急升100bp | 利率+100bp、债券−8% | 参照历史单季最大利率变动幅度 | 冲击偏轻，考虑上调至150bp | 每季 |
| 人民币急贬5% | USD/CNY +5% | 参照历史单日最大波幅并留有余量 | 参数合理，保留 | 每季 |

留痕要点：自建情景最容易被复核挑战的地方是“参数从哪来”。每个参数都要能追溯到一段可指认的历史观测或一项明确的假设，并注明复核日期与结论；参数无依据的情景在正式报告中不应使用。

**示例 5｜压力测试结果与限额的联动（结果必须落到动作）**

| 情景损失 | 限额状态 | 联动动作 | 是否需要审批 |
|---------|---------|---------|------------|
| <10% | 限额内 | 仅记录，不触发动作 | 否 |
| 10%–15% | 预警区 | 出具情景专项说明，投资经理确认 | 风控负责人 |
| >15% | 超限 | 启动降仓预案，T+1内降至60%以下 | 投决会 |
| 流动性情景 >25% | 严重超限 | 优先减仓低流动性标的，冻结新增买入 | 投决会 |

联动要点：压力测试不是“跑完出个数”，而是要把结果映射到限额层级与审批链。只输出损失百分比而不说明触发哪一级动作，报告在复核时会被判定为不可用。



### 3. Risk Contribution Analysis / 风险贡献分析

```text
# 说明：以下方法为 PortfolioRiskAnalyzer 类的成员，此处单独摘出以突出算法口径，
# 实际使用时应置于该类内部（与 calculate_var / calculate_cvar 等方法并列）。
    def risk_contribution_by_asset(self) -> dict:
        """计算各资产风险贡献"""
        cov_matrix = self.returns.cov
        portfolio_vol = np.sqrt(self.weights @ cov_matrix.values @ self.weights)
        
        # 边际风险贡献 (MCTR)
        mctr = (cov_matrix.values @ self.weights) / portfolio_vol
        
        # 风险贡献
        risk_contrib = self.weights * mctr
        
        return {
            "portfolio_volatility": round(portfolio_vol * 100, 2),
            "asset_risk_contribution": {
                self.returns.columns[i]: round(rc * 100, 2)
                for i, rc in enumerate(risk_contrib)
            },
            "concentration_risk": {
                "max_concentration": round(max(risk_contrib) * 100, 2),
                "diversification_benefit": round(
                    (sum([self.returns[col].std * w 
                         for col, w in zip(self.returns.columns, self.weights)]) - 
                     portfolio_vol) * 100, 2)
            }
        }
```

**示例 1｜权重与风险贡献的错位（最容易忽视的风险）**

| 资产 | 权重 | 波动率 | 风险贡献 | 权重-风险差 | 结论 | 建议动作 |
|------|------|-------|---------|-----------|------|---|
| 股票A | 30% | 32% | 42% | −12pct | 风险贡献显著高于权重，需减配 | 减配至20%以下 |
| 股票B | 20% | 20% | 14% | +6pct | 风险效率较高 | 可维持 |
| 债券C | 40% | 6% | 9% | +31pct | 起到稳定器作用 | 保持压舱石 |
| 黄金ETF | 10% | 15% | 6% | +4pct | 分散化贡献明显 | 保持 |
| **组合** | 100% | — | 71%（含相关项） | — | 组合波动率 14.2% | 整体波动率达标 |

解读要点：权重高不等于风险高——上例中权重30%的股票A贡献了42%的组合风险，是真正需要关注的对象；风险报告应同时展示权重与风险贡献两列，避免只看权重做决策。

**示例 2｜分散化效果评估**

| 场景 | 加权平均波动率 | 组合波动率 | 分散化收益 | 判断 | 应对 |
|------|-------------|----------|-----------|------|---|
| 常态市场 | 18.5% | 14.2% | 4.3pct | 分散化有效 | 维持现有结构 |
| 相关性上浮至0.7 | 18.5% | 17.1% | 1.4pct | 效果显著减弱 | 准备降仓预案 |
| 相关性上浮至0.85（踩踏情景） | 18.5% | 18.2% | 0.3pct | 几乎失效 | 按单一风险暴露处理 |

解读要点：分散化在极端行情下会被显著削弱，"平时低相关"不能作为风险控制的唯一依据；报告须同时给出常态与压力情景下的分散化收益对比。

**示例 3｜风险预算分配（把风险额度当成资源）**

| 资产类别 | 风险预算 | 实际风险贡献 | 偏离 | 调整动作 | 复核周期 |
|---------|---------|------------|-----|---------|---|
| 权益 | 50% | 71% | +21pct | 减配，或增加低波动品种 | 每周 |
| 固收 | 30% | 18% | −12pct | 可适度提升久期 | 每月 |
| 商品/黄金 | 10% | 6% | −4pct | 保持 | 每月 |
| 现金 | 10% | 5% | −5pct | 保持 | 每月 |

使用要点：风险预算与实际贡献偏离超过10pct即需调整；调整时应优先通过降低高波动资产权重实现，而非简单增加杠杆。
**示例 4｜相关性突变时的集中度重估**

| 状态 | 平均相关性 | 有效分散标的数 | 单标的上限 | 处置 |
|------|-----------|--------------|-----------|------|
| 常态 | 0.30 | 约8个 | 15% | 按常规阈值 |
| 预警 | 0.55 | 约4个 | 12% | 收紧单标的上限 |
| 压力 | 0.85 | 约1.5个 | 8% | 视为单一风险暴露，整体降仓 |

重估逻辑：相关性上升时，“持有10只标的”并不等于分散到10个风险源，须按有效分散标的数重估集中度上限；相关性进入压力区间后，分散化收益趋近于零，应直接按单一风险暴露处理。

**示例 5｜资产法风险贡献与因子法归因的交叉验证**

| 风险源 | 资产法风险贡献 | 因子法风险归因 | 差异 | 判断 |
|-------|--------------|--------------|------|------|
| 市场（Beta） | — | 58% | — | 因子法可拆分，资产法不可 |
| 行业因子 | — | 21% | — | 同上 |
| 个股特有风险 | 29%（残差项） | 21% | 8pct | 两法残差口径不同，需说明 |
| 合计解释度 | 100% | R²=0.79 | — | 解释度尚可 |

交叉验证要点：资产法回答“哪一只标的最危险”，因子法回答“组合暴露在哪类系统性风险上”，二者不可互相替代。若因子法R²低于0.7，说明模型遗漏了重要风险因子（常见为行业或风格因子缺失），此时因子归因结论不可单独用于调仓决策。

**示例 6｜风险贡献超预算的分步减仓推演**

| 步骤 | 动作 | 权益风险贡献变化 | 组合波动率变化 | 备注 |
|------|------|----------------|--------------|------|
| 现状 | 权益风险贡献71%，预算50% | 71% | 14.2% | 偏离+21pct |
| 第一步 | 高波动个股A由30%降至20% | 61% | 12.8% | 优先降高波动标的 |
| 第二步 | 增配低波红利品种至15% | 54% | 11.9% | 不引入新风险源 |
| 第三步 | 现金比例由5%提至10% | 50% | 11.1% | 达标 |

推演要点：调仓应分步进行并逐 step 观察风险贡献与组合波动率的联动，避免一次性大幅调仓带来交易成本与冲击成本。若推演后发现无论如何调整都无法把风险贡献压回预算，应反推风险预算本身是否设得过低，而不是硬凑达标。




---

## Quick Command Templates / 快速指令模板

**组合风险评估：**
```
分析以下组合的风险：
- 总规模：1000万
- 持仓：[股票A 30%, 股票B 20%, 债券B 50%]
- 置信度：95%
```

**压力测试：**
```
执行"2015股灾重演"情景压力测试
```

**多情景横向比较：**
```
对以下组合跑全部压力情景，输出情景损失对照表、
最受伤资产、待触发处置动作与优先级：
- 持仓：[标的与权重]
- 组合规模：[X]万
```

**风险贡献与预算：**
```
计算以下组合各资产的风险贡献与风险预算偏离，
给出单标的≤15%、单行业≤35%的集中度检查结果与调整建议。
```

---

## Changelog / 版本变更

| 版本 | 日期 | 变更摘要 |
|------|------|---------|
| 3.0.4 | 2026-10-08 | 收窄触发词并补充英文非触发清单（SQP-1）；监管动态更新至2026-10-08并新增风险揭示、模型风险管理两条与复核频率列；情景结果对照表新增流动性假设列；新增示例：VaR置信度与持有期换算、VaR回退测试、自建情景参数留痕表、压力结果与限额联动、资产法与因子法交叉验证、风险贡献分步减仓推演 |
| 3.0.3 | 2026-09-30 | 新增口径登记表与集中度动态解读示例 |

---


## Disclaimer

This skill provides risk analysis tools for educational purposes. Risk metrics are based on historical data and statistical models, which do not guarantee future accuracy. Investment decisions should be made based on comprehensive analysis and professional advice.

## 本轮增量（2026-11-13）：复核维度与举例补充

> 本节为 2026-11-13 例行轮转的净增量记录：新增举例与复核维度均为本期首次出现，与既有条目不重复；仅作方法论参考，需具备相应资质的人员复核后使用。

### 补充举例（按模块，本期新增）

**1. VaR & Risk Metrics**：

- 报告须同时写明「持有期 / 置信水平 / 历史窗口 / 是否含期权非线性」四项参数；不同参数下的 VaR 不可直接比较，跨报告引用须附口径说明。
- 用历史模拟法时单列「窗口内含极端事件的比例」与「样本外回测的突破次数」，避免只报一个数值而不说明模型局限。

**2. Stress Testing / 压力测试**：

- 情景设计补「冲击传导路径」说明（如利率上行经估值、融资成本、信用利差三条路径影响组合），不只给最终损失数字。
- 对每个情景单列「假设可同时成立性」与「流动性约束」两项复核要点，并标注结果为示意测算，需人工复核后使用。

### 新增复核维度表（2026-11-13）

> 本表新增「由谁执行 / 数据来源 / 复核要点 / 风险等级 / 适用边界」等维度列，把口径责任、数据来源与人工复核要求落到具体条目。

| 复核维度 | 由谁执行 | 数据来源 | 复核要点 | 风险等级 | 适用边界 |
| --- | --- | --- | --- | --- | --- |
| VaR 参数披露 | 风险分析师 + 复核人 | 风险模型参数表 + 回测记录 | 四项参数、极端事件占比、突破次数 | 高 | 仅风险度量草稿，参数须人工确认 |
| 情景传导路径 | 风险分析师 | 情景假设 + 持仓明细 | 传导链条、假设同时成立性、流动性约束 | 高 | 示意测算，需人工复核后使用 |

### 适用边界 / 数据最小化 / 执行边界（本期补齐）

**适用边界**：本技能仅用于组合风险度量与压力测试的方法论参考与结构拆解，输出为供具备相应资质人员复核的草稿；不构成对具体主体、标的、客户或案件的最终结论、指令或承诺。超出该范围的场景（如实盘执行、自动审批、对外正式报送、系统登记）不适用本技能，应转由相应业务系统与授权人员处理。

### 时效性说明

- 本期时效性核查：**截至 2026-11-13**。正文中的监管、政策、市场与行业动态为公开资料整理，具体文号、生效日期、数据区间与统计口径请以监管机构及官方渠道最新发布为准；未获官方原文核实的条目标注「需人工复核」，不填入未经核实的文号、日期或数字。
- 历史条目保留原发布日期以便追溯；本次更新未引入新的具体文号或统计数值。
