---
name: trading-agents
description: 基于 AgentScope 的多智能体股票诊断系统。一键执行完整诊断流程，自动生成技术面、基本面、舆情面分析、研究员辩论、交易员决策、风控讨论及最终投资决策报告。
---

# Trading Agents 股票投资分析系统

基于 AgentScope 框架的多智能体协作股票诊断系统，**一键执行完整诊断流程**。

## 核心特性

✅ **一键全自動执行** - 单次调用完成所有角色分析和报告生成  
✅ **多智能体协作** - 分析师、研究员、交易员、风控、基金经理五层决策  
✅ **完整报告输出** - 自动生成 7 份专业 MD 报告和 1 份合并 PDF  
✅ **后台运行支持** - 避免长任务超时，自动保存中间结果  
✅ **数据驱动** - 集成 Tushare/AKShare 实时金融数据  

## 系统架构

### 智能体团队架构

1. **分析师团队** (ReActAgent) - 数据采集
   - MarketAnalyst: 技术面分析
   - FundamentalsAnalyst: 基本面分析
   - NewsAnalyst: 舆情面分析

2. **研究员团队** (AgentBase) - 多空辩论
   - BullishResearcher: 看多研究员
   - BearishResearcher: 看空研究员
   - ResearchFacilitator: 研究主持人

3. **交易与风控团队** - 决策与风控
   - Trader: 交易员
   - AggressiveRisk: 激进型风控
   - NeutralRisk: 中性型风控
   - ConservativeRisk: 保守型风控
   - RiskFacilitator: 风控协调人

4. **基金经理** - 最终决策
   - Manager: 做出最终投资决策

**所有角色通过一次调用自动完成：**
```python
advisor = StockAdvisorSystem()
result = advisor.diagnose("600519.SH")  # 一键执行所有角色
advisor.save_report(result)  # 生成所有报告
```

### 一键自动执行所有角色（推荐）

**这是最简单也是最推荐的使用方式，一次调用完成所有分析并生成所有报告：**

```python
from trading_agents import StockAdvisorSystem

# 创建系统实例
advisor = StockAdvisorSystem()

# 一键执行完整诊断（自动完成所有角色）
result = advisor.diagnose("600519.SH", base_report_dir="report")

# 保存所有报告（JSON + PDF）
advisor.save_report(result)

print(f"✅ 所有报告已生成：{result['report_dir']}")
print(f"📊 最终决策：{result['final_decision']}")
```

**以上代码会自动完成以下所有步骤：**

```
阶段 1: 数据采集（分析师团队）
  ├─ MarketAnalyst → 技术面分析报告.md
  ├─ FundamentalsAnalyst → 基本面分析报告.md
  └─ NewsAnalyst → 舆情面分析报告.md
      ↓
阶段 2: 研究员辩论
  ├─ BullishResearcher vs BearishResearcher
  └─ → 研究员辩论报告.md
      ↓
阶段 3: 交易员决策
  ├─ Trader 综合分析所有报告
  └─ → 交易员决策报告.md
      ↓
阶段 4: 风险管理讨论
  ├─ AggressiveRisk vs NeutralRisk vs ConservativeRisk
  └─ → 风险管理讨论报告.md
      ↓
阶段 5: 基金经理最终决策
  ├─ Manager 做出最终决策
  └─ → 最终决策报告.md
      ↓
阶段 6: 报告生成
  ├─ complete_diagnosis_report.json
  └─ {股票名}_{代码}_{时间}_{决策}.pdf
```

### 分步执行（可选）

```python
from trading_agents import StockAdvisorSystem

advisor = StockAdvisorSystem()

# 阶段 1: 分析师数据采集
result = advisor.diagnose("600519.SH")  # 已完成所有分析师报告

# 阶段 2-5: 后续流程自动完成
# 研究员辩论 → 交易员决策 → 风控讨论 → 经理决策

# 阶段 6: 保存所有报告
advisor.save_report(result)
```



## 快速开始

### 一键完整诊断（推荐）

#### 方式 1：使用 OpenClaw 技能调用

```python
from trading_agents import StockAdvisorSystem

# 创建系统实例
advisor = StockAdvisorSystem()

# 一键执行完整诊断（自动完成所有角色分析并生成所有报告）
result = advisor.diagnose("600519.SH", base_report_dir="report")

# 保存完整报告（包含 JSON 和合并 PDF）
advisor.save_report(result)

print(f"✅ 所有报告已生成：{result['report_dir']}")
print(f"📊 最终决策：{result['final_decision']}")
```

#### 方式 2：命令行执行

```bash
# 直接运行诊断脚本
python3 scripts/stock_advisor.py --stock 600519.SH

# 或使用 nohup 后台运行（适合长时间任务）
nohup python3 scripts/stock_advisor.py --stock 600519.SH > diagnose.log 2>&1 &
```

#### 方式 3：后台运行模式（防超时）

