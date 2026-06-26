> 公共参考见 [`_common.md`](./_common.md)：CLI 调用模板、Domain 表、错误码、返回结构、限流约束。本文档只描述账户管理接口独有的参数与字段。

# 账户管理接口（3 个）

**本文件接口**：CoinQuery、CoinStream、RequestStream

> 以下 3 个接口为全平台通用，适用于 Amazon / Shopee / Walmart 任意站点。

---

### 1. 查询积分余额 (CoinQuery)
- **接口说明**: 查询当前账户积分余额。积分于每月 10 号凌晨发放，不区分站点和平台
- **消耗请求数**: 1次
- **请求参数**: 无
- **使用示例**:
  ```bash
  sorftime api CoinQuery '{}' --domain 1
  ```
- **返回数据**: data 为 [CoinQueryObject](./amazon-data-types.md#coinqueryobject)，包含 `coin`（Integer）字段，表示当前积分余额。

---

### 2. 积分流水查询 (CoinStream)
- **接口说明**: 查询积分消耗流水记录
- **消耗请求数**: 1次
- **请求参数**:
  | 参数 | 类型 | 必填 | 说明 |
  |------|------|------|------|
  | Platform | Integer | 否 | 平台筛选，0=Amazon（默认），1=Shopee，2=Walmart |
  | QueryDate | String Array | 否 | 查询时间范围：[开始日期, 结束日期]，格式 yyyy-MM-dd。默认近6个月，最长不超过近12个月 |
  | PageIndex | Integer | 否 | 分页查询，第几页，默认1 |
  | PageSize | Integer | 否 | 每页条数，默认20，最大200 |
- **使用示例**:
  ```bash
  # 查询全部积分流水
  sorftime api CoinStream '{}' --domain 1

  # 查询指定时间范围
  sorftime api CoinStream '{"QueryDate": ["2024-01-01", "2024-01-31"]}' --domain 1

  # 查询第2页
  sorftime api CoinStream '{"PageIndex": 2, "PageSize": 20}' --domain 1
  ```
- **返回数据**: data 为 String 数组，4 元素重复模式：`[任务类型, 消耗时间, 消耗积分数, 剩余积分]`。

---

### 3. 请求流水查询 (RequestStream)
- **接口说明**: 查询请求购买和消耗流水记录，request 查询不区分站点，各站点查询均为总 request 余额
- **消耗请求数**: 1次
- **请求参数**:
  | 参数 | 类型 | 必填 | 说明 |
  |------|------|------|------|
  | Platform | Integer | 否 | 平台筛选，0=Amazon（默认），1=Shopee，2=Walmart |
- **使用示例**:
  ```bash
  sorftime api RequestStream '{}' --domain 1
  ```
- **返回数据**: data 为 [RequestStreamObject](./amazon-data-types.md#requeststreamobject)，包含 `purchase` 和 `consume` 两个字段。
  - `purchase`：二维 String 数组，每行格式 `[日期, 购买金额, 剩余请求数, 过期时间]`
  - `consume`：二维 String 数组，每行格式 `[月份, 消耗请求数]`

---
