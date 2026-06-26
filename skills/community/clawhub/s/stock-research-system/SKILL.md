---
name: stock-research-system
description: 专业级股权研究自动化系统。支持首发覆盖报告（6,000-10,000字）和季报更新报告（3,000-5,000字）。触发词：股票研究、深度研究、首发覆盖、季报更新、DCF估值。
tags: [投研, 财报分析, DCF估值, ROIC]
---

# 股票深度研究系统

> 专业级股权研究自动化系统，集成DataHub统一数据获取层

---

## 核心改进（2026-05-19）

**✅ 集成DataHub统一数据获取层**
- 替代多数据源直接调用，统一入口管理
- 智能缓存（quote: 5分钟, financial: 1小时）
- 自动降级机制（NeoData → WeStock → AkShare）
- 发布-订阅架构支持实时数据推送

**✅ 简化数据获取流程**
- 便捷函数：`quick_quote()`, `quick_financial()`, `quick_macro()`
- 生产管理器：`get_production()`
- 自然语言查询：`quick_query()`

**✅ 增强代码示例**
- 完整可执行的Python代码
- 明确的路径和依赖
- 统一的异常处理

---

## 执行流程

### Step 1: 任务解析

提取参数：
- `stock_code`（必需）- 股票代码
- `company_name`（必需）- 公司名称
- `report_type`（默认 initiating_coverage）- 报告类型
- `market`（自动推断）- 市场（A股/港股/美股）
- `report_period`（季报必需）- 报告期

❌ 缺少必需参数 → 提示用户补充

### Step 2: 数据获取（data_fetch）- DataHub统一接口

**数据源优先级（基于DataHub）**：

```
DataHub自动路由（优先级由Producer定义）：
1. LocalWikiProducer（优先级1）- 本地Wiki知识库
2. NeoDataProducer（优先级12）- 自然语言查询
3. WeStockProducer（优先级13）- 腾讯自选股
4. AkShareProducer（优先级15）- AkShare开源数据
5. YFinanceProducer（优先级16）- Yahoo Finance
```

**DataHub便捷函数使用**：

```python
import asyncio
import sys
# 用户需自行配置DataHub路径
# sys.path.insert(0, "<YOUR_DATAHUB_PATH>")

from datahub.production_startup import (
    quick_quote,
    quick_financial,
    quick_macro,
    quick_query,
    get_production
)

async def fetch_research_data(stock_code: str, market: str = 'cn') -> dict:
    """获取研究所需全部数据"""
    prod = await get_production()

    # 并发获取多维度数据
    tasks = [
        quick_quote(stock_code, market=market),
        quick_financial(stock_code, report_type='balance'),
        quick_financial(stock_code, report_type='income'),
        quick_financial(stock_code, report_type='cashflow'),
    ]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    return {
        'quote': results[0] if not isinstance(results[0], Exception) else None,
        'balance': results[1] if not isinstance(results[1], Exception) else None,
        'income': results[2] if not isinstance(results[2], Exception) else None,
        'cashflow': results[3] if not isinstance(results[3], Exception) else None,
    }

# 执行
asyncio.run(fetch_research_data("600519", market='cn'))
```

**自然语言查询示例**：

```python
from datahub.production_startup import quick_query

async def query_financial_data(query: str) -> dict:
    """自然语言查询金融数据"""
    result = await quick_query(query)

    if result['status'] == 'success':
        return result['data']
    else:
        print(f"查询失败: {result.get('error')}")
        return None

# 示例查询
asyncio.run(query_financial_data("贵州茅台最新财报营收和净利润"))
asyncio.run(query_financial_data("新能源板块资金流向"))
asyncio.run(query_financial_data("比亚迪机构评级和目标价"))
```

**主题订阅（高级用法）**：

```python
import asyncio
from datahub import get_datahub, register_all_producers

async def subscribe_realtime_data(stock_code: str, callback):
    """订阅实时数据推送"""
    datahub = get_datahub()
    register_all_producers(datahub)

    topic = f"westock:cn:quote:{stock_code}"
    datahub.subscribe(topic, callback)
    await datahub.request_refresh(topic)

# 示例回调
async def on_quote_update(data):
    print(f"行情更新: {data}")

asyncio.run(subscribe_realtime_data("600519", on_quote_update))
```

