---
name: 螃蟹投研-股票行业Collector
description: 收集A股某行业全部上市公司资料，包括代码、名称、交易所、行业、财务数据（ROE、毛利率、净利率、资产负债率、现金流、增长率）、控股股东及持股比例
metadata:
  {
    "openclaw": {
      "emoji": "📊",
      "requires": {"pip": ["baostock", "akshare", "pandas"]}
    }
  }
keywords:
  - 股票
  - 行业分析
  - 财报
  - 财务数据
  - ROE
  - 控股股东
  - 股东持股
  - 申万行业
  - 中证行业
  - baostock
  - akshare
---

# 股票行业数据收集器 v2.3

## 功能

收集A股某行业的全部上市公司详细信息，包含完整财务数据和控股股东数据

## 【重要】获取行业全部公司的方法

本技能使用 **akshare 行业分类** 获取股票，确保不遗漏任何公司：

### 方法1：使用申万行业分类
```python
c.collect(industry_name="煤炭")  # 自动转换为申万行业代码 BK0437
c.collect(industry_name="焦煤")  # BK1494
c.collect(industry_name="煤化工") # BK1419
```

### 方法2：直接使用申万行业代码
```python
c.collect(industry_code="BK0437")   # 煤炭
c.collect(industry_code="BK1494")   # 焦煤
c.collect(industry_code="BK1493")   # 动力煤
c.collect(industry_code="BK1419")   # 煤化工
```

### 支持的行业
| 行业名称 | 申万代码 | 说明 |
|---------|---------|------|
| 煤炭 | BK0437 | 煤炭开采 |
| 焦煤 | BK1494 | 焦炭 |
| 动力煤 | BK1493 | 动力煤 |
| 煤化工 | BK1419 | 煤化工 |
| 石油 | BK0411 | 石油开采 |
| 燃气 | BK0501 | 燃气 |
| 电力 | BK0502 | 电力 |
| 光伏 | BK1033 | 光伏 |

## 输出字段

| 字段 | 说明 | 数据来源 |
|------|------|---------|
| 代码 | 股票代码 | 基本信息 |
| 名称 | 公司名称 | 基本信息 |
| 交易所 | 沪市/深市 | 基本信息 |
| 行业 | 证监会行业分类 | 行业数据 |
| ROE | 净资产收益率(%) | 利润表 |
| 毛利率 | 毛利率(%) | 利润表 |
| 净利率 | 净利率(%) | 利润表 |
| 营业收入 | 营业收入(元) | 利润表 |
| 净利润 | 净利润(元) | 利润表 |
| 总资产 | 总资产(元) | 资产负债表 |
| 总负债 | 总负债(元) | 资产负债表 |
| 资产负债率 | 负债/权益 | 资产负债表 |
| 经营现金流 | 经营现金流(元) | 现金流量表 |
| 营收增长 | 营收增长率(%) | 成长能力 |
| 净利润增长 | 净利润增长率(%) | 成长能力 |
| 控股股东 | 控股股东名称 | 十大流通股东 |
| 控股比例 | 持股比例(%) | 十大流通股东 |
| 股东性质 | 国企/民企 | 自动判断 |
| 所在地 | 省份 | 手动维护 |
| 产区 | 主要生产区 | 手动维护 |

## 数据来源

- **baostock** - 财务数据（免费无需注册）
- **akshare** - 股东数据、行业分类（需清除代理）

## 使用

```python
from stock_industry_collector import IndustryCollector

c = IndustryCollector()

# 方法1：按行业名称
df = c.collect(industry_name="煤炭")

# 方法2：按申万行业代码
# df = c.collect(industry_code="BK0437")

print(f"找到 {len(df)} 只煤炭行业股票")

# 格式化
df['ROE'] = df['ROE'].apply(lambda x: str(round(float(x)*100, 2)) + '%' if x else '')
df['净利润'] = df['净利润'].apply(lambda x: str(round(float(x)/1e8, 2)) + '亿' if x else '')

print(df[['代码','名称','控股股东','ROE','净利润']].head())

# 保存Excel
df.to_excel("煤炭行业财务分析.xlsx", index=False)
```

## 注意事项

1. **行业股票获取**：使用 akshare 申万/中证行业分类，不遗漏
2. **财报年份**：默认获取2024年年报（year=2024, quarter=4）
3. **数据延迟**：每年4月底发布上年年报
4. **请求限速**：已内置延时，避免请求过快
5. **代理问题**：akshare 需要清除系统代理才能正常工作
