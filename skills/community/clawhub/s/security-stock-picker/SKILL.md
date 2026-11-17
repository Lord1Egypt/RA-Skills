---
name: AI-Powered Stock Selection Engine
slug: security-stock-screening
description: AI-powered intelligent stock selection engine for China A-share market — covers quantitative factor screening, fundamental analysis ranking, technical signal detection, sector rotation analysis, and portfolio construction. Built for retail investors, fund managers, and quantitative analysts. Updated 2026 with latest factor models, short-seller vulnerability detection, and AI-enhanced stock screening. Keywords: stock selection, quantitative screening, factor investing, technical analysis, China A-share, stock picker, AI investing, 选股引擎, 量化选股, 因子投资, 技术分析, A股, 智能选股, 选股策略, 量化策略, AI选股, 股票筛选, 价值投资, 成长股, 短线选股.
version: "3.0.4"
---

# AI-Powered Stock Selection Engine / 智能选股引擎

> **English:** AI-powered intelligent stock selection engine for China A-share market — combines quantitative factor screening, fundamental analysis, technical signals, and sector rotation analysis. Solves pain points: information overload, emotional decision-making, and inconsistent stock picking criteria. Built for investors and analysts at all levels.
>
> **中文:** 智能选股引擎——整合量化因子筛选、基本面分析、技术信号检测、行业轮动分析的全流程选股工具。解决痛点：信息过载、情绪化决策、选股标准不统一。适用：各级投资者、基金经理、量化分析师。


---

## 数据最小化声明与执行边界 / Data Minimisation & Execution Boundary

**数据最小化前置声明：** 使用本技能时，请只提供构建筛选规则所必需的字段——股票代码、因子数值、报告期、已脱敏的持仓与可用资金规模。**不要**粘贴证券账户号、身份证号、银行账号、实际成交明细或他人持仓信息。若需基于个人持仓做再平衡分析，请用“标的+权重”的脱敏形式输入，不提供账户标识。

**保存与预览确认：** 本技能不执行任何保存动作。若你在自己环境中依据本技能生成候选池、组合方案或回测脚本，请在落盘或提交交易前**先预览结果、确认参数与阈值无误，再保存或执行**。

**代码块性质与执行边界**

| 内容 | 性质 | 谁来执行 |
|------|------|---------|
| `StockScreener` 类与因子权重表 | 因子定义、打分与归一化的口径说明 | 由研究员在自己的量化环境中取数并复现；技能不取数、不运行 |
| `THEMATIC_SCREENING` | 主题产业链拆解与筛选标准的结构化字典 | 由研究员按公开资料自行更新标的与标准 |
| `TechnicalSignals` 类 | 均线/支撑压力/量价异常的计算口径示意 | 由研究员在自有行情终端或回测框架中实现 |
| `FraudDetection` 类 | 财报异常指标的判定阈值说明 | 由研究员用公开财报数据计算，结论需人工复核 |
| `PortfolioBuilder` 类 | 等权重与风险平价的权重算法示意 | 由研究员在自有系统中运行；技能不下单、不调仓 |

本技能未配置任何工具调用权限，不执行代码、不读写文件、不访问行情或财报数据源，也不产生可直接执行的交易指令。文中代码块均为模型与阈值的教学示意，读者可在自己环境中参考实现；选股结果不构成投资建议，实盘前须独立核验数据与合规要求。

---


### 证券监管最新动态 [2026-11-13更新]

| 动态类型 | 内容摘要 | 影响范围 | 选股侧应对动作 | 责任岗 | 优先级 |
|---------|---------|---------|--------------|-------|-------|
| 证券监管 | 2026年A股量化资金占比30%-40%，选股模型需考虑量化冲击 | 选股引擎需增加量化冲击识别和极端行情风控 | 模型输出附带流动性冲击提示与成交结构说明 | 研究 | 高 |
| 证券监管 | 2026年3月23日量化踩踏案例（单日蒸发4.29万亿），风控需加强 | 选股引擎需增加量化冲击识别和极端行情风控 | 引入集中度与拥挤度指标，作为风控前置条件 | 研究 | 高 |
| 证券监管 | 上证周线级别中枢震荡，2026年核心区间3200-4000点 | 选股引擎需增加量化冲击识别和极端行情风控 | 震荡区间内降低趋势类因子权重 | 研究 | 中 |
| 程序化交易 | 程序化交易报告与异常交易监控要求细化 | 与量化资金相关的流动性与波动分析 | 在流动性评估中单独列示程序化交易影响 | 研究 | 中 |
| 信息披露 | 财务信息披露质量监管持续强化 | 财报异常检测、因子取数 | 因子取数须标注报告期与公告编号 | 研究 | 高 |
| 市值管理 | 上市公司市值管理行为披露要求趋严 | 涉及回购、增减持的个股筛选 | 筛选中单列股东行为事件标签 | 研究 | 中 |
| 业绩预告 | 业绩预告披露质量受关注 | 事件驱动类选股 | 使用预告数据时区分预告口径与实际口径 | 研究 | 高 |
| 投资者保护 | 投顾与荐股类内容传播边界收紧 | 选股结果对外输出 | 输出结果保留风险提示与免责声明 | 合规 | 高 |
| 程序化交易 | 2026年9月下旬：程序化交易报备与异常交易监控的执行细节进一步明确 | 高频与量化相关策略的流动性评估 | 冲击成本估算中单列程序化交易影响假设 | 研究 | 中 |
| 信息披露 | 2026年三季度：财务信息披露质量监管强化，业绩预告与实际数据偏差受关注 | 因子取数、事件驱动选股 | 预告与实际数据分栏并建立偏差跟踪字段 | 研究 | 高 |

