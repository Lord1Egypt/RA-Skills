---
name: unified-asset-advisor
description: 统一大类资产配置分析技能（融合版）。基于宏观经济分析和申万一级行业趋势，生成中国大类资产配置建议报告。数据源采用 AKShare（底层对接国家统计局/东方财富等权威源，非黑盒）。输出三格式：HTML（可视化卡片+产业链图）、Markdown（完整分析文档）、Excel（8 Sheet结构化数据）。覆盖宏观经济→资产周期→行业筛选→产业链分析→品种操作（A股/港股通/QDII/ETF/债券基金/商品基金）→期货期权策略（含置信度评级+止损参考）。触发词：资产配置、宏观分析、大类资产、行业配置、投资建议、还有哪些资产值得关注。当用户手动选择此 skill 或使用这些触发词时使用。
agent_created: true
---

# Unified Asset Advisor — 统一大类资产配置分析

## Overview

本 skill 融合三个资产配置 skill 的最优设计，形成单一权威分析流程：

| 来源 | 吸收的优点 |
|------|----------|
| **asset-allocation-advisor**（主框架） | 置信度评级、产业链详细箭头图、多空信号矩阵、止损参考 |
| **macro-asset-advisor** | 七步递进框架、HTML可视化资产卡片、QDII自动匹配规则、动态实时查询 |
| **asset-allocation** | Excel多Sheet输出、清晰Markdown模板、债券/股票/商品/期货期权全覆盖 |

**数据源**：四源混合策略（经过实测验证，TDX响应17-25ms零断连）
- **TDX连接器**（首选行业/个股数据源）→ 行业板块涨跌/PE/PB/ROE、产业链图谱（nodes+links）、资金流向（4级拆分）、龙虎榜/融资融券/大宗交易、行业重要事件、行业财务/估值排名、研报评级一致预期、涨停跌停分析、北向资金、选股器、港股三大表
- **AKShare 国家统计局源**（最稳定）→ 宏观数据 PPI/CPI/PMI/GDP/M2/社融/LPR/中美国债利率
- **AKShare 新浪源**（稳定补充）→ 全球指数、港股指数、A股指数、期货主力、ETF分类行情
- **WebSearch**（兜底）→ 全球宏观补充（DXY/布伦特/黄金/标普/汇率）、政策催化补充、QDII基金列表
- ❌ 东方财富EM接口 (`*_em`) 频繁 RemoteDisconnected，不得作为主数据源
- ❌ westock-data 未安装且 TDX 已完全替代其功能，不再依赖
- ❌ 以下函数已验证不可用：`macro_china_rmb()`、`stock_sector_spot_indicator()`、`stock_sector_fund_flow_rank()`、`fund_qdii_spot_em()`

**输出格式**：HTML + Markdown + Excel（三份齐出）

## 执行流程

```
Step 1: 宏观数据采集（AKShare国家统计局源 + 新浪源 + WebSearch兜底）
  ↓
Step 2: 大类资产周期判断（四宫格 + 置信度）
  ↓
Step 3: 申万一级行业筛选（TDX 板块涨跌+资金+事件，替代westock-data）
  ↓
Step 4: 产业链上下游分析（TDX 产业链图谱 nodes+links 自动渲染）
  ↓
Step 5: 品种操作建议（TDX 实时行情+资金+研报评级 + AKShare新浪源ETF）
  ↓
Step 6: 期货期权策略（AKShare新浪源期货 + option-strategy-advisor期权链）
  ↓
Step 7: 三格式输出（HTML + Markdown + Excel）
```

---

## Step 1 — 宏观数据采集（三源混合）

### 1.1 Python 环境

使用已安装 akshare 的 venv 执行 `scripts/fetch_macro.py`。
若 venv 不存在，先创建并安装依赖：

```bash
# 创建 venv（路径基于当前用户的 ~/.workbuddy/binaries/python/envs/akshare）
python -m venv ~/.workbuddy/binaries/python/envs/akshare
# 安装依赖
~/.workbuddy/binaries/python/envs/akshare/Scripts/pip install akshare
```

执行脚本时使用 venv 中的 python：

```bash
# Windows
~/.workbuddy/binaries/python/envs/akshare/Scripts/python.exe scripts/fetch_macro.py china
# macOS/Linux
~/.workbuddy/binaries/python/envs/akshare/bin/python scripts/fetch_macro.py china
```

### 1.2 中国宏观指标（AKShare 国家统计局源，必查）

