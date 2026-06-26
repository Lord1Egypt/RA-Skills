> 公共参考见 [`_common.md`](./_common.md)：CLI 调用模板、Domain 表、错误码、返回结构、限流约束。
> 监控通用规则（period 表达式、积分消耗、站点矩阵）见 [`amazon-monitoring.md`](./amazon-monitoring.md)。
> 本文档只描述关键词监控接口独有的参数与字段。

# Amazon 关键词监控接口（5 个）

**本文件接口**：KeywordBatchSubscription、KeywordTasks、KeywordBatchTaskUpdate、KeywordBatchScheduleList、KeywordBatchScheduleDetail

---

#### 1. 关键词监控注册 (KeywordBatchSubscription)
- **接口说明**: 定时监控ASIN在关键词下的搜索排名，支持使用手机或PC监控
- **消耗**: 0 request，改为消耗积分
- **注意**: 不受关注类目限制，可监控任意关键词
- **请求参数**:
  | 参数 | 类型 | 必填 | 说明 |
  |------|------|------|------|
  | keyword | String Array | 是 | 监控关键词列表，如["kw1","kw2"] |
  | mode | Integer | 是 | 监控模式：0=电脑浏览器，1=手机浏览器 |
  | area | String | 条件性 | 监控地区邮编（见下方说明） |
  | page | Integer | 是 | 监控前N页：1,3,5,7（手机模式始终为1，返回约120+产品） |
  | period | String | 是 | 监控频率表达式：<每周哪几日>\|<每天哪些时段>\|<监控频率> |
- **area地区说明**:
  - **PC模式 (mode=0)**:
    - US: 10041(纽约), 60601(芝加哥), 94102(旧金山)
    - GB: N1P 3AA(伦敦)
    - DE: 10115(柏林)
    - FR: 75001(巴黎)
    - CA: V5K 0A1(温哥华)
    - JP: 120-0015(东京)
    - ES: 28001(马德里)
    - IT: 66030(罗马)
  - **手机模式 (mode=1)**:
    - US: 98101(西雅图)
    - GB: B10 0AB(伯明翰)
    - DE: 20095(汉堡)
    - FR: 13001(马赛)
    - CA: V5K 0A1(维多利亚)
    - JP: 550-0004(大阪)
    - ES: 08001(巴塞罗那)
    - IT: 16100(热那亚)
- **period频率表达式**: `<每周哪几日>\|<每天哪些时段>\|<监控频率>`
  - `<每周哪几日>`: 1-7（逗号分割，1=周一，7=周日）
  - `<每天哪些时段>`: 1-6（每个时段4小时，北京时区）
    - 1: 1-4点, 2: 5-8点, 3: 9-12点, 4: 13-16点, 5: 17-20点, 6: 21-0点
  - `<监控频率>`:
    - 1: 时段内任意时刻一次
    - 11-14: 时段内第1-4个时间刻度执行（可能因任务量过多而失败）
    - 2: 时段内每小时1次
    - 3: 时段内每2小时1次（随机双数或单数）
    - 31: 时段内单数小时执行，共2次（可能因任务量过多而失败）
    - 32: 时段内双数小时执行，共2次（可能因任务量过多而失败）
- **使用示例**:
  ```bash
  # 周一至周五，每天5-8点和9-12点，每个时段执行一次，监控前3页，PC模式（纽约）
  sorftime api KeywordBatchSubscription '{"keyword": ["power bank"], "mode": 0, "area": "10041", "page": 3, "period": "1,2,3,4,5|2,3|1"}' --domain 1

  # 每天全天候，每小时监控1次，手机模式（西雅图）
  sorftime api KeywordBatchSubscription '{"keyword": ["power bank"], "mode": 1, "page": 1, "period": "1,2,3,4,5,6,7|1,2,3,4,5,6|2"}' --domain 1

  # 每天0-4点，每2小时监控一次，PC模式（伦敦），监控首页
  sorftime api KeywordBatchSubscription '{"keyword": ["power bank"], "mode": 0, "area": "N1P 3AA", "page": 1, "period": "1,2,3,4,5,6,7|1|3"}' --domain 2
  ```
- **返回**: `["keyword:taskId", ...]`，taskId=-999表示注册失败（时段内任务过多）

---

