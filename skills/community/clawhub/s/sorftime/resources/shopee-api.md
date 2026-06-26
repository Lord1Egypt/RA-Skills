> 公共参考见 [`_common.md`](./_common.md)：CLI 调用模板、Domain 表（Shopee 201-208）、错误码、返回结构、Shopee gzip+base64 解码说明、saleIsCorrection 字段说明、限流约束。
> 数据类型定义见 [`shopee-data-types.md`](./shopee-data-types.md)。本文档只描述 Shopee 接口独有的参数与字段。

# Shopee 接口（5 个）

**本文件接口**：CategoryTree、CategoryRequest、ProductRequest、ProductTrend、ShopRequest

### 一、类目树

#### 1. 类目树 (CategoryTree)
- **接口说明**: 返回Shopee全量类目树结构
- **消耗请求数**: 5次
- **注意**: 返回数据很大（约10MB+），建议设置较长超时时间
- **请求参数**: 无
- **使用示例**:
  ```bash
  # Shopee越南站类目树
  sorftime api CategoryTree --domain 201
  ```
- **返回数据**: data 为 [CategoryTreeObject](./shopee-data-types.md#categorytreeobject) 数组。

---

### 二、类目市场

#### 2. 类目市场 (CategoryRequest)
- **接口说明**: 查询类目Best Seller Top 500产品数据
- **消耗请求数**: 10次
- **注意**:
  - 数据范围：best seller top 500
  - 仅细分类目支持历史回看，非细分类目始终返回当前数据
- **请求参数**:
  | 参数 | 类型 | 必填 | 说明 |
  |------|------|------|------|
  | nodeId | String | 是 | 需要查找的类目Id（从CategoryTree获取） |
  | queryDate | String | 否 | 格式yyyy-MM-dd，查询历史（指定日期所处自然周）榜单数据 |
- **历史回看说明**:
  - 例如：2025-03-10，表示查询2025-03-10 ~ 2025-03-16自然周的数据
  - 仅细分类目支持，非细分类目时此参数无效
- **使用示例**:
  ```bash
  # 查询当前Best Seller数据
  sorftime api CategoryRequest '{"nodeId": "11035813"}' --domain 201

  # 查询历史数据（2025-03-10所在自然周）
  sorftime api CategoryRequest '{"nodeId": "11035813", "queryDate": "2025-03-10"}' --domain 201
  ```
- **返回数据**: data 为 [CategoryObject](./shopee-data-types.md#categoryobject)，其中 `data.products` 为 [ProductSummeryObject](./shopee-data-types.md#productsummeryobject) 数组。

---

### 三、产品类接口

#### 3. 产品详情 (ProductRequest)
- **接口说明**: 查询单个产品的详细信息
- **消耗请求数**: 1次
- **请求参数**:
  | 参数 | 类型 | 必填 | 说明 |
  |------|------|------|------|
  | productId | String | 是 | 需要查询的产品Id |
- **使用示例**:
  ```bash
  sorftime api ProductRequest '{"productId": "21584486278"}' --domain 201
  ```
- **返回数据**: data 为 [ProductSummeryObject](./shopee-data-types.md#productsummeryobject)。

---

### 四、产品历史趋势

#### 4. 产品历史趋势 (ProductTrend)
- **接口说明**: 查询产品历史趋势数据（销量、价格、评论等）
- **消耗请求数**: 2次
- **注意**: 当ProductRequest返回saleIsCorrection=true时，建议调用此接口重新拉取数据
- **请求参数**:
  | 参数 | 类型 | 必填 | 说明 |
  |------|------|------|------|
  | productId | String | 是 | 需要查询的产品Id |
- **使用示例**:
  ```bash
  sorftime api ProductTrend '{"productId": "21584486278"}' --domain 201
  ```
- **返回数据**: data 为 [ProductTrendObject](./shopee-data-types.md#producttrendobject)。趋势字段格式见数据类型定义。

---

### 五、店铺类接口（Shopee专属）

#### 5. 店铺查询 (ShopRequest)
- **接口说明**: 查询店铺的详细信息和运营数据
- **消耗请求数**: 5次
- **请求参数**:
  | 参数 | 类型 | 必填 | 说明 |
  |------|------|------|------|
  | shopId | String | 是 | 需要查询的店铺Id |
- **使用示例**:
  ```bash
  sorftime api ShopRequest '{"shopId": "123456"}' --domain 201
  ```
- **返回数据**: data 为 [ShopObject](./shopee-data-types.md#shopobject)。

---

## 注意事项

1. **请求频率**: 最高10次/秒，建议批量查询时控制速度
2. **账户配置**: 所有接口默认使用当前活跃profile的Account-SK

---

## 最佳实践

### 1. 完整的类目分析流程
```bash
# 步骤1: 获取类目树，找到目标类目的nodeId
sorftime api CategoryTree --domain 201

# 步骤2: 查询该类目的Best Seller Top 500
sorftime api CategoryRequest '{"nodeId": "11035813"}' --domain 201

# 步骤3: 查询具体产品的详细信息
sorftime api ProductRequest '{"productId": "21584486278"}' --domain 201

# 步骤4: 如果销量已校准，重新拉取趋势数据
sorftime api ProductTrend '{"productId": "21584486278"}' --domain 201
```

### 2. 店铺分析
```bash
# 查询店铺详细信息
sorftime api ShopRequest '{"shopId": "123456"}' --domain 201

# 分析店铺的Top 500产品表现
# 从返回的top500Products中获取产品ID列表
# 然后逐个查询产品详情
sorftime api ProductRequest '{"productId": "21584486278"}' --domain 201
```

### 3. 多站点对比分析
```bash
# 越南站
sorftime api CategoryRequest '{"nodeId": "11035813"}' --domain 201

# 泰国站
sorftime api CategoryRequest '{"nodeId": "11035813"}' --domain 204

# 马来西亚站
sorftime api CategoryRequest '{"nodeId": "11035813"}' --domain 205
```

### 4. 历史数据分析
```bash
# 查询指定自然周的Best Seller数据
sorftime api CategoryRequest '{"nodeId": "11035813", "queryDate": "2025-03-10"}' --domain 201
# 这将查询2025-03-10至2025-03-16自然周的数据
```

### 5. 产品趋势追踪
```bash
# 查询产品的完整历史趋势
sorftime api ProductTrend '{"productId": "21584486278"}' --domain 201

# 分析返回的趋势数据：
# - saleCountTrend: 近30日每日销量
# - priceTrend: 价格变化历史
# - reviewCountTrend: 月度评论数变化
# - starTrend: 月度星级变化
```