使用 `scripts/fetch_macro.py china` 一键拉取，或逐项调用：

```python
import akshare as ak

# ✅ 稳定可用的宏观函数
df = ak.macro_china_ppi()     # PPI 月度同比
df = ak.macro_china_cpi()     # CPI 月度同比
df = ak.macro_china_pmi()     # PMI 制造业+非制造业
df = ak.macro_china_gdp()     # GDP 季度
df = ak.macro_china_money_supply()  # M2
df = ak.macro_china_shrzgm()  # 社融
df = ak.macro_china_lpr()     # LPR
```

| 指标 | AKShare 函数 | 输出列 | 可用性 |
|------|------------|--------|:------:|
| PPI 同比 | `macro_china_ppi()` | 当月同比增长 | ✅ |
| CPI 同比 | `macro_china_cpi()` | 当月同比增长 | ✅ |
| 制造业 PMI | `macro_china_pmi()` | 制造业 | ✅ |
| GDP 增速 | `macro_china_gdp()` | 当季同比 | ✅ |
| M2 增速 | `macro_china_money_supply()` | 货币供应量 | ✅ |
| 社融规模 | `macro_china_shrzgm()` | 社会融资规模 | ✅ |
| LPR | `macro_china_lpr()` | 1年期/5年期 | ✅ |
| 人民币汇率 | `macro_china_rmb()` | — | ❌ TypeError，用WebSearch兜底 |

### 1.3 全球宏观指标（新浪源 + 中美国债利率 + WebSearch 兜底）

```python
# ✅ 新浪源（稳定）
df = ak.stock_info_global_sina()        # 全球指数（道琼斯/标普/纳斯达克/恒生等，20行）
df = ak.stock_hk_index_spot_sina()      # 港股指数（恒生/国企/红筹等，38行）
df = ak.stock_zh_index_spot_sina()     # A股指数（上证/深证/创业板，562行）

# ✅ 中美国债利率（AKShare 稳定）
df = ak.bond_zh_us_rate()               # 中美国债收益率对照，9270行

# ❌ 以下EM接口不可用（频繁 RemoteDisconnected），勿用
# stock_us_spot_em(), stock_hk_spot_em(), stock_hk_ggt_components_em()
```

如 AKShare 数据不全，**必须** WebSearch 补充：标普500、恒生指数、DXY、布伦特原油、COMEX黄金等。

### 1.4 数据验证

**关键宏观数据（PPI/CPI/PMI/GDP）必须双重确认**：
1. AKShare 拉取 → 
2. WebSearch 查 `stats.gov.cn` 官方发布值 →
3. 两者一致才写入报告，不一致时以 stats.gov.cn 为准修正

---

## Step 2 — 大类资产周期判断

基于 Step 1 数据，对照 `references/asset_cycle_logic.md` 美林时钟框架。

### 2.1 宏观环境六维判断

| 维度 | 判断 | 关键指标 |
|------|------|---------|
| 经济增长动能 | 扩张/收缩/中性 | GDP、PMI |
| 通胀压力 | 上行/下行/稳定 | CPI、PPI |
| 货币政策取向 | 宽松/中性/收紧 | LPR、MLF、准备金率 |
| 流动性环境 | 充裕/中性/偏紧 | M2、社融 |
| 外部需求 | 改善/恶化/稳定 | 出口、全球PMI |
| 风险偏好 | 上升/下降/震荡 | 汇率、VIX、外资流向 |

### 2.2 四类资产趋势判断

每类资产给出**方向+置信度（高/中/低）+1-2句逻辑**：

```
债券（Bond）：看空 | 置信度：高
  → PPI 加速至+2.8%推升通胀预期，美债10Y升至4.46%形成压制，降息紧迫性降低

商品（Commodity）：看多 | 置信度：高
  → 全球再通胀交易，黄金避险+原油地缘溢价+铜铝供需偏紧，三重共振
  → 直接推荐商品ETF：518880(黄金ETF)、159980(有色ETF)、159981(能源化工ETF)

股票（Stock）：看多 | 置信度：中
  → 盈利改善+流动性充裕，但需警惕PPI过快上行挤压中下游利润

现金（Cash）：中性偏减持 | 置信度：中
  → 实际利率收窄，通胀侵蚀购买力；保留部分灵活性等待回撤机会
```

---

## Step 3 — 申万一级行业筛选

### 3.1 行业数据获取（TDX连接器为主，响应17-25ms）

