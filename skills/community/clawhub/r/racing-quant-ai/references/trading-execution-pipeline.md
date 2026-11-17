# 策略持仓 → QMT 交易执行流水线

本文件描述如何将赛马量化AI的策略持仓转换为QMT实际下单交易。

## 整体架构

```
Hermes Linux 端                          QMT Windows 端
─────────────────                       ────────────────
MySQL策略库 ─→ racing_to_qmt.py          racing_to_qmt.py
  (读持仓)      generate-only 模式         execute 模式
                  │                         │
                  ▼                         ▼
             指令JSON文件 ──(文件同步)──→ 读取指令JSON
             latest_orders.json           → xtquant下单
```

## 核心脚本

**路径：** `~/.hermes/scripts/racing_to_qmt.py`

### 三种运行模式

| 模式 | 运行位置 | 功能 |
|------|---------|------|
| `generate-only` | Hermes Linux | 读策略→算指令→生成JSON |
| `execute` | QMT Windows | 读JSON→连接xtquant→下单 |
| `full` | QMT Windows | 读策略→算指令→下单（一步到位） |

### 命令行用法

```bash
# 1. 查看推荐策略
python3 racing_to_qmt.py --list-strategies

# 2. Hermes端：生成指令
python3 racing_to_qmt.py --mode=generate-only \
    --strategy="短周期机器学习时序交叉版" \
    --capital=100000 --top-n=10

# 3. QMT端：执行下单
python racing_to_qmt.py --mode=execute \
    --account=1234567890

# 4. 完整模式（QMT端一步到位）
python racing_to_qmt.py --mode=full \
    --strategy="短周期机器学习时序交叉版" \
    --account=1234567890 --capital=100000

# 5. 试运行（只计算不下单）
python racing_to_qmt.py --mode=full --dry-run
```

### 交易规则（Config类可配）

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `FULL_REBALANCE` | True | 全量换仓(卖旧买新) |
| `MIN_ORDER_AMOUNT` | 2000 | 最低下单金额 |
| `TOP_N_TRADE` | 10 | 下单前N只重仓股 |
| `PRICE_LIMIT_PCT` | 0.10 | 偏离昨收10%以上跳过 |
| `ORDER_TYPE` | "limit" | 限价单 |
| `PRICE_OFFSET` | 0.005 | 限价偏移(买+0.5%) |
| `MAX_DAILY_TRADES` | 20 | 单日最大交易笔数 |

## QMT 依赖安装

在QMT Windows机器上：

```bash
pip install pymysql
# xtquant 通常随QMT安装，无需单独装
# 如果缺失：pip install xtquant
```

## 架构要点

1. **MySQL可达性**：QMT机器需要能访问 `47.121.180.199:3306` (full/execute模式需要)
2. **文件桥接**：如果QMT机器不能直接访问MySQL，用 generate-only 模式生成JSON同步过去
3. **行情来源**：脚本使用东方财富批量API (`ulist.np/get`) 获取实时行情，无需akshare
4. **下单方式**：限价单（买价=现价×1.005，卖价=现价×0.995）确保成交