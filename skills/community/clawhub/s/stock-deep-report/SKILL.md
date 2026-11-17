---
name: stock-deep-report
description: 生成个股三维深度分析单页HTML报告。支持A股、港股、美股，从基本面、新闻面、资金面、技术面、估值、同行对比、股东结构等多个维度进行全面分析，输出精美可打印的HTML报告。触发关键词：三维深度分析、个股分析报告、股票深度报告、生成股票HTML报告、Deep Stock Analysis Report。
display_name: "stock-deep-report"
display_name_zh: "个股深度分析报告生成器"
display_name_en: "Deep Stock Analysis Report Generator"
visibility: "user"
agent_created: true

# ─────────────────────────────────────────────
# Capability & Least-Privilege Declarations
# 严格遵循 MCP 最小权限原则；所有读写限制在 ${cwd} 内，
# 避免 /tmp 硬编码（Windows 不存在）和路径逃逸。
# ─────────────────────────────────────────────
allowed-tools:
  - Read                                           # 读取 JSON / 脚本
  - Write                                          # 写入 stock_data.json / build_json.py
  - Edit                                           # 增量更新 JSON
  - Bash                                           # 仅用于执行 references/build.py
  - WebFetch                                       # 抓取东方财富公开网页
  - WebSearch                                      # 检索近 30 天新闻 / 研报
  - present_files                                  # 最终交付 HTML
file-access:
  scope: workspace                                 # 仅限当前工作目录 ${cwd}
  write:
    - "${cwd}/stock_data.json"                     # 采集后的结构化数据
    - "${cwd}/build_json.py"                       # 分块构建 JSON 的辅助脚本
    - "${cwd}/*_三维深度分析报告_*.html"           # 最终报告
  read:
    - "${cwd}/**"
    - "~/.workbuddy/skills/stock-deep-report/references/build.py"   # 只读渲染脚本
  deny:
    - "/tmp/**"                                    # 明确禁止旧版硬编码路径
    - "/etc/**"
    - "~/.ssh/**"
    - "~/.aws/**"
    - "~/.config/**"
network-access:
  mode: allowlist
  domains:
    - "*.eastmoney.com"
    - "cninfo.com.cn"
subprocess:
  - "python3 ~/.workbuddy/skills/stock-deep-report/references/build.py <input_json> <output_html>"
---

# 个股三维深度分析报告生成器

## 架构说明

**数据采集（AI 做）**：调 API + WebSearch，实时判断和补充缺失数据，输出标准 JSON
**HTML 生成（脚本做）**：`references/build.py` 读取 JSON，用内置模板渲染完整 HTML

> ⚠️ 不要把数据采集写成脚本——API 调用、新闻搜索、情绪判断、同行筛选这些步骤需要 AI 实时决策，脚本做不到。

---

## 概述

根据用户提供的股票名称或代码，自动采集多维度数据，生成一份精美的**单页 HTML 深度分析报告**，可直接用浏览器打开、打印或分享。

报告包含 **17 个主章节（SEC 01–17）**：

| SEC | 章节 | 核心内容 |
|-----|------|---------|
| 01 | 基本面分析 | 营收/净利润/毛利率/ROE/研发费用率，核心指标卡片 |
| 02 | 历年财务指标 | 近3年年度数据表（营收/净利润/毛利率/ROE/EPS） |
| 03 | 新闻面（近30天） | 新闻情绪标注（正面🟢/中性🟡/负面🔴）+ 情绪统计 |
| 04 | 综合评分 | 环形评分（4维度）+ 投资建议 |
| 05 | 资金面分析 | 近5日主力净流入 + 当日资金拆解（超大单/大单/中单/小单） |
| 06 | 技术面（完整指标） | RSI/MACD/MA/布林带/KDJ/量比，含信号标注 |
| 07 | 业务与机构调研 | 产品收入拆分 + 最新机构调研Q&A全文 |
| 08 | 估值与相对表现 | 历史估值通道（PS/PB近1年分位）+ 指数对比(Alpha) |
| 09 | 同行对比 | 同行PE/PB/营收/净利润对比表 |
| 10 | 股东结构 | 前十大股东（持股比例+较上期变动） |
| 11 | 融资融券与北向资金 | 融资余额/融券余量（若适用）+ 北向持股占比/变化趋势 |
| 12 | 分析师评级与一致预期 | 券商评级分布、一致目标价、近期评级变动 |
| 13 | 解禁日历与分红回购 | 限售股解禁时间表、历史分红记录、回购进展 |
| 14 | 大宗交易与龙虎榜 | 近30日大宗交易记录、龙虎榜上榜记录及席位动向 |
| 15 | 风险提示 | 具体风险点 + 非投资建议声明 |
| 16 | 数据来源 | 各维度数据来源说明表 |
| **17** | **🤖 AI 综合点评** | **AI 综合全部信息给出一句话总评、核心逻辑、优势/风险两栏、分类型投资者建议（保守/稳健/进取）、操作策略（买点/目标/止损/仓位）、5大跟踪信号、结语** |

---

## 数据获取方式（2026-07 更新版）

### 首选方式：web_fetch 解析东方财富网页

> ⚠️ **重要**：东方财富 API 可能需要浏览器 cookie 或 IP 白名单，在当前环境中可能不可用。**优先使用 `web_fetch` 工具访问东方财富网页，解析 HTML 表格数据。**

#### 股票代码识别与 URL 构建

**第1步：识别股票代码和市场**

