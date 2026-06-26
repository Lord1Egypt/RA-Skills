# 区块链API服务文档

## 接口地址及配置

| 环境 | 接口请求地址 |
|------|-------------|
| 测试环境 | `https://test-apisix-gateway.shuzhi.shuqinkeji.cn` |

## 认证方式

所有接口使用 HMAC-SHA256 签名认证，请求头需包含：

| 参数名称 | 说明 | 必须 |
|----------|------|------|
| X-HMAC-ACCESS-KEY | 应用 appKey | 是 |
| X-APP-PRODUCT-ID | 应用产品标识 | 是 |
| X-HMAC-ALGORITHM | 固定值：hmac-sha256 | 是 |
| X-HMAC-SIGNATURE | 全局签名 | 是 |
| X-HMAC-DIGEST | 请求体 body 签名 | 是 |
| Date | GMT格式时间 | 是 |

## 签名算法

### 全局签名（X-HMAC-SIGNATURE）

```
signingString = HTTP Method + \n + URI + \n + "" + \n + appKey + \n + Date + \n
X-HMAC-SIGNATURE = Base64(HMAC-SHA256(appSecret, signingString))
```

### Body签名（X-HMAC-DIGEST）

```
X-HMAC-DIGEST = Base64(HMAC-SHA256(appSecret, body))
```

---

## 接口列表

### 1. 上链接口

- **接口地址**: `POST /2036009920811413506`
- **产品标识**: 需配置
- **描述**: 对数据进行上链操作

**请求参数**:

| 参数名 | 类型 | 说明 | 必填 |
|--------|------|------|------|
| data | string | 业务数据（JSON字符串） | 是 |
| requestId | string | 请求ID | 是 |
| business | array | 业务名，如 `["EVIDENCE_PRESERVATION"]` | 否 |
| source | array | 来源，如 `["BQ_INTERNATIONAL"]` | 否 |
| extension | array | 扩展内容 | 否 |

**请求示例**:
```json
{
  "business": ["EVIDENCE_PRESERVATION"],
  "data": "{\"ano\":\"BQ912612831273123\",\"sha256\":\"868ac2385cf0b98803ae89cf3dc204e7b97b80dbf0559de0fd0740a3402c8f6a\"}",
  "requestId": "d7c8c267a9fe4ef1b92b9ed17b0a420d",
  "source": ["BQ_INTERNATIONAL"]
}
```

**响应参数**:

| 参数名 | 类型 | 说明 |
|--------|------|------|
| code | int | 状态码 |
| msg | string | 错误提示信息 |
| data.index | string | 交易索引号 |

**响应示例**:
```json
{
  "code": 200,
  "data": {
    "code": 0,
    "data": {
      "index": "d670b1db-926c-4e71-bf65-92df6c3b8aeb"
    },
    "msg": "success"
  },
  "requestId": "f38e9880b5b4c5bd5dfae32973c2c850",
  "message": "成功"
}
```

---

### 2. 批量查询上链结果

- **接口地址**: `POST /2036010888269574146`
- **产品标识**: 需配置
- **描述**: 批量查询上链结果

**请求参数**:

| 参数名 | 类型 | 说明 | 必填 |
|--------|------|------|------|
| index_list | array[string] | 交易索引号列表 | 是 |

**请求示例**:
```json
{
  "index_list": [
    "d670b1db-926c-4e71-bf65-92df6c3b8aeb"
  ]
}
```

**响应参数**:

| 参数名 | 类型 | 说明 |
|--------|------|------|
| code | int | 状态码 |
| msg | string | 错误提示消息 |
| data | array | 业务数据 |
| data[].anchor_data | object | 请求参数 |
| data[].anchor_data.business | array | 业务名 |
| data[].anchor_data.source | array | 来源 |
| data[].anchor_data.data | string | 业务数据（存证数据） |
| data[].anchor_data.requestId | string | 请求ID |
| data[].chain_results | array | 上链结果 |
| data[].chain_results[].index | string | 索引号 |
| data[].chain_results[].chain | string | 链名 |
| data[].chain_results[].hash | string | 交易哈希 |
| data[].chain_results[].block_hash | string | 区块哈希 |
| data[].chain_results[].height | int | 区块高度 |
| data[].chain_results[].status | int | 上链状态 |

**状态码说明**:

| 值 | 说明 |
|----|------|
| 0 | 上链失败 |
| 1 | 上链成功 |
| 2 | 等待上链 |

**响应示例**:
```json
{
  "code": 200,
  "data": {
    "code": 0,
    "data": [
      {
        "anchor_data": {
          "business": ["EVIDENCE_PRESERVATION"],
          "source": ["BQ_INTERNATIONAL"],
          "data": "{\"ano\":\"BQ912612831273123\",\"sha256\":\"868ac2385cf0b98803ae89cf3dc204e7b97b80dbf0559de0fd0740a3402c8f6a\"}",
          "extension": null,
          "requestId": "d7c8c267a9fe4ef1b92b9ed17b0a420d"
        },
        "chain_results": [
          {
            "index": "d670b1db-926c-4e71-bf65-92df6c3b8aeb",
            "chain": "tritium",
            "hash": "0xfd91f74bd2406bae4c42403cf6df23a64f48f38bd0da4870f9bee16bba83e0df",
            "block_hash": "0x97a50c249e9ffc525ff7c52cc909d9908fd883d51fe79309d5db5521110f01d4",
            "height": 17036614,
            "status": 1
          },
          {
            "index": "d670b1db-926c-4e71-bf65-92df6c3b8aeb",
            "chain": "conflux",
            "hash": "0xccae9154575489094b3e7bf1376d644c0a402526692f4601178db232133cf6ef",
            "block_hash": "0xba9564bbc9f47d24823d53eb311bc0c83a82ed27e353eb9dd094833f37a04faa",
            "height": 247138655,
            "status": 1
          }
        ]
      }
    ],
    "msg": "success"
  },
  "requestId": "f38e9880b5b4c5bd5dfae32973c2c850",
  "message": "成功"
}
```

---

## 链类型

| 值 | 说明 |
|----|------|
| tritium | Tritium 链 |
| conflux | Conflux 链 |

---

## 服务响应状态码

| 状态码 | 说明 |
|--------|------|
| 0 | 成功 |
| 500 | 程序异常 |

---

## 全局响应格式

```json
{
  "code": 200,
  "message": "成功",
  "requestId": "xxx",
  "data": {}
}
```

- `code`: 200 表示请求成功
- `data.code`: 0 表示服务成功