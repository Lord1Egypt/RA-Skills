> 公共参考见 [`_common.md`](./_common.md)：CLI 调用模板、Domain 表、错误码、返回结构、限流约束。本文档只描述 Amazon 产品核心接口独有的参数与字段。

# Amazon 产品核心接口（11 个）

**本文件接口**：ProductRequest、ProductSearch、AsinSalesVolume、ProductVariationHistory、ProductReviewsCollection、ProductReviewsCollectionStatusQuery、ProductReviewsQuery、ProductSearchFromName、ASINSubscription、ASINSubscriptionQuery、ASINSubscriptionCollection

---

## 一、产品基础查询

### 1. 产品详情 (ProductRequest)
- **接口说明**: 产品（Listing）详情查询，支持单ASIN或多ASIN查询
- **消耗请求数**: 1次（多ASIN查询也是1次，最多10个ASIN）
- **请求参数**:
  | 参数 | 类型 | 必填 | 说明 |
  |------|------|------|------|
  | asin | String | 是 | 需要查询的ASIN，多asin用逗号分割，最多10个 |
  | trend | Integer | 否 | 是否包含趋势数据：1=包含（默认），2=不包含 |
  | queryTrendStartDt | String | 否 | 趋势查询起始日期，格式yyyy-MM-dd，不指定默认返回近15天 |
  | queryTrendEndDt | String | 否 | 趋势查询截止日期，格式yyyy-MM-dd |
- **注意**:
  - 当请求历史趋势超过15天时，消耗request=2
  - 趋势数据仅返回近15天，如需更多数据需指定queryTrendStartDt
