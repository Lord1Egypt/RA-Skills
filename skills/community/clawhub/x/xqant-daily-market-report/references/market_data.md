# 市场数据查询参考

本文件说明 15:30 市场简报所需的 Wind 数据查询函数。

---

## 1. 主要指数查询

### 函数
```
f_myfund_nav(代码，日期)  # 获取净值
或
f_index_basic(代码)       # 获取基本信息
```

### 指数代码
| 指数 | 代码 | 说明 |
|------|------|------|
| 上证指数 | 000001.SH | 上海证券交易所综合指数 |
| 沪深 300 | 000300.SH | 沪深 300 指数 |
| 深证成指 | 399001.SZ | 深圳证券交易所综合指数 |
| 创业板指 | 399006.SZ | 创业板指数 |
| 科创 50 | 000688.CSI | 科创板 50 指数 |
| 万得全 A | 881001.WI | 万得全 A 指数 |

### 当日涨跌幅获取
```python
# 方法 1: 直接查询涨跌幅
data = run_function("f_index_return", "000001.SH", "2026-03-24")
# 返回：1.78 (上证指数当日涨跌幅%)

# 方法 2: 获取净值后计算
nav_data = run_function("f_index_nav", "000001.SH", "2026-03-24")
prev_nav = run_function("f_index_nav", "000001.SH", "2026-03-23")
return_pct = (nav_data - prev_nav) / prev_nav * 100
```

---

## 2. 行业涨跌幅查询

### 申万一级行业
```python
# 查询所有申万一级行业当日涨跌幅
data = run_function("f_industry_return", "SW2021", "2026-03-24")
# 返回：{"环保": 4.29, "纺织服饰": 3.99, ..., "煤炭": -0.86, ...}
```

### 获取前 10 名和后 5 名
```python
sorted_industries = sorted(data.items(), key=lambda x: x[1], reverse=True)
top_10 = sorted_industries[:10]
bottom_5 = sorted_industries[-5:]
```

---

## 3. 债券收益率查询

### 国债收益率
| 期限 | 代码 | 说明 |
|------|------|------|
| 10 年期国债 | 000018.CSI | 10 年期国债到期收益率 |
| 30 年期国债 | 000019.CSI | 30 年期国债到期收益率 |

### 查询函数
```python
# 10 年期国债收益率
data = run_function("f_yield_curve", "000018.CSI", "2026-03-24")
# 返回：2.37

# 30 年期国债收益率
data = run_function("f_yield_curve", "000019.CSI", "2026-03-24")
# 返回：2.35
```

### 国债期货
| 合约 | 代码 | 说明 |
|------|------|------|
| 10 年期国债期货 | TF2606.CZC | 2026 年 6 月到期 |
| 30 年期国债期货 | TL2606.CZC | 2026 年 6 月到期 |

---

## 4. 成交量查询

### 沪深两市成交额
```python
data = run_function("f_market_volume", "ALL", "2026-03-24")
# 返回：21000 (单位：亿元)
```

### 对比前一日
```python
today_volume = run_function("f_market_volume", "ALL", "2026-03-24")
yesterday_volume = run_function("f_market_volume", "ALL", "2026-03-23")
change = today_volume - yesterday_volume
change_pct = change / yesterday_volume * 100
```

---

## 5. 板块热度分析

### 概念板块
```python
# 查询当日涨幅靠前的概念板块
data = run_function("f_concept_return", "ALL", "2026-03-24")
top_concepts = sorted(data.items(), key=lambda x: x[1], reverse=True)[:20]
```

### 热门概念
根据历史数据，以下概念常与固收 + 相关:
- 高送转
- 环保
- 有色金属
- 新能源
- 医药生物

---

## 6. 数据汇总模板

```python
def get_market_summary(date):
    """
    获取完整市场摘要
    """
    summary = {
        "date": date,
        "indices": {
            "上证指数": run_function("f_index_return", "000001.SH", date),
            "深证成指": run_function("f_index_return", "399001.SZ", date),
            "创业板指": run_function("f_index_return", "399006.SZ", date),
            "科创 50": run_function("f_index_return", "000688.CSI", date),
        },
        "volume": run_function("f_market_volume", "ALL", date),
        "top_industries": get_top_industries(date, n=10),
        "bond_rates": {
            "10 年期": run_function("f_yield_curve", "000018.CSI", date),
            "30 年期": run_function("f_yield_curve", "000019.CSI", date),
        },
    }
    return summary
```

---

## 7. 固收 + 赛道预测逻辑

### 预测因素
1. **股市表现**: 大盘涨跌 → 影响固收 + 权益部分
2. **债券市场**: 利率走势 → 影响固收 + 债券部分
3. **行业涨跌**: 环保/有色金属等 → 影响持仓匹配度
4. **成交量**: 资金情绪 → 影响波动率

### 预测规则
| 市场情况 | 低波 | 90 天 | 中波 | 高波 |
|----------|------|------|------|------|
| 股市大涨 + 债市稳 | ✅ | ✅ | ✅ | ⚠️ |
| 股市大跌 + 债市稳 | ✅ | ✅ | ⚠️ | ❌ |
| 股市稳 + 债市涨 | ✅ | ✅ | ✅ | ⚠️ |
| 股市稳 + 债市跌 | ⚠️ | ⚠️ | ⚠️ | ❌ |

---

## 8. 注意事项

1. **数据时效性**: 必须在 15:30 后获取当日收盘数据
2. **非交易日**: 跳过或查询最近交易日
3. **数据验证**: 对比多个数据源确保一致性
4. **历史记录**: 保存每日市场摘要用于趋势分析
