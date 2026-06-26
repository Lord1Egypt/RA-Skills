---
name: uctoo-api-skill
description: 完整的 uctoo 后端 API 集成技能。将自然语言请求转换为 uctoo-backend API 调用，支持用户管理、产品管理、订单管理、登录认证等功能。使用时用户提及 "uctoo"、"后端API"、"用户管理"、"产品"、"订单"、"登录"、"认证" 等关键词时，你应该直接使用 http_request 工具发起实际的 API 请求。
license: MIT
compatibility: 需要网络访问 uctoo 后端 API
metadata:
  author: UCToo Team
  version: "7.0.0"
  category: api-integration
allowedTools:
---

# UCTOO API Skill - 后端 API 集成技能

## 概述

**本技能指导你使用框架内置的 `http_request` 工具来发起 HTTP 请求。**

**当用户请求 uctoo 相关的 API 操作时，你必须：**
1. 分析用户需求，确定要调用哪个 API 端点
2. **直接调用 `http_request` 工具发起 HTTP 请求**
3. 将响应结果返回给用户

**⚠️ 禁止事项：**
- ❌ 不要调用 `uctoo-api-skill` 工具（这是技能文档，不是工具）
- ✅ 直接使用 `http_request` 工具

## 🎉 自动 Token 管理（重要）

**系统已实现自动 Token 管理机制，你无需手动处理认证！**

### 自动管理功能
1. **自动保存**：当登录接口返回 `access_token` 时，系统会自动保存到会话中
2. **自动注入**：后续请求会自动在 headers 中添加 `Authorization: Bearer {token}`
3. **无需手动传递**：你不需要在请求中手动添加 Authorization header

### 你只需要做的事
- 调用登录接口完成登录
- 后续请求直接调用即可，系统会自动处理认证

## API 基础配置

**API 基础地址**：`https://javatoarktsapi.uctoo.com`

**完整 URL 格式**：`{基础地址}{API路径}`
- 示例：`https://javatoarktsapi.uctoo.com/api/uctoo/auth/login`

## http_request 工具参数格式

**工具名称**：`http_request`

**参数说明：**

| 参数 | 必需 | 类型 | 说明 |
|------|------|------|------|
| method | 是 | string | HTTP 方法：GET、POST、PUT、DELETE |
| url | 是 | string | 完整的请求 URL |
| headers | 否 | string | JSON 字符串格式的请求头（可选，系统会自动注入 Authorization） |
| body | 否 | string | JSON 字符串格式的请求体（POST/PUT 需要） |

**⚠️ 重要：headers 和 body 参数必须是 JSON 字符串格式！**

## 常用 API 端点

### 认证相关

| 端点 | 方法 | 说明 | 需要认证 |
|------|------|------|----------|
| `/api/uctoo/auth/login` | POST | 用户登录 | 否 |
| `/api/uctoo/auth/signin` | POST | 用户登录（带验证码） | 否 |
| `/api/uctoo/auth/logout` | GET | 用户登出 | 自动 |
| `/api/uctoo/auth/me` | GET | 获取当前用户信息 | 自动 |

### Entity 相关

| 端点 | 方法 | 说明 | 需要认证 |
|------|------|------|----------|
| `/api/uctoo/entity/{limit}/{page}` | GET | 获取实体列表 | 否 |
| `/api/uctoo/entity/{id}` | GET | 获取单个实体 | 否 |
| `/api/uctoo/entity/add` | POST | 添加实体 | 自动 |
| `/api/uctoo/entity/edit` | POST | 编辑实体 | 自动 |
| `/api/uctoo/entity/del` | POST | 删除实体 | 自动 |

## 完整调用示例

### 示例 1：用户登录

**用户请求：** "请以用户名 demo 密码 123456 进行登录"