> **数据截止**: 2026-11-13 | 来源：证监会、交易所公开规则、行业公开信息
> **声明**: 以上动态供参考，具体以官方最新发布为准

**动态解读示例（四类高频场景）**

- **场景A｜量化冲击识别**：某标的近20日成交额中位数仅0.8亿元，模型给出买入信号 → 命中"流动性冲击"风险 → 输出中增加"预估冲击成本"，并提示单笔建仓不超过日均成交额的5%。
- **场景B｜拥挤度预警**：某板块因子暴露高度集中、机构持仓占比快速抬升 → 命中"踩踏风险" → 在风控前置条件中加入拥挤度阈值，超阈值则降低该板块权重。
- **场景C｜因子取数可追溯**：ROE取数未标注报告期 → 命中"取数须可追溯" → 因子表增加"报告期"与"公告编号"两列，便于回溯与复算。
- **场景D｜预告口径混用**：用业绩预告中值直接作为当年利润因子 → 命中"预告与实际口径混用" → 预告期数据单列"预告口径"标记，与实际披露数据分栏展示。

- **场景E｜程序化交易影响未计入**：策略回测收益良好，实盘却因滑点大幅衰减 → 命中“程序化交易影响须单列” → 在冲击成本模型中增加“程序化成交占比”假设参数，并对小市值标的提高滑点设定，回测与实盘差异超过1个百分点时重新校准参数。
- **场景F｜预告偏差未跟踪**：依据预告中值选出的标的，实际披露后大面积不及预期 → 命中“预告与实际偏差受关注” → 因子表新增“预告偏差”字段（实际值−预告中值），连续两期偏差超过10%的公司下调其预告数据可信度权重。

口径自检三条：因子看报告期、回测看滑点假设、预告看历史偏差。三者缺一，选股结果的可信度无法自证。


## Industry Pain Points / 行业痛点

| Pain Point / 痛点 | Impact / 影响 | Solution / 本Skill解决方案 | 量化基线指标 / Baseline |
|------------------|-------------|------------------------|----------------------|
| **信息过载** | A股5000+股票，无法逐一研究 | 多维度因子筛选，快速缩小范围 | 一次筛选候选池 ≤50只 |
| **情绪化决策** | 追涨杀跌，高买低卖 | 量化标准选股，避免主观干扰 | 交易决策中规则触发占比 ≥80% |
| **选股标准模糊** | 没有系统性方法论 | 完整选股框架+评分模型 | 每条选股逻辑可量化复现 |
| **财报造假风险** | 康美药业、瑞幸等案例警示 | 财报异常信号检测+预警 | 高风险标的排除率 100% |
| **行业轮动难把握** | 踏错节奏，板块轮动踏空 | 宏观+情绪+资金三维轮动模型 | 轮动判断命中率 ≥60% |
| **流动性陷阱** | 小市值标的无法顺利进出 | 流动性门槛+冲击成本估算 | 单笔建仓 ≤日均成交额5% |
| **拥挤度风险** | 机构持仓过度集中引发踩踏 | 拥挤度指标与阈值监控 | 超阈值板块权重自动下调 |
| **样本外失效** | 因子在样本内有效、样本外失效 | 分区间验证与滚动检验 | 样本外IC保持同向 ≥60%窗 |

---

## Trigger Keywords / 触发关键词

**English Triggers:** stock selection, quantitative screening, factor investing, fundamental analysis, technical analysis, China A-share, stock picker, AI investing, momentum stocks, value investing, growth stocks, sector rotation, portfolio construction

**中文触发词（须落在“构造/检验一个选股规则”任务上才触发）：** 智能选股 / 量化选股 / 因子选股 / 因子有效性检验 / 基本面选股 / 技术面选股 / 行业轮动模型 / 板块轮动模型 / 主题选股 / 财报异常检测 / 组合构建 / 风险平价配置 / 建仓节奏 / 选股策略回测

**不触发（Scope Exclusions）：** 以下泛化词单独出现时**不**触发本技能——选股、价值投资、成长股、蓝筹股、小盘股、低估值、高成长、破净股、涨停板、龙虎榜、北向资金、资金流向、业绩超预期、AI选股、机器选股。它们只有在明确指向“设定筛选条件、检验因子、构建候选池或组合”时才路由到本技能；仅查询单只股票的行情、基本面或新闻，请改用行情与研报类技能。

**路由判定三步：** ① 任务是否要产出“一篮子股票”或“一条可复用的筛选规则”？② 是否涉及因子打分、信号检测、财报异常或组合权重？③ 两者同时为“是”才启用。只问“某只股票怎么样”的请求不启用。

---

## Core Capabilities / 核心能力

### 1. Quantitative Factor Screening / 量化因子筛选