| 代码开头 | 市场 | 行情URL前缀 | 数据URL前缀 |
|---------|------|------------|------------|
| 000-001 | 深圳主板 | sz | sz |
| 002-003 | 深圳中小板 | sz | sz |
| 300-301 | 深圳创业板 | sz | sz |
| 600-601 | 上海主板 | sh | sh |
| 603-605 | 上海主板 | sh | sh |
| 688 | 上海科创板 | sh | sh |
| 430/830-831 | 北交所 | bj | bj |
| 00700 | 港股 | hk | hk |
| AAPL | 美股 | us | us |

**第2步：构建各维度数据 URL**

根据 `eastmoney_guide.md`，以下是经过验证的东方财富 URL 模板：

| 数据维度 | URL 模板 | 说明 |
|---------|---------|------|
| 股票详情页 | `https://quote.eastmoney.com/{market}{code}.html` | 实时行情、估值指标（若返回 302，跟随重定向到 `https://quote.eastmoney.com/unify/cr/{secid}` 的新版页面） |
| 个股资料(F10) | `https://emweb.securities.eastmoney.com/pc_hsf10/pages/index.html?type=web&code={market}{code}` | 公司概况、财务分析、股东研究 |
| 财务分析 | `{F10_URL}#/cwfx` | 利润表、资产负债表、现金流量表 |
| 股东研究 | `{F10_URL}#/gdyj` | 前十大股东、机构持仓 |
| 资金流向 | `https://data.eastmoney.com/zjlx/{code}.html` | 主力资金净流入、超大单/大单/中单/小单 |
| 融资融券 | `https://data.eastmoney.com/rzrq/detail/{code}.html` | 融资余额、融券余量（仅适用于融资融券标的） |
| 沪深港通持股 | `https://data.eastmoney.com/hsgtcg/stock.html?scode={code}` | 北向/南向资金持仓变化（仅适用于沪深港通标的） |
| 公司公告 | `https://data.eastmoney.com/notices/stock/{code}.html` | 近30天公告列表 |
| 个股新闻 | `https://so.eastmoney.com/news/s?keyword={股票名称}` | 近30天新闻 |
| 研究报告 | `https://data.eastmoney.com/report/stock/{code}.html` | 券商研报、分析师评级 |
| 限售股解禁 | `https://data.eastmoney.com/dxljcx/{code}.html` | 解禁时间表 |
| 分红配送 | `https://data.eastmoney.com/dividend/{code}.html` | 历史分红记录 |
| 公司回购 | `https://data.eastmoney.com/bgsj/{code}.html` | 回购进展 |
| 大宗交易 | `https://data.eastmoney.com/bbsj/{code}.html` | 大宗交易记录 |
| 龙虎榜 | `https://data.eastmoney.com/lhb/{code}.html` | 龙虎榜上榜记录、席位买卖 |
| 股权质押 | `https://data.eastmoney.com/gpzy/{code}.html` | 大股东质押情况 |

**第3步：使用 `web_fetch` 获取数据**

```
1. 调用 web_fetch 工具，URL 填入上表中的对应地址
2. 在 prompt 中说明需要提取的数据字段
3. 示例：
   - "提取页面中的实时价格、涨跌幅、成交量、市值、PE、PB"
   - "提取最近5年的营业收入、净利润、毛利率数据"
   - "提取前十大股东名称、持股比例、较上期变动"
```

#### 数据解析注意事项

1. **实时行情数据**：从股票详情页提取，字段包括：最新价、涨跌额、涨跌幅、成交量、成交额、总市值、流通市值、PE、PB、PS
2. **财务数据**：从 F10 财务分析页面提取，注意区分年报、季报
3. **资金流向数据**：从资金流向页面提取，包括主力净流入、超大单、大单、中单、小单
4. **新闻数据**：从新闻搜索页提取，注意标注情绪（正面/中性/负面）
5. **如遇页面动态加载**：等待 2-3 秒让 JS 执行，或查看页面源代码中的 JSON 数据

### 备选方式：API 调用（仅当 web_fetch 不可用时）

> ⚠️ **注意**：以下 API 可能需要在浏览器环境中运行（需要 cookie），如果调用失败，请立即切换到 `web_fetch` 方式。

#### 实时行情 API
```
https://push2.eastmoney.com/api/qt/stock/get?secid={secid}&fields=f43,f44,f45,f46,f47,f48,f57,f58,f162,f163,f167,f168,f169,f170,f171
```
- `{secid}` 格式：沪市/科创板=`1.{代码}`，深市/创业板=`0.{代码}`
- 示例：`1.688620`（安凯微，科创板）

#### K线数据 API（用于计算技术指标）
```
https://push2his.eastmoney.com/api/qt/stock/kline/get?secid={secid}&fields1=f1,f2,f3,f4,f5,f6&fields2=f51,f52,f53,f54,f55,f56,f57,f58&klt=101&fqt=1&beg=20260101&end=20261231&lmt=120
```
- `klt=101`：日K线
- `fqt=1`：前复权
- `lmt=120`：最近120个交易日

#### 资金流向 API
```
https://push2.eastmoney.com/api/qt/stock/fflow/daykline/get?secid={secid}&fields=timestamp,netAmount,netPct,addRate,minusRate,close
```

### 方式三：WebSearch（新闻、研报、分析师观点）

- **WebSearch** — 近30天新闻、公告、研报摘要、分析师评级、专利/技术动态
  - 搜索关键词：`{股票名} 分析报告 site:eastmoney.com OR site:cninfo.com.cn`
  - 分析师评级：`{股票名} 评级 目标价 研报`
  - 专利动态：`{股票名} 专利 技术突破`

### 数据获取优先级