**调用 http_request 工具：**
```json
{
  "method": "POST",
  "url": "https://javatoarktsapi.uctoo.com/api/uctoo/auth/login",
  "headers": "{\"Content-Type\": \"application/json\"}",
  "body": "{\"username\": \"demo\", \"password\": \"123456\"}"
}
```

**成功响应示例：**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": "505cf909-5e0e-4dde-b215-74274d2cc548",
    "name": "UCTooApp",
    "username": "demo",
    "email": "demo@uctoo.com"
  }
}
```

**注意**：登录成功后，系统会自动保存 token，后续请求无需手动添加 Authorization header。

### 示例 2：获取实体列表

**用户请求：** "获取前10条实体数据"

**调用 http_request 工具：**
```json
{
  "method": "GET",
  "url": "https://javatoarktsapi.uctoo.com/api/uctoo/entity/10/0"
}
```

### 示例 3：编辑实体（自动认证）

**用户请求：** "将 id 为 fd0a410a-7038-4c62-a5e4-9f7950d3d406 的实体的 link 字段更新为 uctoo.com"

**调用 http_request 工具：**
```json
{
  "method": "POST",
  "url": "https://javatoarktsapi.uctoo.com/api/uctoo/entity/edit",
  "headers": "{\"Content-Type\": \"application/json\"}",
  "body": "{\"id\": \"fd0a410a-7038-4c62-a5e4-9f7950d3d406\", \"link\": \"uctoo.com\"}"
}
```

**注意**：系统会自动注入 Authorization header，你不需要手动添加。

**⚠️ 关键注意事项：**
- `id` 必须是实际的 UUID 值，格式如 `fd0a410a-7038-4c62-a5e4-9f7950d3d406`
- **不要使用占位符** 如 `实体ID`、`YOUR_ID`、`id` 等
- 如果用户没有提供具体的 ID，先查询列表获取 ID

### 示例 4：获取当前用户信息

**用户请求：** "获取当前登录用户的信息"

**调用 http_request 工具：**
```json
{
  "method": "GET",
  "url": "https://javatoarktsapi.uctoo.com/api/uctoo/auth/me"
}
```

**注意**：系统会自动注入 Authorization header。

## 错误处理

| 状态码 | 说明 | 处理方式 |
|--------|------|----------|
| 200 | 成功 | 正常处理响应 |
| 400 | 请求参数错误 | 检查请求参数格式 |
| 401 | 未授权/Token过期 | 提示用户重新登录 |
| 403 | 无权限 | 检查是否登录或是否有权限 |
| 404 | 资源不存在 | 检查URL路径是否正确 |
| 500 | 服务器内部错误 | 联系管理员或稍后重试 |

## 常见错误及解决方案

### 错误 1：UUID 格式错误
**错误信息：** `Error creating UUID, invalid character`
**原因：** 传递的 id 不是有效的 UUID 格式
**解决方案：** 确保 id 是实际的 UUID 值，如 `fd0a410a-7038-4c62-a5e4-9f7950d3d406`

### 错误 2：未登录
**错误信息：** `not login` 或 `403 Forbidden`
**原因：** 用户尚未登录或 token 已过期
**解决方案：** 先调用登录接口，系统会自动保存 token

### 错误 3：参数格式错误
**错误信息：** `400 Bad Request`
**原因：** body 参数格式不正确
**解决方案：** 确保 body 是有效的 JSON 字符串，且字段名和值正确

## 重要提醒

1. **✅ 直接调用 http_request 工具**
2. **✅ headers 和 body 必须是 JSON 字符串格式**
3. **✅ POST 请求必须设置 Content-Type: application/json**
4. **✅ 认证 token 由系统自动管理，无需手动处理**
5. **✅ id 参数必须是实际的 UUID 值，不能是占位符**
6. **❌ 不要调用 uctoo-api-skill 工具**
7. **❌ 不要使用 `实体ID`、`YOUR_ID` 等占位符**
8. **❌ 不要手动添加 Authorization header（系统自动注入）**