```bash
# 使用后台诊断脚本
python3 scripts/background_diagnose.py 600519.SH 贵州茅台
```

### ⚠️ 重要提示

完整诊断流程需要 **10-15 分钟**，包含以下自动执行步骤：

1. ✅ **数据采集** - 3 位分析师独立获取数据并生成报告
2. ✅ **研究员辩论** - 看多看空双方辩论形成共识
3. ✅ **交易员决策** - 综合分析报告制定交易策略
4. ✅ **风控讨论** - 三种风险偏好评估风险
5. ✅ **经理决策** - 做出最终投资决策
6. ✅ **报告生成** - 自动生成所有 MD 报告和合并 PDF

**推荐使用后台运行模式**以避免会话超时：
- 详见 [BACKGROUND_RULES.md](BACKGROUND_RULES.md)
- 自动保存中间结果，防止中断丢失数据

### 使用方法

**作为 OpenClaw 技能使用:**

将本目录复制到 OpenClaw 项目的 skills 目录：
```bash
cp -r trading-agents /path/to/openclaw/skills/
```

**OpenClaw 中调用示例（一键完成所有角色）:**
```python
# OpenClaw 会自动加载技能
from trading_agents import StockAdvisorSystem

# 创建系统实例
advisor = StockAdvisorSystem()

# 一键执行完整诊断（自动完成所有角色分析并生成所有报告）
result = advisor.diagnose("600519.SH", base_report_dir="report")

# 保存所有报告（JSON + PDF）
advisor.save_report(result)

# 输出包含：
# - MarketAnalyst_技术面分析.md
# - FundamentalsAnalyst_基本面分析.md
# - NewsAnalyst_舆情面分析.md
# - 研究员辩论报告.md
# - 交易员决策报告.md
# - 风险管理讨论报告.md
# - 最终决策报告.md
# - complete_diagnosis_report.json
# - {股票名}_{代码}_{时间}_{决策}.pdf
```

**作为 Python 包安装:**

```bash
# 安装整个技能包
pip install /path/to/trading-agents/

# 或进入 scripts 目录安装核心代码
pip install /path/to/trading-agents/scripts/
```

**独立使用:**
```python
from trading_agents import StockAdvisorSystem

# 创建系统实例
advisor = StockAdvisorSystem()

# 一键诊断股票（自动执行所有角色并生成所有报告）
result = advisor.diagnose("600519.SH", base_report_dir="report")

# 保存完整报告
advisor.save_report(result)

print(f"报告目录：{result['report_dir']}")
print(f"最终决策：{result['final_decision']}")
```

### 使用特定模型

```python
from trading_agents.config import config

# 切换模型
config.model_name = "qwen-max-2025-01-25"  # 或其他支持的模型

# 支持的模型:
# - kimi-k2.5
# - qwen-max-2025-01-25
# - qwen3.5-plus
# - glm-5
# - MiniMax/MiniMax-M2.5
```

## 配置说明

### 环境变量

```bash
# Tushare API Token
TUSHARE_TOKEN=your_token_here

# 阿里云百炼 API Key
ALIYUN_BAILIAN_API_KEY=your_key_here
```

### 配置参数

```python
from trading_agents.config import config

# 辩论轮数
config.debate_rounds = 2

# 风控讨论轮数
config.risk_discussion_rounds = 2

# 权重配置
config.tech_weight = 0.25    # 技术面权重
config.fund_weight = 0.35    # 基本面权重
config.news_weight = 0.20    # 舆情面权重
config.research_weight = 0.20 # 研究员共识权重
```

## 输出报告（自动生成）

系统自动生成以下报告文件:

### 分析师报告（阶段 1）
- `MarketAnalyst_技术面分析.md` - 技术面分析报告
- `FundamentalsAnalyst_基本面分析.md` - 基本面分析报告
- `NewsAnalyst_舆情面分析.md` - 舆情面分析报告

### 研究员辩论（阶段 2）
- `研究员辩论报告.md` - 看多看空辩论记录

### 交易员决策（阶段 3）
- `交易员决策报告.md` - 交易策略报告

### 风控讨论（阶段 4）
- `风险管理讨论报告.md` - 风险评估报告

### 经理决策（阶段 5）
- `最终决策报告.md` - 最终投资决策

### 完整报告（阶段 6）
- `complete_diagnosis_report.json` - 完整 JSON 数据
- `{股票名}_{代码}_{时间}_{决策}.pdf` - 合并 PDF 报告

**所有报告通过一键调用自动生成：**
```python
advisor = StockAdvisorSystem()
result = advisor.diagnose("600519.SH")
advisor.save_report(result)  # 自动生成所有 MD 和 PDF
```

## 核心组件（可选）

> 注意：推荐使用一键调用方式，以上代码已自动完成所有角色。以下为高级用法，可按需单独调用。

### 分析师智能体

