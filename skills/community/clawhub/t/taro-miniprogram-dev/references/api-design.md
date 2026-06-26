# API 设计规范

## 请求封装

统一使用 `services/utils/request.ts` 中的 `get` / `post` / `put` / `del` 方法。

## 接口规范

### 请求格式

```typescript
// GET
GET /api/{module}/{action}?key=value

// POST
POST /api/{module}/{action}
Content-Type: application/json
Body: { ... }
```

### 响应格式

```json
{
  "code": 0,
  "msg": "success",
  "data": { ... }
}
```

| code | 说明 |
|------|------|
| 0 | 成功 |
| 401 | 未授权（token 过期）|
| 403 | 无权限 |
| 404 | 资源不存在 |
| 500 | 服务器错误 |

## 模块划分

| 模块 | 前缀 | 说明 |
|------|------|------|
| Auth | `/api/auth/` | 登录、用户信息 |
| Circle | `/api/circle/` | 圈子管理 |
| Task | `/api/task/` | 任务系统 |
| Coin | `/api/coin/` | 金币系统 |

## 必传参数

所有需要登录的接口，需在 header 中携带：

```
Authorization: Bearer {token}
```

token 获取方式：
```typescript
const token = wx.getStorageSync('token')
```

## Mock vs 真实接口

```typescript
// services/utils/request.ts
const IS_MOCK = true  // 开发阶段为 true，切换后端时改为 false
```

IS_MOCK = false 时，需配置：
```typescript
const BASE_URL = 'https://api.yourdomain.com'
```