**❌ AKShare 以下函数不可用：**
- `stock_sector_spot_indicator()` — 函数不存在
- `stock_board_industry_name_em()` — 频繁 RemoteDisconnected
- `stock_sector_fund_flow_rank()` — KeyError 编码问题

**✅ TDX连接器替代（核心接口）：**

#### 3.1.1 板块涨跌幅（替代 westock-data sector）
```
DeferExecuteTool: mcp__tdx-connector__tdx_api_data
  entry="TdxSharePCCW.skef10_bk_cpbd_jczl"
  branch="003"           # 阶段涨幅
  code="881001"          # 申万一级行业代码（881001=农林牧渔...881031=综合）
  timeType="1m"          # 近1月累计涨幅；可选 5d/1m/3m/6m/1y
```
返回：行业名称、近N日累计涨幅、同期上证涨幅对比

#### 3.1.2 板块PE/PB/ROE（新增能力，之前无法获取）
```
DeferExecuteTool: mcp__tdx-connector__tdx_api_data
  entry="TdxSharePCCW.skef10_bk_cpbd_jczl"
  branch="001"           # 基础资料
  code="881001"
  timeType="1m"
```
返回：PE(TTM)、PB、ROE、资产负债率等

#### 3.1.3 板块市场统计（量价配合，新增能力）
```
DeferExecuteTool: mcp__tdx-connector__tdx_api_data
  entry="TdxSharePCCW.skef10_bk_cpbd_jczl"
  branch="004"           # 市场统计
  code="881001"
  timeType="1m"
```
返回：成交量、成交额、换手率、涨跌家数

#### 3.1.4 行业重要事件（替代 WebSearch 政策催化）
```
DeferExecuteTool: mcp__tdx-connector__tdx_api_data
  entry="TdxSharePCCW.skef10_hy_zxdt_hyzysj"
  industryCode="881001"   # 行业代码
  title=""                # 空字符串返回全部
```
返回：TDX专业编辑维护的结构化行业事件列表

#### 3.1.5 行业财务/估值排名（新增能力）
```
# 行业财务排名
DeferExecuteTool: mcp__tdx-connector__tdx_api_data
  entry="TdxShareCW.ph_agf10_hypm"
  queryKey="00102"
  code="881001"

# 行业估值排名
DeferExecuteTool: mcp__tdx-connector__tdx_api_data
  entry="TdxShareCW.ph_agf10_hypm"
  queryKey="00105"
  code="881001"
```

#### 3.1.6 个股资金流向（替代 westock-data asfund）
```
DeferExecuteTool: mcp__tdx-connector__tdx_api_data
  entry="TdxSharePCCW.tdxf10_gg_jyds"
  code="000001"           # 6位股票代码
  fixedTag="zjlx"         # 资金流向
  extra="5"               # 近5日
```
返回：主力净额、超大单/大单/中单/小单4级拆分、主买/主卖

#### 3.1.7 龙虎榜（替代 westock-data lhb）
```
DeferExecuteTool: mcp__tdx-connector__tdx_api_data
  entry="TdxSharePCCW.tdxf10_gg_jyds"
  code="000001"
  fixedTag="jglhb"        # 龙虎榜
  extra="5"
```

#### 3.1.8 申万一级行业代码速查表

| 行业 | 代码 | 行业 | 代码 | 行业 | 代码 |
|------|------|------|------|------|------|
| 农林牧渔 | 881001 | 计算机 | 881011 | 电子 | 881021 |
| 采掘 | 881002 | 传媒 | 881012 | 国防军工 | 881022 |
| 化工 | 881003 | 通信 | 881013 | 建筑装饰 | 881023 |
| 钢铁 | 881004 | 公用事业 | 881014 | 机械设备 | 881024 |
| 有色金属 | 881005 | 非银金融 | 881015 | 房地产 | 881025 |
| 建筑材料 | 881006 | 银行 | 881016 | 商业贸易 | 881026 |
| 电气设备 | 881007 | 房地产 | 881017 | 社会服务 | 881027 |
| 家用电器 | 881008 | 医药生物 | 881018 | 轻工制造 | 881028 |
| 食品饮料 | 881009 | 纺织服装 | 881019 | 环保 | 881029 |
| 汽车 | 881010 | 休闲服务 | 881020 | 综合 | 881030 |

> 代码规律：881001~881031，大部分为31个申万一级行业。具体代码可用 `tdx_lookup_stock query="有色金属" range="ZS"` 确认。