- **返回数据**: 单ASIN查询返回单个 [ProductObject](./amazon-data-types.md#productobject)，多ASIN查询返回 ProductObject 数组。趋势字段（当 `trend != 2` 时返回）见数据类型定义。
- **使用示例**:
  ```bash
  # 查询单个ASIN
  sorftime api ProductRequest '{"asin": "B0CVM8TXHP"}' --domain 1

  # 查询多个ASIN（最多10个）
  sorftime api ProductRequest '{"asin": "B0CVM8TXHP,B0XXXXXXX,B0YYYYYYY"}' --domain 1

  # 查询ASIN并包含近30天趋势数据
  sorftime api ProductRequest '{"asin": "B0CVM8TXHP", "trend": 1, "queryTrendStartDt": "2024-01-01"}' --domain 1

  # 查询ASIN但不包含趋势数据（节省请求）
  sorftime api ProductRequest '{"asin": "B0CVM8TXHP", "trend": 2}' --domain 1
  ```

---

### 2. 产品搜索 (ProductSearch)
- **接口说明**: 多维度查产品
- **消耗请求数**: 5次
- **请求参数**:
  | 参数 | 类型 | 必填 | 说明 |
  |------|------|------|------|
  | queryMonth | String | 否 | 回看历史月份，格式yyyy-MM，最长支持2024年1月起2年内数据 |
  | page | Integer | 否 | 分页查询，每页最多100个产品，默认1 |
  | ASIN | String | 否 | 基于ASIN查询同类产品（注意：并非只查询这个ASIN，如果需要这个产品请调用ProductRequest接口） |
  | nodeId | String | 否 | 基于类目(nodeid)查询 |
  | brand | String | 否 | 查询品牌热销产品 |
  | sellerName | String | 否 | 基于卖家名称查询热销产品 |
  | sellerId | String | 否 | 基于卖家SellerId查询热销产品 |
  | keyword | String | 否 | 基于ABA关键词查热销产品（暂仅支持ABA关键词） |
  | attributeName | String | 否 | 基于产品标题(或产品属性)包含词查产品（将匹配标题/产品属性中包含特定词的产品） |
  | peakSellingSeason | String | 否 | 限定查询季节性产品，仅返回所查询月份的季节性产品。如指定多个月份为热卖季，使用逗号分隔',' |
  | shippingType | String | 否 | 限定发货方式查产品 |
  | priceRangeMin | Number | 否 | 限定销售价最小值（val >= 设定值）查产品 |
  | priceRangeMax | Number | 否 | 限定销售价最大值（val <= 设定值）查产品 |
  | monthSaleVolumeRangeMin | Integer | 否 | 限定月销量最小值（val >= 设定值）查产品 |
  | monthSaleVolumeRangeMax | Integer | 否 | 限定月销量最大值（val <= 设定值）查产品 |
  | onlineDateRangeMin | String | 否 | 限定上架时间起始时间查产品，日期格式为yyyy-MM-dd |
  | onlineDateRangeMax | String | 否 | 限定上架时间截止时间查产品，日期格式为yyyy-MM-dd |
  | starRangeMin | Number | 否 | 限定星级最小值查产品 |
  | starRangeMax | Number | 否 | 限定星级最大值查产品 |
  | commentCountRangeMin | Integer | 否 | 限定评论数量最小值查产品 |
  | commentCountRangeMax | Integer | 否 | 限定评论数量最大值查产品 |
  | subCategoryRankRangeMin | Integer | 否 | 限定小类排名最小值（实际排名，第1名，值为1）查产品 |
  | subCategoryRankRangeMax | Integer | 否 | 限定小类排名最大值（实际排名，第100名，值为100）查产品 |
  | variationCountRangeMin  | Integer | 否 | 限定子体数最小值查产品 |
  | variationCountRangeMax  | Integer | 否 | 限定子体数最大值查产品 |
  | categoryRankRangeMin | Integer | 否 | 限定大类最小值（实际排名，第1名，值为1）查产品 |
  | categoryRankRangeMax | Integer | 否 | 限定大类最大值（实际排名，第100名，值为100）查产品 |

- **使用示例**:
  ```bash
  # 基于ASIN查询同类产品
  sorftime api ProductSearch '{"asin": "B0CVM8TXHP"}' --domain 1

  # 基于类目查询
  sorftime api ProductSearch '{"nodeid": "3743561"}' --domain 1

  # 限定价格范围
  sorftime api ProductSearch '{"priceRangeMin": 20.0, "priceRangeMax": 50.0}' --domain 1

  # 类目+月销量+星级
  sorftime api ProductSearch '{"nodeid": "3743561", "monthSaleVolumeRangeMin": 100, "monthSaleVolumeRangeMax": 1000, "starRangeMin": 4.2, "page": 1}' --domain 1

  # 回看历史数据（2024年6月）
  sorftime api ProductSearch '{"nodeid":  "3743561", "queryMonth": "2025-06"}' --domain 1
  ```
- **注意**:
  - AU、BR、IN暂不支持回看
  - US、GB、DE支持回看全细分类目产品（"不限"模式回看）
  - 其余站点支持Top100产品回看
- **返回数据**: data 为 [ProductListObject](./amazon-data-types.md#productlistobject)，其中 `data.products` 为 [ProductSummeryObject](./amazon-data-types.md#productsummeryobject) 数组。

---

## 二、产品历史数据

### 3. 产品官方公布子体销量 (AsinSalesVolume)
- **接口说明**: 查询产品官方公布的子体销量历史数据，最早自2023-07开始
- **消耗请求数**: 1次
- **请求参数**:
  | 参数 | 类型 | 必填 | 说明 |
  |------|------|------|------|
  | asin | String | 是 | 需要查询的ASIN |
  | queryDate | String | 否 | 查询开始时间，格式yyyy-MM-dd，最早支持2023-09-01 |
  | queryEndDate | String | 否 | 查询截止时间，格式yyyy-MM-dd |
  | page | Integer | 否 | 分页查询，每页最多100条数据，默认1 |
- **使用示例**:
  ```bash
  # 查询近30日子体销量
  sorftime api AsinSalesVolume '{"asin": "B0CVM8TXHP"}' --domain 1

  # 查询指定时间段子体销量
  sorftime api AsinSalesVolume '{"asin": "B0CVM8TXHP", "queryDate": "2024-01-01", "queryEndDate": "2024-01-31"}' --domain 1
  ```
- **返回数据**: data 为 [AsinSalesVolumeObject](./amazon-data-types.md#asinsalesvolumeobject)，二维数组，每行格式：`[日期, 销量, 销量类型]`（1=周销量，2=月销量）。

---

### 4. 产品子体变化历史 (ProductVariationHistory)
- **接口说明**: 查询ASIN所有变体变化历史，最多支持近1个月数据
- **消耗请求数**: 1次
- **请求参数**:
  | 参数 | 类型 | 必填 | 说明 |
  |------|------|------|------|
  | asin | String | 是 | 需要查询的ASIN |
- **使用示例**:
  ```bash
  sorftime api ProductVariationHistory '{"asin": "B0CVM8TXHP"}' --domain 1
  ```
- **返回数据**: data 为 [ProductVariationHistoryObject](./amazon-data-types.md#productvariationhistoryobject)，二维数组，每行格式：`[记录时间, ParentASIN, 子体ASIN1, 子体ASIN2, ...]`。


---

## 三、产品评论

### 6. 实时采集产品评论 (ProductReviewsCollection)
- **接口说明**: 实时采集产品评论（不会返回评论内容，需通过 ProductReviewsQuery 拉取）
- **消耗**: 0 request，改为消耗积分
- **注意**:
  - 每成功采集10条评论=2积分
  - 每次启动至少扣2积分（即使未采得任何评论）
  - 相同产品采集成功后，2小时内不能重复采集
- **请求参数**:
  | 参数 | 类型 | 必填 | 说明 |
  |------|------|------|------|
  | asin | String | 是 | 需要采集的ASIN |
  | mode | Integer | 是 | 采集方式：0=top reviews模式，1=most recent模式 |
  | star | String | 否 | 按星级筛选，支持多选（逗号分割）：1-5星，10=消极评论(1-3星)，11=积极评论(4-5星) |
  | onlyPurchase | Integer | 是 | 是否仅采集购买过产品的用户评论：0=不限，1=仅购买用户 |
  | page | Integer | 是 | 采集页数，可选值1-10 |
- **积分计算**: 每页1积分。例如 star="1,2,3,4,5" page=10，则消耗 5×10=50 积分
- **使用示例**:
  ```bash
  # 采集top reviews，不限星级，不限购买用户，1页
  sorftime api ProductReviewsCollection '{"asin": "B0CVM8TXHP", "mode": 0, "onlyPurchase": 0, "page": 1}' --domain 1

  # 采集最近评论，仅5星，仅购买用户，5页
  sorftime api ProductReviewsCollection '{"asin": "B0CVM8TXHP", "mode": 1, "star": "5", "onlyPurchase": 1, "page": 5}' --domain 1

  # 采集消极评论（1-3星），不限购买用户，3页
  sorftime api ProductReviewsCollection '{"asin": "B0CVM8TXHP", "star": "10", "onlyPurchase": 0, "page": 3}' --domain 1

  # 采集积极评论（4-5星），不限购买用户，3页
  sorftime api ProductReviewsCollection '{"asin": "B0CVM8TXHP", "star": "11", "onlyPurchase": 0, "page": 3}' --domain 1
  ```
- **返回数据**: data 为 String 类型，返回查询任务Id（> 0 表示任务创建成功）。

---

### 7. 评论实时查询任务状态 (ProductReviewsCollectionStatusQuery)
- **接口说明**: 查询实时采集产品评论的任务执行状态
- **消耗请求数**: 0次
- **请求参数**:
  | 参数 | 类型 | 必填 | 说明 |
  |------|------|------|------|
  | asin | String | 是 | 采集评论的ASIN |
  | update | Integer | 是 | 执行采集任务距今的时间范围（小时），可选值1-240 |
- **使用示例**:
  ```bash
  # 检查48小时内的采集任务状态
  sorftime api ProductReviewsCollectionStatusQuery '{"asin": "B0CVM8TXHP", "update": 48}' --domain 1
  ```
- **返回数据**: data 为任务状态数组，每个元素包含 `taskId` (Integer) 和 `status` (Integer)，status：0=采集完成，4=积分不足，11=无采集任务，97=ASIN不存在，98=采集失败，99=采集中。

---

### 8. 产品评论查询 (ProductReviewsQuery)
- **接口说明**: 查询已收录的产品评论（如需最新评论，先通过 ProductReviewsCollection 采集）
- **消耗请求数**: 5次
- **请求参数**:
  | 参数 | 类型 | 必填 | 说明 |
  |------|------|------|------|
  | asin | String | 是 | 需要查询的ASIN |
  | querystartdt | String | 否 | 查询reviews起始时间，格式yyyy-MM-dd |
  | star | Integer | 否 | 筛选星级：1-5星，10=消极评论，11=积极评论，多选逗号分割 |
  | onlyPurchase | Integer | 否 | 是否仅采集购买用户评论：0=不限，1=仅购买用户 |
  | pageIndex | Integer | 否 | 查询第几页，默认1，每页100条数据 |
- **使用示例**:
  ```bash
  # 查询所有评论
  sorftime api ProductReviewsQuery '{"asin": "B0CVM8TXHP"}' --domain 1

  # 查询5星评论
  sorftime api ProductReviewsQuery '{"asin": "B0CVM8TXHP", "star": 5}' --domain 1

  # 查询消极评论（1-3星）
  sorftime api ProductReviewsQuery '{"asin": "B0CVM8TXHP", "star": 10}' --domain 1

  # 查询积极评论（4-5星）
  sorftime api ProductReviewsQuery '{"asin": "B0CVM8TXHP", "star": 11}' --domain 1

  # 查询指定日期后的评论
  sorftime api ProductReviewsQuery '{"asin": "B0CVM8TXHP", "querystartdt": "2024-01-01"}' --domain 1

  # 仅查询购买用户的评论
  sorftime api ProductReviewsQuery '{"asin": "B0CVM8TXHP", "onlyPurchase": 1}' --domain 1
  ```
- **返回数据**: data 为 [ReviewsObject](./amazon-data-types.md#reviewsobject) 数组，字段详见数据类型定义。

---

## 四、产品搜索与ASIN订阅

### 9. 通过产品名称搜索 (ProductSearchFromName)
- **接口说明**: 通过产品名称模糊搜索热销产品，最多返回200个产品
- **消耗请求数**: 1次
- **请求参数**:
  | 参数 | 类型 | 必填 | 说明 |
  |------|------|------|------|
  | name | String | 是 | 需要查询的产品名称，支持模糊匹配 |
- **使用示例**:
  ```bash
  # 搜索包含"water bottle"的热销产品
  sorftime api ProductSearchFromName '{"name": "water bottle"}' --domain 1
  ```
- **返回数据**: data 为 [ProductSummeryObject](./amazon-data-types.md#productsummeryobject) 数组，最多返回200个产品。

---

### 10. ASIN关注订阅 (ASINSubscription)
- **接口说明**: 注册ASIN关注，订阅后可查询ASIN的监控数据。每成功更新 1 个 ASIN 消耗 1 积分（日本站 2 积分）
- **消耗**: 0 request
- **注意**: 每次最多支持100个ASIN
- **请求参数**:
  | 参数 | 类型 | 必填 | 说明 |
  |------|------|------|------|
  | asins | String Array | 是 | 需要订阅的ASIN列表，格式 `["+,asin,1", "-,asin,1"]`（+=新增，-=删除） |
- **使用示例**:
  ```bash
  # 添加ASIN订阅
  sorftime api ASINSubscription '{"asins": ["+,B0CVM8TXHP,1", "+,B0XXXXXXX,1"]}' --domain 1

  # 删除ASIN订阅
  sorftime api ASINSubscription '{"asins": ["-,B0CVM8TXHP,1"]}' --domain 1
  ```
- **返回数据**: data 为 String 数组，已订阅的 ASIN 列表。

---

### 11. ASIN订阅查询 (ASINSubscriptionQuery)
- **接口说明**: 查询当前已订阅的所有ASIN
- **消耗请求数**: 0次
- **请求参数**: 无
- **使用示例**:
  ```bash
  sorftime api ASINSubscriptionQuery '{}' --domain 1
  ```
- **返回数据**: data 为 String 数组，已订阅的 ASIN 列表。

---

### 12. ASIN订阅数据提取 (ASINSubscriptionCollection)
- **接口说明**: 提取已订阅ASIN的产品数据摘要
- **消耗请求数**: 0次
- **请求参数**:
  | 参数 | 类型 | 必填 | 说明 |
  |------|------|------|------|
  | asins | String | 否 | 指定查询的ASIN，多个用逗号分割，不指定则返回全部订阅ASIN数据 |
- **使用示例**:
  ```bash
  # 查询全部订阅ASIN数据
  sorftime api ASINSubscriptionCollection '{}' --domain 1

  # 查询指定ASIN数据
  sorftime api ASINSubscriptionCollection '{"asins": "B0CVM8TXHP,B0XXXXXXX"}' --domain 1
  ```
- **返回数据**: data 为 String，JSON 数组格式，每个元素为 AsinSummaryObject 结构。

---

## 注意事项

1. **批量查询优化**: ProductRequest 支持一次查询最多10个ASIN，可以节省请求次数
2. **趋势数据**: 默认返回近15天，如需更多数据需指定 queryTrendStartDt 和 queryTrendEndDt
3. **评论采集**: 采集评论消耗积分，建议先评估需求再决定是否采集

---

## 常见错误

错误码定义见 [`_common.md`](./_common.md#6-完整错误码表)。

---

## 最佳实践

### 1. 批量查询ASIN
```bash
# 一次性查询多个ASIN（最多10个），节省请求次数
sorftime api ProductRequest '{"asin": "B0ASIN1,B0ASIN2,B0ASIN3,B0ASIN4,B0ASIN5"}' --domain 1
```

### 2. 竞品分析流程
```bash
# 步骤1: 基于ASIN查询同类产品
  sorftime api ProductSearch '{"asin": "B0CVM8TXHP" }' --domain 1

# 步骤2: 查询竞品的详细信息
sorftime api ProductRequest '{"asin": "B0CVM8TXHP"}' --domain 1

# 步骤3: 查询竞品的评论
sorftime api ProductReviewsQuery '{"asin": "B0CVM8TXHP"}' --domain 1

# 步骤4: 查询竞品的子体销量
sorftime api AsinSalesVolume '{"asin": "B0CVM8TXHP"}' --domain 1
```

### 3. 产品筛选
```bash
# 查找类目下月销量100-1000、4星以上、FBA发货的产品
sorftime api ProductQuery '{"query": 2, "pattern": [{"queryType": 2, "content": "3743561"}, {"queryType": 9, "content": "100,1000"}, {"queryType": 12, "content": "4,"}, {"queryType": 15, "content": "FBA"}]}' --domain 1
```

### 4. 品牌分析
```bash
# 查询Anker品牌的热销产品
sorftime api ProductQuery '{"query": 1, "queryType": 3, "pattern": "Anker"}' --domain 1
```

### 5. 季节性产品分析
```bash
# 查询1-3月为销售旺季的产品
sorftime api ProductQuery '{"query": 1, "queryType": 10, "pattern": "1,2,3"}' --domain 1
```