> ⚠️ **实测结论（2026-07 更新）**：东方财富 push2 / push2his API 在 curl 直连时经常返回 403 / 空数据（防爬 + 需要 cookie / IP 白名单）。**web_fetch 是当前最可靠的入口**。

1. **web_fetch 解析东方财富网页** — **首选**。行情、财务、资金流向、股东、解禁、分红、回购、大宗交易、龙虎榜、质押。
2. **WebSearch** — 首选补充。近30天新闻、分析师评级、目标价、研报摘要、专利/技术动态。
3. **API 直接调用** — **仅在已知可访问环境（如带浏览器 cookie / 代理）时尝试**；curl 失败立即降级到 web_fetch。
4. **无法获取** — 该章节标注"暂无数据"，不删除章节标题。

**若 K 线 API 不可用（技术指标降级方案）**：
- 从东方财富行情页可直接读出：最新价 / 52 周高低 / 5日均线 / 20日均线 / RSI 等已展示的指标
- 未直接展示的 MACD / KDJ / BOLL 允许基于近期涨跌节奏做**定性估算**，并在 `tech.*_note` 里注明"估算值"，**不要留空**

### 特殊市场处理

- **科创板股票（688开头）**：
  - 暂不纳入融资融券标的
  - 暂不纳入沪深港通（无北向资金数据）
  - 以上两个维度的数据在 SEC 17（AI 综合点评）中标注"科创板股票暂不纳入"
- **港股、美股**：
  - 部分数据维度（如融资融券、龙虎榜）可能不适用
  - 根据实际市场规则调整数据采集范围

---

## 触发条件

- 用户说"生成/做一份 [股票名] 的深度分析报告"
- 用户说"三维深度分析"、"个股分析报告"
- 用户要求输出 HTML 格式的股票分析
- 用户提到"股票报告"、"深度分析"且要求可视化输出
- 直接输入股票代码（如：688620、00700、AAPL）

---

## 执行流程

### Step 0：解析股票代码与市场

接受以下输入格式：

| 输入示例 | 识别结果 |
|---------|---------|
| `安凯微` / `安凯微(688620)` | A股，secid=`1.688620` |
| `600519` / `贵州茅台` | A股沪市，secid=`1.600519` |
| `00700` / `腾讯控股` | 港股，secid=`116.00700` |
| `AAPL` / `苹果` | 美股，secid=`105.AAPL` |

**代码映射规则**：
- A股沪市（6开头）：secid = `1.{code}`
- A股深市（0/3开头）：secid = `0.{code}`
- A股科创板（688开头）：secid = `1.{code}`
- 港股：secid = `116.{code}`
- 美股纳斯达克：secid = `105.{symbol}`

若用户只提供股票名称，先用东方财富搜索接口解析 secid：
```
https://searchapi.eastmoney.com/api/suggest/get?input={name}&type=14&token=DHASFYDKSVDKNAFE
```

---

### Step 1：采集数据并保存为 JSON

**并行采集以下所有维度**，采集完毕后将数据保存为 JSON 文件（路径：`${cwd}/stock_data.json`，`${cwd}` 表示当前工作目录，避免 `/tmp` 在 Windows 不存在或跨平台不一致的问题）。

#### ⚠️ JSON 写入方式（重要）

完整数据 JSON 体积通常 6-10 KB，包含 20+ 字段。**不要用 Write 工具一次性写入超长 content**——实测超过约 5 KB 时会触发 `file_path expected string, but received undefined` 之类的校验异常。

**推荐做法（分块 Python 脚本）**：
1. 写一个短脚本 `${cwd}/build_json.py`，`d = {}` → 逐块 `d["fin_items"] = [...]` → `d["news"] = [...]` → ... → `json.dump(d, open(f"{CWD}/stock_data.json","w"), ensure_ascii=False, indent=2)`，其中 `CWD = os.getcwd()`
2. 分 2-3 块追加：①stock/quote/fin_items/fin_table ②news/score/flow/tech/products ③survey/valuation/peers/holders/risks/sources/ai_analysis
3. 后续追加块用 `d = json.load(open(f"{CWD}/stock_data.json"))` → 更新字段 → 重新 dump，避免覆盖。

> **路径规范**：**禁止**使用 `/tmp/...` 硬编码。所有中间文件必须落在 `${cwd}`（当前工作目录）之下，以确保跨平台可用（Windows 无 `/tmp`）并把文件访问权限锁定在工作目录内，避免路径逃逸。

**优点**：绕开 Write payload 限制、避开 JSON 转义地雷（双引号/斜杠/emoji）、便于随时补充字段。

#### 数据采集优先级

1. **web_fetch 东方财富网页** — 获取结构化数据（行情、财务、资金流向、股东、解禁、分红、回购、大宗交易、龙虎榜、质押）
2. **WebSearch** — 获取新闻、分析师评级、研报摘要、专利/技术动态
3. **API 调用** — 仅在已知可访问环境中尝试；失败立即降级 web_fetch
4. **计算技术指标** — 从 K 线数据本地计算 RSI、MACD、MA、布林带、KDJ；若 K 线不可得，允许基于行情页展示的均线/RSI + 涨跌节奏做定性估算，`*_note` 中注明"估算值"

#### WebSearch 使用说明

**搜索新闻（近30天）**：
```
query: "{股票名称} 股票 最新消息 2026"
topic: news
```
- 提取新闻标题、日期、URL
- 标注情绪：正面🟢（业绩预增、订单落地、机构调研）/ 中性🟡（日常公告）/ 负面🔴（业绩亏损、高管离职、监管处罚）

