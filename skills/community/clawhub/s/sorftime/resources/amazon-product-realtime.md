> 公共参考见 [`_common.md`](./_common.md)：CLI 调用模板、Domain 表、错误码、返回结构、限流约束。本文档只描述 Amazon 产品实时采集接口独有的参数与字段。


# Amazon 产品实时采集接口（5 个）

**本文件接口**：ProductRealtimeRequest、ProductRealtimeRequestStatusQuery、SimilarProductRealtimeRequest、SimilarProductRealtimeRequestStatusQuery、SimilarProductRealtimeRequestCollection

---

## 一、产品实时监控

### 1. 产品实时数据查询 (ProductRealtimeRequest)
- **接口说明**: 如果产品设定时间内未更新过，则实时抓取一次产品信息
- **消耗**: 0 request，改为消耗积分（日本站消耗2积分，其他站点1积分）
- **注意**: 实时抓取预计耗时5分钟，抓取成功后通过 ProductRequest 查询
- **请求参数**:
  | 参数 | 类型 | 必填 | 说明 |
  |------|------|------|------|
  | asin | String | 是 | 需要查询的ASIN |
  | update | Integer | 否 | 未更新则立即更新的时限（小时），默认24，有效范围1-120 |
- **返回码说明**:
  - 0: 产品已更新，可通过 ProductRequest 获取详情
  - 99: 正在实时抓取，预计5分钟，请稍后重试
  - 98: 采集失败
  - 97: ASIN不存在
  - 4: 积分余额不足
- **使用示例**:
  ```bash
  # 24小时内未更新则立即更新
  sorftime api ProductRealtimeRequest '{"asin": "B0CVM8TXHP"}' --domain 1

  # 48小时内未更新则立即更新
  sorftime api ProductRealtimeRequest '{"asin": "B0CVM8TXHP", "update": 48}' --domain 1
  ```
- **返回数据**: code 字段直接表示状态（0=产品已更新，99=采集中，98=采集失败，97=ASIN不存在，4=积分不足），无 data 字段。

---

### 2. 产品实时数据查询状态查询 (ProductRealtimeRequestStatusQuery)
- **接口说明**: 查询产品实时数据查询任务的执行状态
- **消耗请求数**: 0次
- **请求参数**:
  | 参数 | 类型 | 必填 | 说明 |
  |------|------|------|------|
  | queryDate | String | 是 | 查询日期，格式yyyy-MM-dd，返回该日期全部任务 |
- **使用示例**:
  ```bash
  sorftime api ProductRealtimeRequestStatusQuery '{"queryDate": "2024-01-15"}' --domain 1
  ```
- **返回数据**: data 为字符串数组，格式 `<ASIN>:<状态>:<完成时间>`。状态：0=查询中，1=完成，3=采集失败，4=积分不够，5=ASIN不存在。

---

## 二、图搜相似产品（消耗积分）

### 3. 图搜相似产品 (SimilarProductRealtimeRequest)
- **接口说明**: 通过产品图片实时搜索亚马逊平台上相似产品
- **消耗**: 0 request，改为消耗积分（5积分，日本站6积分）
- **注意**:
  - 建议搜索的产品在图片中比例大于80%，背景尽量干净
  - 预计耗时5分钟，预计返回20+产品
  - 仅支持 US、GB、DE、FR、IN、JP、ES、IT 站点
- **请求参数**:
  | 参数 | 类型 | 必填 | 说明 |
  |------|------|------|------|
  | image | String | 是 | 查询的图片，Base64编码 |
- **使用示例**:
  ```bash
  sorftime api SimilarProductRealtimeRequest '{"image": "BASE64_ENCODED_IMAGE"}' --domain 1
  ```
- **返回数据**: data 为 String 类型，返回任务Id（> 0 表示成功）。后续使用此Id通过 SimilarProductRealtimeRequestCollection 查询结果。

---

### 4. 图搜相似产品任务状态查询 (SimilarProductRealtimeRequestStatusQuery)
- **接口说明**: 查询图搜相似产品的任务执行状态，仅支持 domain 1,2,3,4,5,7,8,9（不支持 MX/AU/BR/SA）
- **消耗请求数**: 0次
- **请求参数**:
  | 参数 | 类型 | 必填 | 说明 |
  |------|------|------|------|
  | Update | Integer | 是 | 检查在距当前时间1-240小时内的任务状态 |
- **使用示例**:
  ```bash
  sorftime api SimilarProductRealtimeRequestStatusQuery '{"Update": 48}' --domain 1
  ```
- **返回数据**: data 为任务状态数组，每个元素包含 `taskId` (Integer) 和 `status` (Integer)，status：0=采集完成，4=积分不足，11=无采集任务，97=ASIN不存在，98=采集失败，99=采集中。

---

### 5. 图搜相似产品结果查询 (SimilarProductRealtimeRequestCollection)
- **接口说明**: 查询图搜相似产品结果
- **消耗请求数**: 0次
- **请求参数**:
  | 参数 | 类型 | 必填 | 说明 |
  |------|------|------|------|
  | taskId | String | 是 | 任务Id |
- **使用示例**:
  ```bash
  sorftime api SimilarProductRealtimeRequestCollection '{"taskId": "12345"}' --domain 1
  ```
- **返回数据**: data 为 [SimilarProductObject](./amazon-data-types.md#similarproductobject) 数组。任务不存在或未完成时返回 null。

---

## 注意事项

1. **积分消耗**: ProductRealtimeRequest 消耗积分，适合关键产品的实时监控；日本站消耗2积分，其他站点1积分
2. **图搜功能**: 仅支持8个站点（US、GB、DE、FR、IN、JP、ES、IT），且消耗积分较多（5积分，日本站6积分）
3. **实时抓取耗时**: 所有实时接口预计耗时约5分钟，返回码99表示采集中，请稍后重试
4. **图搜图片建议**: 搜索的产品在图片中比例大于80%，背景尽量干净，可提高识别准确率

---

## 常见错误

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| 4 | 积分余额不足 | 充值积分或等待下月重置 |
| 97 | ASIN不存在 | 检查ASIN是否正确 |
| 98 | 采集失败 | 稍后重试，或联系Sorftime客服 |
| 99 | 正在实时抓取 | 预计耗时5分钟，请稍后重试 |