```python
import pandas as pd
import numpy as np
from typing import List, Dict, Optional

class StockScreener:
    """智能选股引擎"""
    
    def __init__(self):
        self.factors = {
            # 估值因子
            "pe": {"name": "市盈率", "weight": 0.13, "direction": "low_better", "bounds": (0, 100)},
            "pb": {"name": "市净率", "weight": 0.10, "direction": "low_better", "bounds": (0, 10)},
            "ps": {"name": "市销率", "weight": 0.05, "direction": "low_better", "bounds": (0, 20)},
            "pcf": {"name": "市现率", "weight": 0.05, "direction": "low_better", "bounds": (0, 30)},
            
            # 成长因子
            "revenue_growth": {"name": "营收增速", "weight": 0.14, "direction": "high_better", "bounds": (-50, 100)},
            "profit_growth": {"name": "利润增速", "weight": 0.13, "direction": "high_better", "bounds": (-100, 200)},
            "gross_margin": {"name": "毛利率", "weight": 0.08, "direction": "high_better", "bounds": (0, 100)},
            
            # 质量因子
            "roe": {"name": "ROE", "weight": 0.10, "direction": "high_better", "bounds": (-20, 50)},
            "debt_ratio": {"name": "资产负债率", "weight": 0.05, "direction": "low_better", "bounds": (0, 100)},
            "current_ratio": {"name": "流动比率", "weight": 0.03, "direction": "high_better", "bounds": (0.5, 10)},
            
            # 动量因子
            "momentum_20d": {"name": "20日动量", "weight": 0.03, "direction": "high_better", "bounds": (-30, 50)},
            "momentum_60d": {"name": "60日动量", "weight": 0.01, "direction": "high_better", "bounds": (-50, 100)},
            
            # 股东回报因子
            "dividend_yield": {"name": "股息率", "weight": 0.05, "direction": "high_better", "bounds": (0, 8)},
            
            # 科创属性因子
            "rd_ratio": {"name": "研发投入占比", "weight": 0.05, "direction": "high_better", "bounds": (0, 30)}
        }
    
    def screen(self, stocks: pd.DataFrame, 
               criteria: Dict[str, tuple],
               min_score: float = 60) -> pd.DataFrame:
        """
        量化筛选主函数
        Args:
            stocks: 股票数据（含各因子列）
            criteria: 筛选条件 {因子名: (最小值, 最大值)}
            min_score: 最低综合评分
        Returns:
            符合条件的股票
        """
        result = stocks.copy
        
        # Step 1: 硬性条件筛选
        for factor, (min_val, max_val) in criteria.items:
            if factor in result.columns:
                result = result[(result[factor] >= min_val) & (result[factor] <= max_val)]
        
        # Step 2: 因子打分
        result = self._factor_scoring(result)
        
        # Step 3: 综合评分排序
        result = result[result["综合评分"] >= min_score].sort_values("综合评分", ascending=False)
        
        return result
    
    def _factor_scoring(self, df: pd.DataFrame) -> pd.DataFrame:
        """因子打分（百分制）"""
        scores = pd.DataFrame(index=df.index)
        
        for factor, config in self.factors.items:
            if factor in df.columns:
                raw = df[factor].copy
                min_val, max_val = config["bounds"]
                
                # 标准化到0-100
                normalized = (raw - min_val) / (max_val - min_val) * 100
                normalized = normalized.clip(0, 100)
                
                # 方向调整（部分因子越低越好）
                if config["direction"] == "low_better":
                    normalized = 100 - normalized
                
                scores[factor] = normalized * config["weight"]
        
        df["综合评分"] = scores.sum(axis=1)
        return df
```

**因子权重与方向一览（可直接核对权重合计）**

| 类别 | 因子 | 权重 | 方向 | 区间 | 震荡市调整建议 |
|------|------|------|------|------|---|
| 估值 | 市盈率/市净率/市销率/市现率 | 0.13/0.10/0.05/0.05 | 越低越好 | 见配置 | 维持或上调 |
| 成长 | 营收增速/利润增速/毛利率 | 0.14/0.13/0.08 | 越高越好 | 见配置 | 维持 |
| 质量 | ROE/资产负债率/流动比率 | 0.10/0.05/0.03 | 前三者高好、负债率低好 | 见配置 | 维持 |
| 动量 | 20日/60日动量 | 0.03/0.01 | 越高越好 | 见配置 | 下调至合计0.05 |
| 股东回报 | 股息率 | 0.05 | 越高越好 | 0-8% | 上调 |
| 科创属性 | 研发投入占比 | 0.05 | 越高越好 | 0-30% | 维持 |
| **合计** | — | **1.00** | — | — | — |

说明：权重合计必须为 1.00，新增因子时须同步下调其他因子权重；震荡市中可临时下调动量类因子权重（合计不超过0.05），以降低追高风险。

**示例 1｜单只标的打分手算（含低估值因子反向处理）**

| 因子 | 原始值 | 归一到0-100 | 方向调整后 | 权重 | 加权得分 |
|------|-------|------------|-----------|------|---------|
| 市盈率 | 18 | (18-0)/(100-0)×100=18 | 100-18=82 | 0.13 | 10.66 |
| 营收增速 | 25% | (25+50)/150×100=50 | 50 | 0.14 | 7.00 |
| 利润增速 | 40% | (40+100)/300×100=46.7 | 46.7 | 0.13 | 6.07 |
| ROE | 18% | (18+20)/70×100=54.3 | 54.3 | 0.10 | 5.43 |
| 股息率 | 3.2% | 3.2/8×100=40 | 40 | 0.05 | 2.00 |
| 研发投入占比 | 8% | 8/30×100=26.7 | 26.7 | 0.05 | 1.33 |
| **合计** | — | — | — | — | **（其余因子相加后）** |

要点：低估值因子必须先归一再用"100−归一值"翻转，否则会把高PE标的误判为最优。

**示例 2｜因子有效性检验（避免"看着好用"）**

