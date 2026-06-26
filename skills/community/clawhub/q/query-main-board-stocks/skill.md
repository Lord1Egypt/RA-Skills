---
name: query-main-board-stocks
description: 查询沪深主板 A 股股票列表（排除创业板、科创板）
version: 1.0.0
metadata: {"clawdbot":{"emoji":"📈","requires":{"bins":["python3"]}}}
---

# query-main-board-stocks

查询沪深主板 A 股股票列表（排除创业板、科创板）的 Baostock 工具。

## 功能

- 使用 Baostock API 获取全部 A 股股票列表
- 过滤出主板股票（沪市主板 600/601/603/605，深市主板 000/001/002/003）
- 排除创业板（300/301）和科创板（688）
- 输出 JSON 和 CSV 格式结果

## 使用方法

```bash
python query_main_board_stocks.py
```

## 输出文件

- `main_board_stocks.json` - 包含股票列表的 JSON 文件
- `main_board_stocks.csv` - CSV 格式股票列表（代码、名称）

## 依赖

```bash
pip install baostock pandas
```

## 数据源

Baostock - 免费 A 股数据平台（无需注册）

## 示例输出

```
=====================================================================
沪深主板股票查询（非创业板、非科创板）
=====================================================================
✅ 获取到 4800 只股票
✅ 主板股票：3200 只

📊 统计结果
  主板股票：3200 只
  沪市主板：1800 只
  深市主板：1400 只
```