**搜索分析师评级**：
```
query: "{股票名称} 分析师评级 目标价 研报"
topic: news
```
- 提取券商名称、评级、目标价、发布日期
- 汇总评级分布（买入/增持/中性/减持/卖出）

**搜索专利/技术动态**：
```
query: "{股票名称} 专利 技术突破 2026"
topic: news
```

#### 数据验证规则

| 字段 | 验证规则 |
|------|---------|
| `price` | 必须为正数，否则标注"数据异常" |
| `change_pct` | 应在 [-15%, +15%] 范围内（正常交易日），否则需核实 |
| `mktcap_y` | 应为数字（单位：元），转换为亿/万亿展示 |
| `rsi` | 应在 [0, 100] 范围内 |
| `pe` | 亏损公司应为 null 或负值 |
| 日期字段 | 应为 YYYY-MM-DD 格式 |

#### 缺失数据处理

- **web_fetch 抓取失败** → 尝试 API（若环境允许） / 换搜索关键词 / 通过 WebSearch 从财经媒体取数
- **数据明显异常** → 二次核实，无法核实则标注"数据待核实"
- **章节无数据** → 显示"暂无数据"提示，保持章节结构完整

---

JSON 格式（嵌套结构，与 `references/build.py` 一致）：

```json
{
  "report_date": "2026-07-03",
  "stock": {
    "name": "安凯微",
    "code": "688620",
    "market": "A股科创板",
    "secid": "1.688620",
    "badge": "科创板 · 半导体 · AI芯片",
    "company": "芜湖安凯微电子技术股份有限公司"
  },
  "quote": {
    "price": 15.67,
    "change_pct": 1.88,
    "change_amt": 0.29,
    "mktcap_y": 3100000000,
    "ps": 11.5,
    "pb": 4.82,
    "low_52w": 10.00,
    "high_52w": 17.45,
    "ytd_pct": 25.63,
    "rsi": 78.71
  },
  "fin_items": [
    {"label": "营业收入 (2026Q1)", "val": "1.50亿", "sub": "同比 +47.2%", "note": "2025年报：5.08亿", "color": "blue"},
    {"label": "归母净利润 (2026Q1)", "val": "-0.12亿", "sub": "", "note": "亏损收窄", "color": "red"},
    {"label": "毛利率 (2026Q1)", "val": "26.8%", "sub": "↑ 修复中", "note": "2025年报：23.94%", "color": "purple"},
    {"label": "研发费率 (2025)", "val": "28.16%", "sub": "行业很高", "note": "研发费用/营收", "color": "amber"},
    {"label": "资产负债率", "val": "12.3%", "sub": "", "note": "财务稳健", "color": "green"},
    {"label": "每股净资产 (BPS)", "val": "3.25元", "sub": "", "note": "PB=4.82x，溢价较高", "color": "blue"}
  ],
  "fin_table": {
    "headers": ["年度", "营收(亿)", "同比", "净利润(亿)", "同比", "毛利率", "ROE", "EPS(元)"],
    "rows": [
      {"cells": ["2024年报", "5.27", "-7.9%", "-0.57", "-311.5%", "18.3%", "-3.8%", "-0.15"]},
      {"cells": ["2025年报", "5.37", "+1.9%", "-1.40", "-147.2%", "13.6%", "-10.3%", "-0.36"]},
      {"cells": ["<b>2026Q1</b>", "<b>1.50</b>", "+47.1%", "-0.20", "+11.2%", "<b>26.8%</b>", "-1.5%", "-0.05"], "highlight": true}
    ],
    "note": "2025年营收同比+1.9%，净利润由-0.57亿扩大至-1.40亿。2026Q1营收同比+47.1%，毛利率修复至26.8%，亏损幅度收窄。",
    "trend": [
      {"icon": "📈", "title": "营收趋势", "color": "green", "text": "2019→2024 营收CAGR ~25%；2026Q1同比+47.1%，修复势头较强。"},
      {"icon": "📉", "title": "净利润趋势", "color": "red", "text": "2022年起持续亏损；2026Q1亏损收窄，拐点待确认。"}
    ]
  },
  "news": [
    {"date": "2026-07-02", "title": "...", "sentiment": "neutral", "tag": "中性"}
  ],
  "news_summary": "近30天情绪总结文字",
  "score": {
    "total": 4.8,
    "label": "观望等待",
    "advice": "建议等待回调至 ¥12~13 区间再关注",
    "items": [
      {"label": "基本面", "score": 5.0, "color": "amber"},
      {"label": "新闻面", "score": 7.0, "color": "green"},
      {"label": "资金面", "score": 3.0, "color": "red"},
      {"label": "技术面", "score": 3.5, "color": "amber"}
    ]
  },
  "flow": {
    "today_net": -1203,
    "bars": [
      {"label": "今日主力净额", "val": -1203, "unit": "万", "sign": "流出"},
      {"label": "今日主力净比", "val": -5.35, "unit": "%", "sign": "流出"}
    ],
    "detail": "📊 近5日主力净流入：<span class='down'>-5717万</span><br>📋 融资融券：暂未纳入标的"
  },
  "tech": {
    "rsi": 78.71,
    "rsi_note": "超买区 (>70)，警惕回调",
    "macd": "0.897 金叉",
    "macd_note": "DIF>DEA，多头信号",
    "kdj": "K=82 D=71 J=95",
    "kdj_note": "K,D已进入高位",
    "boll": {"u": 16.82, "m": 14.31, "l": 11.80, "note": "当前价 15.67，接近上轨"},
    "ma": {"ma5": 15.12, "ma20": 13.29, "note": "价格站上所有均线"},
    "vol_ratio": 1.32,
    "vol_note": "今日成交量略高于近5日均量",
    "alpha_index_name": "科创板指数",
    "alpha": [
      {"days": 3, "stock": 8.2, "index": 3.1, "alpha": 5.1},
      {"days": 5, "stock": 12.4, "index": 4.8, "alpha": 7.6},
      {"days": 10, "stock": 18.9, "index": 6.2, "alpha": 12.7},
      {"days": 20, "stock": 33.96, "index": 9.8, "alpha": 24.2}
    ]
  },
  "products": [
    {"name": "AI SoC芯片（物联网+AI眼镜）", "pct": 55, "color": "blue"},
    {"name": "蓝牙音频芯片", "pct": 25, "color": "purple"},
    {"name": "视觉处理芯片", "pct": 12, "color": "amber"},
    {"name": "思澈SF系列（新）", "pct": 8, "color": "green"}
  ],
  "products_note": "* 收入占比根据2025年报产品分类及调研记录估算，非精确披露",
  "survey": {
    "date": "2026-06-25",
    "orgs": "中信证券、华夏基金、广发基金等38家",
    "qas": [
      {"q": "Q1：AI眼镜芯片的进展如何？", "a": "公司AI眼镜芯片已完成投片，目前处于客户验证阶段，预计2026年Q3有订单落地。"},
      {"q": "Q2：与同行相比，公司芯片的竞争优势？", "a": "..."},
      {"q": "Q3：毛利率的修复节奏？", "a": "..."}
    ]
  },
  "valuation": {
    "ps": 11.5,
    "ps_pct": 85,
    "pb": 4.82,
    "pb_pct": 72,
    "note": "📏 PS=11.5x 处于近1年85%高分位，已反映较多AI预期；PB=4.82x处于72%分位，溢价偏高。"
  },
  "index_alpha": {
    "rows": [
      {"label": "近5日 Alpha", "val": 7.6},
      {"label": "近10日 Alpha", "val": 12.7},
      {"label": "近20日 Alpha", "val": 24.2},
      {"label": "近60日 Alpha", "val": 18.5}
    ],
    "warning": "近20日相对科创指超额收益达24.2%，距30%异动披露阈值仅差约5.8个百分点，需密切关注监管动态。"
  },
  "peers": {
    "headers": ["公司", "代码", "PE(TTM)", "PB", "PS(TTM)", "营收(最近)", "净利润(最近)"],
    "rows": [
      {"cells": ["安凯微", "688620", "亏损", "4.82x", "11.5x", "5.08亿", "-0.50亿"], "highlight": true},
      {"cells": ["全志科技", "300458", "~45x", "~3.8x", "~4.2x", "~18亿", "~1.2亿"]},
      {"cells": ["瑞芯微", "603893", "~55x", "~6.5x", "~8.0x", "~32亿", "~2.8亿"]},
      {"cells": ["晶晨股份", "688099", "~62x", "~4.1x", "~5.5x", "~58亿", "~5.1亿"]}
    ],
    "note": "💡 安凯微PS(11.5x)高于同行均值(~5.9x)，反映市场对其AI芯片转型的高预期；但净利润仍亏损，需持续跟踪盈利拐点。"
  },
  "holders": [
    {"rank": 1, "name": "安凯技术（芜湖）有限公司", "note": "控股股东", "pct": "15.66%", "pct_color": "blue", "chg": "不变", "chg_color": "muted"},
    {"rank": 2, "name": "凯瑞达（芜湖）投资有限公司", "note": "一致行动人", "pct": "7.25%", "pct_color": "blue", "chg": "不变", "chg_color": "muted"},
    {"rank": 3, "name": "Primrose Capital Limited", "note": "外资", "pct": "4.82%", "pct_color": "muted", "chg": "+0.12%", "chg_color": "green"},
    {"rank": 5, "name": "中国建设银行-华夏国证半导体ETF", "pct": "1.87%", "pct_color": "muted", "chg": "-0.35%", "chg_color": "red"}
  ],
  "holders_note": "数据来源：2026年一季报，持仓变化为相较2025年年报",
  "risks": [
    "公司尚未盈利，若AI芯片订单落地不及预期，短期继续亏损概率高",
    "RSI(14)=78.71已进入超买区，技术面回调压力较大",
    "近20日股价相对科创指超额收益+24.2%，接近30%异动披露阈值，需警惕监管风险",
    "PS(TTM)=11.5x处于近1年85%高分位，估值已反映较多AI预期，若预期落空有回调风险",
    "科创板流动性较主板差，大资金进出可能产生较大冲击成本",
    "一致行动协议已于2026-07-02到期，部分股东股份解除限售，关注潜在减持压力"
  ],
  "sources": [
    {"dim": "实时行情/市值/PS/PB", "source": "东方财富 push2 API", "note": "secid=1.688620"},
    {"dim": "年度财务数据", "source": "东方财富 ZYZBAjaxNew API", "note": "emweb.securities.eastmoney.com"},
    {"dim": "主力资金流向", "source": "东方财富 fflow API", "note": "push2.eastmoney.com/api/qt/stock/fflow"},
    {"dim": "K线/技术指标", "source": "东方财富 K线 API + 本地计算", "note": "push2his.eastmoney.com/api/qt/stock/kline/get"},
    {"dim": "近30天新闻情绪", "source": "WebSearch", "note": "关键词：股票名+回购/调研/芯片，近30天"},
    {"dim": "机构调研详情", "source": "同花顺/公司公告", "note": "参与机构、Q&A全文"},
    {"dim": "同行估值对比", "source": "东方财富 API + WebSearch", "note": "PE/PB/PS 来自实时行情"},
    {"dim": "前十大股东", "source": "WebSearch + 公司季报", "note": "2026Q1 一季报"},
    {"dim": "近期公告", "source": "WebSearch + 东方财富公告API", "note": "近30天公告列表"}
  ],
  "ai_analysis": {
    "overview": "一句话总评（可含 <b> 标签）",
    "thesis": "核心投资逻辑，2-4 段，用 <br> 分行",
    "strengths": ["优势1（可含<b>）", "优势2", "优势3", "优势4", "优势5"],
    "weaknesses": ["风险1", "风险2", "风险3", "风险4", "风险5"],
    "advice_by_profile": [
      {"profile": "🛡️ 保守型投资者", "stance": "建议回避", "tone": "red",   "advice": "..."},
      {"profile": "⚖️ 稳健型投资者", "stance": "观望等待", "tone": "amber", "advice": "..."},
      {"profile": "🚀 进取型投资者", "stance": "小仓位跟踪", "tone": "green", "advice": "..."}
    ],
    "action_plan": {
      "ideal_entry": "¥13.0 - 14.0",
      "current_stance": "¥16.62 属高位，追高性价比低",
      "target": "短期 ¥18-19 / 中期 ¥22-25",
      "stop_loss": "破 ¥13 或 Q2 增速跌破 +25%",
      "position": "单只不超过总仓位 5%"
    },
    "triggers": {
      "watch": ["🎯 2026Q2 财报兑现", "🎯 新一代 SoC 发布", "🎯 大客户订单", "⚠️ 解禁减持", "⚠️ 主力资金"]
    },
    "ending": "总结性寄语，包含 <b> 强调标签"
  }
}
```