**✅ AKShare 新浪源补充：**
```python
# A股指数行情（562行，含各行业指数）
df = ak.stock_zh_index_spot_sina()
```

### 3.2 三维筛选模型

| 维度 | 权重 | 数据来源 | 评分标准 |
|------|:----:|---------|---------|
| 趋势（近20日涨跌） | 40% | TDX `board_cpbd_stage_return` (branch=003) | 涨幅前10 = 高分 |
| 资金（近5日净流入） | 30% | TDX `capital_flow` (fixedTag=zjlx) | 主力净流入 = 高分 |
| 政策（近期催化） | 30% | TDX `industry_important_events` | 有明确催化 = 高分 |

**默认模式**（用户未指定行业）：
- 选出得分最高的 **5个上升行业**
- 选出得分最低的 **5个下降行业**

**全行业模式**（触发词："全行业"/"全部"/"所有行业"/"31个"）：
- 对31个申万一级行业逐一打分并排序

**指定行业模式**：仅分析用户指定的行业

### 3.3 行业与宏观关联

基于 PPI/CPI/PMI 等宏观数据，分析行业受益/受损：
- 上游受益行业（有色/石化/煤炭/钢铁）— PPI上行直接受益
- 中游分化行业（化工/建材/机械设备，成本推升但转嫁能力不一）
- 下游承压行业（家电/汽车/食品饮料，成本侵蚀利润）

---

## Step 4 — 产业链上下游分析（TDX自动渲染）

### 4.1 TDX产业链图谱（核心升级：从手动文本→结构化图谱）

```
DeferExecuteTool: mcp__tdx-connector__tdx_api_data
  entry="TdxSharePCCW.cfg_tk_gethy"
  industryCode="881001"     # 申万一级行业代码
```

返回结构化产业链数据：
- `nodes[]`: 节点列表，每个节点含 `id`、`name`、`category`（上游/中游/下游）
- `links[]`: 连接列表，每条含 `source`→`target`、`label`（传导关系）

**HTML渲染**：将 nodes+links 直接渲染为 SVG 力导向图，替代原有的文本箭头图。
**Markdown输出**：仍可转为文本格式：`上游(名称) → 传导关系 → 下游(名称)`

### 4.2 产业链分析维度（保留）

对每个筛选出的行业，分析内容：
- 上游原材料价格走势（对成本的影响）
- 下游需求景气度（对收入的影响）
- 产业链利润分配格局（谁在赚钱/谁在承压）
- 库存周期位置（主动补库/被动去库/主动去库/被动补库）

### 4.3 产业链增强数据（TDX新增）

| 数据 | TDX接口 | 用途 |
|------|---------|------|
| 板块PE/PB/ROE | `board_cpbd_basic_info` (branch=001) | 产业链各环节估值对比 |
| 板块阶段涨幅 | `board_cpbd_stage_return` (branch=003) | 上下游价格传导验证 |
| 板块市场统计 | `board_cpbd_market_stats` (branch=004) | 量价配合判断 |
| 行业重要事件 | `industry_important_events` | 产业链催化/风险事件 |
| 个股主营构成 | `business_composition` (fixedTag=00202) | 验证个股在产业链中的位置 |

---

## Step 5 — 品种操作建议

### 5.1 A股标的（TDX连接器为主）

**❌ AKShare EM接口不可用：** `stock_board_industry_cons_em()`、`stock_zh_a_spot_em()` 频繁断连

**✅ 使用 TDX连接器替代：**

#### 5.1.1 代码检索
```
DeferExecuteTool: mcp__tdx-connector__tdx_lookup_stock
  query="紫金矿业"         # 按名称搜索
  range="AG"              # A股
```

#### 5.1.2 实时行情
```
DeferExecuteTool: mcp__tdx-connector__tdx_quotes
  code="601899"           # 6位股票代码（不带sh/sz前缀）
  setcode="1"             # 1=沪市, 0=深市, 2=北交所
  hasCalcInfo="1"         # 含PE/PB/总市值等
  hasCwInfo="1"           # 含财务信息
```

#### 5.1.3 K线行情
```
DeferExecuteTool: mcp__tdx-connector__tdx_kline
  code="601899"
  setcode="1"
  period="4"              # 4=日线, 5=周线, 6=月线
  wantNum="20"            # 最近20根K线
```

#### 5.1.4 条件选股（新增能力）
```
DeferExecuteTool: mcp__tdx-connector__tdx_screener
  message="主力净流入"     # 自然语言条件
  rang="AG"               # A股
  pageSize="10"
```