| 检验项 | 方法 | 通过标准 | 不通过时处置 | 检验频率 |
|-------|------|---------|------------|---|
| 单因子IC | 因子值与下期收益的秩相关 | 绝对值 ≥0.03 且方向稳定 | 降低权重或剔除 | 每月 |
| 分组单调性 | 分5组看收益排序 | 收益随分组单调 | 检查极值处理方式 | 每季度 |
| 样本外表现 | 分年度滚动验证 | 样本外方向一致 | 缩短回看窗口 | 每半年 |
| 换手成本 | 统计换仓频率与手续费 | 年化换手成本 <3% | 引入换手惩罚 | 每次调仓 |
| 相关性 | 因子间相关系数 | 两两相关 <0.7 | 合并或删减冗余因子 | 每次新增因子 |

**示例 3｜权重调整与再平衡（新增因子后如何不破坏权重合计）**

| 操作 | 调整前 | 调整后 | 理由 |
|------|-------|-------|------|
| 新增“ESG评分”因子 | 权重合计1.00 | 新增0.05 | 需占用权重额度 |
| 下调动量类 | 0.03+0.01 | 0.02+0.01 | 震荡市降低追高风险 |
| 下调市销率 | 0.05 | 0.03 | 与市现率信息重叠 |
| 校验合计 | — | 1.00 | 必须回归1.00 |

再平衡规则：任何新增因子都必须从现有因子中等额扣减，扣减优先选择信息重叠度高或当前市场状态下失效的因子；调整后须重跑历史检验，确认样本外表现未显著恶化。



### 2. Thematic Stock Screening / 主题投资筛选

```python
THEMATIC_SCREENING = {
    "AI人工智能": {
        "核心标的": ["科大讯飞", "海康威视", "中科曙光", "寒武纪", "商汤-W"],
        "概念股池": {
            "基础层": ["芯片", "算力", "服务器"],
            "技术层": ["大模型", "算法", "API"],
            "应用层": ["办公", "医疗", "金融", "教育"]
        },
        "筛选标准": {
            "市值": ">100亿",
            "研发投入": ">10%",
            "AI收入占比": ">30%"
        },
        "风险提示": "技术迭代快，竞争格局未定，估值波动大"
    },
    
    "新能源汽车": {
        "核心标的": ["比亚迪", "宁德时代", "理想汽车-W", "小鹏汽车-W"],
        "筛选维度": {
            "整车": ["销量增速", "毛利率", "智能化水平"],
            "电池": ["能量密度", "成本", "产能"],
            "配件": ["单车价值量", "客户集中度"]
        },
        "政策催化": "以旧换新补贴、购置税减免、新能源渗透率目标"
    },
    
    "创新药": {
        "核心标的": ["恒瑞医药", "百济神州", "信达生物", "药明康德"],
        "筛选标准": {
            "管线丰富度": ">10个临床管线",
            "first-in-class": "至少1个",
            "BD能力": "有海外授权记录"
        },
        "风险因素": "医保谈判降价、临床失败风险、同靶点竞争"
    },
    
    "红利低波": {
        "筛选标准": {
            "股息率": ">3%",
            "连续分红年数": ">=3年",
            "近1年波动率": "低于全市场中位数",
            "自由现金流": "为正且覆盖分红"
        },
        "适用环境": "利率下行、市场震荡、追求现金流回报",
        "风险提示": "股息率因股价下跌被动抬高需剔除；分红不可持续的高股息为陷阱"
    },
    
    "高端制造": {
        "筛选维度": {
            "机床/母机": ["订单增速", "国产化率", "毛利率"],
            "自动化": ["下游资本开支", "在手订单"],
            "精密零部件": ["单车/单机价值量", "客户集中度"]
        },
        "政策催化": "设备更新改造、国产替代、制造业投资周期",
        "风险因素": "下游资本开支不及预期、价格竞争、应收账款回收"
    }
}
```

**主题筛选执行清单（从主题到候选池）**

| 步骤 | 动作 | 产出 | 卡点 | 责任岗 |
|------|------|------|------|---|
| 1 | 拆解产业链上下游环节 | 环节清单 | 环节定义须无重叠 | 研究 |
| 2 | 为每个环节设定量化筛选标准 | 标准表 | 标准须可用财报数据验证 | 研究 |
| 3 | 拉取候选池并剔除不达标标的 | 候选清单 | 剔除理由须留档 | 研究+数据 |
| 4 | 补充流动性与拥挤度过滤 | 可交易候选池 | 单笔建仓 ≤日均成交额5% | 风控 |
| 5 | 计算综合评分排序 | 排序表 | 标注数据报告期 | 研究 |
| 6 | 输出并附风险提示 | 主题选股报告 | 保留免责声明 | 合规 |

**示例｜同一主题的两种筛选口径对比**

| 口径 | 条件 | 候选数量 | 入选标的特征 | 适用场景 | 风险提示重点 |
|------|------|---------|------------|---------|---|
| 严格口径 | 研发占比>10% + 主题收入占比>30% + 市值>100亿 | 8只 | 纯度高、弹性中等 | 中长期配置 | 纯度高但数量少，注意流动性 |
| 宽松口径 | 主题收入占比>10% 或 有明确订单 | 26只 | 纯度低、弹性大 | 主题轮动早期 | 须注明纯度较低 |
| 事件口径 | 近3个月有订单/中标/产能公告 | 12只 | 催化明确、波动大 | 事件驱动交易 | 催化退坡后回撤大 |

