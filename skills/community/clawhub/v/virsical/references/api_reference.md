# Virsical API Reference

## 概述

Virsical（威思客）智慧空间管理平台 API 参考文档。所有 API 请求需要在请求头中携带签名信息。

## 基础信息

- **Base URL**: 通过 `scripts/config.py` 获取，见 SKILL.md 概述
- **认证方式**: OAuth2 Authorization Code Flow + 请求签名
- **Token 类型**: Bearer Token
- **签名算法**: SHA256(token + SIGNATURE_KEY + timestamp + path + query + body)

## 认证相关 API

### OAuth2 授权

```
GET /vsk/virsical-auth/oauth2/authorize
```

**Query 参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| response_type | string | 是 | 固定值 `code` |
| client_id | string | 是 | OAuth 客户端 ID（已固定为 `login-agent`） |
| redirect_uri | string | 是 | 回调地址 `http://127.0.0.1:1455/callback` |
| state | string | 是 | CSRF 防护的随机状态值（32字节 hex） |

**响应**: 重定向到授权页面，用户授权后回调 redirect_uri 并携带 `code` 和 `state`。

### 获取/刷新 Token

```
POST /vsk/virsical-auth/oauth/token
```

**Content-Type**: `application/x-www-form-urlencoded`

**授权码模式**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| grant_type | string | 是 | `authorization_code` |
| code | string | 是 | 授权码 |
| redirect_uri | string | 是 | 回调地址 |

**刷新模式**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| grant_type | string | 是 | `refresh_token` |
| refresh_token | string | 是 | 刷新令牌 |

**注意**: OAuth 凭证（client_id 和 client_secret）通过 Basic Auth 头传递，已使用固定值。

**成功响应**:
```json
{
  "access_token": "xxx",
  "refresh_token": "xxx",
  "expires_in": 43200,
  "user_id": "xxx",
  "tenant_id": "xxx",
  "username": "xxx"
}
```

### 检查 Token 有效性

```
POST /vsk/virsical-auth/oauth/check_token
```

**认证**: Basic Auth（已使用固定凭证）

**Query 参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| token | string | 是 | 要检查的 access_token |

**响应**: 返回 token 的详细信息（有效）或错误（无效/过期）。

### 登出

```
POST /vsk/virsical-auth/token/logout
```

**认证**: Bearer Token

**Body**:
```json
{
  "access_token": "xxx"
}
```

---

## 会议室 API

### 查询会议室详情

```
POST /vsk/smt-meeting/ai/rooms
```

**Body**:
```json
{
  "tenantId": 1040,
  "capacity": -1,
  "excludeCapacities": "1;8",
  "meetingId": 0
}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| tenantId | number | 是 | 租户 ID（从 token 获取） |
| capacity | number | 是 | 会议室类型，-1 表示不限制 |
| excludeCapacities | string | 是 | 排除的会议室类型，分号分隔如 "1;8" |
| meetingId | number | 是 | 会议 ID，固定 0 |

**响应**: 返回会议室列表，每个会议室包含 `roomId`, `roomName`, `capacity`, `zoneName`, `deviceName` 等字段。

### 查询会议室占用状态

```
POST /vsk/smt-meeting/ai/rooms/occupied
```

**Body**:
```json
{
  "tenantId": 1040,
  "capacity": -1,
  "excludeCapacities": "1;8",
  "meetingId": 0,
  "startTime": "2026-06-02T09:00:00+08:00",
  "endTime": "2026-06-02T10:00:00+08:00"
}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| tenantId | number | 是 | 租户 ID（从 token 获取） |
| capacity | number | 是 | 会议室类型，-1 表示不限制 |
| excludeCapacities | string | 是 | 排除的会议室类型，分号分隔如 "1;8" |
| meetingId | number | 是 | 会议 ID，固定 0 |
| startTime | string | 否 | 开始时间（ISO 8601） |
| endTime | string | 否 | 结束时间（ISO 8601） |
| roomName | string | 否 | 会议室名称（模糊搜索） |

**响应**: 返回会议室列表，每个会议室包含 `roomName`, `roomId`, `capacity`, `occupied`, `occupiedTime` 等字段。

### 预订会议室

```
POST /vsk/smt-meeting/ai/meeting/reserve
```

