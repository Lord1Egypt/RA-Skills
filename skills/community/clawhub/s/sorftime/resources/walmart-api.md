> 公共参考见 [`_common.md`](./_common.md)：CLI 调用模板、Domain 表（Walmart domain=21）、错误码、返回结构、限流约束。
> 数据类型定义见 [`walmart-data-types.md`](./walmart-data-types.md)。本文档只描述 Walmart 类目与产品接口独有的参数与字段。

# Walmart 类目与产品接口（5 个）

**本文件接口**：CategoryTree、CategoryRequest、ProductRequest、ProductTrendRequest、ProductSalesVolume

---

## 一、类目市场类接口

### 1. 类目树 (CategoryTree)
- **接口说明**: 返回Walmart全量类目树结构
- **消耗请求数**: 5次
- **注意**:
  - 返回数据很大（约10MB+），建议设置较长超时时间
  - 可选gzip压缩参数
- **请求参数**:
  | 参数 | 类型 | 必填 | 说明 |
  |------|------|------|------|
  | gzip | Integer | 否 | 0或1，默认为0。设置为1时使用gzip压缩并返回base64字符串 |
- **使用示例**:
  ```bash
  # Walmart美国站类目树（不压缩）
  sorftime api CategoryTree --domain 21

  # 启用gzip压缩
  sorftime api CategoryTree '{"gzip": 1}' --domain 21
  ```
- **返回数据**: data 为 [CategoryTreeObject](./walmart-data-types.md#categorytreeobject) 数组。

---

### 2. 类目市场报告 (CategoryRequest)
- **接口说明**: 查询类目Best Seller Top 80产品数据
- **消耗请求数**: 5次
- **注意**: 数据范围为best seller top 80
- **请求参数**:
  | 参数 | 类型 | 必填 | 说明 |
  |------|------|------|------|
  | nodePath | String | 是 | 需要查找的类目节点路径 |
- **使用示例**:
  ```bash
  sorftime api CategoryRequest '{"nodePath": "4044_623679_1032619_5842891_9823303"}' --domain 21
  ```
- **返回数据**: data 为 [ProductSummeryObject](./walmart-data-types.md#productsummeryobject) 数组。

---

## 二、产品类接口

### 3. 产品数据查询 (ProductRequest)
- **接口说明**: 查询单个产品的详细信息
- **消耗请求数**: 1次
- **请求参数**:
  | 参数 | 类型 | 必填 | 说明 |
  |------|------|------|------|
  | productId | String | 是 | 需要查询的产品Id |
- **使用示例**:
  ```bash
  sorftime api ProductRequest '{"productId": "3319869184"}' --domain 21
  ```
- **返回数据**: data 为 [ProductSummeryObject](./walmart-data-types.md#productsummeryobject)。

---

### 4. 产品历史趋势 (ProductTrendRequest)
- **接口说明**: 查询产品历史趋势数据（销量、价格、评论、排名等）
- **消耗请求数**: 2次
- **请求参数**:
  | 参数 | 类型 | 必填 | 说明 |
  |------|------|------|------|
  | productId | String | 是 | 需要查询的产品Id |
- **使用示例**:
  ```bash
  sorftime api ProductTrendRequest '{"productId": "3319869184"}' --domain 21
  ```
- **返回数据**: data 为 [ProductTrendObject](./walmart-data-types.md#producttrendobject)。趋势字段格式见数据类型定义。

---

### 5. 产品官方公布子体销量 (ProductSalesVolume)
- **接口说明**: 查询产品官方公布的产品销量历史数据，最早自2024-01开始
- **消耗请求数**: 1次
- **请求参数**:
  | 参数 | 类型 | 必填 | 说明 |
  |------|------|------|------|
  | productId | String | 是 | 需要查询的产品Id |
  | queryDate | String | 否 | 查询开始时间（yyyy-MM-dd），最早支持2023-09-01 |
  | queryEndDate | String | 否 | 查询截止时间（yyyy-MM-dd） |
  | pageIndex | Integer | 否 | 分页查询，默认1，每页最多100条数据 |
- **注意**:
  - 默认（不传参数或参数无效时）返回近30日数据
  - 最早支持从2023年09月01日开始
- **使用示例**:
  ```bash
  # 查询近30日数据
  sorftime api ProductSalesVolume '{"productId": "3319869184"}' --domain 21

  # 查询指定时间段
  sorftime api ProductSalesVolume '{"productId": "3319869184", "queryDate": "2024-01-01", "queryEndDate": "2024-03-31"}' --domain 21
  ```
- **返回数据**: data 为二维 String 数组，每行格式 `[日期, 销量, 类型]`，其中类型 `2` 表示昨日销量。

---

## 最佳实践

### 1. 完整的类目分析流程
```bash
# 步骤1: 获取类目树
sorftime api CategoryTree --domain 21

# 步骤2: 查询类目Best Seller Top 80
sorftime api CategoryRequest '{"nodePath": "4044_623679_1032619_5842891_9823303"}' --domain 21

# 步骤3: 查询具体产品详情
sorftime api ProductRequest '{"productId": "3319869184"}' --domain 21

# 步骤4: 查询产品历史趋势
sorftime api ProductTrendRequest '{"productId": "3319869184"}' --domain 21
```

### 2. 产品销量分析
```bash
# 查询官方公布的子体销量历史
sorftime api ProductSalesVolume '{"productId": "3319869184", "queryDate": "2024-01-01", "queryEndDate": "2024-03-31"}' --domain 21
```

### 3. 产品对比分析
```bash
# 批量查询多个产品
sorftime api ProductRequest '{"productId": "prod1"}' --domain 21
sorftime api ProductRequest '{"productId": "prod2"}' --domain 21
sorftime api ProductRequest '{"productId": "prod3"}' --domain 21

# 对比它们的价格、销量、评论等指标
```