使用要点：三种口径不可混用；若报告使用宽松口径，必须在结论中注明"纯度较低、可能与主题关联度不足"。

**示例 2｜主题生命周期与筛选口径的选择**

| 阶段 | 特征 | 推荐口径 | 仓位建议 | 退出信号 |
|------|------|---------|---------|---------|
| 萌芽期 | 政策出台、标的少 | 事件口径 | 轻仓试错 | 政策落地不及预期 |
| 成长期 | 订单落地、业绩兑现 | 严格口径 | 逐步加仓 | 增速连续两季下滑 |
| 扩散期 | 概念股大量增加 | 宽松口径转严格 | 降低纯度低标的 | 龙头见顶 |
| 退潮期 | 业绩证伪、估值回落 | 停止新增 | 逐步退出 | 跌破止损位 |

要点：同一主题在不同阶段应切换口径，而不是全程用一种口径；从成长期进入扩散期时，应把“宽松口径”切回“严格口径”，避免买入仅有关联度而无实际业务的标的。



### 3. Technical Signal Detection / 技术信号检测

```python
class TechnicalSignals:
    """技术信号检测"""
    
    @staticmethod
    def detect_moving_average_signals(prices: pd.Series, 
                                      short_ma: int = 20,
                                      long_ma: int = 60) -> dict:
        """均线信号检测"""
        ma_short = prices.rolling(short_ma).mean
        ma_long = prices.rolling(long_ma).mean
        
        # 金叉/死叉判断
        current_ma_diff = ma_short.iloc[-1] - ma_long.iloc[-1]
        prev_ma_diff = ma_short.iloc[-2] - ma_long.iloc[-2]
        
        if current_ma_diff > 0 and prev_ma_diff <= 0:
            signal = "GOLDEN_CROSS"  # 金叉
        elif current_ma_diff < 0 and prev_ma_diff >= 0:
            signal = "DEAD_CROSS"  # 死叉
        else:
            signal = "NEUTRAL"
        
        return {
            "signal": signal,
            "short_ma": round(ma_short.iloc[-1], 2),
            "long_ma": round(ma_long.iloc[-1], 2),
            "ma_diff_pct": round((current_ma_diff / ma_long.iloc[-1]) * 100, 2)
        }
    
    @staticmethod
    def detect_support_resistance(prices: pd.Series, 
                                 lookback: int = 60) -> dict:
        """支撑压力位检测"""
        recent = prices.tail(lookback)
        
        # 计算枢轴点
        pivot = (recent.max + recent.min + recent.iloc[-1]) / 3
        
        r1 = 2 * pivot - recent.min
        s1 = 2 * pivot - recent.max
        r2 = pivot + (recent.max - recent.min)
        s2 = pivot - (recent.max - recent.min)
        
        return {
            "resistance_1": round(r1, 2),
            "resistance_2": round(r2, 2),
            "pivot": round(pivot, 2),
            "support_1": round(s1, 2),
            "support_2": round(s2, 2),
            "current_price": round(prices.iloc[-1], 2)
        }
    
    @staticmethod
    def detect_volume_anomaly(prices: pd.Series, 
                             volumes: pd.Series,
                             threshold: float = 2.0) -> dict:
        """量价异常检测"""
        avg_volume = volumes.tail(20).mean
        current_volume = volumes.iloc[-1]
        volume_ratio = current_volume / avg_volume
        
        # 价格与成交量背离
        price_change = (prices.iloc[-1] - prices.iloc[-2]) / prices.iloc[-2]
        
        return {
            "volume_ratio": round(volume_ratio, 2),
            "is_volume_surge": volume_ratio > threshold,
            "price_change": round(price_change * 100, 2),
            "divergence": "量价背离" if (price_change > 0 and volume_ratio < 0.5) or
                                      (price_change < 0 and volume_ratio > 2) else "正常"
        }
```

**信号组合矩阵（单一信号不决策，组合才决策）**

| 均线信号 | 量能状态 | 价格位置 | 综合判断 | 建议动作 | 仓位参考 |
|---------|---------|---------|---------|---------|---|
| 金叉 | 放量（>2倍） | 突破压力位 | 强势确认 | 可分批建仓 | 可至八成 |
| 金叉 | 缩量（<0.8倍） | 未突破压力位 | 信号弱，可能反复 | 观察，暂不动 | 不超过四成 |
| 金叉 | 放量 | 已连续大涨后 | 追高风险 | 不追，等回调 | 不加仓 |
| 死叉 | 放量 | 跌破支撑位 | 趋势转弱 | 按纪律减仓 | 降至两成 |
| 死叉 | 缩量 | 支撑位附近 | 可能假跌破 | 观察一日再定 | 维持观察 |
| 中性 | 量价背离 | 高位滞涨 | 分歧加大 | 降低仓位 | 降至四成 |

**示例｜信号有效性统计（先验证再使用）**

| 信号 | 样本数 | 5日胜率 | 20日胜率 | 平均20日收益 | 结论 | 适用市场状态 |
|------|-------|--------|---------|------------|------|---|
| 金叉+放量 | 320 | 58% | 61% | +3.2% | 保留，作为主要信号 | 上涨/震荡 |
| 金叉（缩量） | 410 | 49% | 47% | +0.4% | 弱化，需叠加其他条件 | 仅上涨 |
| 死叉+跌破支撑 | 260 | — | — | -2.8% | 保留，作为减仓信号 | 全状态 |
| 量价背离 | 180 | 44% | 41% | -1.1% | 作为预警信号使用 | 高位预警 |

