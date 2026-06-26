---
name: stock-scanner
description: >
  跨市场股票技术指标扫描系统。数据来源 TradingView，支持 A股/港股/美股/日股。
  从用户 Obsidian vault 中的 watchlist 读取 ticker 列表，运行14项技术信号扫描
  （MA交叉、RSI、MACD、BOLL、放量突破、缩量回调、量价背离、周K共振、综合评分等），
  并将扫描报告（Markdown + 可选 Excel）保存回 Obsidian vault。
  设计为每日定时运行。
  当用户提到"股票扫描"、"技术指标扫描"、"stock scanner"、"run the scanner"、
  "跑一下扫描"、"技术分析日报"、"watchlist scan"、"每日扫描"时触发本 skill。
  也适用于用户要求对 watchlist 做批量技术分析、生成技术信号报告、或提到
  TradingView 数据扫描等场景。
---

# 跨市场股票技术指标扫描系统 (TradingView Edition)

## 概述

本 skill 从用户 Obsidian vault 中读取 watchlist CSV，通过 TradingView 获取 OHLCV 日线数据，
计算 14 类技术信号并生成综合评分，最终将 Markdown 报告写回 Obsidian vault。

## 配置

用户需在对话中提供或确认以下路径（首次使用时询问）：

| 配置项 | 说明 | 示例 |
|--------|------|------|
| `obsidian_vault` | Obsidian vault 根目录 | `/Users/sarah/Documents/MyVault` |
| `watchlist_path` | vault 内 watchlist CSV 相对路径 | `Investing/watchlist.csv` |
| `output_dir` | vault 内输出目录相对路径 | `Investing/技术指标扫描` |

### Watchlist CSV 格式

```csv
ticker,name,market,sector
AAPL,苹果,US,科技
0700.HK,腾讯,港股,科技
600519.SS,贵州茅台,A股,消费
7203.T,丰田,日股,汽车
```

- `ticker`（必须）：TradingView 格式的代码
- `name` / `market` / `sector`：可选辅助列

## 运行流程

1. **读取 SKILL.md**（你正在做的事）
2. **安装依赖**：`pip install tradingview_ta pandas numpy requests openpyxl --break-system-packages`
3. **读取用户 Obsidian vault 中的 watchlist CSV**
4. **运行扫描脚本**：
   ```bash
   python /path/to/skill/scripts/scanner.py \
     --csv "<obsidian_vault>/<watchlist_path>" \
     --output "<obsidian_vault>/<output_dir>" \
     --workers 6
   ```
5. **将生成的 Markdown 报告通过 `present_files` 展示给用户**

## 每日定时运行

本 skill 本身不包含 cron 调度器（因为 Claude 会话是临时的）。要实现每日自动运行：

### 方案 A：用户本地 cron（推荐）
告诉用户在本机设置：
```bash
# crontab -e
0 18 * * 1-5 cd /path/to/vault && python /path/to/scanner.py --csv watchlist.csv --output 技术指标扫描/
```

### 方案 B：每次对话时手动触发
用户说"跑一下扫描"即可触发本 skill。

## 技术信号列表（14 项）

| # | 信号 | 类型 |
|---|------|------|
| 1 | MA5 上穿 MA10（量能+趋势确认）| 趋势 |
| 2 | MA5 下穿 MA10（量能确认）| 趋势 |
| 3 | RSI 超卖回升 / 底背离 | 动量 |
| 4 | RSI 超买 | 动量 |
| 5 | 突破历史新高（252日窗口）| 趋势 |
| 6 | BOLL 上轨突破 / 下轨跌破 | 波动 |
| 7 | 下行趋势均线收窄靠拢 MA20 | 趋势 |
| 8 | MACD 金叉 / 死叉 | 动量 |
| 9 | 放量突破 | 量价 |
| 10 | 缩量回调 | 量价 |
| 11 | 量价背离预警 | 量价 |
| 12 | 周K趋势 | 趋势 |
| 13 | 日K与周K共振 | 趋势 |
| 14 | 综合评分（0-100）| 综合 |

## 评分体系

- 趋势类（最高 40 分）：日周共振多头 +20，黄金交叉确认 +14，历史新高 +10
- 动量类（最高 35 分）：RSI 超卖回升 +15，MACD 零轴上金叉 +14
- 量价类（最高 25 分）：放量突破 +18，缩量回调 +8
- 负分惩罚：死亡交叉 -15，量价背离 -12，RSI 超买 -8

## 脚本位置

主脚本：`scripts/scanner.py`（约 1300 行，完整技术指标计算 + 报告生成）

运行前务必先安装依赖，脚本会从 TradingView 拉取数据。

## 注意事项

- TradingView 非官方 API 有频率限制，默认并发 6 线程 + 0.2s 延迟
- A 股 ticker 使用 `.SS`（上交所）或 `.SZ`（深交所）后缀
- 港股使用 `.HK`，日股使用 `.T`
- 美股直接使用 ticker symbol（如 AAPL, MSFT）
- 报告为 Markdown 格式，可直接在 Obsidian 中渲染
