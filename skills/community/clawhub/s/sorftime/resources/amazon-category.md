> 公共参考见 [`_common.md`](./_common.md)：CLI 调用模板、Domain 表、错误码、返回结构、限流约束。本文档只描述 Amazon 类目接口独有的参数与字段。

# Amazon 类目接口（5 个）

**本文件接口**：CategoryTree、CategoryRequest、CategoryProducts、CategoryTrend、CategorySearchFromName

### 1. 类目树 (CategoryTree)
- **接口说明**: 返回Best Seller类目树结构
- **消耗请求数**: 5次
- **注意**: 返回数据很大（约10MB+），建议设置较长超时时间
- **请求参数**: 无
- **使用示例**:
  ```bash
  # 获取亚马逊美国站类目树
  sorftime api CategoryTree --domain 1
  
  # 获取亚马逊英国站类目树
  sorftime api CategoryTree --domain 2
  
  # 获取亚马逊日本站类目树
  sorftime api CategoryTree --domain 7
  ```
- **返回数据**: data 为 [CategoryTreeObject](./amazon-data-types.md#categorytreeobject) 数组。

- **返回示例**:
  ```json
  {
    "data": [
      {
        "Id": 1,
        "ParentId": 0,
        "NodeId": "3743561",
        "Name": "Kitchen & Dining",
        "CNName": "厨房与餐饮",
        "URL": "https://www.amazon.com/best-sellers-kitchen-dining/zgbs/kitchen"
      }
    ]
  }
  ```

---

### 2. 类目Best Sellers (CategoryRequest)
- **接口说明**: 查询类目Best Seller Top100产品，支持最长2年历史回看
- **消耗请求数**: 
  - 当前数据：5次
  - 历史回看：每3天跨度消耗10次（天跨度向上取整）
  - 例如：查询3天消耗10 request，查询4天消耗20 request
- **注意**: 历史回看不支持站点：印度(in=5)、阿联酋(ae=11)、澳大利亚(au=12)、巴西(br=13)、沙特(sa=14)
- **请求参数**:
  | 参数 | 类型 | 必填 | 说明 |
  |------|------|------|------|
  | nodeId | String | 是 | 类目NodeId（从CategoryTree接口获取） |
  | queryStart | String | 否 | 历史查询开始时间，格式yyyy-MM-dd，最长可查近2年，天跨度3-40天 |
  | queryDate | String | 否 | 历史查询结束时间，格式yyyy-MM-dd，最近可查距当前2日前，天跨度3-40天 |
  | queryDays | Integer | 否 | 老版本兼容参数，指定queryDate后向前查询N天 |
- **使用示例**:
  ```bash
  # 查询当前Best Seller数据
  sorftime api CategoryRequest '{"nodeId": "3743561"}' --domain 1
  
  # 查询历史数据（2024-01-01至2024-01-10，共10天）
  sorftime api CategoryRequest '{"nodeId": "3743561", "queryStart": "2024-01-01", "queryDate": "2024-01-10"}' --domain 1
  
  ```
- **数据说明**:
  - 产品销量：取产品在时间范围内的最后一日统计的近30日销量
  - 如果产品的月销量极低，统一返回月销量为5

- **返回数据**: data 为 [CategoryObject](./amazon-data-types.md#categoryobject)，其中 `data.products` 为 [ProductSummeryObject](./amazon-data-types.md#productsummeryobject) 数组。

---

### 3. 类目全部热销产品 (CategoryProducts)
- **接口说明**: 查询类目下全部热销产品，对于长尾类目可返回1000+产品
- **消耗请求数**: 5次
- **请求参数**:
  | 参数 | 类型 | 必填 | 说明 |
  |------|------|------|------|
  | nodeId | String | 是 | 类目NodeId |
  | page | Integer | 否 | 分页查询，每页最多100个产品，默认1（从1开始，非0） |
- **使用示例**:
  ```bash
  # 查询第1页
  sorftime api CategoryProducts '{"nodeId": "3743561", "page": 1}' --domain 1
  
  # 查询第2页
  sorftime api CategoryProducts '{"nodeId": "3743561", "page": 2}' --domain 1
  
  # 查询第3页
  sorftime api CategoryProducts '{"nodeId": "3743561", "page": 3}' --domain 1
  ```

- **返回数据**: data 为 [ProductListObject](./amazon-data-types.md#productlistobject)，其中 `data.products` 为 [ProductSummeryObject](./amazon-data-types.md#productsummeryobject) 数组。

---

### 4. 查询市场历史趋势 (CategoryTrend)
- **接口说明**: 查询该类目市场历史趋势（近2年top100类目市场趋势）
- **消耗请求数**: 2次
- **请求参数**:
  | 参数 | 类型 | 必填 | 说明 |
  |------|------|------|------|
  | nodeId | String | 是 | 类目NodeId |
  | trendIndex | Integer | 是 | 趋势类型（0-39，见下方说明） |
- **trendIndex趋势类型说明**:
  | 值 | 趋势类型 | 单位说明 |
  |----|---------|---------|
  | 0 | 销量趋势 | - |
  | 1 | 品牌数量趋势 | - |
  | 2 | 卖家数量趋势 | - |
  | 3 | 平均售价趋势 | 当地货币最小单位（如$15.99返回1599） |
  | 4 | 平均评价数趋势 | - |
  | 5 | 平均星级趋势 | - |
  | 6 | 1个月新品占比趋势 | 百分比（如50%返回50） |
  | 7 | 3个月新品占比趋势 | 百分比 |
  | 8 | 6个月新品占比趋势 | 百分比 |
  | 9 | 亚马逊自营占比趋势 | 百分比 |
  | 10 | FBM产品数占比趋势 | 百分比 |
  | 11 | A+产品数占比趋势 | 百分比 |
  | 12 | 平均单次产品利润趋势 | 当地货币最小单位 |
  | 13 | 平均跟卖数量趋势 | - |
  | 14 | top100产品占有率趋势 | 百分比 |
  | 15 | 平均大类排名趋势 | - |
  | 16 | 1个月新品平均星级趋势 | - |
  | 17 | 3个月新品平均星级趋势 | - |
  | 18 | 6个月新品平均星级趋势 | - |
  | 19 | 1个月新品平均评价数趋势 | - |
  | 20 | 3个月新品平均评价数趋势 | - |
  | 21 | 6个月新品平均评价数趋势 | - |
  | 22 | 1个月新品最高评价数趋势 | - |
  | 23 | 3个月新品最高评价数趋势 | - |
  | 24 | 6个月新品最高评价数趋势 | - |
  | 25 | 1个月新品最低评价数趋势 | - |
  | 26 | 3个月新品最低评价数趋势 | - |
  | 27 | 6个月新品最低评价数趋势 | - |
  | 28 | 前3 Listing垄断系数趋势 | - |
  | 29 | 前5 Listing垄断系数趋势 | - |
  | 30 | 前10 Listing垄断系数趋势 | - |
  | 31 | 前20 Listing垄断系数趋势 | - |
  | 32 | 前3品牌垄断系数趋势 | - |
  | 33 | 前5品牌垄断系数趋势 | - |
  | 34 | 前10品牌垄断系数趋势 | - |
  | 35 | 前20品牌垄断系数趋势 | - |
  | 36 | 前3卖家垄断系数趋势 | - |
  | 37 | 前5卖家垄断系数趋势 | - |
  | 38 | 前10卖家垄断系数趋势 | - |
  | 39 | 前20卖家垄断系数趋势 | - |
- **使用示例**:
  ```bash
  # 查询销量趋势
  sorftime api CategoryTrend '{"nodeId": "3743561", "trendIndex": 0}' --domain 1
  
  # 查询平均售价趋势
  sorftime api CategoryTrend '{"nodeId": "3743561", "trendIndex": 3}' --domain 1
  
  # 查询前10品牌垄断系数趋势
  sorftime api CategoryTrend '{"nodeId": "3743561", "trendIndex": 34}' --domain 1
  
  # 查询前5卖家垄断系数趋势
  sorftime api CategoryTrend '{"nodeId": "3743561", "trendIndex": 37}' --domain 1
  ```
- **返回数据**: data 为 String 数组，格式 `[年月,值,年月,值,...]`。偶数下标为月份（如202010），奇数下标为对应数据值。货币类趋势（trendIndex=3,12）值为当地货币最小单位，百分比类趋势单位为百分比。

---

### 5. 通过类目名称搜索类目 (CategorySearchFromName)
- **接口说明**: 通过类目名称模糊搜索相关类目
- **消耗请求数**: 1次
- **请求参数**:
  | 参数 | 类型 | 必填 | 说明 |
  |------|------|------|------|
  | name | String | 是 | 需要查询的类目名称，支持模糊匹配 |
- **使用示例**:
  ```bash
  # 搜索包含"kitchen"的类目
  sorftime api CategorySearchFromName '{"name": "蓝牙耳机"}' --domain 1
  ```
- **返回数据**: data 为 String，JSON 格式，包含最多5个相关类目的 nodeid 和名称。

---

## 注意事项

1. **类目ID获取**: 必须先调用CategoryTree接口获取NodeId，然后才能进行其他类目查询
2. **历史回看**: 历史回看功能在部分站点不可用（印度、阿联酋、澳大利亚、巴西、沙特）
3. **天跨度限制**: 历史回看的天跨度有效范围为3-40天
4. **请求频率**: 最高10次/秒

---

## 最佳实践

### 1. 完整的类目分析流程
```bash
# 步骤1: 获取类目树，找到目标类目的NodeId
sorftime api CategoryTree --domain 1

# 步骤2: 查询该类目的Best Seller
sorftime api CategoryRequest '{"nodeId": "3743561"}' --domain 1

# 步骤3: 查询该类目的销量趋势
sorftime api CategoryTrend '{"nodeId": "3743561", "trendIndex": 0}' --domain 1

# 步骤4: 查询该类目的价格趋势
sorftime api CategoryTrend '{"nodeId": "3743561", "trendIndex": 3}' --domain 1

# 步骤5: 查询该类目的品牌垄断系数
sorftime api CategoryTrend '{"nodeId": "3743561", "trendIndex": 34}' --domain 1
```

### 2. 历史数据分析
```bash
# 查询过去10天的Best Seller数据
sorftime api CategoryRequest '{"nodeId": "3743561", "queryStart": "2024-01-01", "queryDate": "2024-01-10"}' --domain 1

# 注意：10天跨度需要消耗 10/3 向上取整 × 10 = 40 request
```

### 3. 多站点对比分析
```bash
# 美国站
sorftime api CategoryTrend '{"nodeId": "3743561", "trendIndex": 0}' --domain 1

# 英国站
sorftime api CategoryTrend '{"nodeId": "3743561", "trendIndex": 0}' --domain 2

# 德国站
sorftime api CategoryTrend '{"nodeId": "3743561", "trendIndex": 0}' --domain 3
```
