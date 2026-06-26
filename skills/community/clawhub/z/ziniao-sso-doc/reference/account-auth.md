# 认证鉴权接口

> 本文件是 ziniao-sso-doc 的 Level 2 参考文档。
> 仅在需要查阅 get_app_token 或 user-login 接口的详细参数时加载。
>
> **响应说明**：以下各接口的"响应参数"均为业务层字段，实际位于网关响应的 `data` 内部。完整响应结构见 `api-guide.md` 公共响应参数。

## 获取应用 Token

> 仅在"复杂鉴权模式"下需要调用此接口。如使用"简单鉴权模式"（直接用 API Key），无需调用此接口，跳过本节即可。

### 基本信息

| 项目 | 值 |
|------|------|
| 路径 | `/auth/get_app_token` |
| 方法 | POST |
| Content-Type | application/json |

### 请求 Headers

| 参数名称 | 参数值 | 是否必须 |
|----------|--------|----------|
| Content-Type | application/json | true |
| Authorization | Bearer {API_Key} | true |

### 请求 Body

无需请求体参数。

### 响应参数

| 参数名称 | 参数说明 | 类型 |
|----------|----------|------|
| appAuthToken | 应用授权令牌 | string |
| expiresIn | 令牌有效期（秒），-1 表示永久有效 | string |

### 请求示例

```bash
curl --location 'https://sbappstoreapi.ziniao.com/openapi-router/auth/get_app_token' \
--header 'Authorization: Bearer {API_Key}' \
--header 'Content-Type: application/json' \
--data-raw ''
```

### 响应示例

```json
{
  "appAuthToken": "xxxxxxxxxxxxxxxx",
  "expiresIn": "-1"
}
```

---

## 获取指定用户登录 Token

> 需联系紫鸟在线客服申请接口权限（走特殊申请 OA 单，Boss 验证后生效）。
> 目前仅支持 Windows 版客户端。

### 基本信息

| 项目 | 值 |
|------|------|
| 路径 | `/superbrowser/rest/v1/token/user-login` |
| 方法 | POST |
| Content-Type | application/json |

### 请求 Headers

| 参数名称 | 参数值 | 是否必须 |
|----------|--------|----------|
| Content-Type | application/json | true |
| Authorization | Bearer {API_Key} | true |

### 请求 Body

| 参数名称 | 参数说明 | 是否必须 | 数据类型 |
|----------|----------|----------|----------|
| companyId | 公司 ID | false | number |
| userId | 用户 ID | false | number |

### 响应参数

> 注意：此接口业务层使用 `code`/`msg` 结构，与其他接口的 `ret`/`status`/`msg`/`count` 结构不同，判断成功应检查 `code == 0` 而非 `ret == 0`。

| 参数名称 | 参数说明 | 类型 |
|----------|----------|------|
| code | 0 表示成功 | number |
| msg | 状态描述（成功时为 "SUCCESS"） | string |
| data | 响应数据对象 | object |
| data.token | 用户登录 token（即 openapiToken） | string |
| data.expireTime | 过期时长（秒） | number |
| data.timeUnit | 时间单位（SECONDS） | string |

### 请求示例

```bash
curl --location 'https://sbappstoreapi.ziniao.com/openapi-router/superbrowser/rest/v1/token/user-login' \
--header 'Authorization: Bearer {API_Key}' \
--header 'Content-Type: application/json' \
--data-raw '{"companyId":"15393571083459","userId":"15393571087094"}'
```

### 响应示例

```json
{
  "code": 0,
  "msg": "SUCCESS",
  "data": {
    "token": "79db5b0c8d16d5d7eecded06101a7e39",
    "expireTime": 1800,
    "timeUnit": "SECONDS"
  }
}
```

### 使用说明

获取到的 token 即为 Schema URL 中的 `openapiToken` 参数，拼接格式为：

```
superbrowser://OpenStrore?storeId={账号ID}&openapiToken={token}&userId={用户ID}
```

如果本地已登录紫鸟客户端，且 userId 与本地登录用户一致，可不传 openapiToken（客户端版本 v5.290 或 v6.25 以上）。