**关键格式说明**：
- `quote.mktcap_y`：总市值，单位**元**（不是亿）。**换算示例**：`37410000000` → 显示 "374.1 亿"（build.py 内部 ÷1e8）；`3100000000` → "31 亿"。
- `fin_items`：6个核心财务指标卡片，每个有 `label/val/sub/note/color`
- `fin_table.rows[].cells`：表格行文本。**若整行需要强调，用 `highlight: true`** 让 build.py 自动加粗背景色；不要在 cell 内再嵌 `<b>` 造成双重强调（除非只想突出单个字段）
- `fin_table.trend`：趋势分析，2个卡片（营收趋势/净利润趋势）
- `flow.today_net`：今日主力净额，**单位万元**（不是元）
- `flow.bars`：资金面柱状图数据，每个有 `label/val/unit/sign`
- `flow.detail`：资金面详细说明（可包含 HTML 标签）
- `tech.alpha`：相对指数 Alpha 数据，数组，每个有 `days/stock/index/alpha`
- `tech.alpha_index_name`：Alpha 对比的指数名称，根据股票所属市场自动设置：A股主板/创业板用"沪深300"，科创板用"科创板指数"，港股用"恒生科技指数"，美股用"纳斯达克"
- `products`：产品收入拆分，每个有 `name/pct/color`，`pct` 是百分比数字（0-100）
- `survey.qas`：机构调研 Q&A，每个有 `q/a`
- `valuation.ps_pct` / `pb_pct`：近1年分位数（0-100）
- `holders[].pct`：**带百分号的字符串**（如 `"15.66%"`）
- `holders[].pct_color` / `chg_color`：`"blue"`/`"red"`/`"green"`/`"amber"`/`"purple"`/`"muted"`
- `holders[].chg`：**规范为四选一** —— `"不变"` / 带符号数值字符串（`"+0.12%"` / `"-0.35%"`）/ `"新进"` / `"减持"`。避免 `"新进/加仓"` 这类多义值
- `risks`：风险提示数组，每个元素是一段文字
- `sources`：数据来源数组，每个有 `dim/source/note`
- `margin`：**融资融券与北向资金**（SEC 11），结构：
  ```json
  "margin": {
    "is_margin_target": true,           // 是否为融资融券标的
    "is_hk_connect": true,              // 是否为沪深港通标的
    "margin_balance": "12.50亿",        // 最新融资余额（字符串，含单位）
    "margin_balance_chg": "+5.2%",      // 较上期变化
    "margin_trend": "近5日融资余额持续上升，杠杆资金做多意愿强",
    "short_selling": "1200万股",        // 最新融券余量
    "hk_connect_pct": "2.35%",         // 北向资金持股占比
    "hk_connect_chg": "+0.15%",        // 较上期变化
    "hk_connect_trend": "北向资金近30日持续加仓"
  }
  ```
  > 若非融资融券标的：`is_margin_target: false`，函数自动显示"暂非融资融券标的"；科创板/H股类似处理。