使用要点：胜率需按市场状态分层统计（上涨/震荡/下跌），单一整体胜率可能掩盖失效区间；若某信号在震荡市胜率低于45%，应暂停使用。

**示例｜信号与仓位对应（把信号变成纪律）**

| 综合评分 | 信号状态 | 建议仓位上限 | 单标的上限 | 止损参考 | 检查频率 |
|---------|---------|------------|-----------|---------|---|
| ≥80 | 金叉+放量 | 80% | 15% | −8% | 每日 |
| 70-79 | 金叉（等确认） | 60% | 12% | −8% | 每日 |
| 60-69 | 中性 | 40% | 10% | −10% | 每周 |
| <60 | 死叉或背离 | 20% | 8% | 立即评估 | 每日 |

**示例 2｜信号失效的排查流程（按状态分层）**

| 步骤 | 动作 | 判定标准 | 处置 |
|------|------|---------|------|
| 1 | 按市场状态分层统计胜率 | 上涨/震荡/下跌三组分别统计 | 找出失效区间 |
| 2 | 检查样本量是否充足 | 每组样本 ≥100 | 不足则延长回看窗口 |
| 3 | 检查是否含未来函数 | 信号是否用到了当时不可得的数据 | 有则剔除重算 |
| 4 | 检查交易成本假设 | 是否计入滑点与印花税 | 未计入则补算 |
| 5 | 复核结论 | 净收益是否仍为正 | 为正则保留，否则停用 |

排查原则：信号整体胜率达标但在某状态下失效时，应“按状态停用”而非整体停用；同时必须检查未来函数，这是实盘失效最常见的原因。



### 4. Financial Fraud Detection / 财报异常检测

```python
class FraudDetection:
    """财报异常信号检测"""
    
    @staticmethod
    def check_revenue_quality(stock_code: str, 
                             financial_data: dict) -> dict:
        """营收质量检测"""
        indicators = {
            # 应收账款异常
            "ar_growth_vs_revenue": financial_data.get("ar_growth", 0) - 
                                    financial_data.get("revenue_growth", 0),
            
            # 存货异常
            "inventory_growth_vs_cost": financial_data.get("inv_growth", 0) - 
                                        financial_data.get("cost_growth", 0),
            
            # 现金流匹配
            "cash_flow_ratio": financial_data.get("cfo", 0) / 
                              max(financial_data.get("net_profit", 1), 1),
            
            # 毛利率异常
            "gross_margin_volatility": financial_data.get("gm_std", 0),
            
            # 关联交易占比
            "related_party_ratio": financial_data.get("rpt_revenue", 0) / 
                                  max(financial_data.get("total_revenue", 1), 1)
        }
        
        # 预警信号
        warnings = []
        if indicators["ar_growth_vs_revenue"] > 30:
            warnings.append("应收账款增速显著高于营收增速，可能存在虚构收入")
        if indicators["cash_flow_ratio"] < 0.5:
            warnings.append("经营现金流显著低于净利润，盈利质量存疑")
        if indicators["related_party_ratio"] > 0.5:
            warnings.append("关联交易占比过高，存在利益输送风险")
        
        return {
            "indicators": indicators,
            "warnings": warnings,
            "overall_risk": "高" if len(warnings) >= 2 else 
                           "中" if warnings else "低"
        }
    
    @staticmethod
    def check_auditor_warnings(audit_reports: list) -> dict:
        """审计意见检测"""
        risk_keywords = ["保留意见", "无法表示意见", "非标准无保留", 
                        "持续经营重大不确定性", "强调事项段"]
        
        findings = []
        for report in audit_reports:
            for keyword in risk_keywords:
                if keyword in report:
                    findings.append({
                        "keyword": keyword,
                        "context": report
                    })
        
        return {
            "has_warnings": len(findings) > 0,
            "findings": findings,
            "risk_level": "高" if findings else "低"
        }
```

**财报异常指标阈值表（触发即预警）**

| 指标 | 计算口径 | 关注阈值 | 预警阈值 | 说明 | 数据来源 |
|------|---------|---------|---------|------|---|
| 应收增速−营收增速 | 两个同比增速之差 | >15pct | >30pct | 可能虚构收入或放宽信用 | 资产负债表/附注 |
| 存货增速−成本增速 | 同比增速之差 | >15pct | >30pct | 可能存货积压或虚增 | 资产负债表/附注 |
| 经营现金流/净利润 | CFO ÷ 归母净利润 | <0.8 | <0.5 | 盈利质量存疑 | 现金流量表 |
| 毛利率波动率 | 近8期标准差 | >2.5pct | >4pct | 可能人为调节 | 利润表 |
| 关联交易收入占比 | 关联收入 ÷ 营收 | >30% | >50% | 利益输送风险 | 关联交易章节 |
| 商誉/净资产 | 商誉 ÷ 净资产 | >20% | >40% | 减值风险 | 资产负债表 |
| 审计意见类型 | 意见段 | 带强调事项段 | 保留/无法表示意见 | 直接排除 | 审计报告意见段 |

**示例｜综合风险判定（三项指标联动）**

| 标的 | 应收−营收 | CFO/净利润 | 关联占比 | 命中预警数 | 风险判定 | 处置 | 复核要求 |
|------|----------|-----------|---------|-----------|---------|------|---|
| 标的A | +8pct | 1.12 | 12% | 0 | 低 | 正常纳入评分 | 常规复核 |
| 标的B | +34pct | 0.62 | 21% | 2 | 高 | 直接排除，不参与评分 | 出具排除说明并留档 |
| 标的C | +18pct | 0.75 | 33% | 2 | 高 | 核查后决定是否排除 | 完成核查前不得纳入 |
| 标的D | +5pct | 0.95 | 8% | 0 | 低 | 正常纳入评分 | 常规复核 |

