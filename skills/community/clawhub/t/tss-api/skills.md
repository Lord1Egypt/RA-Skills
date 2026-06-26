# Compass TSS API Skills

> TSS 跨链服务 API 技能文档
> Base URL: `https://tss-api.chainservice.io`
> Version: 1.0

---

## 概述

Compass TSS API 是一套跨链交易查询服务接口，提供跨链交易记录查询、链上扫描高度获取、Pending 交易列表等功能。

---

## 数据模型

### CrossData

跨链交易基础数据结构。

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `chain` | string | 链标识 | `""` |
| `chain_and_gas_limit` | string | 链及 Gas 限制 | `""` |
| `height` | integer | 区块高度 | `81507414` |
| `is_memoized` | boolean | 是否已缓存 | `false` |
| `log_index` | integer | 日志索引 | `1` |
| `order_id` | string | 订单 ID | `""` |
| `timestamp` | integer | 时间戳（Unix） | `1767097427` |
| `topic` | string | 事件主题 | `""` |
| `tx_hash` | string | 交易哈希 | `""` |

### CrossSet

跨链交易完整数据集合，描述一笔跨链交易在各链上的状态。

| 字段 | 类型 | 说明 |
|------|------|------|
| `src` | CrossData | 源链交易 |
| `relay` | CrossData | 中继链交易 |
| `relay_signed` | CrossData | 中继签名交易（前端可忽略） |
| `dest` | CrossData | 目标链交易 |
| `map_dest` | CrossData | 映射目标交易 |
| `order_id` | string | 订单 ID |
| `status` | integer | 跨链状态码 |
| `status_str` | string | 跨链状态描述 |
| `now` | integer | 当前时间戳 |

### StatusOfCross（跨链状态枚举）

| 值 | 名称 | 说明 |
|----|------|------|
| `0` | StatusOfInit | 初始化 |
| `1` | StatusOfPending | 等待处理 |
| `2` | StatusOfSend | 已发送 |
| `3` | StatusOfCompleted | 已完成 |
| `4` | StatusOfFailed | 失败 |

---

## API 接口

### 1. 获取当前扫描最高高度

根据 chainId 获取当前扫描有交易的最高区块高度。

- **Method:** `GET`
- **Path:** `/cross/chain/height`
- **Tags:** 交易记录

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `chainId` | query | string | 是 | 链 ID |

#### 响应

**200 OK**

```json
{
  "height": "string"
}
```

#### 示例

```bash
curl -X GET "https://tss-api.chainservice.io/cross/chain/height?chainId=1"
```

---

### 2. 获取高度对应的交易集群

根据 chainId 和区块高度获取该高度下的交易 orderId 集合。

- **Method:** `GET`
- **Path:** `/cross/chain/height/orders`
- **Tags:** 交易记录

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `chainId` | query | string | 是 | 链 ID（如 `1`） |
| `height` | query | string | 是 | 区块高度（如 `12245`） |

#### 响应

**200 OK**

```json
{
  "height": "string",
  "set": ["orderId_1", "orderId_2"]
}
```

#### 示例

```bash
curl -X GET "https://tss-api.chainservice.io/cross/chain/height/orders?chainId=1&height=12245"
```

---

### 3. 根据高度区间获取交易列表

根据 chainId 和起止高度查询区间内的所有跨链交易。

- **Method:** `GET`
- **Path:** `/cross/height/range/txs`
- **Tags:** 交易记录

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `chainId` | query | string | 是 | 链 ID |
| `startHeight` | query | string | 是 | 起始高度 |
| `endHeight` | query | string | 是 | 结束高度 |

#### 响应

**200 OK**

返回 `CrossSet` 数组：

```json
[
  {
    "data": {
      "src": { ... },
      "relay": { ... },
      "dest": { ... },
      "order_id": "string",
      "status": 0,
      "status_str": "string",
      "now": 0
    }
  }
]
```

#### 示例

```bash
curl -X GET "https://tss-api.chainservice.io/cross/height/range/txs?chainId=1&startHeight=1000&endHeight=2000"
```

---

### 4. 通过 orderId 获取交易记录

根据跨链订单 ID 查询完整的交易记录。

- **Method:** `GET`
- **Path:** `/cross/order`
- **Tags:** 交易记录

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `orderId` | query | string | 是 | 跨链订单 ID |

#### 响应

**200 OK**

```json
{
  "data": {
    "src": { ... },
    "relay": { ... },
    "relay_signed": { ... },
    "dest": { ... },
    "map_dest": { ... },
    "order_id": "string",
    "status": 3,
    "status_str": "completed",
    "now": 1767097427
  }
}
```

#### 示例

```bash
curl -X GET "https://tss-api.chainservice.io/cross/order?orderId=your_order_id"
```

---

### 5. 获取 Pending 交易列表

根据 chainId 获取当前处于 Pending 状态的交易列表。

- **Method:** `GET`
- **Path:** `/cross/pending/tx`
- **Tags:** 交易记录

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `chainId` | query | string | 是 | 链 ID |

#### 响应

**200 OK**

```json
{
  "txs": ["tx_hash_1", "tx_hash_2"]
}
```

#### 示例

```bash
curl -X GET "https://tss-api.chainservice.io/cross/pending/tx?chainId=1"
```

---

### 6. 通过 txHash 获取交易记录

根据交易哈希查询跨链交易记录。

- **Method:** `GET`
- **Path:** `/cross/tx`
- **Tags:** 交易记录

#### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `tx` | query | string | 是 | 交易哈希（txHash） |

#### 响应

**200 OK**

```json
{
  "data": {
    "src": { ... },
    "relay": { ... },
    "relay_signed": { ... },
    "dest": { ... },
    "map_dest": { ... },
    "order_id": "string",
    "status": 3,
    "status_str": "completed",
    "now": 1767097427
  }
}
```

#### 示例

```bash
curl -X GET "https://tss-api.chainservice.io/cross/tx?tx=0xYourTransactionHash"
```

---

## 错误码

| HTTP 状态码 | 说明 |
|------------|------|
| `200` | 请求成功 |
| `400` | 请求参数错误 |

---

## 接口总览

| # | 方法 | 路径 | 说明 |
|---|------|------|------|
| 1 | GET | `/cross/chain/height` | 获取当前扫描最高高度 |
| 2 | GET | `/cross/chain/height/orders` | 获取高度对应的交易集群 |
| 3 | GET | `/cross/height/range/txs` | 根据高度区间获取交易列表 |
| 4 | GET | `/cross/order` | 通过 orderId 获取交易记录 |
| 5 | GET | `/cross/pending/tx` | 获取 Pending 交易列表 |
| 6 | GET | `/cross/tx` | 通过 txHash 获取交易记录 |