- `analyst`：**分析师评级与一致预期**（SEC 12），结构：
  ```json
  "analyst": {
    "rating_count": {"买入": 8, "增持": 3, "中性": 1, "减持": 0},
    "consensus_target": "47.00",        // 一致目标价（字符串，含单位元）
    "target_high": "63.00",
    "target_low": "35.00",
    "recent_ratings": [
      {"date": "2026-04-01", "org": "西南证券", "rating": "买入", "target": "63.00"},
      {"date": "2026-03-15", "org": "中信证券", "rating": "买入", "target": "52.00"}
    ],
    "note": "12家机构一致推荐，目标价区间35-63元"
  }
  ```
- `corporate_actions`：**解禁日历与分红回购**（SEC 13），结构：
  ```json
  "corporate_actions": {
    "lockup": [
      {"date": "2026-10-15", "shares": "1200万股", "pct": "1.5%", "type": "首发原股东限售"}
    ],
    "dividend_history": [
      {"year": "2025", "amount": "10派2.00元", "yield": "0.5%"}
    ],
    "buyback": "截至2026Q1，公司尚未实施回购计划",
    "note": "下一次大规模解禁在2026年10月，关注股东减持压力"
  }
  ```
- `block_lhb`：**大宗交易与龙虎榜**（SEC 14），结构：
  ```json
  "block_lhb": {
    "block_trades": [
      {"date": "2026-06-15", "price": "35.20", "vol": "50万股", "amount": "1760万", "premium": "-1.2%", "buyer": "机构专用"}
    ],
    "lhb_records": [
      {"date": "2026-04-22", "reason": "日涨幅偏离值达7%", "net_buy": "8500万", "main_buyer": "机构专用"}
    ],
    "note": "近30日大宗交易以机构买入为主，龙虎榜上榜2次，机构净买入"
  }
  ```