#### 5.1.5 研报评级一致预期（新增能力）
```
DeferExecuteTool: mcp__tdx-connector__tdx_api_data
  entry="TdxSharePCCW.tdxf10_gg_ybpj"
  code="601899"
  fixedTag="yzyq"
```
返回：券商评级、目标价、一致预期EPS

#### 5.1.6 估值历史（新增能力）
```
DeferExecuteTool: mcp__tdx-connector__tdx_api_data
  entry="TdxShareCW.ph_agf10_gzfx"
  code="601899"
  extraOne="1"            # PE历史分位
  extraTwo="0"
```

#### 5.1.7 涨停/跌停分析（新增能力，行业情绪判断）
```
# 涨停分析
DeferExecuteTool: mcp__tdx-connector__tdx_api_data
  entry="TdxSharePCCW.tdxf10_gg_jyds"
  code="000001"
  fixedTag="ztfx"
  extra="5"

# 跌停分析
  fixedTag="dtfx"
```

每个行业输出 **2-3只** 精选标的（兼顾龙头和弹性），含代码、最新价、涨跌幅、PE/PB。

### 5.2 港股通标的

**✅ 使用 TDX连接器：**

```
# 代码检索
DeferExecuteTool: mcp__tdx-connector__tdx_lookup_stock
  query="腾讯控股"
  range="HK-GP"

# 实时行情（target必须设为"1"）
DeferExecuteTool: mcp__tdx-connector__tdx_quotes
  code="00700"            # 5位港股代码
  setcode="31"            # 港股setcode
  target="1"              # ⚠️ 港股必须传1

# 港股三大表
DeferExecuteTool: mcp__tdx-connector__tdx_api_data
  entry="TdxSharePCCW.skef10_hk_cwfx"
  code="00700"
  fixedTag="1"            # 1=损益表, 2=资产负债表, 3=现金流量表
```

输出港股代码、最新价(HKD)、AH溢价、三大表数据。

### 5.2.1 北向资金（新增能力）
```
DeferExecuteTool: mcp__tdx-connector__tdx_api_data
  entry="TdxSharePCCW.tdxf10_gg_zlcc"
  code="000001"
  fixedTag="bszj"
  extra="5"
```

### 5.3 ETF/基金

**✅ TDX连接器 + AKShare 新浪源：**

```
# 基金代码检索
DeferExecuteTool: mcp__tdx-connector__tdx_lookup_stock
  query="510300"
  range="JJ"

# 基金实时行情
DeferExecuteTool: mcp__tdx-connector__tdx_quotes
  code="510300"
  setcode="1"

# 基金指标查询（规模、净值等）
DeferExecuteTool: mcp__tdx-connector__tdx_indicator_select
  message="华泰柏瑞沪深300ETF的基金规模和最新净值"
  rang="JJ"
```

```python
# ✅ 新浪源 ETF 分类行情（382行，稳定）
df = ak.fund_etf_category_sina()

# ✅ AKShare EM源 ETF 行情（1490行，可能断连）
df = ak.fund_etf_spot_em()

# ❌ QDII函数不存在
# fund_qdii_spot_em() — AttributeError，用WebSearch查QDII基金列表
```

输出1-2只流动性好的ETF（优先规模>5亿、日均成交额>1000万）。

### 5.4 QDII跨境基金自动匹配

| 条件触发 | QDII基金类别 |
|---------|-------------|
| 电子/计算机行业上升 | 纳斯达克100 / 全球科技 QDII |
| 医药生物行业上升 | 全球医疗保健 QDII |
| 商品看多 | 原油QDII / 黄金QDII |
| 债券看多 | 全球债券 / 美元债 QDII |
| 股票看多（整体） | 标普500 QDII / 全球股票 QDII |
| 消费/互联网上升 | 全球消费 / 中概互联 QDII |

### 5.4.1 商品ETF自动匹配（比QDII更直接）

| 条件触发 | 商品ETF | 代码 | 说明 |
|---------|---------|------|------|
| 商品整体看多 | 黄金ETF | 518880 | 规模1022亿，流动性最强 |
| 有色金属行业上升 | 有色金属ETF | 159980 | 规模66亿，铜铝锡全面受益 |
| 有色金属+贵金属 | 白银基金LOF | 161226 | 规模75亿，兼具工业+贵金属属性 |
| 石油石化行业上升 | 能源化工ETF | 159981 | 规模34亿，原油+化工双线 |
| 原油看多 | 南方原油LOF | 160723 | 规模14亿，跟踪原油价格 |
| 农产品看多 | 豆粕ETF | 159985 | 规模30亿，通胀传导受益 |

