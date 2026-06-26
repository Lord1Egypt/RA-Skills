---
name: spm-api
version: 1.0.0
description: API设计规范 — REST端点/错误码/分页/版本控制。Agent 经常各写一套，本技能统一标准。SPM Phase 2 自动注入 Context Brief。
---

# SPM API — API 设计规范

## 自动检测

SPM Phase 2 写 WBS 计划时，检测到 API 端点相关任务 → 自动将本技能的 URL/状态码/分页规范注入 Context Brief。

## 独立使用

不走 SPM 也可以直接说："按 spm-api 规范设计用户模块的 REST 接口。"

---

## URL 设计

```
✅ GET    /api/users              # 列表
✅ GET    /api/users/:id          # 详情
✅ POST   /api/users              # 创建
✅ PUT    /api/users/:id          # 全量更新
✅ PATCH  /api/users/:id          # 部分更新
✅ DELETE /api/users/:id          # 删除

✅ GET    /api/users/:id/orders   # 子资源

❌ GET    /api/getUsers           # 动词
❌ POST   /api/createUser         # 动词
❌ GET    /api/user_list          # 下划线
```

---

## 响应格式

```typescript
// ✅ 统一信封
{
  "data": T | T[],
  "pagination"?: { page, pageSize, total },
  "error"?: { code: string, message: string }
}
```

---

## HTTP 状态码

| 场景 | 码 | 说明 |
|------|-----|------|
| 查询成功 | `200` | 有数据或无数据(空数组) |
| 创建成功 | `201` | + Location header |
| 更新成功 | `200` | 返回更新后的完整对象 |
| 删除成功 | `204` | 无 body |
| 参数校验失败 | `400` | 字段级错误："username is required" |
| 未认证 | `401` | token 缺失或无效 |
| 无权限 | `403` | 有 token但没权限 |
| 不存在 | `404` | "User not found" |
| 冲突 | `409` | 唯一约束、重复创建 |
| 请求体过大 | `413` | |
| 服务器错误 | `500` | 仅内部异常 |

**BANNED ❌:**
- `200` + body 里 `{ "error": "something" }` — 用正确的状态码
- `500` 包所有错误 — 区分 4xx vs 5xx

---

## 分页

```typescript
// Request
GET /api/users?page=1&pageSize=20

// Response
{
  "data": [...],
  "pagination": {
    "page": 1,
    "pageSize": 20,
    "total": 156
  }
}
```

**规则：**
- 所有列表接口默认分页（即使现在只有 10 条）
- `pageSize` 默认 20，最大 100
- 即使 `page=1` 也必须返回 pagination

---

## 版本控制

```
✅ URL 前缀: /api/v1/users
✅ Header:   Accept: application/vnd.myapp.v1+json

❌ Query:    /api/users?version=1
❌ 无版本
```

**MVP 阶段可以不设版本。** 在首次公开 API 时加 `/v1/`。

---

## 认证

```
✅ Authorization: Bearer <token>
✅ 统一用 auth 中间件，不每路由手写

❌ 把 token 放 body
❌ 把 token 放 query string
❌ 每路由写一遍 token 验证逻辑
```

---

## 错误处理

```json
// ✅
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "username is required",
    "details": [
      { "field": "username", "reason": "required" }
    ]
  }
}

// ❌ 
{
  "error": "Something went wrong"
}
```

**规则：**
- `code` 是机器可读枚举（前端用它做 if/switch）
- `message` 是人类可读（可以展示给用户）
- `details` 仅在 400 时提供字段级错误

---

## Agent 常见 API 反模式

| # | 反模式 | 改法 |
|---|--------|------|
| 1 | 每个路由自己写 try-catch | 统一 error handler 中间件 |
| 2 | 错误响应格式不一致 | 统一 `{ error: { code, message } }` |
| 3 | 不验证输入直接进数据库 | 每个端点先 validate，再处理 |
| 4 | 不设 rate limit | 至少在 auth 端点加 |
| 5 | N+1 查询 | 用 JOIN / batch query / DataLoader |