- `ai_analysis`：**AI 综合点评（SEC 17），可选但强烈推荐生成**
  - `overview`：一句话总评（可含 `<b>` 标签）
  - `thesis`：核心投资逻辑，2-4 段用 `<br>` 分行
  - `strengths[]` / `weaknesses[]`：核心优势/风险列表，各 3-5 条
  - `advice_by_profile[]`：分类型投资者建议数组，每项包含 `profile`（含 emoji 的类型名）/ `stance`（态度标签）/ `tone`（`red`/`amber`/`green`/`blue`）/ `advice`（具体建议）
  - `action_plan`：操作策略，可选字段 `ideal_entry` / `current_stance` / `target` / `stop_loss` / `position`
  - `triggers.watch[]`：后续需关注的信号列表（3-6 条，可用 🎯 / ⚠️ 前缀）
  - `ending`：结语，AI 总结性寄语

> ⚠️ **HTML 转义必读（2026-07 经验教训）**
>
> `build.py` 内部会对所有用户提供的文本字段自动调用 `esc()` 转义 `& < >` 三字符，**避免破坏 HTML 结构**。但**以下内容必须保持原样不被转义**：
>
> | 字段 | 允许的 HTML 标签 | 说明 |
> |------|-----------------|------|
> | `ai_analysis.overview` / `thesis` | `<b>`, `<br>`, `<i>` | AI 加粗强调 |
> | `ai_analysis.advice_by_profile[].advice` | `<b>`, `<br>`, `<i>` | 段落内强调 |
> | `ai_analysis.triggers.watch[]` | `<b>` | 信号强调 |
> | `ai_analysis.ending` | `<b>`, `<br>`, `<i>` | 结语强调 |
> | `fin_table.rows[].cells[]` | `<b>...</b>` | 单 cell 加粗 |
> | `fin_table.trend[].text` | 无（纯文本） | 趋势说明 |
> | `news[].title` | 无 | 新闻标题 |
> | `survey.qas[].q/a` | 无 | 调研问答 |
> | `risks[]` | 无 | 风险文字 |
> | `holders[].name` | 无 | 股东名 |
> | `flow.detail` | `<b>`, `<span class="up/down">`, `<br>` | 资金说明 |
> | `peers.note` | 无 | 同行说明 |
>
> **绝对禁止在文本中直接出现**：
> - 原始的 `<` 或 `>` 符号（如 `MA5<MA20`）→ 会被 `esc()` 转成 `&lt;`，**用户看到的也是字面字符**，不会破坏布局
> - 未配对的 HTML 标签（`<MA20=445>` 这种伪标签）→ 一定要用全角符号 `＜` `＞` 或 `MA5小于MA20` 替代
> - `&` 单独使用（不是 `&amp;`）→ 必须先转义
>
> **AI 写入 JSON 时的规范**：
> - 想加粗用 `<b>xxx</b>`，会被保留
> - 想换行用 `<br>`，会被保留
> - 想表达比较关系：用文字 "MA5 小于 MA20" 或 "MA5<MA20" 中的 `<` 会被转义为 `&lt;`，**这是正确行为**


---

### Step 2：计算综合评分

根据以下维度计算综合评分（满分10分）：

| 维度 | 评分标准 |
|------|---------|
| 基本面 | 营收增速>30% +2；毛利率>30% +1.5；净利润为正 +2；ROE>10% +1.5；研发费用率>15% +1；最高5分 |
| 新闻面 | 正面>负面 +2；机构调研积极 +2；无重大负面 +2；中性偏正面 +1；最高7分（归一化到10分制） |
| 资金面 | 近5日主力净流入 +2；当日主力净比>0 +1.5；超大单净流入 +1.5；融资余额上升 +1；最高5分 |
| 技术面 | RSI<70（非超买）+1.5；MACD金叉 +2；股价在MA20上方 +1.5；量比>1 +1；最高5分 |

**综合评分 = 基本面×0.3 + 新闻面×0.2 + 资金面×0.25 + 技术面×0.25**

投资建议阈值：
- ≥7分：**积极关注**
- 5–7分：**观望等待**
- <5分：**谨慎回避**

将评分结果加入 JSON 的 `score` 字段，重新保存 `${cwd}/stock_data.json`。

---

### Step 2.5：生成 AI 综合点评（`ai_analysis`）

在计算完评分后，基于已采集的**全部维度信息**（基本面、新闻、资金面、技术面、估值、同行、股东、机构调研），生成 SEC 13 的 AI 综合点评。要求：

