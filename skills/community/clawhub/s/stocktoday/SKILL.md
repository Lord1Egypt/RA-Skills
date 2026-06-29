---
name: stocktoday
description: A股 / 港股 / 美股 / 基金 / 期货 / 期权 / 债券 / 宏观 数据研究技能. 提供 235+ 个数据接口, 后端走 StockToday 自定义加速 (https://tushare.citydata.club/), 接口命名跟 tushare 100% 兼容. 适用于把"看走势 / 查财报 / 比较公司 / 看板块 / 看资金流 / 梳理公告新闻 / 看宏观 / 拉数据导出"这类请求, 转成可执行的金融数据获取 / 清洗 / 对比 / 筛选 / 导出流程.
author: stocktoday.pro
version: 2.0.2
requirements:
  python: 3.7+
  packages:
    - name: tushare
    - name: pandas
  environment_variables:
    - name: TUSHARE_TOKEN
      required: true
      sensitive: true
      description: 必填, 你的 StockToday API token. 申请地址 https://stocktoday.cn
  network_access: true
---

# stocktoday

StockToday 自有数据研究技能, 提供 235+ 个数据接口, 后端走 StockToday 自定义加速 (`https://tushare.citydata.club/`). 接口命名跟 tushare 100% 兼容, LLM 用标准 tushare 写法即可调用.

## 🚀 首次使用 (必读, 3 步)

> **⚠️ 没有 token 任何接口都返 TOKEN 无效**. 装好 skill 后, **第 1 步**就是配 token.

### Step 1: 申请 token
去 [https://stocktoday.cn](https://stocktoday.cn) 注册账号, 在控制台拿 API token.

### Step 2: 设置环境变量
```bash
# Windows PowerShell
$env:TUSHARE_TOKEN = "your_token_here"

# macOS / Linux
export TUSHARE_TOKEN="your_token_here"
```

### Step 3: 验证
```bash
TUSHARE_TOKEN=your_token python <skill_dir>/scripts/proxy_demo.py
```

5 个 demo 全通 (茅台日线 / 财务指标 / 白酒对比 / 资金流 / 板块) = 装好 ✅.

> LLM 提示: 装好 skill 后, **主动**告诉用户这 3 步. 不要直接 exec 才发现没 token 报错.

```python
import tushare as ts
pro = ts.pro_api("your_token")
pro._DataApi__http_url = "https://tushare.citydata.club/"  # 走 stocktoday gateway
df = pro.daily(ts_code="600519.SH", start_date="20240101", end_date="20241231")
```

> 详见 [scripts/proxy_demo.py](./scripts/proxy_demo.py), 提供 `get_client()` 封装, 一行初始化完成接入.

## ⚡ 客户端初始化 (1 段就够, 别再翻文档)

```python
import sys
sys.path.insert(0, "<skill_dir>/scripts")
from proxy_demo import get_client

pro = get_client("your_token_here")
# 或者从环境变量读:
# export TUSHARE_TOKEN="your_token_here"
# pro = get_client()  # 自动读 env

# 然后跟 tushare 官方用法完全一样
df = pro.daily(ts_code="600519.SH", start_date="20240101", end_date="20241231")
print(df.head())
```

> 💡 小贴士: `TUSHARE_TOKEN` 可以用环境变量, 也可以在调用 `get_client(token=...)` 时显式传. skill 内部**不存储**任何 token, 也不上传到任何第三方, 流量直连 `https://tushare.citydata.club/`.

## 🧭 任务驱动 (从自然语言到接口)

> **核心原则**: 用户说人话时, 先**判断任务类型** → **选推荐接口** → **套默认参数**, 不要从 235 个接口里瞎挑.
> 下方 10 大任务路由覆盖 95% 真实请求.

### 自然语言触发 (这些说法直接进 skill)

- "看下 XX 最近怎么样" / "XX 这段时间涨了多少" / "今年表现" / "最近强不强" → **行情/趋势**
- "看 XX 财报" / "营收趋势" / "ROE 多少" / "现金流好不好" → **财务/估值**
- "对比 XX 和 YY" / "谁更强" / "排个前 10" → **多标的对/排行**
- "最近哪个板块最强" / "半导体行情" / "指数成分" → **板块/指数**
- "北向资金" / "主力流入" / "龙虎榜" → **资金流/情绪**
- "今天涨停" / "连板梯队" / "炸板率" → **打板/情绪**
- "XX 公告" / "新闻" / "最近政策" → **公告/新闻**
- "CPI / PMI / 利率" / "港股美股" → **宏观/跨市场**
- "导出 XX 行情 CSV" / "做回测数据" → **数据导出**
- "快速研究 XX" / "做份简报" → **综合研究**

### 10 大任务路由 (默认接口 + 默认参数)

#### 1. 行情/趋势 → `daily` + `pro_bar` + `daily_basic`
- 默认窗口: "最近" = 近 20 个交易日; "这段时间" = 近 3 个月
- 配套: `daily_basic` 拿 PE/PB/换手率, `adj_factor` 算复权

#### 2. 财务/估值 → `income` + `fina_indicator` + `balancesheet` + `cashflow`
- **不传 `period` 自动取最近季度报告期** (skill 端友好增强)
- 配套: `forecast`/`express` 看业绩预告, `disclosure_date` 看披露计划

#### 3. 多标的对/排行 → `daily_basic` + `fina_indicator` (排序打分)
- 推荐: 选 3-5 个关键指标 (PE / ROE / 营收增速), 用 `fields` 限定
- 配套: 多 `ts_code` 逗号分隔, 一次拉

#### 4. 板块/指数 → `index_daily` + `index_member_all` + `ths_index`/`ths_member`
- ⚠️ **指数代码 (000001.SH / 000300.SH) 不要用 `daily`, 必须用 `index_daily`**
- 分类口径: 行业用 `sw_daily`, 概念用 `ths_index`, 地域用 `dc_index`
- 配套: `ths_hot` / `dc_hot` 看热度榜

#### 5. 资金流/情绪 → `moneyflow` + `moneyflow_hsgt` + `top_list`/`top_inst`
- 口径区分: 北向=沪深港通 / 主力=moneyflow 大单 / 龙虎榜=top_list
- 配套: `moneyflow_ind_dc` 看板块资金, `moneyflow_mkt_dc` 看市场资金

#### 6. 打板/情绪 → `limit_list_d` + `limit_step` + `kpl_list` + `ths_hot`/`dc_hot`
- 默认窗口: 当日 `trade_date=今天`, 涨停梯队看 `limit_step` 的 `nums='2,3,4'`
- 配套: `cyq_perf` 看筹码活跃度

#### 7. 公告/新闻 → `anns_d` + `news` + `major_news` + `npr`
- `anns_d` 必传 `ts_code + start_date + end_date`
- 配套: `research_report` 看券商研报, `irm_qa_sh/sz` 看互动问答

#### 8. 宏观/跨市场 → `cn_cpi/ppi/pmi/m` + `us_tycr` + `hk_daily` + `us_daily`
- 配套: `shibor` / `shibor_lpr` 看利率

#### 9. 数据导出 → `daily` + `pro_bar` + `fina_indicator` (按 ts_code+日期范围)
- 长区间分段拉: 日线按年/季度切, 财报按年切, 分钟按月切
- 输出 CSV / parquet, 命名格式: `daily_600519.SH_20240101_20241231_20260620.csv`

#### 10. 综合研究简报 → 组合调 1+2+5+7
- 一句话结论 → 行情 → 财务 → 资金流 → 公告 → 风险点
- 配套: `token_info` 自查权限 (高级接口需要 V2+)

### ⭐ 29 个核心接口 (覆盖 80% 任务)

> 优先从这 29 个里选, 其它 200+ 接口按需翻 `references/数据接口.md`.

| 分类 | 接口 |
|---|---|
| 基础 | `stock_basic`, `trade_cal`, `token_info` |
| 行情 | `daily`, `pro_bar`, `daily_basic`, `adj_factor` |
| 财务 | `income`, `balancesheet`, `cashflow`, `fina_indicator`, `forecast`, `express` |
| 资金/情绪 | `moneyflow`, `moneyflow_hsgt`, `hsgt_top10`, `top_list`, `top_inst` |
| 指数/板块 | `index_daily`, `index_basic`, `sw_daily`, `ths_index`, `ths_member` |
| 打板 | `limit_list_d`, `limit_step`, `ths_hot`, `dc_hot` |
| 公告/宏观 | `anns_d`, `news`, `cn_cpi`, `us_tycr` |

### 🎯 中文自然语言默认口径

| 用户说 | 解释为 |
|---|---|
| "最近 / 这段时间" | 近 20 个交易日 |
| "今年 / 今年以来" | 1 月 1 日至今 |
| "财报 / 业绩" | 最近 8 个季度 + 最近年度 |
| "强不强" | 走势 + 相对强弱 + 活跃度 |
| "资金关注" | 净流入 + 活跃成交 + 龙虎榜/北向 |
| "估值" | PE / PB / 股息率 |
| "对比 / 排前 10" | 选 3-5 个关键指标排序 |

## 📤 交付规范 (Output Contract)

> **核心原则**: 用户没明说只要原始表, 就要按"先结论 → 再数据 → 后风险"的方式给, 不要直接吐 pandas DataFrame.

### 5 段式输出 (默认结构)

每次给结果, 严格按这 5 段:

1. **一句话结论** — 用一句话回答用户的核心问题 (涨跌 / 估值高低 / 资金方向 / 风险点)
2. **数据范围与口径** — 标的代码 / 时间窗口 / 数据源 / 是否包含复权 / 是否含交易日历过滤
3. **关键指标 / 关键表格** — 3-7 个最关键数字, 或对比表 (PE/ROE/涨跌幅/净流入), 不要全字段 dump
4. **异常点 / 风险点 / 解释限制** — 数据缺失原因 / 非交易日 / 接口权限 / 单日噪声 / 字段含义
5. **本地输出 (如有)** — CSV / parquet 路径, 方便用户回看

### 4 种交付形态 (按任务复杂度选)

| 复杂度 | 形态 | 适用 |
|---|---|---|
| 小 | Markdown 摘要 + 简短表格 | 1-2 个标的关键指标查询 |
| 中 | Markdown 摘要 + CSV (5-1000 行) | 多标的对比, 区间数据, 财报趋势 |
| 大 | Markdown 摘要 + Parquet (1000+ 行) | 多年日线, 分钟数据, 全市场扫描 |
| 流程化 | 附 Python 脚本 | 客户要"可复用流程", 或要回测/二次分析 |

### 元信息 (生成文件时必带)

- 接口名 (e.g. `daily`)
- 请求参数 (e.g. `ts_code=600519.SH, start_date=20240101, end_date=20241231`)
- 拉取时间 (UTC+8)
- 数据行数
- 字段列表
- 是否存在缺失 / 失败分段

### 按任务类型的输出模板

#### 行情/趋势任务 (单只)
```
📌 结论: 茅台 2024 年累计下跌 8.5%, 跑输沪深 300 (涨 14.7%)
📊 范围: 600519.SH / 2024-01-02 ~ 2024-12-31 / 复权(qfq) / 共 243 个交易日
📈 关键:
  - 年初: 1715 元 → 年末: 1569 元 (复权后)
  - 区间最大回撤: -23.4% (5-7 月)
  - 平均换手率: 0.32%
⚠️ 注意: 6-7 月震荡下行, 9-10 月企稳反弹; 数据按 2026-06-20 拉取
```

#### 财务/估值任务 (单只)
```
📌 结论: 茅台 2025Q3 ROE 24.1% (行业头部), PE 23x (略高于近 5 年中位 20x)
📊 范围: 600519.SH / 8 季度 2023Q4-2025Q3 + 2024 年报
💰 关键 (单位: 亿元):
  | 指标       | 2024A   | 2025Q3  | 同比   |
  |------------|---------|---------|--------|
  | 营收       | 1738    | 1285    | +15%   |
  | 归母净利   | 862     | 638     | +13%   |
  | ROE        | 26.5%   | 24.1%   | -2.4pp |
  | 毛利率     | 91.8%   | 91.3%   | -0.5pp|
⚠️ 风险: 增速放缓但盈利质量仍优; PE 偏高需关注估值消化
```

#### 多标的对/排行
```
📌 结论: 3 只白酒中, 茅台综合最强 (ROE 24%, 毛利率 91%); 泸州老窖增速最快
📊 范围: 600519.SH / 000858.SZ / 000568.SZ / 2024 年报
📊 对比表:
  | 指标     | 茅台     | 五粮液   | 泸州老窖 |
  |----------|----------|----------|----------|
  | ROE      | 26.5%    | 22.1%    | 24.8%    |
  | 毛利率   | 91.8%    | 75.3%    | 87.5%    |
  | 营收增速 | 15.7%    | 8.4%     | 22.6%    |
  | PE       | 23x      | 18x      | 20x      |
```

#### 资金流任务
```
📌 结论: 茅台 6/18 主力净流出 2.3 亿 (大单), 但北向净买入 1.1 亿
📊 范围: 600519.SH / 2026-06-18
💰 关键:
  - 主力净流入: -2.3 亿 (大单 -1.8 / 特大单 -0.5)
  - 北向净买入: +1.1 亿
  - 涨跌: -0.42%
⚠️ 解读: 主力减仓但北向接盘, 信号矛盾需看后续 1-2 日确认
```

#### 板块/打板任务
```
📌 结论: 6/18 涨停 47 只 (连板 12 只), 半导体板块最热 (涨停 8 只)
📊 范围: 全市场 / 2026-06-18
🔥 板块强度: 半导体 +5.2% / 新能源车 +3.8% / AI +3.1%
📊 连板梯队: 6 板 1 只 / 5 板 2 只 / 4 板 3 只
⚠️ 风险: 涨停炸板率 18% (偏高), 明日分歧概率大
```

#### 公告/新闻任务
```
📌 结论: 寒武纪 6/18 公告 3 条, 核心是定增预案修订 (募资 50 亿)
📊 范围: 688256.SH / 近 30 日 / anns_d + news
📰 关键:
  - 6/18: 定增预案修订 (募资 50 亿, 用于 AI 芯片研发)
  - 6/15: 5 月经营数据公告
  - 6/10: 投资者关系活动记录
⚠️ 注意: 定增属利好但稀释 EPS, 关注发行价折扣
```

### ⚠️ 不要做的 5 件事

1. **不要直接吐 pandas DataFrame** — 用户看不懂, 至少要前 3 行 + 摘要
2. **不要忘记标"非交易日"** — 周末/节假日返空要在异常点说明
3. **不要用绝对收益承诺** — "必涨 20%" 这种话别说, 数据只描述历史
4. **不要漏单位** — 金额"亿/万"、涨跌幅"%"、换手率"%", 必须标
5. **不要把单日信号当趋势** — 资金流单日 1 天噪声, 至少看 5 日才稳

## 🎯 实战示例 (新手必看)

### 1. 单只股票最近的行情

```python
import sys
sys.path.insert(0, "<skill_dir>/scripts")
from proxy_demo import get_client

pro = get_client("your_token_here")
df = pro.daily(ts_code="600519.SH", trade_date="20260618")
print(df)
```

### 2. 查 1 只股票一段时间的行情

```python
df = pro.daily(ts_code="600519.SH", start_date="20260601", end_date="20260618")
# 或用 pro_bar 拿复权
df = pro.pro_bar(ts_code="600519.SH", start_date="20260601", end_date="20260618", adj="qfq")
```

### 3. 查 1 只股票最新财务数据

```python
# 利润表 (不传 period 自动取最近季度报告期)
df = pro.income(ts_code="600519.SH", period="20251231")
# period: 报告期末 (年报=1231, 半年报=0630, 一季报=0331, 三季报=0930)
```

### 4. 同时查 1 只股票的 3 张报表

```python
ts_code = "000001.SZ"
period = "20251231"
income = pro.income(ts_code=ts_code, period=period)
balance = pro.balancesheet(ts_code=ts_code, period=period)
cashflow = pro.cashflow(ts_code=ts_code, period=period)
ratios = pro.fina_indicator(ts_code=ts_code, period=period)
```

### 5. 查龙虎榜

```python
# 6/18 上交所龙虎榜
df = pro.top_list(trade_date="20260618")
# 或加 ts_code 看单只上榜详情
df = pro.top_list(trade_date="20260618", ts_code="600519.SH")
# 机构席位
df = pro.top_inst(trade_date="20260618", ts_code="600519.SH")
```

### 6. 查 1 只股票的资金流向

```python
# 平安银行 6/18 主力资金
df = pro.moneyflow(ts_code="000001.SZ", trade_date="20260618")
# 字段: net_mf_vol/net_mf_amount 主力净流, buy_lg/sell_lg 大单, buy_elg/sell_elg 特大单
```

### 7. 查北向资金 / 沪深港通

```python
# 6/18 北向买了多少
df = pro.moneyflow_hsgt(trade_date="20260618")
# 字段: hgt 沪股通, sgt 深股通, north_money 北向合计
# 沪市北向前 10
df = pro.hsgt_top10(trade_date="20260618", market_type="1")
```

### 8. 查指数 (注意: 指数代码用 `index_daily`, 不要用 `daily`)

```python
# 上证指数 6/18
df = pro.index_daily(ts_code="000001.SH", trade_date="20260618")
# 沪深 300
df = pro.index_daily(ts_code="000300.SH", trade_date="20260618")
# 创业板指
df = pro.index_daily(ts_code="399006.SZ", trade_date="20260618")
```

### 9. 综合研究 (调 5+ 个接口)

```python
ts_code = "600519.SH"
period = "20251231"

# 1. 行情
quote = pro.daily(ts_code=ts_code, start_date="20250101", end_date="20251231")
# 2. 财务 3 表 + 指标
income = pro.income(ts_code=ts_code, period=period)
balance = pro.balancesheet(ts_code=ts_code, period=period)
cashflow = pro.cashflow(ts_code=ts_code, period=period)
ratios = pro.fina_indicator(ts_code=ts_code, period=period)
# 3. 资金流
money = pro.moneyflow(ts_code=ts_code, trade_date="20260618")
# 4. 公告
ann = pro.anns_d(ts_code=ts_code, start_date="20260101", end_date="20260618")
```

## 📅 数据时间规则

| 场景 | 数据可用性 | 备注 |
|------|------------|------|
| 行情 (日线) | T+1 18:00 后 | 当天数据当晚 6 点后可用 |
| 行情 (分钟) | 实时 | 盘中每分钟更新 |
| 实时 Tick | 实时 | 盘中每 3 秒 |
| 财务 (季报) | 公告日 | 4/30 一季报, 8/30 半年报, 10/30 三季报, 4/30 年报 |
| 财务 (年报) | 4/30 前 | 1/1-4/30 是年报披露季 |
| 业绩预告 | 季报前后 | 1/15, 4/15, 7/15, 10/15 前后集中 |
| 龙虎榜 | T+1 18:00 后 | 盘后公布 |
| 限流阈值 | 100/分钟 | (perMin=100) |

**重要**: 周末/节假日调接口会返空,这是**正常**,不是接口坏。

## 🚨 错误排查速查

| 现象 | 原因 | 解决 |
|------|------|------|
| `TOKEN无效` | token 错/过期 | 调 `token_info(token=自己)` 看状态 |
| `参数不能为空` | 必填参数没传 | 看 schema 里的 `required: true` |
| `您的IP因异常请求已被临时封禁` | 5 分钟内 5+ 次 IP_KEY 错 | 改对 token,等 5h |
| `单次查询数据量不可超过 10000 条` | 数据范围太大 | 缩 start_date~end_date |
| 返空 `[]` | 节假日/未发数据/股票不存在 | 调 `trade_cal` 确认日期 |
| `HTTP 400` (stock_hsgt) | 缺 ts_code | 传 ts_code 或 trade_date |
| `data: null` (fut/hk 接口) | 合约/港股代码错 | 检查后缀 (.SHF/.HK) |
| `pro.daily(ts_code='000001.SH')` 返空 | 指数代码不能用 daily | 改用 `pro.index_daily(ts_code='000001.SH')` |

## 🔑 Token 4 种类型

调 `token_info(token=自己)` 自动检测自己属于哪一档:

| 类型 | 适用 | 特征 |
|------|------|------|
| V0 免费 | 注册即得 | 只 6 个基础接口,需要 plugin 解锁 |
| V1 基础 | 旗舰积分 | 193 个基础接口 (无实时) |
| V2 高级 | 龙虾套餐 | 全部 193+48 = 241 个 |
| V3/V4 高级 | 大客户 | 同 V2 |

接口分 2 档:
- **基础档** (193 个): daily/income/top_list/stock_basic/...
- **实时档** (48 个): rt_k/rt_tick/rt_min/cb_price_chg/anns_d/news/...

## 🛠️ 工具列表 (按分类)

> 完整 235 个工具,按 23 个分类列出。**所有 schema 含 `type` / `required` / `pattern` / `enum` / `default`**, 详见 [references/数据接口.md](./references/数据接口.md).

### 股票-基础数据 (18)
| 工具 | 说明 |
|---|---|
| `stock_basic` | **查股票列表**: list_status='L' 上市 / 'D' 退市 / 'P' 暂停 |
| `stk_premarket` | 新股上市 |
| `trade_cal` | **交易日历**: is_open='1' 交易日 / '0' 休市, 节假日调这个 |
| `stock_st` | ST 股票列表 (需 trade_date) |
| `namechange` | 股票名称变更 |
| `stock_company` | 上市公司信息 (1 只: ts_code) |
| `stk_managers` | 公司管理层 |
| `stk_rewards` | 高管薪酬 |
| `new_share` | 新股发行 (需 start_date) |
| `bak_basic` | 备用基础数据 |
| `bse_mapping` | 北交所新旧代码对照 |
| `stock_hsgt` | 沪深港通股票列表 (需 ts_code 或 trade_date) |
| ... | 还有 6 个,见 references/数据接口.md |

### 股票-行情数据 (21)
| 工具 | 说明 | 必填 |
|---|---|---|
| `daily` | 日线行情 | ts_code + (trade_date \| start_date+end_date) |
| `weekly` | 周线行情 | 同上 |
| `monthly` | 月线行情 | 同上 |
| `pro_bar` | 行情(支持复权) | ts_code + start_date + end_date, **adj** 可选 qfq/hfq/none, **freq** D/W/M |
| `stk_weekly_monthly` | 周月线行情 (高频首选) | ts_code + freq='W' 或 'M' |
| `stk_week_month_adj` | 周月线复权 | 同上 |
| `adj_factor` | 复权因子 | ts_code + start_date + end_date |
| `daily_basic` | 每日指标 (PE/PB/换手率) | ts_code + trade_date |
| `stk_limit` | 涨跌停价格 | ts_code + trade_date |
| `suspend_d` | 停复牌 | ts_code + start_date + end_date |
| `hsgt_top10` | 沪/深股通前 10 | trade_date + market_type (1=沪/3=深) |
| `ggt_top10` | 港股通前 10 | trade_date + market_type (2=沪/4=深) |
| `ggt_daily` | 港股通每日 | trade_date |
| `ggt_monthly` | 港股通每月 | trade_date |
| `bak_daily` | 备用每日行情 | trade_date |
| `stk_mins` | 股票历史分钟 | ts_code + freq='1min'~'60min' **小写** |
| `idx_mins` | 指数历史分钟 (必传 ts_code + freq) | ts_code + freq |
| ... | 还有 4 个,见 references/数据接口.md |

### 股票-财务数据 (17)
| 工具 | 说明 | 必填 |
|---|---|---|
| `income` | 利润表 | **ts_code** + 可选 period/ann_date |
| `balancesheet` | 资产负债表 | 同上 |
| `cashflow` | 现金流量表 | 同上 |
| `forecast` | 业绩预告 | ts_code 或 ann_date |
| `express` | 业绩快报 | ts_code 或 ann_date |
| `dividend` | 分红送股 | ts_code |
| `fina_indicator` | **财务指标** (ROE/EPS/PE/PB) | ts_code + 可选 period |
| `fina_audit` | 财务审计 | ts_code + period |
| `fina_mainbz` | 主营业务 | ts_code + period + type (P=产品/D=地区) |
| `disclosure_date` | 披露日期 | ts_code + end_date |
| `income_vip` | VIP 利润表 | ts_code + period |
| `balancesheet_vip` | VIP 资产负债表 | ts_code + period |
| `cashflow_vip` | VIP 现金流量表 | ts_code + period |
| `fina_indicator_vip` | VIP 财务指标 | ts_code + period |
| `express_vip` | VIP 业绩快报 | ts_code + period |
| `forecast_vip` | VIP 业绩预告 | ts_code + period |
| `fina_mainbz_vip` | VIP 主营业务 | ts_code + period + type |

### 资金流向 (8)
| 工具 | 说明 |
|---|---|
| `moneyflow` | 股票资金流向 (ts_code + trade_date) |
| `moneyflow_hsgt` | **沪深港通北向** (trade_date) |
| `moneyflow_ths` | 同花顺资金流 (ts_code + trade_date) |
| `moneyflow_dc` | 东方财富资金流 (ts_code + trade_date) |
| `moneyflow_ind_ths` | 同花顺行业资金流 (trade_date) |
| `moneyflow_ind_dc` | 东方财富行业资金流 (trade_date) |
| `moneyflow_mkt_dc` | 东方财富市场资金流 (trade_date) |
| `moneyflow_cnt_ths` | 同花顺概念资金流 (trade_date) |

### 指数数据 (22)
| 工具 | 说明 |
|---|---|
| `index_basic` | 指数基本信息 (market='SSE'/'SZSE'/'BSE') |
| `index_daily` | **指数日线** (ts_code) - 指数代码必须用这个, 不要用 `daily` |
| `index_weekly` | 指数周线 |
| `index_monthly` | 指数月线 |
| `index_weight` | 指数成分股权重 (index_code + trade_date) |
| `index_dailybasic` | 指数每日指标 (PE/PB/换手率) |
| `index_classify` | 指数分类 |
| `index_member_all` | 指数成分股 |
| `ci_daily` | 中证指数日线 |
| `sw_daily` | 申万指数日线 |
| `idx_factor_pro` | 指数因子 (PE/PB/动量) |
| ... | 还有 11 个,见 references/数据接口.md |

### 打板专题 (16)
| 工具 | 说明 |
|---|---|
| `ths_index` | 同花顺概念/行业/地域指数 |
| `ths_daily` | 同花顺指数日线 (ts_code + trade_date) |
| `ths_member` | 同花顺成分股 (ts_code) |
| `ths_hot` | 同花顺热榜 (trade_date) |
| `dc_index` | 东财指数 (idx_type 必填) |
| `dc_daily` | 东财指数日线 |
| `dc_member` | 东财成分股 (trade_date) |
| `dc_hot` | 东财热榜 (trade_date) |
| `kpl_list` | 开盘啦榜单 (trade_date) |
| `kpl_concept` | 开盘啦概念 (trade_date) |
| `kpl_concept_cons` | 开盘啦概念成分 (trade_date) |
| `limit_list_d` | 涨跌停明细 (trade_date) |
| `limit_list_ths` | 同花顺涨跌停榜单 (trade_date) |
| `limit_step` | 涨停连板天梯 (trade_date, 可选 nums='2,3') |
| `limit_cpt_list` | 涨停最强板块 (trade_date) |
| `hm_detail` | 游资详情 (trade_date) |

### 实时数据 (13, 需实时档 token)
| 工具 | 说明 |
|---|---|
| `rt_k` | 股票实时日线 (ts_code 通配符 `6*.SH`) |
| `rt_tick` | 股票实时 Tick (只返回最后一条) |
| `rt_min` | 股票实时分钟 (ts_code + freq='1MIN'/'5MIN'... **大写**) |
| `rt_idx_k` / `rt_idx_min` / `rt_idx_tick` | 指数实时 |
| `rt_etf_k` / `rt_etf_tick` | ETF 实时 |
| `rt_fut_min` | 期货实时分钟 |
| `rt_hk_k` / `rt_hk_tick` | 港股实时 |

### 港股 (9) / 美股 (9)
| 工具 | 说明 |
|---|---|
| `hk_basic` / `hk_daily` | 港股基本信息/日线 (代码 `00700.HK`) |
| `hk_income` / `hk_balancesheet` / `hk_cashflow` | 港股三大财务报表 (period='20251231') |
| `us_basic` / `us_daily` | 美股基本信息/日线 (代码纯 ticker, e.g. 'AAPL', **不带** .US) |
| `us_income` / `us_balancesheet` / `us_cashflow` / `us_fina_indicator` | 美股财务 |

### 基金 (13) / 期货 (10) / 期权 (2) / 可转债 (7) / 债券 (6)
- 基金: `fund_basic` / `fund_nav` / `fund_daily` / `fund_portfolio` / `etf_basic` / ...
- 期货: `fut_basic` (exchange='DCE'/'CZSE'/'CFFEX'/'SHFE'/'INE'/'GFEX') / `fut_daily` (ts_code='CU2507.SHF' 铜 2507) / ...
- 期权: `opt_basic` / `opt_daily`
- 可转债: `cb_basic` / `cb_daily` / `cb_issue` / `cb_call` / `cb_rate` / `cb_share` / `cb_price_chg`
- 债券: `repo_daily` / `bc_otcqt` / `bc_bestotcqt` / `bond_blk` / `bond_blk_detail` / `yc_cb`

### 宏观经济 (17) / 资讯 / 其他
- 宏观: `cn_cpi` (m='202401') / `cn_gdp` (q='2024Q1') / `cn_pmi` / `cn_m` / `cn_ppi` / `shibor` / `shibor_lpr` / `us_tycr` / `hibor` / `libor` / `us_tbr` / ...
- 资讯: `news` (start_date + end_date, src='cls'/'sina'/'ths'/'eastmoney') / `major_news` / `cctv_news` / `npr` / `anns_d` / `research_report`
- 用户自查: `token_info` (必调用, 看 token 状态/可用接口)
- 其他: `tmt_twincome` / `film_record` / `teleplay_record` / `bo_daily` / `bo_weekly` / `bo_monthly` / `bo_cinema` / `irm_qa_sh` / `irm_qa_sz`

## ⚙️ 高级配置 (env vars)

| 环境变量 | 默认 | 说明 |
|---|---|---|
| `TUSHARE_TOKEN` | (无) | **必填**, 你的 API token |
| `TUSHARE_GATEWAY` | `https://tushare.citydata.club/` | 自定义后端地址 |
| `TUSHARE_GATEWAY_BACKUP1` | `http://111.229.164.2:8083/` | 备用 gateway 1 |
| `TUSHARE_GATEWAY_BACKUP2` | `http://124.223.112.152:6331/` | 备用 gateway 2 |
| `TUSHARE_GATEWAY_BACKUP3` | `http://110.42.211.9:9900/` | 备用 gateway 3 |

## 🆘 故障排查

| 症状 | 原因 | 解决 |
|---|---|---|
| `ImportError: No module named 'tushare'` | 依赖没装 | `pip install tushare pandas` |
| `TOKEN无效` | token 错/失效/被封 | 调 `token_info` 自查 |
| 调工具超时 | 网络问题 / gateway 全挂 | 检查 `tushare.citydata.club` 通不通 |
| 频繁返 `请求超限20000次` | token 当日额度用完 | 明日 0 点重置, 或换 token |
| 问"今天"返空 | 今天休市 (周末/节假日) | 改问"最近一个交易日" |
| `pro.daily(ts_code='000001.SH')` 返空 | 指数代码不能用 daily | 改用 `pro.index_daily(ts_code='000001.SH')` |

## 📞 反馈

- ClawHub: `stocktoday-py` skill 页面
- 项目目录: `D:\office\stocktoday-data\`
- 完整接口文档: [references/数据接口.md](./references/数据接口.md)
- 实战示例: [scripts/proxy_demo.py](./scripts/proxy_demo.py), [scripts/finance_demo.py](./scripts/finance_demo.py), [scripts/sector_demo.py](./scripts/sector_demo.py)

## License

MIT