使用要点：命中2项及以上预警阈值即判定为高风险，无论综合评分多高均不纳入候选池；单一指标命中需在报告中说明核查进展，不得直接作为结论。

**示例 2｜造假信号的误报排查（避免错杀）**

| 预警信号 | 可能的正常解释 | 核查动作 | 结论处理 |
|---------|--------------|---------|---------|
| 应收增速高于营收 | 大客户账期延长、并表新增 | 查客户结构与账期政策 | 有合理解释则降为关注 |
| 存货增速高于成本 | 备货旺季、原材料涨价 | 查存货结构与周转天数 | 周转未恶化则降为关注 |
| CFO低于净利润 | 大额资本开支、票据结算 | 查现金流量表附注 | 经营性应收增加过快才预警 |
| 关联交易占比高 | 集团内统购统销模式 | 查定价依据与公允性说明 | 定价公允则降为关注 |
| 毛利率波动大 | 产品结构变化、会计政策变更 | 查分品类毛利率 | 结构性变化则不预警 |

排查原则：单一指标命中只触发“核查”，不直接判定造假；须至少两项指标同时异常且无合理解释，方可判定高风险并排除。



### 5. Portfolio Construction / 组合构建

```python
class PortfolioBuilder:
    """智能组合构建"""
    
    def __init__(self, target_stocks: List[dict], 
                 total_capital: float = 1000000):
        self.stocks = target_stocks
        self.capital = total_capital
    
    def build_equal_weight(self, max_positions: int = 10) -> dict:
        """等权重配置"""
        selected = self.stocks[:max_positions]
        per_stock = self.capital / len(selected)
        
        positions = []
        for stock in selected:
            shares = int(per_stock / stock["price"] / 100) * 100  # 100股整数
            positions.append({
                "code": stock["code"],
                "name": stock["name"],
                "shares": shares,
                "amount": shares * stock["price"],
                "weight": 1 / len(selected)
            })
        
        return {
            "strategy": "等权重",
            "positions": positions,
            "total_invested": sum(p["amount"] for p in positions),
            "cash_remaining": self.capital - sum(p["amount"] for p in positions),
            "expected_return": sum(s.get("expected_return", 0) for s in selected) / len(selected),
            "estimated_risk": self._calculate_portfolio_risk(positions)
        }
    
    def build_risk_parity(self, max_positions: int = 10) -> dict:
        """风险平价配置"""
        selected = self.stocks[:max_positions]
        
        # 使用波动率倒数作为权重
        inv_vol = [1 / s.get("volatility", 0.3) for s in selected]
        total_inv_vol = sum(inv_vol)
        weights = [v / total_inv_vol for v in inv_vol]
        
        positions = []
        for stock, weight in zip(selected, weights):
            amount = self.capital * weight
            shares = int(amount / stock["price"] / 100) * 100
            positions.append({
                "code": stock["code"],
                "name": stock["name"],
                "shares": shares,
                "amount": shares * stock["price"],
                "weight": round(weight * 100, 2)
            })
        
        return {
            "strategy": "风险平价",
            "positions": positions,
            "total_invested": sum(p["amount"] for p in positions)
        }
    
    def _calculate_portfolio_risk(self, positions: list) -> float:
        """简化组合风险估算"""
        # 假设相关性0.3
        individual_risks = [0.25] * len(positions)  # 默认25%波动率
        correlation = 0.3
        
        portfolio_var = 0
        for i, risk_i in enumerate(individual_risks):
            for j, risk_j in enumerate(individual_risks):
                weight_i = 1 / len(positions)
                weight_j = 1 / len(positions)
                corr = correlation if i != j else 1
                portfolio_var += weight_i * weight_j * risk_i * risk_j * corr
        
        return round(np.sqrt(portfolio_var) * 100, 2)
```

**示例 1｜等权重 vs 风险平价（同一候选池两种结果）**

| 标的 | 预期收益 | 波动率 | 等权重 | 风险平价权重 | 差异说明 | 相关性分组 |
|------|---------|-------|-------|------------|---------|---|
| 标的A | 18% | 20% | 10.0% | 12.5% | 低波动，风险平价提升权重 | 防御组 |
| 标的B | 25% | 35% | 10.0% | 7.1% | 高波动，风险平价下调权重 | 周期组 |
| 标的C | 15% | 18% | 10.0% | 13.9% | 最低波动，权重最高 | 防御组 |
| 标的D | 30% | 45% | 10.0% | 5.6% | 最高波动，权重最低 | 周期组 |

结论：等权重简单透明、易执行；风险平价会在不牺牲过多收益的前提下降低组合波动，适合波动容忍度较低的账户。两种方式都应同时给出，便于对照选择。

**示例 2｜组合风控阈值表（建仓前先设红线）**

| 风控项 | 阈值 | 超限动作 | 检查频率 | 责任人 |
|-------|------|---------|---------|---|
| 单标的权重 | ≤15% | 触发即减仓至阈值内 | 每周 | 投研负责人 |
| 单一行业权重 | ≤35% | 新增买入暂停，优先调出 | 每周 | 投研负责人 |
| 前三大标的合计 | ≤40% | 降低集中度 | 每两周 | 风控 |
| 组合预估波动率 | ≤25% | 降仓或增加低波动资产 | 每月 | 风控 |
| 单标的浮亏 | −8%至−10% | 按纪律评估减仓 | 每日 | 交易执行 |
| 组合最大回撤 | −15% | 启动整体降仓预案 | 每日 | 风控 |

