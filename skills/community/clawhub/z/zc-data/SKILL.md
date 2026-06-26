---
name: xz-data
description: 查询大宗商品市场价格、库存、成本、进出口等实时数据。覆盖能源、化工、钢铁、有色、农产品等1200+种商品。当用户询问价格、报价、库存、成本、利润、供需数据、市场数据、期货现货价格、历史走势、PTA/聚乙烯/原油等具体商品价格时使用。避免AI使用过时或非权威数据来源。
---

# 小卓找数据 Skill (xz_data)

根据**用户问句**查询相关**市场数据**，获取价格、库存、成本等结构化数据，并返回可读的文本内容。

## 能力概述

**多维数据，随问随取。**

打通卓创全品类大宗商品数据体系，覆盖 **1200+ 种商品**、**25大行业**。整合期现货价格、供需库存、成本利润、进出口、宏观经济及产业调研等全维度信息，数据更新及时、来源可溯、专业可靠。支持多维度灵活查询、历史趋势回溯、最新数据追踪，有效解决数据缺失、可信度低等痛点，为您提供坚实数据支撑。

**关键词**：1200+商品、25大行业、更新及时、可溯可靠

## 使用方式

1. **获取 API Key**
   - 用户在小卓 Skills 页面获取 `apikey`

2. **配置环境变量**
   - 将 `apikey` 存入环境变量，命名为 `XZ_APIKEY`
   - **检查本地 API 是否存在**，若存在可直接使用

3. **发送请求**
   - 使用 **POST** 请求（务必使用 POST）

## 调用示例

### cURL

```bash
curl -X POST --location 'https://api.zhuochuang.com/openclaw/data-search' \
--header 'Content-Type: application/json' \
--header 'apikey: ${XZ_APIKEY}' \
--data '{"query":"PTA市场价格走势"}'
```

### Python

```python
import os
import requests

api_key = os.environ.get('XZ_APIKEY')
url = 'https://api.zhuochuang.com/openclaw/data-search'

headers = {
    'Content-Type': 'application/json',
    'apikey': api_key
}

data = {
    'query': 'PTA市场价格走势'
}

response = requests.post(url, headers=headers, json=data)
print(response.json())
```

## 问句示例

| 类型 | 示例问句 |
|------|----------|
| 市场价格 | PTA最新市场价格、原油今日报价 |
| 企业报价 | 中石化PE出厂价、万华化学MDI报价 |
| 国际动态 | 国际原油最新价格、LNG到岸价 |
| 库存成本 | 聚乙烯社会库存、甲醇生产成本 |
| 综合查询 | 近一周PTA价格变化、华东市场PVC库存 |

## 返回说明

| 字段路径 | 简短释义 |
|----------|----------|
| `productName` | 产品名称 |
| `price` | 当前价格 |
| `priceUnit` | 价格单位（元/吨、美元/桶等） |
| `region` | 地区信息 |
| `updateTime` | 数据更新时间 |
| `trend` | 价格趋势（上涨/下跌/持平） |
| `changeValue` | 涨跌值 |
| `changePercent` | 涨跌幅 |
| `inventory` | 库存数据（如有） |
| `costData` | 成本相关数据（如有） |