1. **一句话总评（overview）**：给该股一个精准的"人设"定位，例如"业绩拐点+主题稀缺"、"高股息现金牛"、"衰退期反弹"，风格可有观点、可用 `<b>` 强调
2. **核心逻辑（thesis）**：2-4 段说清楚"这只股票为什么值得（或不值得）当前价格"，用 `<br>` 分行
3. **优势 / 风险各 3-5 条（strengths / weaknesses）**：不要抽象，要引用具体数据（营收 +47%、PS 12x、主力净流出 6240 万等）
4. **分类型建议（advice_by_profile）**：必须给保守型/稳健型/进取型三档，`tone` 用颜色区分，各自给出立场（stance）和具体动作
5. **操作策略（action_plan）**：给出理想买入区间、目标价、止损位、仓位建议
6. **跟踪信号（triggers.watch）**：3-6 条 "需要跟踪什么才能确认/证伪当前判断"
7. **结语（ending）**：站在读者角度，给一段可操作的建议，避免模板式"投资有风险"废话（这句声明由 SEC 11 承担）

写作口吻：**像一位有观点、说人话的资深行研分析师**，避免流水账、避免"综上所述"式官腔。允许在 HTML 文本里使用 `<b>`、`<br>`、emoji。

将结果写入 JSON 的 `ai_analysis` 字段，重新保存 `${cwd}/stock_data.json`。

---

### Step 3：运行 build.py 生成 HTML 报告

**重要：不要直接在对话中输出 HTML 代码，用脚本生成。**

运行 skill 目录下的 `references/build.py`（把 `<cwd>` 换成当前工作目录的绝对路径，跨平台可直接用 `os.getcwd()` 或 shell 变量 `$PWD` / `%CD%`）：

```bash
# Unix / macOS
python3 ~/.workbuddy/skills/stock-deep-report/references/build.py "$PWD/stock_data.json" "$PWD/{code}_{name}_三维深度分析报告_{YYYYMMDD}.html"

# Windows PowerShell
python ~/.workbuddy/skills/stock-deep-report/references/build.py "$PWD\stock_data.json" "$PWD\{code}_{name}_三维深度分析报告_{YYYYMMDD}.html"
```

`build.py` 会：
1. 读取 `${cwd}/stock_data.json`
2. 用内置的完整 HTML 模板（含 CSS）生成报告
3. 输出到指定路径（仍限制在 `${cwd}` 内）

**输出路径格式**：`{工作目录}/{code}_{name}_三维深度分析报告_{YYYYMMDD}.html`

`build.py` 已包含：
- 完整的 CSS 样式（v5 蓝紫精致风，A股涨红跌绿配色）
- 全部 17 个 SEC 章节的 HTML 模板
- CSS 花括号冲突处理（用 `___CSS___` 占位符 + `replace()`）
- 单列堆叠布局，每张卡片独占一行

---

### Step 4：交付报告

1. 用 `present_files` 工具交付 HTML 文件
2. 同时输出一段简短的文字摘要（3–5 行），包括：
   - 综合评分和投资建议
   - 当前价 vs 合理价格区间
   - 最值得关注的风险点（1–2条）
3. 更新工作记忆：记录本次生成的股票代码、报告路径、数据来源

---

## 特殊说明

### A股科创板（688开头）注意事项

- 科创板股票**暂未全部纳入沪股通标的**，北向资金数据可能为空，报告中应标注"暂未纳入沪股通标的"
- 科创板股票若上市未满1年，可能有**限售股解禁**压力，建议搜索 `{股票名} 限售股解禁` 补充提示
- 科创板涨跌幅限制为 **±20%**（区别于主板的±10%）

### 亏损公司估值处理

若 PE(TTM) 为 `null`（亏损），报告中：
- PE 栏标注 `—（亏损）`
- 改用 **PS（市销率）** 进行估值参考
- 合理价格区间基于 PS 历史分位 + 同行 PS 对比得出

### 非投资建议声明（必须包含）

报告最下方（SEC 15）必须包含以下声明：

> ⚠️ **非投资建议声明**
> 本报告数据来源于东方财富、同花顺等公开信息，力求准确但不保证完整性。报告中的评分、价格区间、投资建议等内容仅供参考，不构成任何证券投资建议或投资决策依据。股市有风险，投资需谨慎。

---

## 示例

**用户输入**：
> 帮我生成一份「个股三维深度分析报告」单页 HTML，分析安凯微(688620)。

**执行流程**：
1. 识别 secid = `1.688620`
2. 并行采集所有维度数据，保存为 `${cwd}/stock_data.json`（Step 1）
3. 计算综合评分，更新 JSON（Step 2）
4. 运行 `references/build.py` 生成 HTML（Step 3）
5. 交付文件 + 文字摘要（Step 4）

**输出文件**：
`{工作目录}/688620_安凯微_三维深度分析报告_{日期}.html`

---

## 故障排查

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| CSS 样式不生效，页面全是文字 | CSS 花括号被写成 `{{` `}}` | `build.py` 已用 `___CSS___` 占位符处理，检查 `replace()` 逻辑 |
| HTML 文件不完整，浏览器无法打开 | 脚本被截断 | `build.py` 是独立 `.py` 文件，直接用 Python 运行 |
| 近5日主力净流入为0或异常 | API 返回的是当日数据 | 使用 `push2his.eastmoney.com/api/qt/stock/fflow/daykline/get` |
| 北向资金数据为空 | 股票未纳入沪股通/深港通标的 | 报告中标注"暂未纳入标的"，不显示空数据 |
| 同行对比数据不准确 | 同行选择不当 | 优先选主营业务最相近的上市公司 |
| `build.py` 报错 | JSON 字段缺失 | 检查 `${cwd}/stock_data.json` 是否包含所有必需字段 |
