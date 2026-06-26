# API 调用指南

> 本文件是 ziniao-erp-api-doc 的 Level 2 参考文档。
> 仅在需要了解认证方式、请求构造方法、代码示例或常见错误时加载。

## 概述

紫鸟开放平台使用"简单通用模式"进行 API 认证，通过 API Key 作为 Bearer Token 传递。

## 1. 获取 companyId（紫鸟企业ID）

在开放平台首页右侧可获取紫鸟企业ID（即 companyId），几乎所有接口都需要传此参数。

## 2. 获取 API Key

前提：在紫鸟开放平台创建"卖家自研应用"，API 身份验证方式选择**简单通用模式**。在控制台中可以找到 API Key。

## 3. 配置 IP 白名单

在紫鸟开放平台的**应用管理**中，点击【设置】进入该应用的【应用概览】页面，点击【安全中心】下的【IP 白名单设置】，添加调用接口的服务器 IP。建议使用一台 IP 固定的服务器发起 API 请求。

## 4. 构造请求头

```
Authorization: Bearer {你的API_Key}
Content-Type: application/json
```

`Bearer` 和 API Key 之间必须有一个空格。

## 5. 请求地址

Base URL：`https://sbappstoreapi.ziniao.com/openapi-router`

完整请求地址 = Base URL + 接口路径。例如：
`https://sbappstoreapi.ziniao.com/openapi-router/superbrowser/rest/v1/erp/store/list`

## 6. 响应结构

### 网关层（外层）

| 字段 | 类型 | 说明 |
|------|------|------|
| request_id | string | 全局请求ID |
| code | string | "0" 表示成功 |
| msg | string | 返回码描述 |
| sub_code | string | 业务返回码（成功时不返回） |
| sub_msg | string | 业务返回码描述（成功时不返回） |
| data | object | 业务响应参数 |

### 业务层（data 内部）

| 字段 | 类型 | 说明 |
|------|------|------|
| ret | number | 0 成功，其他失败 |
| status | string | "success" 或 "faile" |
| data | array/object | 业务数据（部分接口有） |
| msg | string | 错误信息 |
| count | number | 列表查询时的总条数 |
| 其他字段 | - | 部分接口的业务字段直接在此层级 |

> **关键提醒**：业务数据位置因接口而异，不要假设所有业务数据都在 `data` 字段中。各 reference 文件对每个接口标注了"响应 data"或"响应"——"响应 data"表示数据在业务层的 data 字段中；"响应"后直接列出的字段（如 id、password）表示它们与 ret/status 同级，直接位于业务层根级。

## 7. 代码示例

### Java（OkHttp）

```java
OkHttpClient client = new OkHttpClient().newBuilder().build();
MediaType mediaType = MediaType.parse("application/json");
RequestBody body = RequestBody.create(mediaType, "{\"companyId\": 123456}");
Request request = new Request.Builder()
  .url("https://sbappstoreapi.ziniao.com/openapi-router/superbrowser/rest/v1/erp/store/list")
  .method("POST", body)
  .addHeader("Authorization", "Bearer 你的API_Key")
  .addHeader("Content-Type", "application/json")
  .build();
Response response = client.newCall(request).execute();
```

### Python（requests）

```python
import requests, json
url = "https://sbappstoreapi.ziniao.com/openapi-router/superbrowser/rest/v1/erp/store/list"
headers = {"Authorization": "Bearer 你的API_Key", "Content-Type": "application/json"}
response = requests.post(url, headers=headers, data=json.dumps({"companyId": 123456}))
print(response.json())
```

### JavaScript（Fetch）

```javascript
fetch("https://sbappstoreapi.ziniao.com/openapi-router/superbrowser/rest/v1/erp/store/list", {
  method: "POST",
  headers: { "Authorization": "Bearer 你的API_Key", "Content-Type": "application/json" },
  body: JSON.stringify({ companyId: 123456 }),
})
  .then(r => r.json()).then(console.log).catch(console.error);
```

## 8. 常见问题

**401 错误**：检查 API Key 是否正确、Authorization 格式是否含空格、接口是否支持通用模式、应用是否已申请对应权限点。

**code 非 "0"**：请求未到达业务层，通常是认证或权限问题。

**ret 非 0**：业务操作失败，读取 msg 或 sub_msg 获取错误详情。