**Body**:
```json
{
  "bookType": 0,
  "name": "项目评审会",
  "startTime": 1780358400000,
  "endTime": 1780362000000,
  "roomIds": [522],
  "creatorId": 216,
  "tenantId": 1040
}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| bookType | number | 是 | 预订类型，固定 0 |
| name | string | 是 | 会议标题 |
| startTime | number | 是 | 开始时间（毫秒时间戳） |
| endTime | number | 是 | 结束时间（毫秒时间戳） |
| roomIds | number[] | 是 | 会议室 ID 数组 |
| creatorId | number | 是 | 创建人 ID（从 token userId 获取） |
| tenantId | number | 是 | 租户 ID（从 token tenantId 获取） |

**响应码**:
| code | 含义 |
|------|------|
| 0 | 预订成功 |
| 200999 | 系统异常，预订失败 |
| 202001 | 会议室已被预订 |
| 202148 | 会议时间冲突 |

### 查询会议列表

```
POST /vsk/smt-meeting/ai/meeting/page
```

**Body**:
```json
{
  "size": 30,
  "tenantId": 1040
}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| size | number | 是 | 每页条数，默认 30 |
| tenantId | number | 是 | 租户 ID（从 token 获取） |

**响应**: 分页结果，records 包含会议列表。

---

## 访客 API

### 查询访客邀请列表

```
GET /vsk/vst-visitor/api/invitations
```

**Query 参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| rows | number | 是 | 每页条数，固定 30 |
| from | number | 是 | 固定值 1 |
| locationId | number | 是 | 位置 ID，固定 0 |
| companyId | number | 是 | 租户 ID（从 token 获取） |
| visitorName | string | 否 | 访客姓名（模糊搜索） |
| prdStartDate | number | 否 | 开始日期（毫秒时间戳） |
| prdEndDate | number | 否 | 结束日期（毫秒时间戳） |
| page | number | 否 | 当前页，默认 1 |

**响应**: `data.rows` 包含访客记录数组，`data.total` 为总数。

**访客状态码**（visitorStatus 为字符串）:
| code | 含义 |
|------|------|
| "0" | 未开始 |
| "1" | 未到访 |
| "2" | 已签到 |
| "3" | 已签出 |
| "4" | 已取消 |
| "6" | 已拒绝 |
| "7" | 已过期 |
| "8" | 处理中 |
| "9" | 系统签出 |
| "10" | 失败 |
| "12" | 审批中 |

---

## 工单 API

### 获取工单参数

```
GET /vsk/fm-service/api/requirement/paramsPacking
```

**响应**: 返回项目列表、工单类型、优先级选项等参数。

### 获取项目空间位置

```
GET /vsk/fm-service/api/projectSpace/id
```

**Query 参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| projectId | string | 是 | 项目 ID |

### 创建工单

```
POST /vsk/fm-service/api/requirement/create/v2
```

**Body**:
```json
{
  "projectId": "xxx",
  "requirementContent": "打印机故障，无法打印",
  "requirementTypeId": "xxx",
  "priority": "high",
  "entranceSource": "ai",
  "requirementLocations": [{"id": "xxx"}]
}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| projectId | string | 是 | 项目 ID |
| requirementContent | string | 是 | 工单内容描述 |
| requirementTypeId | string | 是 | 工单类型 ID |
| priority | string | 是 | 优先级：high/medium/low |
| entranceSource | string | 是 | 入口来源，固定 `ai` |
| requirementLocations | array | 否 | 位置信息 |

---

## 组织架构 API

### 查询部门树

```
GET /vsk/virsical-upms/dept/tree
```

**Query 参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| query | string | 是 | 查询字段，如 `id,name` |

**响应格式**:
```json
{
  "code": 0,
  "data": [
    {
      "id": "xxx",
      "name": "总部",
      "children": [...]
    }
  ]
}
```

### 查询用户

```
GET /vsk/virsical-upms/user/page
```

**Query 参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| realName | string | 否 | 用户姓名（模糊搜索） |
| deptId | string | 否 | 部门 ID |
| includeSubDepartments | boolean | 否 | 是否包含子部门，默认 true |
| delFlag | number | 否 | 删除标记，固定 0 |
| current | number | 否 | 当前页，默认 1 |
| size | number | 否 | 每页条数 |

---

## 请求签名

所有非 OAuth 端点的 API 请求均需携带签名头：

```
vsk-signature: <SHA256 签名>
vsk-timestamp: <Unix 时间戳（毫秒）>
```

签名算法详见 `signature.md`。
