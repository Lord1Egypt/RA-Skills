# API 使用指南

> 本文件是 ziniao-sso-doc 的 Level 2 参考文档。
> 仅在需要了解 API 基地址、公共 Headers、公共响应结构或 curl 调用示例时加载。

## Base URL

```
https://sbappstoreapi.ziniao.com/openapi-router
```

所有服务端接口路径均以此为前缀拼接。

## 公共请求 Headers

| Header | 值 | 说明 |
|--------|------|------|
| Content-Type | application/json | 所有接口统一使用 JSON 格式 |
| Authorization | Bearer {API_Key} | API Key 从开放平台自建应用获取 |

## 认证方式

支持两种鉴权模式：

### 简单鉴权模式（推荐）

1. 在紫鸟开放平台创建"卖家自研应用"
2. API 身份验证选择"简单通用模式"
3. 获取 API Key
4. 每次请求在 Header 中携带 `Authorization: Bearer {API_Key}`

无需调用 `get_app_token` 接口，直接用 API Key 即可调用所有业务接口。

### 复杂鉴权模式

1. 创建应用后获取 API Key
2. 调用 `/auth/get_app_token` 获取 appAuthToken
3. 后续请求使用 appAuthToken 进行身份验证

## 公共响应参数

所有接口的网关层返回以下统一结构：

| 参数名称 | 参数说明 | 类型 |
|----------|----------|------|
| request_id | 全局请求 ID，用于追踪定位 | string |
| code | 网关返回码，`"0"` 表示成功 | string |
| msg | 网关返回码描述 | string |
| sub_code | 业务返回码，成功时不返回 | string |
| sub_msg | 业务返回码描述，成功时不返回 | string |
| data | 业务响应参数 | object |

### 业务层响应（data 内部）

部分接口（员工查询、账号查询等）的 data 内部有二级结构：

| 参数名称 | 参数说明 | 类型 |
|----------|----------|------|
| ret | 状态码，0=成功，其他=失败 | number |
| status | `"success"` 或 `"faile"` | string |
| data | 业务数据（数组或对象） | array/object |
| msg | 错误信息 | string |
| count | 总条数 | string/number |

### 响应判断逻辑

```
1. 检查网关层 code 是否为 "0"
   ├── 否 → 打印 request_id、msg、sub_msg，检查 API Key 和权限配置
   └── 是 → 检查业务层是否成功
            ├── 否 → 打印响应获取错误原因
            └── 是 → 解析 data 获取业务数据
```

> **异常处理要求**：请求异常（包括状态码异常）时，必须将 `request_id`、`msg` 和 `sub_msg` 都打印出来，便于追踪定位问题。

## 前置准备

1. 在紫鸟开放平台注册并创建"卖家自研应用"
2. 选择鉴权模式（简单鉴权或复杂鉴权）
3. 获取 API Key
4. 申请所需权限点（如需使用 `user-login` 接口，需联系紫鸟在线客服走特殊申请 OA 单，Boss 验证后生效）
5. 配置 IP 白名单
6. 获取 companyId（调用 `/app/builtin/company` 或在开放平台首页右侧查看）
