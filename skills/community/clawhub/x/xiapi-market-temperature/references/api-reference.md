# API 参考文档

本文档详细介绍市场温度分析的 HTTP API 接口。

## API 概述

**基础 URL**：`https://daxiapi.com`

**认证方式**：Bearer Token（在请求头中添加 Authorization）

## 接口详情

### 获取市场温度数据

**接口路径**：`/coze/get_market_temp`

**请求方式**：`GET`

**请求头**：

```http
Authorization: Bearer YOUR_TOKEN_FROM_DAXIAPI
Content-Type: application/json
```

**请求参数**：无

**请求示例**：

```bash
curl -X GET \
  https://daxiapi.com/coze/get_market_temp \
  -H "Authorization: Bearer YOUR_TOKEN_FROM_DAXIAPI" \
  -H "Content-Type: application/json"
```

**响应字段**：

| 字段             | 类型   | 说明           | 取值范围  |
| ---------------- | ------ | -------------- | --------- |
| date             | string | 交易日期       | YYYY-MM-DD |
| valuation_temp   | number | 估值温度       | 0-100     |
| fear_greed_index | number | 恐贪指数       | 0-100     |
| trend_temp       | number | 趋势温度       | 0-100     |
| momentum_temp    | number | 动量温度       | 0-100     |

**成功响应示例**：

```json
[
  {
    "date": "2025-01-15",
    "valuation_temp": 45,
    "fear_greed_index": 25,
    "trend_temp": 35,
    "momentum_temp": 30
  },
  {
    "date": "2025-01-14",
    "valuation_temp": 45,
    "fear_greed_index": 28,
    "trend_temp": 33,
    "momentum_temp": 32
  }
]
```

**说明**：返回最近 20 个交易日的数据，最新日期在前。

## 错误响应

### 错误码说明

| 错误码 | 说明               | 原因                       |
| ------ | ------------------ | -------------------------- |
| 400    | Bad Request        | 请求参数错误               |
| 401    | Unauthorized       | Token 无效或缺失           |
| 403    | Forbidden          | 无权限访问                 |
| 404    | Not Found          | API 不存在                 |
| 429    | Too Many Requests  | 请求频率超限               |
| 500    | Internal Error     | 服务器内部错误             |

### 错误响应格式

```json
{
  "error": "Unauthorized",
  "message": "Invalid or missing API token",
  "code": 401
}
```

## 认证说明

### Token 获取

1. 访问 [daxiapi.com](https://daxiapi.com) 并登录
2. 进入个人中心或会员中心
3. 开通 API Token 功能
4. 获取生成的 Token

### Token 使用

**方式一：请求头（推荐）**

```http
Authorization: Bearer YOUR_TOKEN_FROM_DAXIAPI
```

**方式二：URL 参数**

```http
GET /coze/get_market_temp?token=YOUR_TOKEN_FROM_DAXIAPI
```

## 限流说明

**请求频率限制**：具体限制请参考大虾皮网站说明

**处理建议**：

- 避免频繁调用
- 收到 429 错误后等待 30-60 秒
- 使用缓存减少重复请求

## 数据更新时间

- **更新频率**：每日收盘后
- **更新时间**：通常在 15:30-16:30 之间
- **非交易日**：数据不更新，返回最近交易日的数据

## 使用示例

### Python 示例

```python
import requests

url = "https://daxiapi.com/coze/get_market_temp"
headers = {
    "Authorization": "Bearer YOUR_TOKEN_FROM_DAXIAPI",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Error: {response.status_code}")
    print(response.text)
```

### JavaScript 示例

```javascript
const fetch = require('node-fetch');

const url = 'https://daxiapi.com/coze/get_market_temp';
const headers = {
  'Authorization': 'Bearer YOUR_TOKEN_FROM_DAXIAPI',
  'Content-Type': 'application/json'
};

fetch(url, { headers })
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));
```

## 最佳实践

### DO ✅

1. 使用 HTTPS 协议
2. 在请求头中传递 Token
3. 处理错误响应和异常情况
4. 检查数据更新时间

### DON'T ❌

1. 不要在 URL 中明文传递 Token（不安全）
2. 不要忽略错误响应
3. 不要假设数据总是最新
4. 不要频繁调用触发限流

## 相关文档

- [CLI 命令参考](cli-commands.md)
- [Token 配置指南](token-setup.md)
- [字段说明](field-descriptions.md)
