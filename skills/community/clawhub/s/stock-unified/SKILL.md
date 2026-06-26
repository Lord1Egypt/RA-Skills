---
name: stock-unified
description: 多源统一股票数据接口，整合通达信(pytdx)/同花顺/东方财富(新版API)/akshare五大股票数据源，自动降级切换。用于A股实时行情查询、K线历史、板块排行与成分股、财务数据、板块搜索等场景。当用户查询股价、板块排行、成分股、K线、财务数据时使用。
---

# 🐂 UnifiedStock — 多源统一股票数据接口

A股 5 大数据源自动整合：通达信(pytdx) + 东方财富(新版datacenter API) + 同花顺(ths) + akshare + 新浪财经。

## 安装依赖

```bash
pip install pytdx akshare requests pandas
```

## 数据源自动降级策略

```
实时行情:    通达信(pytdx) → akshare
K线历史:    通达信(pytdx) → akshare
板块排行:    同花顺(ths) → akshare
板块成分股:  东方财富(datacenter) → akshare
财务数据:    akshare
```

每个源挂了自动换下一个，无需手动指定。

## 快速上手指南

### 1️⃣ 查实时行情

```bash
python3 scripts/unified_stock.py --realtime 600839,002156,002475
```

输出：代码、最新价、涨跌幅、昨收、开盘、最高、最低、成交量

### 2️⃣ 查K线

```bash
python3 scripts/unified_stock.py --kline 600839 --days 30
```

默认最近 10 天，支持任意天数。

### 3️⃣ 板块排行

```bash
python3 scripts/unified_stock.py --sector-top 20
```

输出行业板块 Top N：涨跌幅、涨跌家数、资金净流入、领涨股。

### 4️⃣ 板块成分股

```bash
# 先搜板块代码
python3 scripts/unified_stock.py --search 半导体

# 再查成分股
python3 scripts/unified_stock.py --sector-stocks 917
python3 scripts/unified_stock.py --sector-stocks 917 --live    # 带实时行情
```

板块代码说明：917=半导体概念, 891=国产芯片, 952=第三代半导体, 1137=存储芯片

### 5️⃣ 财务数据

```bash
python3 scripts/unified_stock.py --financial 600839
```

### 6️⃣ JSON 输出

所有命令支持 `--json` 参数，方便程序调用：

```bash
python3 scripts/unified_stock.py --realtime 600839 --json
python3 scripts/unified_stock.py --sector-top 10 --json
```

### 7️⃣ 数据源检测

```bash
python3 scripts/unified_stock.py --status
```

## 板块代码参考（常用）

| 代码 | 板块 | 成分股数 |
|------|------|---------|
| 917 | 半导体概念 | ~480 |
| 891 | 国产芯片 | ~250 |
| 952 | 第三代半导体 | ~150 |
| 1137 | 存储芯片 | ~80 |
| 1037 | 消费电子 | ~200 |
| 1201 | 电子 | ~300 |

可用 `--search` 搜索任意关键词找到代码。

## 架构

```
统一入口 unified_stock.py
├── 实时行情  → tdx_get_quotes()       [通达信]
├── K线      → tdx_get_kline()         [通达信]
├── 板块排行  → ths_industry_summary()  [同花顺]
├── 板块成分股 → east_get_board_stocks() [东方财富]
├── 财务数据  → ak_get_financial()      [akshare]
└── 状态检测  → get_status()            [全部源]
```

Python API：

```python
from unified_stock import get_realtime, get_kline, get_sector_top, get_sector_stocks

# 查行情
quotes = get_realtime(["600839", "002156", "002475"])

# 查K线
kline = get_kline("600839", days=30)

# 板块排行
sectors = get_sector_top(20)

# 板块成分股(带实时价)
stocks = get_sector_stocks("917", live=True)

# 数据源状态
status = get_status()
```
