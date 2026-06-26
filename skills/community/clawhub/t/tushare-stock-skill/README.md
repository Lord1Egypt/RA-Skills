# Tushare A 股研究技能

一个面向中国 A 股的 Tushare 专用技能包，聚焦个股数据获取、估值分析、风险提示与交易观察。

## 简介

这个仓库提供的是一个“更聚焦的 Tushare 技能”，它不是把 Tushare 所有市场、所有资产、所有宏观数据一次性打包，而是专注于中国 A 股个股研究这条主线。

它适合这样的使用方式：

- 想快速查一只股票的核心数据
- 想把数据查询和个股分析放在同一个技能里完成
- 想从估值、财务质量、成长性、趋势、资金流和技术面几个维度看一只股票
- 想把 Tushare 变成一个更像“个股研究助手”的技能，而不是单纯接口封装

## 技能亮点

- 聚焦中国 A 股个股，而不是做大而全的数据杂烩
- 同时覆盖数据查询、分析判断与交易观察
- 支持自然语言路由，也支持显式接口调用
- 内建估值、财务质量、成长性、风险与趋势分析
- 内建量价、资金流、龙虎榜、均线、RSI、KDJ、布林线、MACD 等交易观察能力
- 明确处理 Tushare 的积分门槛与额外权限限制
- 凭证与网络边界清晰，适合上架型技能包

## 与其他 ClawHub Tushare 技能的区别

基于 2026 年 3 月 9 日可见的 ClawHub 页面摘要：

- [`lidayan/tushare-data`](https://clawhub.ai/lidayan/tushare-data) 更像一个覆盖面很广的 Tushare 数据入口，强调股票、基金、期货、数字货币和基础面等多类数据。
- [`StanleyChanH/tushare-finance`](https://clawhub.ai/StanleyChanH/tushare-finance) 也是偏大而全路线，强调 A 股、港股、美股、基金、期货、债券以及宏观指标等更宽的市场覆盖。

而这个技能的取舍很明确：

- 不追求最广覆盖
- 专注中国 A 股个股
- 在个股研究和交易观察上做得更深

如果你的目标是“一个技能横跨多资产、多市场、多宏观主题”，上面两个更偏全能型。
如果你的目标是“把中国 A 股个股研究这件事做深”，这个技能会更合适。

## 能力覆盖

- 股票基础资料与上市清单
- 日线、周线、月线、复权、实时、分钟行情
- `daily_basic` 每日指标与估值指标
- 财务报表、业绩预告、分红、审计、财务指标
- 十大股东、质押、回购、解禁、大宗交易、股东人数
- 券商盈利预测、筹码分布、技术因子、CCASS、AH 比价
- 两融、转融通、资金流向
- 龙虎榜、涨跌停、THS / DC / TDX / KPL 题材与板块数据
- 个股估值、财务质量、成长性、趋势、风险提示
- 交易观察与技术分析：均线、动量、RSI、KDJ、布林线、MACD

## 依赖要求

- Python 3
- 有效的 `TUSHARE_TOKEN`
- [`requirements.txt`](requirements.txt) 中列出的 Python 依赖

## 环境变量

必需：

- `TUSHARE_TOKEN`：所有 Tushare 数据访问都依赖它

可选：

- `TUSHARE_STOCK_ENV_FILE`：可选，指向包含 `TUSHARE_TOKEN` 的 env 文件
- `TUSHARE_POINTS`：可选，用于覆盖积分门槛判断，默认 `5120`
- `TUSHARE_STOCK_CACHE_DIR`：可选，缓存目录，默认 `/tmp/tushare_stock_skill`

## 快速开始

安装依赖：

```bash
pip install -r requirements.txt
```

设置凭证：

- 直接在环境变量中设置 `TUSHARE_TOKEN`
- 或设置 `TUSHARE_STOCK_ENV_FILE` 指向一个仅包含 `TUSHARE_TOKEN` 的 env 文件

说明：

- 技能不会隐式扫描家目录中的配置文件
- 如果使用 `TUSHARE_STOCK_ENV_FILE`，请确保该文件只包含你愿意让技能读取的内容

自然语言查询示例：

```bash
python scripts/tushare_stock.py run --text "贵州茅台近一年每日指标"
```

显式接口调用示例：

```bash
python scripts/tushare_stock.py fetch --endpoint daily_basic --param ts_code=600519.SH --param start_date=20250101 --param end_date=20250301
```

个股分析示例：

```bash
python scripts/tushare_stock.py analyze --text "分析贵州茅台的估值、财务质量和趋势"
```

查看内置技术指标：

```bash
python scripts/tushare_stock.py indicators
```

## 仓库结构

- [`SKILL.md`](SKILL.md)：技能说明与调用约束
- [`scripts/tushare_stock.py`](scripts/tushare_stock.py)：主入口脚本
- [`scripts/trading_analysis.py`](scripts/trading_analysis.py)：技术指标注册与计算逻辑
- [`scripts/build_catalog.py`](scripts/build_catalog.py)：官方文档接口目录构建器
- [`references/stock_endpoints.json`](references/stock_endpoints.json)：机器可读接口目录
- [`references/stock_endpoints.md`](references/stock_endpoints.md)：人工可读接口摘要

## 安全说明

- 技能所需环境变量已经在 `SKILL.md` frontmatter 中显式声明
- `run`、`fetch`、`analyze` 会访问 Tushare 网络接口
- `build_catalog.py` 会访问 `tushare.pro` 官方文档页面
- 技能只读取声明过的 token 相关环境变量，以及显式指定的 env 文件路径
- 技能不会主动扫描其他本地凭证，也不会主动写入 Tushare token 缓存文件

## 上架摘要建议

如果需要一段更适合市场页的简短介绍，可以直接使用：

> 一个面向中国 A 股个股研究的 Tushare 专用技能，提供股票数据查询、估值与财务分析、资金流与龙虎榜观察，以及技术面交易观察能力；相比大而全的 Tushare 包，更聚焦，也更适合个股研究场景。
