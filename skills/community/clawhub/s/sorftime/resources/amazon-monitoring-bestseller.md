> 公共参考见 [`_common.md`](./_common.md)：CLI 调用模板、Domain 表、错误码、返回结构、限流约束。
> 监控通用规则（period 表达式、积分消耗、站点矩阵）见 [`amazon-monitoring.md`](./amazon-monitoring.md)。
> 本文档只描述 Best Seller 榜单监控接口独有的参数与字段。


# Amazon Best Seller 榜单监控接口（4 个）

**本文件接口**：BestSellerListSubscription、BestSellerListTask、BestSellerListDelete、BestSellerListDataCollect

---

#### 1. 榜单监控任务注册 (BestSellerListSubscription)
- **接口说明**: 注册榜单监控任务，所注册的类目需先为关注类目
- **消耗**: 0 request，改为消耗积分
- **注意**:
  - 监控频率：每天1次或12次
  - top100每天10积分，top200每天20积分，top300每天30积分，top400每天40积分
  - 有些类目在对应榜单并没有足量的数据，扣取积分按任务设置而非实际数量
- **请求参数**:
  | 参数 | 类型 | 必填 | 说明 |
  |------|------|------|------|
  | nodeid | String | 是 | 需要监控的nodeid |
  | Range | Integer | 是 | 最多监控的榜单数据范围：1=top100 |
  | Period | Integer | 是 | 监控频率（见下方说明） |
  | BestSellerListType | Integer | 是 | 榜单类型（见下方说明） |
- **Period监控频率**:
  - 100: 每天1次，（北京时间）每天0点
  - 106: 每天1次，（北京时间）每天6点
  - 112: 每天1次，（北京时间）每天12点
  - 118: 每天1次，（北京时间）每天18点
  - 200: 每天12次，双数小时执行（0,2,4,6,8,10,12,14,16,18,20,22）
  - 201: 每天12次，单数小时执行（1,3,5,7,9,11,13,15,17,19,21,23）
- **BestSellerListType榜单类型**:
  - 1: New Releases
  - 3: Most Wished For
  - 4: Gift Ideas
  - 5: Best Sellers
- **使用示例**:
  ```bash
  # 监控Best Sellers榜单，top100，每天0点执行
  sorftime api BestSellerListSubscription '{"nodeid": "3743561", "Range": 1, "Period": 100, "BestSellerListType": 5}' --domain 1

  # 监控New Releases榜单，top100，每天12次（双数小时）
  sorftime api BestSellerListSubscription '{"nodeid": "3743561", "Range": 1, "Period": 200, "BestSellerListType": 1}' --domain 1

  # 监控Most Wished For榜单，top100，每天6点执行
  sorftime api BestSellerListSubscription '{"nodeid": "3743561", "Range": 1, "Period": 106, "BestSellerListType": 3}' --domain 1
  ```
- **返回**: taskId（Integer）

---

#### 2. 榜单监控任务查询 (BestSellerListTask)
- **接口说明**: 查看全部榜单监控任务
- **消耗请求数**: 0次
- **请求参数**:
  | 参数 | 类型 | 必填 | 说明 |
  |------|------|------|------|
  | pageIndex | Integer | 否 | 查询第几页，默认1 |
  | pageSize | Integer | 否 | 每页条数，最小20，默认20，最大200 |
- **使用示例**:
  ```bash
  sorftime api BestSellerListTask '{"pageIndex": 1, "pageSize": 20}' --domain 1
  ```
- **返回格式**: 二维数组
  ```json
  [["<nodeid>", "<BestSellerListType>", "<taskId>", "<Period>", "<status>", "<监控开始日期>", "<监控结束时间>"]]
  ```
  - status: 1=正常，2=已停止，9=榜单不存在
  - 当任务被删除时才有监控结束时间，否则显示为空

---

#### 3. 榜单监控任务删除 (BestSellerListDelete)
- **接口说明**: 删除已注册的榜单监控任务
- **消耗请求数**: 0次
- **请求参数**:
  | 参数 | 类型 | 必填 | 说明 |
  |------|------|------|------|
  | nodeid | String | 是 | 需要删除监控的nodeid |
  | BestSellerListType | Integer | 是 | 榜单类型：1,3,4,5 |
- **使用示例**:
  ```bash
  sorftime api BestSellerListDelete '{"nodeid": "3743561", "BestSellerListType": 5}' --domain 1
  ```
- **返回**: 删除成功返回原始taskId，否则返回-1

---

#### 4. 榜单监控数据提取 (BestSellerListDataCollect)
- **接口说明**: 查询已监控榜单的数据
- **消耗请求数**: 0次
- **请求参数**:
  | 参数 | 类型 | 必填 | 说明 |
  |------|------|------|------|
  | nodeid | String | 是 | 需要查询的nodeid |
  | BestSellerListType | Integer | 是 | 榜单类型：1,3,4,5 |
  | queryDate | String | 否 | 提取监控榜单日期，格式yyyy-MM-dd HH，最早支持从监控日期开始（最长2年） |
- **注意**:
  - 当不输入查询小时数时，默认返回当日的第一批数据
  - 当任务为每天1次时，返回自查询小时数开始6个小时内的第一批数据
  - 当任务为每天12次时，返回自查询小时数开始2个小时内的第一批数据
- **使用示例**:
  ```bash
  # 查询当日第一批数据
  sorftime api BestSellerListDataCollect '{"nodeid": "3743561", "BestSellerListType": 5}' --domain 1

  # 查询指定日期数据
  sorftime api BestSellerListDataCollect '{"nodeid": "3743561", "BestSellerListType": 5, "queryDate": "2024-01-15 00"}' --domain 1

  # 查询指定小时的数据
  sorftime api BestSellerListDataCollect '{"nodeid": "3743561", "BestSellerListType": 5, "queryDate": "2024-01-15 06"}' --domain 1
  ```
- **返回数据**: data 为 [BestSellerListItemObject](./amazon-data-types.md#bestsellerlistitemobject) 数组。