### 5.5 商品ETF品种池

在商品看多或相关行业上升时，**必须**在操作建议中推荐以下商品ETF，与行业ETF并列：

| 代码 | 名称 | 类型 | 规模 | 适用场景 |
|------|------|------|:----:|---------|
| 518880 | 华安黄金ETF | 黄金 | 1022亿 | 商品看多、避险需求、通胀上行 |
| 161226 | 国投瑞银白银基金LOF | 白银 | 75亿 | 有色金属上升、工业金属+贵金属双线 |
| 159980 | 华夏有色金属ETF | 有色金属 | 66亿 | 有色金属行业上升、铜铝锡全面受益 |
| 159985 | 华夏豆粕ETF | 豆粕 | 30亿 | 农产品看多、通胀传导 |
| 159981 | 易方达能源化工ETF | 能源化工 | 34亿 | 石油石化上升、原油化工品涨价 |
| 160723 | 南方原油LOF | 原油 | 14亿 | 原油看多、地缘溢价 |

**推荐规则**：
- 商品大类看多时 → 推荐 **518880(黄金ETF)** 作为首选
- 有色金属行业上升 → 推荐 **159980(有色ETF)** + **161226(白银基金)**，与行业ETF(512400)并列
- 石油石化行业上升 → 推荐 **159981(能源化工ETF)** + **160723(原油LOF)**
- 农林牧渔/农产品看多 → 推荐 **159985(豆粕ETF)**
- 优先推荐规模>50亿、日均成交额>1000万的品种
- 规模<20亿的品种标注"流动性一般，注意冲击成本"

### 5.6 债券/可转债

**✅ AKShare 可用：**

```python
# ✅ 可转债（集思录源，稳定）
df = ak.bond_cb_jsl()

# ✅ 可转债汇总（新浪源，稳定）
df = ak.bond_cb_summary_sina()
```

---

## Step 6 — 期货期权策略

### 6.1 期货策略

**✅ AKShare 新浪源（稳定）：**

```python
# ✅ 期货主力品种列表（82行，含symbol/exchange/name）
df = ak.futures_display_main_sina()

# ✅ 期货主力合约行情（需传symbol参数如'RB0'）
df = ak.futures_main_sina(symbol='RB0')  # 螺纹钢主力

# ✅ 可转债汇总（新浪源）
df = ak.bond_cb_summary_sina()
```

**❌ 以下函数不可用或有坑：**
- `futures_foreign_commodity_realtime()` — 需传symbol参数，不能无参调用
- `futures_hold_pos_sina(symbol)` — symbol参数格式有误

**策略规则**：
| 资产周期 | 期货策略 |
|---------|---------|
| 上升期 | 做多，附主力合约代码+最新价+建议仓位 |
| 下跌期 | 做空，附主力合约代码+最新价+建议仓位 |
| 震荡期 | 观望或区间操作 |
| 不确定 | 减仓 |

### 6.2 期权策略

对 Step 2 判断方向相关的 ETF（510050/510300/510500/159915/588000），给出期权策略。

中国境内存在的 ETF 期权标的：上证50ETF(510050)、沪深300ETF(510300)、中证500ETF(510500)、创业板ETF(159915)、科创50ETF(588000)、深证100ETF(159901)。黄金ETF(518880)目前在中国境内没有对应的期权产品，不得推荐。

给出策略：

| 周期 | 期权策略 | 说明 |
|------|---------|------|
| 上升期 | 买看涨 / 牛市价差 / 卖看跌 | 方向性看多 |
| 下跌期 | 买看跌 / 熊市价差 / 卖看涨 | 方向性看空 |
| 震荡期 | 卖跨式/宽跨式 / 铁鹰价差 | 赚取时间价值 |
| 不确定 | 买跨式/宽跨式 | 做多波动率 |

### 6.3 每个建议必须包含

```
品种：合约代码 + 最新价
方向：做多/做空/卖出期权
推荐策略：策略名称
具体参数：
  - 行权价：XXXX（期权）
  - 到期月：XXXX年X月
  - 建议仓位：X%
  - 止损参考：XXXX（期货）/ 最大亏损：XXXX（期权）
风险提示：关键注意事项
```