**货币单位注意**：
- 港股财报返回**港元/美元**，美股返回**美元**
- 展示时必须标注正确货币单位，禁止使用人民币符号

**检查点**：`⚠️ 数据质量确认 - 是否继续？[Y/n]`

### Step 3: 财务分析（financial_analysis）

**使用DataHub财务数据**：

```python
from datahub.production_startup import quick_financial

async def analyze_financials(stock_code: str) -> dict:
    """财务分析"""
    # 获取三大报表
    balance = await quick_financial(stock_code, report_type='balance')
    income = await quick_financial(stock_code, report_type='income')
    cashflow = await quick_financial(stock_code, report_type='cashflow')

    # 提取关键指标
    if all(r['status'] == 'success' for r in [balance, income, cashflow]):
        bal_data = balance['data']
        inc_data = income['data']
        cf_data = cashflow['data']

        # 计算核心指标
        metrics = {
            '毛利率': (inc_data['营收'] - inc_data['营业成本']) / inc_data['营收'],
            '净利率': inc_data['净利润'] / inc_data['营收'],
            'ROE': inc_data['净利润'] / bal_data['股东权益合计'],
            'ROIC': calculate_roic(inc_data, bal_data),
        }

        return metrics

    return None

def calculate_roic(income: dict, balance: dict) -> float:
    """计算ROIC"""
    nopat = income['净利润'] + income['利息支出'] * (1 - 0.25)  # 假设税率25%
    invested_capital = balance['股东权益合计'] + balance['有息负债'] - balance['现金及等价物']
    return nopat / invested_capital if invested_capital > 0 else None
```

**异常处理**：

| 异常 | 处理 |
|-----|-----|
| 指标无法计算 | 标注"N/A"，不估算 |
| 负权益公司 | 用经营资产法计算 ROIC |
| 数据不足（<3年） | 标注"分析可靠性降低" |
| DataHub返回错误 | 检查Producer注册，切换备用源 |

### Step 4: 估值分析（valuation）

**DCF估值（Python计算）**：

```python
def dcf_valuation(
    free_cash_flow: float,
    growth_rate: float = 0.05,
    discount_rate: float = 0.10,
    terminal_growth: float = 0.03,
    years: int = 10
) -> dict:
    """DCF估值计算"""
    # 预测未来现金流
    fcf_projections = []
    fcf = free_cash_flow
    for year in range(years):
        fcf *= (1 + growth_rate)
        fcf_projections.append(fcf)

    # 折现
    discounted_fcf = []
    for i, fcf in enumerate(fcf_projections, 1):
        discounted = fcf / ((1 + discount_rate) ** i)
        discounted_fcf.append(discounted)

    # 终值
    terminal_value = fcf_projections[-1] * (1 + terminal_growth) / (discount_rate - terminal_growth)
    discounted_terminal = terminal_value / ((1 + discount_rate) ** years)

    # 企业价值
    enterprise_value = sum(discounted_fcf) + discounted_terminal

    return {
        'enterprise_value': enterprise_value,
        'pv_fcf': sum(discounted_fcf),
        'pv_terminal': discounted_terminal,
        'assumptions': {
            'growth_rate': growth_rate,
            'discount_rate': discount_rate,
            'terminal_growth': terminal_growth,
        }
    }
```

**异常处理**：

| 异常 | 处理 |
|-----|-----|
| 无可比公司 | 仅用 DCF |
| 负自由现金流 | 改用 P/B 或 EV/Sales |
| DataHub无估值数据 | 从财报手动计算 |

**检查点**：`⚠️ 估值假设确认 - 是否接受？[Y/edit]`

### Step 5: 行业分析（仅首发覆盖）

**使用DataHub + 搜索引擎**：

