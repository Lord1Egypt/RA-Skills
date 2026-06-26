# Stock-A Skill

💼 A股股票行情数据获取工具，支持多个免费数据源。

## 功能

- **实时行情** - 获取个股实时价格、涨跌幅、成交量等
- **历史K线** - 获取日线/周线/月线历史数据
- **多数据源** - mootdx、新浪财经、腾讯财经、东方财富、Tushare

---

## 📊 数据源汇总

### 1. mootdx（通达信/同花顺）⭐ 推荐

| 功能 | 状态 | 说明 |
|------|------|------|
| 实时行情 | ✅ 可用 | 默认数据源，需本地安装 |
| 历史K线 | ✅ 可用 | 支持日线/周线/月线 |
| F分钟线 | ✅ 可用 | 1/5/15/30/60分钟 |
| 财务数据 | ✅ 可用 | 财务指标、利润表等 |

```bash
# mootdx 实时行情
python -c "
from mootdx import quotes
q = quotes.StdQuotes()
result = q.daily(symbol='600519')
print(result)
"

# mootdx 历史K线
python -c "
from mootdx import reader
r = reader.Reader()
df = r.daily(symbol='600519', adjust='qfq')
print(df.tail())
"
```

---

### 2. 新浪财经

| 功能 | 状态 | 说明 |
|------|------|------|
| 实时行情 | ✅ 可用 | 推荐使用 |
| 历史K线 | ✅ 可用 | |

```bash
# 新浪财经 - 实时行情 (推荐)
python scripts/sina_realtime.py sh600519

# 新浪财经 - 历史K线
python scripts/sina_history.py sh600519 2024-03-01 2024-03-25
```

---

### 3. 腾讯财经

| 功能 | 状态 | 说明 |
|------|------|------|
| 实时行情 | ✅ 可用 | |

```bash
# 腾讯财经 - 实时行情
python scripts/tengxun_realtime.py sh600519
```

---

### 4. 东方财富

| 功能 | 状态 | 说明 |
|------|------|------|
| 实时行情 | ⚠️ 不稳定 | 需网络稳定环境 |

```bash
# 东方财富 - 实时行情
python scripts/eastmoney_realtime.py sh600519
```

---

### 5. Tushare

| 功能 | 状态 | 说明 |
|------|------|------|
| 实时行情 | ⚠️ 备用 | 即将停用，免费Token |

```bash
# Tushare - 实时行情
python scripts/tushare_realtime.py 600519
```

---

## 📋 数据源测试结果汇总

| 数据源 | 实时行情 | 历史K线 | 财务数据 | 状态 |
|--------|----------|---------|----------|------|
| **mootdx** | ✅ | ✅ | ✅ | ⭐ 推荐 |
| 新浪财经 | ✅ | ✅ | ❌ | ✅ 可用 |
| 腾讯财经 | ✅ | ❌ | ❌ | ✅ 可用 |
| 东方财富 | ⚠️ | ❌ | ❌ | ⚠️ 不稳定 |
| Tushare | ⚠️ | ❌ | ❌ | ⚠️ 备用 |
| 网易财经 | ❌ | ❌ | ❌ | ❌ 502错误 |
| Tushare Pro | ❌ | ❌ | ❌ | ❌ 需Token |

---

## 🔧 代码说明

- `sh600519` - 上海市场 (60xxxx)
- `sz000001` - 深圳市场 (00xxxx)
- `sz300750` - 创业板 (30xxxx)
- `bjxxxx` - 北交所 (8xxxx/4xxxx)

---

## 📖 使用示例

### 实时行情输出示例

```
贵州茅台 (SH600519)
==============================
最新价: 1408.81
涨跌: +1.48
涨跌幅: +0.11%
开盘: 1410.11
最高: 1417.87
最低: 1401.01
成交量: 1,409手
成交额: 157.35亿
```

---

## 安装新数据源

```bash
# 安装 mootdx (如未安装)
pip install mootdx

# 安装 Tushare (备用)
pip install tushare
```