---

## Step 7 — 三格式输出

### 7.1 HTML 报告

使用 `assets/report_template.html` 模板，填充占位符。特点：
- 顶部四张资产卡片（`.asset-card` 样式，涨红跌绿）
- 行业产业链可视化箭头图
- QDII 专区独立卡片
- 期货期权策略表（含止损参考列）

保存为 `asset_config_report_{YYYY-MM-DD}.html`，调用 `preview_url` 预览。

### 7.2 Markdown 报告

使用 `assets/report_template.md` 结构模板。输出结构：

```markdown
# 资产配置建议报告
报告日期：YYYY年MM月DD日 | 数据源：TDX连接器 + AKShare（国家统计局）+ AKShare新浪

## 一、宏观经济概况
### 中国宏观
### 全球宏观
### 宏观综合判断（六维度 + 周期定位）

## 二、大类资产趋势
[配置权重表 + 置信度评级]

## 三、重点行业分析
### [上升行业] XX
#### 产业链传导
#### 操作建议（A股/港股通/ETF/QDII/债券/商品）
#### 期货期权策略

### [下降行业] XX
（同上结构）

## 四、期货期权综合策略
### 国债期货 / 商品期货 / 股指期货
### 股指期权 / 商品期权 / ETF期权

## 五、风险提示与免责声明
```

保存为 `asset_config_report_{YYYY-MM-DD}.md`。

### 7.3 Excel 报告

使用 openpyxl 创建，包含 8 个 Sheet：

| Sheet名 | 内容 |
|---------|------|
| 宏观概览 | 中国+全球核心指标 |
| 行业分析 | 行业列表、趋势、评级、三维评分 |
| 战略配置 | 四大类资产配置权重+置信度 |
| 债券配置 | 各行业可转债+债券基金 |
| 股票基金 | A股/港股通/QDII/ETF 标的 |
| 商品配置 | 商品品种和基金 |
| 期货期权 | 全部期货期权策略（含止损参考） |
| 风险提示 | 风险因素+免责声明 |

表头加粗+背景色、列宽自适应、数据区域边框、涨红跌绿。

保存为 `asset_config_report_{YYYY-MM-DD}.xlsx`。

### 7.4 输出交付

三份文件保存到工作目录后：
1. 调用 `preview_url` 预览 HTML 报告
2. 调用 `deliver_attachments` 交付 Markdown + Excel
3. 口头总结核心配置建议（3-5句话）

---

## 数据查询优先级

1. **TDX连接器**（17-25ms响应）→ 行业板块、产业链图谱、资金流向、龙虎榜、融资融券、财务报表、研报评级、估值历史、涨停跌停、北向资金、选股器、港股三大表
2. **AKShare 国家统计局源**：宏观数据（PPI/CPI/PMI/GDP/M2/社融/LPR/中美国债利率）— 最稳定
3. **AKShare 新浪源**：全球指数、港股指数、A股指数、期货主力、ETF分类行情 — 稳定补充
4. **WebSearch**：全球宏观补充（DXY/布伦特/黄金/标普/恒生/汇率）、QDII基金列表
5. **option-strategy-advisor**：期权链数据（具体合约参数）

## 数据源可用性速查表