```python
from datahub.production_startup import quick_query
# 搜索引擎（通过Skill调用）
# multi-search-engine: 16引擎聚合
# news-search: 财经资讯专用
# wechat-article-search: 公众号文章

async def industry_analysis(industry: str) -> dict:
    """行业分析"""
    # DataHub获取行业数据
    industry_data = await quick_query(f"{industry}行业规模和增长率")
    competitors = await quick_query(f"{industry}主要上市公司市场份额")

    return {
        'industry_data': industry_data,
        'competitors': competitors,
    }
```

**搜索引擎优先级（通过Skill调用）**：

1. **multi-search-engine**（最高优先级）
   - 16个引擎聚合（7中文 + 9国际）
   - 无需API密钥
   - 智能语言识别

2. **news-search**（财经专用）
   - 财经领域资讯
   - 覆盖官媒、主流财经媒体

3. **wechat-article-search**（公众号）
   - 科技/AI、财经、职场
   - 深度分析文章

Python：行业规模、市场份额、周期判断
AI：波特五力、政策影响、技术趋势

### Step 6: 竞争分析（仅首发覆盖）

Python：竞争对手筛选、指标对比
AI：护城河评估（5类评级）

### Step 7: 报告生成（report_generation）

Python：数据压缩（~50K → ~3K tokens）、章节编排
AI：各章节内容生成（使用对应模板）

**检查点**：`⚠️ 报告生成完成 - 是否输出？[Y/preview/edit]`

### Step 8: 对抗性检验（可选）

使用 `adversarial_challenge` 模板质疑结论、识别逻辑漏洞

---

## 触发词

股票研究、深度研究、首发覆盖、季报更新、DCF估值、可比公司分析、财务分析、ROIC分析

---

## 报告类型

| 类型 | 字数 | 章节 | 模块 |
|-----|-----|-----|-----|
| 首发覆盖 | 6,000-10,000 | 投资+公司+行业+财务+估值+风险+建议 | 全部模块 |
| 季报更新 | 3,000-5,000 | 业绩+经营+财务+预测+估值+建议 | data+financial+valuation+report |

---

## Python/AI 分工

| Python | AI |
|-------|-----|
| 数据获取（DataHub）、指标计算、估值建模 | 财报解读、因果推理、定性判断 |
| 数据压缩、统计分析、图表 | 投资要点、风险提示、护城河评估 |

---

## AI 提示词模板（10个）

| 模板 | 用途 |
|-----|-----|
| `investment_highlights` | 投资要点提炼 |
| `earnings_deep_dive` | 财报深度解读（5步框架）|
| `financial_quality` | 财务质量诊断（4维度）|
| `industry_analysis` | 行业深度分析（波特五力）|
| `competitive_analysis` | 竞争格局（护城河评估）|
| `valuation_analysis` | 估值分析（多方法对比）|
| `risk_analysis` | 风险分析（4类矩阵）|
| `investment_recommendation` | 投资建议（评级+目标价）|
| `adversarial_challenge` | 对抗性质疑（空头视角）|
| `tracking_checklist` | 跟踪验证清单 |

---

## 完整使用示例

### 示例1：首发覆盖报告

