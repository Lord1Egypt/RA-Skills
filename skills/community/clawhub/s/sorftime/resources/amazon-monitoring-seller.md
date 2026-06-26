> 公共参考见 [`_common.md`](./_common.md)：CLI 调用模板、Domain 表、错误码、返回结构、限流约束。
> 监控通用规则（period 表达式、积分消耗、站点矩阵）见 [`amazon-monitoring.md`](./amazon-monitoring.md)。
> 本文档只描述跟卖监控接口独有的参数与字段。

# Amazon 跟卖监控接口（5 个）

**本文件接口**：ProductSellerSubscription、ProductSellerTasks、ProductSellerTaskUpdate、ProductSellerTaskScheduleList、ProductSellerTaskScheduleDetail

---

#### 1. 跟卖&库存监控注册 (ProductSellerSubscription)
- **接口说明**: 定时监控ASIN的跟卖卖家（最多前30个卖家）
- **消耗**: 0 request，改为消耗积分
- **注意**:
  - 每个ASIN每次监控消耗2积分（日本站4积分）
  - 启用库存检查时，额外消耗1积分（日本站2积分）
- **请求参数**:
  | 参数 | 类型 | 必填 | 说明 |
  |------|------|------|------|
  | asin | String | 是 | 需要监控的ASIN |
  | checkstock | Integer | 否 | 0=不检查库存（默认），1=检查库存 |
  | period | String | 是 | 监控频率表达式：<每周哪几日>\|<每天哪些时段>\|<监控频率> |
- **period频率表达式**: 同关键词监控
- **使用示例**:
  ```bash
  # 不检查库存，周一至周五，每天5-8点和9-12点，每个时段执行一次
  sorftime api ProductSellerSubscription '{"asin": "B0CVM8TXHP", "checkstock": 0, "period": "1,2,3,4,5|2,3|1"}' --domain 1

  # 检查库存，每天全天候，每小时监控1次
  sorftime api ProductSellerSubscription '{"asin": "B0CVM8TXHP", "checkstock": 1, "period": "1,2,3,4,5,6,7|1,2,3,4,5,6|2"}' --domain 1

  # 不检查库存，每天0-4点，每2小时监控一次
  sorftime api ProductSellerSubscription '{"asin": "B0CVM8TXHP", "checkstock": 0, "period": "1,2,3,4,5,6,7|1|3"}' --domain 1
  ```
- **返回**: `["asin:taskId", ...]`

---

#### 2. 跟卖&库存监控任务查询 (ProductSellerTasks)
- **接口说明**: 查看全部有效的（非删除的）跟卖监控任务
- **消耗请求数**: 0次
- **请求参数**:
  | 参数 | 类型 | 必填 | 说明 |
  |------|------|------|------|
  | pageIndex | Integer | 否 | 查询第几页，默认1 |
  | pageSize | Integer | 否 | 每页条数，最小20，默认20，最大200 |
- **使用示例**:
  ```bash
  sorftime api ProductSellerTasks '{"pageIndex": 1, "pageSize": 20}' --domain 1
  ```
- **返回数据**: data 为 [ProductSellerTaskObject](./amazon-data-types.md#productsellertaskobject) 数组。

---

#### 3. 修改跟卖&库存监控任务 (ProductSellerTaskUpdate)
- **接口说明**: 修改跟卖监控任务（暂停、启动、删除、修改设置）
- **消耗请求数**: 0次
- **请求参数**:
  | 参数 | 类型 | 必填 | 说明 |
  |------|------|------|------|
  | taskId | Integer | 是 | 任务Id |
  | update | Integer | 是 | 0=修改设置，1=暂停，2=启动，9=删除 |
  | period | String | 条件性 | update=0时有效，频率表达式 |
- **使用示例**:
  ```bash
  # 暂停任务
  sorftime api ProductSellerTaskUpdate '{"taskId": 12345, "update": 1}' --domain 1

  # 启动任务
  sorftime api ProductSellerTaskUpdate '{"taskId": 12345, "update": 2}' --domain 1

  # 删除任务
  sorftime api ProductSellerTaskUpdate '{"taskId": 12345, "update": 9}' --domain 1

  # 修改任务设置
  sorftime api ProductSellerTaskUpdate '{"taskId": 12345, "update": 0, "period": "1,2,3,4,5|2,3|1"}' --domain 1
  ```
- **返回数据**: data 为 Integer，> 0 表示修改成功（返回 taskId），-999 表示修改失败（时段内任务过多）。

---

#### 4. 查询跟卖&库存监控任务执行批次 (ProductSellerTaskScheduleList)
- **接口说明**: 查询跟卖监控全部执行任务批次
- **消耗请求数**: 0次
- **请求参数**:
  | 参数 | 类型 | 必填 | 说明 |
  |------|------|------|------|
  | TaskId | Integer | 是 | 任务Id |
- **使用示例**:
  ```bash
  sorftime api ProductSellerTaskScheduleList '{"TaskId": 12345}' --domain 1
  ```
- **返回数据**: data 为字符串数组，格式 `<执行时间yyyyMMddHHmm>:<批次Id>`。

---

#### 5. 提取跟卖&库存监控执行结果详细数据 (ProductSellerTaskScheduleDetail)
- **接口说明**: 提取某次跟卖监控结果数据
- **消耗请求数**: 0次
- **请求参数**:
  | 参数 | 类型 | 必填 | 说明 |
  |------|------|------|------|
  | ScheduelId | String | 是 | 批次任务Id |
- **使用示例**:
  ```bash
  sorftime api ProductSellerTaskScheduleDetail '{"ScheduelId": "batch123"}' --domain 1
  ```
- **返回数据**: data 为 [ProductSellerScheduleDetailObject](./amazon-data-types.md#productsellerscheduledetailobject) CSV格式字符串数组，每行格式：`<采集时间>,<asin>,<卖家名称>,<卖家ID>,<是否buybox>,<发货方式>,<类型>,<售价>,<库存>,<是否限购>`。