| 数据类型 | 主数据源 | 备用源 | ❌ 不可用 |
|---------|---------|--------|----------|
| PPI/CPI/PMI/GDP | AKShare 国家统计局 | WebSearch | — |
| M2/社融/LPR | AKShare 国家统计局 | WebSearch | — |
| 中美国债利率 | AKShare `bond_zh_us_rate()` | WebSearch | — |
| 人民币汇率 | WebSearch | — | `macro_china_rmb()` TypeError |
| 全球指数 | AKShare 新浪源 | WebSearch | `stock_us_spot_em()` 断连 |
| A股指数 | AKShare 新浪源 | TDX `tdx_quotes` | `stock_zh_a_spot_em()` 断连 |
| **行业板块涨跌** | **TDX `board_cpbd_stage_return`** | AKShare 新浪 | `stock_board_industry_name_em()` 断连 |
| **行业PE/PB/ROE** | **TDX `board_cpbd_basic_info`** | — | 之前无法获取 |
| **行业资金流向** | **TDX `capital_flow`** | — | `stock_sector_fund_flow_rank()` KeyError |
| **行业重要事件** | **TDX `industry_important_events`** | WebSearch | 之前需手动搜索 |
| **行业财务/估值排名** | **TDX `industry_rank`/`valuation_rank`** | — | 之前无法获取 |
| **产业链图谱** | **TDX `industry_chain`** | — | 之前手写文本 |
| **个股行情** | **TDX `tdx_quotes`** | AKShare新浪分时 | `stock_zh_a_spot_em()` 断连 |
| **个股资金流向** | **TDX `capital_flow`** | — | westock-data 未安装 |
| **K线** | **TDX `tdx_kline`** | AKShare新浪 | — |
| **研报评级一致预期** | **TDX `report_rating_consensus`** | — | 之前无法获取 |
| **估值历史分位** | **TDX `valuation_history`** | — | 之前无法获取 |
| **条件选股** | **TDX `tdx_screener`** | — | 之前无法获取 |
| **涨停跌停分析** | **TDX `limit_up/down_analysis`** | — | 之前无法获取 |
| **北向资金** | **TDX `northbound_funds`** | — | 之前无法获取 |
| **龙虎榜** | **TDX `dragon_tiger_list`** | — | westock-data 未安装 |
| **融资融券** | **TDX `margin_trading`** | — | westock-data 未安装 |
| **大宗交易** | **TDX `block_trade`** | — | westock-data 未安装 |
| **港股行情** | **TDX `tdx_quotes` (target=1)** | AKShare 新浪 | `stock_hk_spot_em()` 断连 |
| **港股三大表** | **TDX `hk_income/balance/cashflow`** | — | 之前无法获取 |
| **业绩预警** | **TDX `earnings_warning`** | — | 之前无法获取 |
| **主营构成** | **TDX `business_composition`** | — | 之前无法获取 |
| ETF行情 | AKShare `fund_etf_category_sina()` | TDX `tdx_quotes` | — |
| QDII基金 | WebSearch | — | `fund_qdii_spot_em()` 不存在 |
| 期货主力 | AKShare 新浪源 | — | `futures_foreign_commodity_realtime()` 需参数 |
| 可转债 | AKShare `bond_cb_jsl()` | `bond_cb_summary_sina()` | — |

## Fallback 机制

| 失败场景 | Fallback |
|---------|---------|
| TDX连接器不可用 | **切换到 AKShare 新浪源或 WebSearch**，TDX是行业数据首选但非唯一 |
| AKShare EM接口 RemoteDisconnected | **切换到 TDX连接器或新浪源**，勿重试EM |
| AKShare `macro_china_rmb()` TypeError | WebSearch 查 USD/CNY |
| AKShare 行业数据不可用 | TDX `board_cpbd_*` 系列接口 |
| AKShare QDII 不存在 | WebSearch 查QDII基金列表 |
| AKShare PPI/CPI 与官方不一致 | **以 stats.gov.cn 官方为准**，覆盖 AKShare 返回值 |
| TDX行业代码不确定 | `tdx_lookup_stock query="行业名" range="ZS"` 查确认 |
| TDX港股行情返回异常 | 检查 `target="1"` 和 `setcode="31"` 是否正确 |
| HTML 模板缺失 | 使用 `references/` 中的备用简化模板 |
| openpyxl 未安装 | `pip install openpyxl`，仍失败则仅输出 MD+HTML |

## TDX连接器调用注意事项

1. **setcode 规则**：沪市=1，深市=0，北交所=2，港股=31
2. **港股/美股行情必须 `target="1"`**：默认target="0"只适合A股L1行情
3. **申万行业代码**：881001~881031，用 `tdx_lookup_stock range="ZS"` 确认
4. **板块接口 branch 参数**：001=基础资料，002=详解，003=阶段涨幅，004=市场统计
5. **固定格式 fixedTag**：zjlx=资金流向，jglhb=龙虎榜，dzjy=大宗交易，rzrq=融资融券，ztfx=涨停，dtfx=跌停
6. **资金流向 extra**：数字表示查询天数，如"5"=近5日
7. **代码不带前缀**：TDX用6位纯数字（如"601899"），不带"sh"/"sz"前缀

## 参考文件

- `references/asset_cycle_logic.md`：美林时钟框架+宏观指标数据源映射
- `references/sw_industry_list.md`：申万31行业列表+上下游关联+港股通对标
- `references/futures_options_guide.md`：期货期权策略框架+品种映射
- `assets/report_template.html`：HTML报告模板
- `assets/report_template.md`：Markdown报告模板
- `scripts/fetch_macro.py`：AKShare宏观数据一键拉取脚本