```python
import asyncio
import sys
# 用户需自行配置DataHub路径
# sys.path.insert(0, "<YOUR_DATAHUB_PATH>")

from datahub.production_startup import get_production

async def initiating_coverage(stock_code: str, company_name: str, market: str = 'cn'):
    """首发覆盖报告完整流程"""
    prod = await get_production()

    print(f"=== {company_name} ({stock_code}) 首发覆盖研究 ===")

    # 1. 数据获取
    print("\n[1/7] 数据获取...")
    data = await fetch_all_data(prod, stock_code, market)

    # 2. 财务分析
    print("\n[2/7] 财务分析...")
    financials = await analyze_financials(data)

    # 3. 估值分析
    print("\n[3/7] 估值分析...")
    valuation = perform_valuation(data, financials)

    # 4. 行业分析
    print("\n[4/7] 行业分析...")
    industry = await analyze_industry(company_name)

    # 5. 竞争分析
    print("\n[5/7] 竞争分析...")
    competition = analyze_competition(data, industry)

    # 6. 报告生成
    print("\n[6/7] 生成报告...")
    report = generate_report({
        'company': company_name,
        'stock_code': stock_code,
        'data': data,
        'financials': financials,
        'valuation': valuation,
        'industry': industry,
        'competition': competition,
    })

    # 7. 对抗性检验
    print("\n[7/7] 对抗性检验...")
    challenges = adversarial_review(report)

    return report

async def fetch_all_data(prod, stock_code: str, market: str) -> dict:
    """获取全维度数据"""
    from datahub.production_startup import quick_quote, quick_financial

    tasks = [
        quick_quote(stock_code, market=market),
        quick_financial(stock_code, report_type='balance'),
        quick_financial(stock_code, report_type='income'),
        quick_financial(stock_code, report_type='cashflow'),
    ]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    return {
        'quote': results[0] if not isinstance(results[0], Exception) else None,
        'balance': results[1] if not isinstance(results[1], Exception) else None,
        'income': results[2] if not isinstance(results[2], Exception) else None,
        'cashflow': results[3] if not isinstance(results[3], Exception) else None,
    }

# 执行
asyncio.run(initiating_coverage("600660", "福耀玻璃", market='cn'))
```

### 示例2：季报更新报告

```python
import asyncio
import sys
# 用户需自行配置DataHub路径
# sys.path.insert(0, "<YOUR_DATAHUB_PATH>")

from datahub.production_startup import quick_quote, quick_financial, quick_query

async def earnings_update(stock_code: str, company_name: str, report_period: str, market: str = 'cn'):
    """季报更新报告"""
    print(f"=== {company_name} {report_period} 季报更新 ===")

    # 1. 获取最新数据
    quote = await quick_quote(stock_code, market=market)
    income = await quick_financial(stock_code, report_type='income')
    news = await quick_query(f"{company_name} {report_period} 财报分析")

    # 2. 分析业绩
    if income['status'] == 'success':
        data = income['data']
        analysis = {
            '营收同比': data.get('营收同比增长'),
            '净利润同比': data.get('净利润同比增长'),
            '毛利率变动': data.get('毛利率变动'),
        }

    # 3. 生成报告
    report = {
        'company': company_name,
        'period': report_period,
        'quote': quote,
        'income': income,
        'analysis': analysis,
        'news': news,
    }

    return report

# 执行
asyncio.run(earnings_update("00700", "腾讯控股", "2024Q3", market='hk'))
```

---

## 关键约束

1. **AI 不计算，只解读** — 所有数值由 Python 计算
2. **必须引用数据** — 禁止模糊表述，每个结论引用具体数值
3. **区分事实与推测** — 推测标注"需验证"
4. **缺失数据显式标注** — 绝不估算，缺失项标注"N/A"
5. **分层处理** — 数据压缩后再交给 AI，避免上下文溢出
6. **DataHub统一入口** — 所有数据获取通过DataHub，不直接调用独立数据源

---

## DataHub故障排查

### Q: Producer未注册

```python
from datahub import get_datahub, register_all_producers

datahub = get_datahub()
producers = register_all_producers(datahub)
print(f"已注册Producer: {len(producers)}")
```

### Q: 数据获取失败

```python
from datahub.production_startup import quick_quote

result = await quick_quote("600519", market='cn')

if result['status'] == 'success':
    print(result['data'])
elif result['status'] == 'timeout':
    print("请求超时，检查网络连接")
elif result['status'] == 'error':
    print(f"错误: {result.get('error')}")
```

### Q: 缓存命中率低

```python
from datahub import get_datahub

datahub = get_datahub()
stats = datahub.get_stats()
print(f"缓存统计: {stats}")
```

---

## 相关文档

- **DataHub Skill**: 需配合 datahub skill 使用
- **DataHub生产指南**: 参考 datahub 文档
- **Python/AI分工**: 参考 docs/PYTHON_AI_DIVISION.md
- **AI提示词模板**: 参考 docs/AI_PROMPT_TEMPLATES.md

---

**股票研究系统已集成DataHub统一数据层，数据获取更高效、更可靠！**
