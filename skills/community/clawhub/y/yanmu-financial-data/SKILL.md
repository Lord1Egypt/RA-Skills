---
name: yanmu-financial-data
description: 股票研究专家研木的Skill — 采集目标公司及可比公司的核心财务数据
---

# 研木 · 金融数据采集 (yanmu-financial-data)

## 功能
根据用户选择的股票，采集目标公司及可比公司的核心财务数据，包括：
- 营收、净利润、NOPAT、净利率/毛利率
- 资本开支(Capex)、营运资本变动(NWC)
- 自由现金流(FCF)
- 总股本、市值
- PE/PB/ROE等估值指标
- 分析师一致预期

## 市场覆盖

| 市场 | 支持标的 | 实时行情来源 | API示例 |
|------|---------|------------|---------|
| 🇨🇳 **A股** | 600519(茅台)、300750(宁德)、002594(比亚迪)等10支 | **新浪财经** | `hq.sinajs.cn/list=sh600519` → 字段[3] |
| 🇭🇰 **港股** | 00700(腾讯控股) | **新浪财经 rt_hk** | `hq.sinajs.cn/list=rt_hk00700` → 字段[6] |
| 🇺🇸 **美股** | NVDA(NVIDIA) | **新浪财经 gb_** | `hq.sinajs.cn/list=gb_nvda` → 字段[1] |

> 每次运行时自动从新浪财经API获取最新股价，覆盖内置硬编码价格。
> 采集失败时回退到内置数据库的静态数据（课程演示用）。

## 数据源（按优先级）
| 市场 | 第一优先级 | 回退方案 |
|------|-----------|---------|
| A股 | 新浪财经 `hq.sinajs.cn/list=sh/sz` | 静态数据库 |
| 港股 | 新浪财经 `hq.sinajs.cn/list=rt_hk` | 静态数据库 |
| 美股 | 新浪财经 `hq.sinajs.cn/list=gb_`（代码需全小写） | 静态数据库 |

## 工作流程

### 1. 获取数据
```bash
python3 {baseDir}/scripts/fetch_financial_data.py \
  --ticker <股票代码> \
  --market <a-share|hk|us> \
  --comps <可比公司代码1,可比公司代码2,...> \
  --output <json|text>
```

### 2. 实时行情覆盖
脚本内置 `fetch_live_price()` 函数，流程如下：
```
用户输入 → 加载数据库 → 请求新浪API(5秒超时) → 成功则用实时价覆盖 → 失败则用数据库价
```
- A股: `sh600519` / `sz300750` → 字段[3]为当前价
- 港股: `rt_hk00700` → 字段[6]为当前价
- 美股: `gb_nvda` → 字段[1]为当前价（代码必须小写）

### 3. 联动更新
获取实时股价后自动联动更新：
- `market_cap`（市值）= `current_price × shares_outstanding`
- `pe_ttm`（市盈率）= `current_price ÷ last_eps`

### 4. 输出内容
输出格式（JSON）：
```json
{
  "target": {
    "name": "公司名",
    "market": "a-share|hk|us",
    "current_price": "实时股价",
    "market_cap": "实时市值",
    "history": {"2023": {...}, "2024": {...}, "2025": {...}},
    "estimates": {"2026E": {...}, "2027E": {...}, "2028E": {...}},
    "valuation": {"pe_ttm": "...", "pb": "...", ...}
  },
  "comps": {"代码": {...}, ...}
}
```

## 注意事项
- 港股和A股的财报周期不同，需注意数据对齐
- 美股代码必须**小写**（新浪API要求），如 `nvda` 而非 `NVDA`
- 非交易时段返回最近收盘价，数据仍然有效
- 部分数据需要估算（如NOPAT = EBIT × (1-税率)）
- 可比公司仅支持已经内置在数据库中的标的
