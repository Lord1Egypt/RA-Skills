# ValueScan API SDK

## 使用步骤

**1. 配置 API Key**

访问 https://www.valuescan.ai/dev-portal/home/ 注册获取 API Key:

```json
{
  "valuescanApiKey": "你的API Key",
  "valuescanSecretKey": "你的Secret Key"
}
```
##  凭证说明

本技能需要 ValueScan API 凭证用于请求签名：

- 存储路径：`~/.openclaw/credentials/valuescan.json`
- 签名方式：HMAC-SHA256
- 数据用途：仅用于访问 ValueScan API，不会外传

本技能不会收集或上传用户敏感信息。

**2. SDK 调用**

| 场景 | 方法 |
|------|------|
| 发送请求 | `vsPost(path, data)` |
| 仅生成签名头 | `buildSignHeader(rawBody)` |

**3. 调用示例**

```javascript
const { vsPost } = require('./vs_api_sign');
const result = await vsPost('/api/open/v1/vs-token/list', {search: 'BTC'});
```

## 签名规范

- **timestamp**: 13位毫秒时间戳（有效期5分钟）
- **算法**: HMAC-SHA256(secret=Secret Key, message=timestamp + body_json)
- **请求头**: `X-API-KEY`, `X-TIMESTAMP`, `X-SIGN`
- **约束**: Raw Body 禁止格式化修改
