---
name: pywencai-stock
description: 使用 pywencai 库获取同花顺问财股票数据，支持实时行情、财务指标、龙虎榜、资金流向等查询。适用于需要快速获取A股市场数据的场景。
version: 1.0.0
author: QIQ (original by Minimax Agent AI)
license: MIT
tags:
  - stock
  - data
  - china
  - finance
  - pywencai
---

# PyWenCai 股票数据技能

通过 pywencai 库无缝访问同花顺问财的股票数据API。

## 核心能力

- ✅ 实时行情查询（涨停、跌停、涨幅榜）
- ✅ 财务数据（净利润、市盈率、ROE）
- ✅ 资金流向（主力净流入、龙虎榜）
- ✅ 个股详细信息
- ✅ 板块/概念股检索
- ✅ 返回结构化 pandas DataFrame

## 安装前置条件

```bash
# 1. 安装 pywencai
pip install pywencai

# 2. 如果需要处理大量数据，安装 pandas（通常已自带）
pip install pandas
```

## 使用方法

### 1. 基本搜索

```python
# 查询今日涨停股票
result = skill('pywencai-stock').search(query='A股涨停')
print(result)  # pandas.DataFrame
```

### 2. 查询个股

```python
# 查询600519（贵州茅台）的财务指标
result = skill('pywencai-stock').search(
    query='600519 财务指标',
    sort_key='净利润',
    sort_order='desc'
)
```

### 3. 获取热门板块

```python
# 查询芯片概念股
result = skill('pywencai-stock').search(
    query='芯片概念股',
    page=1,
    perpage=20
)
```

### 4. 资金流向

```python
# 查询主力净流入最多的股票
result = skill('pywencai-stock').search(
    query='主力净流入最多的股票',
    loop=True  # 自动翻页获取全部
)
```

## 常用查询示例

| 目的 | query 参数 |
|------|-----------|
| 今日涨停 | `'A股涨停'` |
| 今日跌停 | `'A股跌停'` |
| 涨幅前10 | `'沪深A股涨幅前10'` |
| 换手率前10 | `'换手率最高的股票'` |
| 龙虎榜 | `'今日龙虎榜'` |
| 净利润最高 | `'净利润最高的公司'` |
| 市盈率最低 | `'市盈率最低的股票'` |
| ROE最高 | `'ROE最高的股票'` |
| 芯片概念 | `'芯片概念股'` |
| 新能源车 | `'新能源汽车概念股'` |

### 高级参数

```python
result = skill('pywencai-stock').search(
    query='沪深A股',
    page=1,           # 页码（从1开始）
    perpage=50,       # 每页条数（默认50，最大100）
    sort_key='涨跌幅', # 排序字段
    sort_order='desc', # asc/desc
    loop=False        # 是否自动翻页合并结果
)
```

## 输出格式

- 返回 `pandas.DataFrame`，可直接：
  - `result.to_csv('data.csv')`
  - `result.to_excel('data.xlsx')`
  - `result.to_json(orient='records')`
- DataFrame 包含所有问财返回的列（具体字段取决于查询内容）

## 注意事项

- ⚠️ 请勿高频调用，建议单次查询间隔 >1秒
- ⚠️ 问财接口可能随时调整，如遇错误请检查 pywencai 版本
- ⚠️ 某些查询可能需要登录Cookie（本技能使用公开接口，有限制）

## 故障排除

```bash
# 升级到最新版本
pip install -U pywencai

# 如果遇到 SSL 错误，尝试关闭验证（不推荐）
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
```

## 参考资源

- [pywencai GitHub](https://github.com/stephanj/pywencai)
- [同花顺问财](https://www.iwencai.com/)

## 版本历史

- **v1.0.0** (2025-03-07): 初始发布，封装为基础搜索技能
