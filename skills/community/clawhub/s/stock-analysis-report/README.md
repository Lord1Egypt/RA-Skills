<div align="center">

# 📈 A 股股票市场分析 Skill

专为 OpenClaw 等智能体设计的 A 股股票分析技能

[![License: MIT-0](https://img.shields.io/badge/License-MIT--0-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-green.svg)](https://github.com/openclaw)

基于 [daily\_stock\_analysis](https://github.com/ZhuLinsen/daily_stock_analysis) 项目精简重写，去除 WebUI、通知推送、Agent 问股等非核心功能，聚焦分析能力本身。

</div>

***

## ✨ 功能特性

### 📊 个股分析

输入股票代码，输出结构化分析结果：

- **技术面分析**：MA5/MA10/MA20/MA60 均线、多头排列判断、乖离率、量比
- **筹码分布**：获利比例、平均成本、集中度
- **舆情情报**：妙想金融资讯（新闻/研报/公告，LLM 分析）+ 多引擎新闻搜索
- **实时行情**：当前价、涨跌幅、成交量、换手率等
- **分析结论**：一句话核心结论 + 评分 + 操作方向 + 精确买卖点位 + 操作检查清单 + 买卖策略

### 🌐 市场分析

每日 A 股市场复盘：

- **主要指数**：上证指数、深证成指、创业板指
- **市场统计**：涨跌家数、涨停跌停数
- **板块排名**：领涨 / 领跌板块 Top5
- **分析结论**：市场情绪判断 + 操作建议 + 完整复盘报告

### 🔄 多源数据架构

#### 推荐配置：妙想金融

配置 `MX_APIKEY` 后，妙想金融自动成为行情数据、财务/资金/估值、资讯搜索的**最高优先级数据源**，覆盖能力最全、数据质量最高。推荐优先配置。

👉 前往 [妙想 Skills 页面](https://dl.dfcfs.com/m/itc4) 获取 API Key

#### 行情数据采用自动容灾策略：

| 优先级 | 数据源          | 说明                          |    需要 Token   |
| :-: | ------------ | --------------------------- | :-----------: |
|  0  | **妙想金融**     | 东财妙想 API，覆盖行情 + 财务数据        | ✅ `MX_APIKEY` |
|  1  | **Efinance** | 基于东财接口，覆盖日 K、实时行情、板块排名、市场统计 |       ❌       |
|  2  | **AkShare**  | 东财 + 新浪双通道，额外支持筹码分布         |       ❌       |

> - 配置 `MX_APIKEY` 后妙想自动成为最高优先级；未配置时从 Efinance 开始
> - 任意数据源异常时自动切换到下一级，无需人工干预

## 🚀 快速开始

### 方式一：通过 ClawHub 安装（推荐）

使用 OpenClaw CLI 一键安装：

```bash
openclaw skill install stock-analysis-report
```

安装后即可在 OpenClaw 中直接使用：

```
分析贵州茅台
市场分析
```

### 方式二：本地开发

#### 1. 安装依赖

```bash
pip install -r requirements.txt
```

#### 2. 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的 API Key：

```env
# LLM 配置（必填）— 支持 DeepSeek 和 OpenAI 兼容模型
LLM_BASE_URL=https://api.deepseek.com/v1
LLM_API_KEY=your-api-key-here
LLM_MODEL=deepseek-chat

# 妙想金融数据（可选，配置后自动成为第一优先级数据源 + 资讯搜索源）
MX_APIKEY=

# 新闻搜索（至少配置一个，可选）
SERPAPI_KEY=
TAVILY_KEY=
BRAVE_KEY=
BOCHA_KEY=
```

> 💡 行情数据源（Efinance / AkShare）均为免费接口，无需配置任何 Token。

#### 3. 调用分析

#### 生成 Markdown 报告（推荐）

```bash
# 个股分析报告 → reports/{代码}_{日期}.md
python3 scripts/report.py stock 600519

# 市场分析报告 → reports/market_{日期}.md
python3 scripts/report.py market

# 同时输出 JSON
python3 scripts/report.py stock 600519 --json

# 自定义输出目录
python3 scripts/report.py stock 600519 -o ./my-reports
```

#### JSON 输出

```bash
python3 scripts/analyze_stock.py 600519    # 个股分析
python3 scripts/analyze_market.py          # 市场分析
```

#### Python API

```python
import asyncio
from src.index import analyze_stock, analyze_market

# 个股分析 + 保存报告
result = asyncio.run(analyze_stock("600519", save=True))
print(result.core_conclusion)   # 一句话核心结论
print(result.action)            # 买入/观望/卖出

# 市场分析 + 保存报告
result = asyncio.run(analyze_market(save=True))
print(result.sentiment)         # 偏多/中性/偏空
```

#### OpenClaw Handler

```python
from src.index import handler

result = await handler({"mode": "stock", "code": "600519"})
result = await handler({"mode": "market", "save": True})
```

<details>
<summary>自定义配置</summary>

```python
from src.config import SkillConfig

config = SkillConfig(
    llm_base_url="https://api.openai.com/v1",
    llm_api_key="sk-xxx",
    llm_model="gpt-4o",
)

result = asyncio.run(analyze_stock("000001", config=config))
```

</details>

## 📁 项目结构

```
stock-analysis/
├── SKILL.md                     # Skill 定义（OpenClaw 标准入口）
├── manifest.yaml                # 机器可读元数据 + 输入输出 Schema
├── src/                         # 源代码
│   ├── index.py                 # Skill 入口（handler + analyze_stock/market）
│   ├── config.py                # 配置管理（环境变量 + .env）
│   ├── models.py                # 数据模型定义
│   ├── report.py                # Markdown 报告生成
│   ├── analyzer/
│   │   ├── stock.py             # 个股分析引擎
│   │   ├── market.py            # 市场分析引擎
│   │   └── prompts.py           # Prompt 模板
│   ├── data/
│   │   ├── provider.py          # 数据源抽象基类
│   │   ├── efinance_provider.py # Efinance 数据源（优先级 1）
│   │   ├── akshare_provider.py  # AkShare 数据源（优先级 2）
│   │   ├── manager.py           # 数据源管理器（多源自动容灾）
│   │   └── utils.py             # 公共工具（缓存/统计/限流）
│   ├── search/
│   │   ├── base.py              # 搜索引擎抽象基类
│   │   ├── miaoxiang.py         # 妙想金融资讯搜索（优先级 0）
│   │   ├── serpapi.py           # SerpAPI 搜索
│   │   ├── tavily.py            # Tavily 搜索
│   │   ├── brave.py             # Brave 搜索
│   │   └── bocha.py             # Bocha 搜索
│   └── llm/
│       └── client.py            # LLM 客户端（OpenAI 兼容接口）
├── scripts/                     # CLI 入口脚本
│   ├── report.py                # 报告生成器（推荐入口）
│   ├── analyze_stock.py         # 个股分析 JSON 输出
│   └── analyze_market.py        # 市场分析 JSON 输出
├── references/                  # 按需加载的详细文档
│   └── data-sources.md          # 数据源架构详细说明
├── test/                        # 测试
├── requirements.txt
├── config.example.yaml          # YAML 格式示例配置
├── .env.example
└── .gitignore
```

## 🏗️ 架构设计

```
┌──────────────────────────────────────────┐
│         SKILL.md / manifest.yaml          │
│         OpenClaw Skill 定义层             │
└──────────────────┬───────────────────────┘
                   │
┌──────────────────▼───────────────────────┐
│         src/index.py（接口层）              │
│  handler()  analyze_stock()  analyze_market() │
└──────────────────┬───────────────────────┘
                   │
┌──────────────────▼───────────────────────┐
│        src/analyzer/（分析层）              │
│     组装数据 + 构建 Prompt + 调用 LLM       │
└──┬───────────────┬───────────┬───────────┘
   │               │           │
   ▼               ▼           ▼
┌────────────┐ ┌──────┐ ┌──────────┐
│  src/data/ │ │search│ │   llm/   │
│   数据层    │ │搜索层 │ │  模型层   │
│ 三级自动容灾 │ │5 引擎 │ │DeepSeek  │
│            │ │(可扩展)│ │(OpenAI兼容)│
│ 妙想(可选)  │ └──────┘ └──────────┘
│  ↓ 失败     │
│ Efinance   │
│  ↓ 失败     │
│ AkShare    │
└────────────┘
```

每层均通过抽象基类解耦，可独立扩展：

- **数据层**：实现 `MarketDataProvider` 即可接入新数据源，`DataProviderManager` 自动管理容灾切换
- **搜索层**：实现 `NewsSearchEngine` 即可接入新搜索引擎
- **模型层**：所有 OpenAI 兼容 API 均可直接使用

### 数据源能力矩阵

| 能力      | 妙想金融 | Efinance | AkShare |
| ------- | :--: | :------: | :-----: |
| 股票基本信息  |   ✅  |     ✅    |    ✅    |
| 日 K 线数据 |   ✅  |     ✅    |    ✅    |
| 实时行情    |   ✅  |     ✅    |    ✅    |
| 筹码分布    |   ❌  |     ❌    |    ✅    |
| 板块排名    |   ❌  |     ✅    |    ✅    |
| 市场统计    |   ❌  |     ✅    |    ✅    |
| 指数数据    |   ✅  |     ✅    |    ✅    |
| 财务数据    |   ✅  |     ❌    |    ❌    |
| 主力资金    |   ✅  |     ❌    |    ❌    |
| 估值数据    |   ✅  |     ❌    |    ❌    |

### 资讯搜索架构

| 优先级 | 搜索引擎     | 数据源          |     需要 Key    | 返回内容            |
| :-: | -------- | ------------ | :-----------: | --------------- |
|  0  | **妙想搜索** | 东财妙想资讯 API   | ✅ `MX_APIKEY` | 完整正文 + 新闻/研报/公告 |
|  1  | SerpAPI  | Google 搜索    |       ✅       | snippet         |
|  2  | Tavily   | Tavily AI 搜索 |       ✅       | snippet         |
|  3  | Brave    | Brave 搜索     |       ✅       | snippet         |
|  4  | Bocha    | 博查搜索         |       ✅       | snippet         |

> - 配置 `MX_APIKEY` 后妙想搜索自动成为最高优先级，返回新闻 + 研报 + 公告三种类型
> - 妙想搜索返回完整正文，直传 LLM 进行分析；其他引擎仅返回 snippet
> - 研报类型含机构名称和评级（如"中泰证券·研报·买入"），LLM 可据此参考机构观点

### 反封禁策略

参照原项目实现，内置多项反封禁措施：

- 随机 User-Agent 轮换（5 组 UA）
- 请求间随机 Sleep（1.5 \~ 3.0 秒抖动）
- 全市场实时行情缓存（TTL 600 秒）
- 涨停 / 跌停精确计算（科创板 / 创业板 20%、北交所 30%、ST 5%、普通 10%）

## ⚙️ 配置说明

| 环境变量                |  必填 | 默认值                           | 说明                                                                  |
| ------------------- | :-: | ----------------------------- | ------------------------------------------------------------------- |
| `LLM_BASE_URL`      |  ✅  | `https://api.deepseek.com/v1` | OpenAI 兼容 API 地址                                                    |
| `LLM_API_KEY`       |  ✅  | —                             | API Key                                                             |
| `LLM_MODEL`         |  ✅  | `deepseek-chat`               | 模型名称                                                                |
| `SERPAPI_KEY`       |  ❌  | —                             | SerpAPI Key                                                         |
| `TAVILY_KEY`        |  ❌  | —                             | Tavily Key                                                          |
| `BRAVE_KEY`         |  ❌  | —                             | Brave Search Key                                                    |
| `BOCHA_KEY`         |  ❌  | —                             | 博查搜索 Key                                                            |
| `MX_APIKEY`         |  ❌  | —                             | 妙想金融数据 API Key（[前往获取](https://dl.dfcfs.com/m/itc4)），配置后自动成为第一优先级数据源 |
| `BIAS_THRESHOLD`    |  ❌  | `5.0`                         | 乖离率阈值（%）                                                            |
| `NEWS_MAX_AGE_DAYS` |  ❌  | `3`                           | 新闻最大时效（天）                                                           |
| `ENABLE_CHIP`       |  ❌  | `true`                        | 是否启用筹码分布                                                            |
| `LOG_LEVEL`         |  ❌  | `INFO`                        | 日志级别：DEBUG/INFO/WARNING/ERROR                                       |

## 📋 分析结果结构

<details>
<summary>个股分析 — StockAnalysisResult</summary>

| 字段                   | 类型               | 说明                   |
| -------------------- | ---------------- | -------------------- |
| `stock_code`         | str              | 股票代码                 |
| `stock_name`         | str              | 股票名称                 |
| `core_conclusion`    | str              | 一句话核心结论              |
| `score`              | int              | 评分 0-100             |
| `action`             | str              | 操作方向：买入/观望/卖出        |
| `trend`              | str              | 趋势判断：看多/震荡/看空        |
| `buy_price`          | float            | 建议买入价                |
| `stop_loss_price`    | float            | 止损价                  |
| `target_price`       | float            | 目标价                  |
| `checklist`          | list\[CheckItem] | 操作检查清单               |
| `risk_alerts`        | list\[str]       | 风险警报                 |
| `positive_catalysts` | list\[str]       | 利好催化                 |
| `strategy`           | str              | 买卖策略建议               |
| `raw_report`         | str              | LLM 完整分析报告（Markdown） |
| `disclaimer`         | str              | 免责声明                 |

</details>

<details>
<summary>市场分析 — MarketAnalysisResult</summary>

| 字段                | 类型                | 说明                   |
| ----------------- | ----------------- | -------------------- |
| `date`            | str               | 分析日期                 |
| `core_conclusion` | str               | 一句话核心结论              |
| `indices`         | list\[IndexData]  | 主要指数数据               |
| `statistics`      | MarketStatistics  | 涨跌统计                 |
| `top_sectors`     | list\[SectorData] | 领涨板块                 |
| `bottom_sectors`  | list\[SectorData] | 领跌板块                 |
| `sentiment`       | str               | 市场情绪：偏多/中性/偏空        |
| `strategy`        | str               | 操作建议                 |
| `raw_report`      | str               | LLM 完整复盘报告（Markdown） |
| `disclaimer`      | str               | 免责声明                 |

</details>

## ⚠️ 注意事项

- **免 Token 数据源**：Efinance / AkShare 均为免费接口，无需注册；妙想金融需配置 `MX_APIKEY`
- **自动容灾**：任一数据源异常时自动切换至下一级，日志输出 `[数据源切换]` 提示
- **网络环境**：东财接口在企业内网 / 代理下可能受限，系统会自动回退至新浪通道
- **API 限流**：搜索 API 有调用频率限制，频繁调用可能触发限流
- **数据时效**：实时行情基于最新日线数据，盘中数据可能有延迟
- **无状态设计**：Skill 不保存任何分析结果，每次调用独立执行

## 📄 License

本项目基于 [MIT-0 License](LICENSE) 开源。

## ⚖️ 免责声明

本项目所有分析结果仅供参考，不构成投资建议。股市有风险，投资需谨慎。
