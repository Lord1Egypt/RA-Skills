---
name: stock-watchlist
description: Query real-time stock prices, basic quote fields, and manage a Markdown watchlist for A-share, Hong Kong, and US stocks. Use when users ask in Chinese or by ticker/code to search stocks, inspect current price and quote basics, or maintain a watchlist stored in a Markdown file.
---

# stock-watchlist

## 概览

这个 Skill 用于处理三类任务：

1. 按中文名、代码或带市场前缀的符号查询股票。
2. 返回实时价格和常用基础字段，例如涨跌幅、开高低、昨收、市值、PE、PB、换手率。
3. 用 Markdown 文档维护自选列表，并按持仓成本和数量汇总盈亏。

当前脚本使用公开可访问的东财搜索与行情接口。这样可以稳定支持“中文名检索 + 实时行情”，避免当前公开雪球搜索接口的风控限制。

## 工作流

### 1. 单只或多只股票查询

优先调用 `scripts/stock_watchlist.py quote ...`。

支持这些输入形态：

1. 中文名，例如 `贵州茅台`、`腾讯`。
2. 裸代码，例如 `600519`、`00700`、`TSLA`。
3. 带前缀代码，例如 `SH600519`、`SZ000001`、`HK00700`。

示例：

```bash
python scripts/stock_watchlist.py quote 贵州茅台 HK00700 TSLA
```

脚本输出 JSON。读取结果后，用中文向用户总结最重要的字段，不要把整段 JSON 原样抄回去，除非用户明确要求。

### 2. 遇到简称或歧义先搜索

对短中文名或明显存在歧义的输入，先调用 `search` 再决定是否直接报价。

典型例子：

1. `腾讯` 可能扩散到 `腾讯控股`、`腾讯音乐`、相关指数或板块。
2. `平安` 可能对应银行、保险、ETF 或指数。

示例：

```bash
python scripts/stock_watchlist.py search 腾讯
```

处理规则：

1. 如果第一候选明显符合用户意图，可以直接继续 `quote`。
2. 如果前几项都合理，先把前 3 个候选简要列给用户，再继续。

### 3. 用 Markdown 管理自选列表

先初始化 Markdown 模板：

```bash
python scripts/stock_watchlist.py watchlist init --file ./watchlist.md
```

模板位于 [assets/watchlist-template.md](assets/watchlist-template.md)。

Markdown 文档必须保留这两个标记：

1. `<!-- stock-watchlist:start -->`
2. `<!-- stock-watchlist:end -->`

脚本只会回写标记之间的表格，其它正文会保留。

### 4. 自选列表维护动作

新增或更新一行：

```bash
python scripts/stock_watchlist.py watchlist add \
  --file ./watchlist.md \
  --query 贵州茅台 \
  --cost-price 1395 \
  --quantity 100 \
  --note core
```

删除一行：

```bash
python scripts/stock_watchlist.py watchlist remove \
  --file ./watchlist.md \
  --query SH600519
```

把手工编辑过的 `query` 统一解析成规范符号：

```bash
python scripts/stock_watchlist.py watchlist sync --file ./watchlist.md
```

查询整个自选列表并计算汇总：

```bash
python scripts/stock_watchlist.py watchlist quote --file ./watchlist.md
```

## Watchlist 约束

表格必须包含这些列：

1. `query`
2. `symbol`
3. `quote_id`
4. `name`
5. `cost_price`
6. `quantity`
7. `note`

字段含义：

1. `query`：原始查询词，适合手工维护，例如中文名或代码。
2. `symbol`：规范代码，例如 `SH600519`、`HK00700`、`TSLA`。
3. `quote_id`：行情接口使用的内部标识，保留后可以减少再次搜索。
4. `cost_price`：可选，留空则不计算该行盈亏。
5. `quantity`：可选，留空则不计算该行盈亏。

建议：

1. 手工改完 `query` 后执行一次 `watchlist sync`。
2. 不要删除表头，也不要删掉标记行。
3. 如果只想保留观察列表，不关心成本，可以只维护 `query/symbol/quote_id/name/note`。

## 安全边界

1. 仅把 watchlist 放在当前工作目录内的 Markdown 文件中，例如 `./watchlist.md`。
2. 不要把 `--file` 指向系统目录、隐藏配置目录或无关文档。
3. 如确实需要在工作目录外使用，先显式设置 `STOCK_WATCHLIST_ALLOWED_ROOTS`，只加入你确认安全的目录。
4. `watchlist init --force` 仅用于覆盖已有的 watchlist 文件，不要把它用于普通 Markdown 文档。

## 输出要求

脚本返回 JSON 后，按场景组织最终回答：

1. 单只股票：优先总结 `name/symbol/current_price/change_percent/open_price/high_price/low_price/previous_close/total_market_cap/pe_ttm/pb`。
2. 多只股票：按股票分组，避免混成一段。
3. 自选列表：先给组合汇总，再列重点持仓。

如果用户明确要“基本信息”，默认至少包含：

1. 当前价
2. 涨跌额
3. 涨跌幅
4. 今开
5. 最高
6. 最低
7. 昨收
8. 总市值
9. PE(TTM)
10. PB

## 资源

1. 主脚本：[scripts/stock_watchlist.py](scripts/stock_watchlist.py)
2. Markdown 模板：[assets/watchlist-template.md](assets/watchlist-template.md)