**示例 3｜建仓分批节奏（避免一次性买在高点）**

| 批次 | 触发条件 | 投入比例 | 备注 | 失败处理 |
|------|---------|---------|------|---|
| 第1批 | 信号确认（金叉+放量） | 40% | 建立底仓 | 信号证伪则停止后续批次 |
| 第2批 | 回踩支撑不破 | 30% | 摊薄成本 | 破位则转为减仓 |
| 第3批 | 突破前高确认 | 30% | 趋势延续加仓 | 未突破则观望 |
| 例外 | 跌破止损位 | 0%（不补） | 按纪律减仓 | 立即执行减仓 |
**示例 4｜组合再平衡的触发条件（避免频繁调仓）**

| 触发类型 | 条件 | 动作 | 是否立即执行 |
|---------|------|------|------------|
| 阈值触发 | 单标的权重偏离目标 ±5pct | 调回目标权重 | 是 |
| 时间触发 | 每季度末 | 全面复核并再平衡 | 是 |
| 风险触发 | 组合波动率超25% | 降低高波动标的权重 | 是 |
| 事件触发 | 标的命中财报预警 | 剔除并补入候选池下一名 | 是 |
| 噪声波动 | 偏离 <±3pct | 不动作 | 否 |

再平衡原则：设置“噪声带”（±3pct以内不动）以控制换手成本；再平衡前须先检查是否触发风控阈值，风控优先于再平衡。




---

## Usage Examples / 使用示例

**启动选股：**
```
用以下条件筛选股票：
- 市盈率 < 30
- 营收增速 > 20%
- ROE > 15%
- 综合评分 > 70
```

**主题选股：**
```
筛选AI人工智能概念中估值最低的10只股票
```

**技术面选股：**
```
找出所有出现均线金叉且放量突破的股票
```

**因子有效性检验：**
```
对[因子名称]做有效性检验：输出IC值、分组单调性、
样本外方向一致性、换手成本与因子间相关性，并给出是否保留的结论。
```

**组合构建与风控：**
```
用以下候选池构建组合，同时输出等权重与风险平价两种方案，
并检查单标的上限（15%）、行业上限（35%）、组合波动率（≤25%）是否超限。
```

---

## Disclaimer

This skill provides stock screening tools and analysis for educational purposes. Stock selection results are based on quantitative models and historical data, which do not guarantee future performance. All investment decisions should be made based on independent research and professional advice. Past performance does not indicate future results.

## 本轮增量（2026-11-13）：复核维度与举例补充

> 本节为 2026-11-13 例行轮转的净增量记录：新增举例与复核维度均为本期首次出现，与既有条目不重复；仅作方法论参考，需具备相应资质的人员复核后使用。

### 补充举例（按模块，本期新增）

**1. Quantitative Factor Screening**：

- 因子入选前先做「行业中性化 / 市值中性化」检查，并记录缺失值处理方式，避免把行业暴露误读为选股能力。
- 对同一因子在多区间做稳定性检查（如分季度看 IC 方向是否一致），方向频繁翻转的因子先降权并标注待复核，不直接并入打分。

**4. Financial Fraud Detection**：

- 把「应收账款增速与收入增速背离」「经营现金流与净利润长期背离」「毛利率显著偏离同业且无业务解释」列为并列观察项，输出疑点清单与需核对的报表科目，不下结论。
- 疑点复核须标注所用财报期间与口径，跨期比较前先对齐会计政策变更，避免把口径变化误判为异常。

### 新增复核维度表（2026-11-13）

> 本表新增「由谁执行 / 数据来源 / 复核要点 / 风险等级 / 适用边界」等维度列，把口径责任、数据来源与人工复核要求落到具体条目。

| 复核维度 | 由谁执行 | 数据来源 | 复核要点 | 风险等级 | 适用边界 |
| --- | --- | --- | --- | --- | --- |
| 因子中性化检查 | 研究员 | 行情与财务数据 + 因子暴露报告 | 行业/市值暴露、缺失值处理、区间方向 | 中 | 仅研究框架，不构成标的推荐 |
| 疑点口径对齐 | 研究员 + 复核人 | 财报原文 + 会计政策变更说明 | 财报期间、口径变化、科目对应关系 | 高 | 需人工复核，模型疑点不作定论 |

### 适用边界 / 数据最小化 / 执行边界（本期补齐）

**适用边界**：本技能仅用于量化选股与财务疑点识别的方法论参考与结构拆解，输出为供具备相应资质人员复核的草稿；不构成对具体主体、标的、客户或案件的最终结论、指令或承诺。超出该范围的场景（如实盘执行、自动审批、对外正式报送、系统登记）不适用本技能，应转由相应业务系统与授权人员处理。

### 时效性说明

- 本期时效性核查：**截至 2026-11-13**。正文中的监管、政策、市场与行业动态为公开资料整理，具体文号、生效日期、数据区间与统计口径请以监管机构及官方渠道最新发布为准；未获官方原文核实的条目标注「需人工复核」，不填入未经核实的文号、日期或数字。
- 历史条目保留原发布日期以便追溯；本次更新未引入新的具体文号或统计数值。