#### 2. 关键词任务查询 (KeywordTasks)
- **接口说明**: 查看全部有效的（非删除的）关键词监控任务
- **消耗请求数**: 0次
- **请求参数**:
  | 参数 | 类型 | 必填 | 说明 |
  |------|------|------|------|
  | pageIndex | Integer | 否 | 查询第几页，默认1 |
  | pageSize | Integer | 否 | 每页条数，最小20，默认20，最大200 |
  | taskid | String | 否 | 如需指定taskid查询，多个taskid用逗号分割 |
  | keyword | String | 否 | 模糊匹配keyword |
- **使用示例**:
  ```bash
  # 查询所有任务
  sorftime api KeywordTasks '{"pageIndex": 1, "pageSize": 20}' --domain 1

  # 查询指定taskid
  sorftime api KeywordTasks '{"taskid": "12345,12346"}' --domain 1

  # 模糊匹配keyword
  sorftime api KeywordTasks '{"keyword": "power"}' --domain 1
  ```
- **返回数据**: data 为 [KeywordTaskObject](./amazon-data-types.md#keywordtaskobject) 数组。

---

#### 3. 修改关键词监控任务 (KeywordBatchTaskUpdate)
- **接口说明**: 修改关键词任务（暂停、启动、删除、修改设置）
- **消耗请求数**: 0次
- **请求参数**:
  | 参数 | 类型 | 必填 | 说明 |
  |------|------|------|------|
  | taskId | Integer | 是 | 关键词监控任务Id |
  | update | Integer | 是 | 0=修改设置，1=暂停，2=启动，9=删除 |
  | mode | Integer | 条件性 | update=0时有效：0=PC，1=手机 |
  | area | String | 条件性 | update=0时有效，地区邮编 |
  | page | Integer | 条件性 | update=0时有效：1,3,5,7 |
  | period | String | 条件性 | update=0时有效，频率表达式 |
- **使用示例**:
  ```bash
  # 暂停任务
  sorftime api KeywordBatchTaskUpdate '{"taskId": 12345, "update": 1}' --domain 1

  # 启动任务
  sorftime api KeywordBatchTaskUpdate '{"taskId": 12345, "update": 2}' --domain 1

  # 删除任务
  sorftime api KeywordBatchTaskUpdate '{"taskId": 12345, "update": 9}' --domain 1

  # 修改任务设置
  sorftime api KeywordBatchTaskUpdate '{"taskId": 12345, "update": 0, "mode": 0, "area": "10041", "page": 3, "period": "1,2,3,4,5|2,3|1"}' --domain 1
  ```
- **返回**: taskId > 0 表示成功，-999表示修改失败（时段内任务过多）

---

#### 4. 查询关键词监控任务执行批次 (KeywordBatchScheduleList)
- **接口说明**: 查询关键词监控全部执行任务批次
- **消耗请求数**: 0次
- **请求参数**:
  | 参数 | 类型 | 必填 | 说明 |
  |------|------|------|------|
  | TaskId | Integer | 是 | 关键词监控任务Id |
  | queryDate | String | 否 | 格式yyyy-MM-dd，默认查询全部，指定则查询该日期到最近的数据 |
- **使用示例**:
  ```bash
  # 查询全部批次
  sorftime api KeywordBatchScheduleList '{"TaskId": 12345}' --domain 1

  # 查询指定日期后的批次
  sorftime api KeywordBatchScheduleList '{"TaskId": 12345, "queryDate": "2024-01-15"}' --domain 1
  ```
- **返回数据**: data 为 [KeywordBatchScheduleObject](./amazon-data-types.md#keywordbatchscheduleobject) 字符串数组，格式 `<执行时间yyyyMMddHHmm>:<批次Id>:<状态>:<完成时间>`。

---

#### 5. 提取关键词监控产品列表详细数据 (KeywordBatchScheduleDetail)
- **接口说明**: 提取某次关键词监控搜索结果全部ASIN列表数据
- **消耗请求数**: 0次
- **请求参数**:
  | 参数 | 类型 | 必填 | 说明 |
  |------|------|------|------|
  | ScheduelId | String | 是 | 批次任务Id，支持多任务Id查询（逗号分割），最多20个 |
- **使用示例**:
  ```bash
  # 查询单个批次
  sorftime api KeywordBatchScheduleDetail '{"ScheduelId": "batch123"}' --domain 1

  # 查询多个批次（最多20个）
  sorftime api KeywordBatchScheduleDetail '{"ScheduelId": "batch123,batch124,batch125"}' --domain 1
  ```
- **返回数据**: data 为 [KeywordBatchScheduleDetailObject](./amazon-data-types.md#keywordbatchscheduledetailobject) CSV格式字符串数组，每行包含asin、主图链接、产品标题、曝光类型、标志、曝光排名等20个字段。
