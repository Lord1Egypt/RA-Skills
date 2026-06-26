---
name: yang-selection
description: 杨永兴尾盘选股法 - 腾讯财经实时筛选，智能市值缓存
version: 1.0.0
metadata: {"clawdbot":{"emoji":"📈","requires":{"bins":["python3"]}}}
---

# 杨永兴尾盘选股法

基于腾讯财经 API 的实时股票筛选工具，实现杨永兴尾盘买入法策略。

## 功能特点

- ✅ 腾讯财经实时行情（无需 Baostock 登录）
- ✅ 智能市值缓存（30 天内不重复查询）
- ✅ 两步筛选：基础筛选 + 深度筛选
- ✅ 速率限制：每秒 10 只股票

## 筛选条件

### 基础条件（腾讯财经）
1. 涨幅 3%-5%
2. 换手率 5%-10%
3. 市值 50 亿 -200 亿

### 深度条件（Baostock）
4. 量比 > 1
5. 近 5 日成交量持续放大
6. 5/10/20 日均线在 60 日线上方
7. 股价创当天新高

## 使用方法

```bash
# 1. 先查询主板股票列表
python3 query_main_board_stocks.py

# 2. 运行杨永兴选股
python3 yang_selection.py
```

## 依赖

```bash
pip install baostock pandas numpy requests
```

## 输出文件

- `market_cap_cache.json` - 市值缓存（30 天有效期）
- 筛选结果直接输出到终端

## 数据源

- 实时行情：腾讯财经 API
- 历史数据：Baostock（仅深度筛选）
- 股票列表：query-main-board-stocks skill