```python
from trading_agents.agents import (
    MarketAnalystAgent,
    FundamentalsAnalystAgent,
    NewsAnalystAgent
)

# 技术面分析
market_analyst = MarketAnalystAgent()
report = market_analyst.analyze("600519.SH")

# 基本面分析
fund_analyst = FundamentalsAnalystAgent()
report = fund_analyst.analyze("600519.SH")

# 舆情分析
news_analyst = NewsAnalystAgent()
report = news_analyst.analyze("600519.SH", "贵州茅台")
```

### 数据工具

```python
from trading_agents.tools import TushareTools, AKShareTools

# Tushare 数据
tushare = TushareTools(token)
data = tushare.get_stock_daily("600519.SH", days=60)
indicators = tushare.get_technical_indicators("600519.SH")

# AKShare 数据
akshare = AKShareTools()
news = akshare.get_stock_news("600519.SH", days=7)
sentiment = akshare.get_market_sentiment()
```

### AgentScope 工具包

```python
from trading_agents.tools import (
    create_market_analyst_toolkit,
    create_fundamentals_analyst_toolkit,
    create_news_analyst_toolkit,
    create_stock_toolkit
)

# 创建工具包
toolkit = create_stock_toolkit()
```

## 批量诊断

```python
from trading_agents.batch_diagnose import batch_diagnose

stocks = ["600519.SH", "000858.SZ", "002594.SZ"]
results = batch_diagnose(stocks, output_dir="report/batch")
```

## 依赖安装

```bash
# 基础依赖
pip install agentscope>=0.0.5
pip install tushare>=1.2.89
pip install akshare>=1.12.0
pip install pandas>=2.0.0
pip install numpy>=1.24.0
pip install requests>=2.31.0
pip install openai>=1.0.0
pip install fpdf2>=2.8.0
pip install python-dotenv

# 阿里云夸克搜索 SDK（可选）
pip install alibabacloud_iqs20241111>=1.0.0
pip install alibabacloud_tea_openapi>=0.3.0

# Web 界面（可选）
pip install streamlit>=1.28.0
```

## 项目结构

### Skill 目录结构 (OpenClaw 兼容)

```
trading-agents/              # 技能根目录
├── SKILL.md                 # Skill 说明文档 (必需)
├── __init__.py              # Python 包标识 (OpenClaw 需要)
├── setup.py                 # 安装配置
└── scripts/                 # 完整源代码
    ├── __init__.py
    ├── stock_advisor.py  # 主系统入口
    ├── config.py            # 系统配置
    ├── batch_diagnose.py    # 批量诊断
    ├── streamlit_app.py     # Web 界面
    ├── requirements.txt     # 依赖清单
    ├── agents/
    │   ├── __init__.py
    │   ├── analysts.py      # 分析师团队 (ReActAgent)
    │   ├── researchers.py   # 研究员团队 (AgentBase)
    │   ├── trader.py        # 交易员
    │   ├── risk_managers.py # 风险管理团队
    │   └── manager.py       # 基金经理
    └── tools/
        ├── __init__.py
        ├── tushare_tools.py # Tushare 数据接口
        ├── akshare_tools.py # AKShare 数据接口
        └── toolkit.py       # AgentScope 工具注册
```

### 移植到其他项目

只需复制整个 `trading-agents` 目录：

```bash
# 从源项目复制到目标项目
cp -r /source/project/.qoder/skills/trading-agents \
      /target/project/.qoder/skills/

# 或在目标项目中克隆后复制
mkdir -p /target/project/.qoder/skills/
cp -r trading-agents /target/project/.qoder/skills/
```

## 注意事项

1. **API Token**: 需要配置 TUSHARE_TOKEN 和 ALIYUN_BAILIAN_API_KEY
2. **中文字体**: PDF 生成需要系统中文字体支持
3. **网络连接**: 需要访问阿里云百炼 API
4. **数据限制**: Tushare 免费版有数据调用限制
5. **执行时间**: 完整诊断流程需要 10-15 分钟，建议使用后台运行模式

## 总结

### 为什么选择 Trading Agents？

✅ **一键完成所有角色** - 无需手动调用多个函数，一次诊断完成所有分析  
✅ **自动化报告生成** - 自动生成 7 份 MD 报告和 1 份合并 PDF，无需手动整理  
✅ **专业智能体团队** - 5 层决策流程，模拟专业投资机构的工作流  
✅ **实时数据驱动** - 集成 Tushare/AKShare 获取最新市场数据  
✅ **灵活可配置** - 支持多种模型、权重、辩论轮数等参数配置  

### 快速上手

```python
from trading_agents import StockAdvisorSystem

# 一行代码完成股票诊断
result = StockAdvisorSystem().diagnose("600519.SH")

# 一行代码保存所有报告
StockAdvisorSystem().save_report(result)
```

就这么简单！所有复杂的分析、辩论、决策过程都由智能体团队自动完成。
