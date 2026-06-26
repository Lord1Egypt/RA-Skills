# Design Spec: JWT 用户认证系统

**Date**: 2026-05-09  
**Phase**: 1 — Requirements  
**Status**: ✅ Approved

---

## 灵魂拷问（Phase 1 输出）

| 问题 | 回答 |
|------|------|
| 认证流程？ | 用户名+密码注册 → 登录返回 access_token(24h) + refresh_token(7d) |
| 无状态还是有状态？ | 无状态 JWT。access_token 不存服务端，refresh_token 存数据库以便吊销 |
| 权限层级？ | 两个角色：普通用户、管理员。通过 JWT payload 中的 `role` 字段区分 |
| 需要 refresh_token 吗？ | 需要。access_token 24h 过期后用 refresh_token 换新 |
| 密码安全？ | bcrypt 加密存储，salt rounds=12 |

---

## ASSUMPTIONS

1. 数据库已有 `users` 表（本任务需创建迁移脚本）
2. 前端在 Authorization header 中传递 `Bearer <token>`
3. Express 中间件可以通过 `req.user` 访问当前用户信息
4. 注册时不需要邮箱验证（MVP 阶段）
5. 管理员角色通过数据库字段控制（不在本任务中实现管理后台）

---

## API 契约

### POST /api/auth/register
```
Request:  { username, password }
Response: { id, username, created_at }
Errors:   409 (username exists), 400 (validation)
```

### POST /api/auth/login
```
Request:  { username, password }
Response: { access_token, refresh_token, expires_in }
Errors:   401 (invalid credentials)
```

### POST /api/auth/refresh
```
Request:  { refresh_token }
Response: { access_token, expires_in }
Errors:   401 (invalid/expired refresh_token)
```

### GET /api/me (需认证)
```
Headers:  Authorization: Bearer <access_token>
Response: { id, username, role, created_at }
Errors:   401 (invalid/expired token), 403 (insufficient permissions)
```

---

## 架构决策

- **Token 算法**：HS256（当前仅单服务，不需要非对称加密）
- **密钥管理**：`process.env.JWT_SECRET`（生产环境用密钥管理服务）
- **密码哈希**：bcrypt with salt rounds=12
- **Token 存储**：access_token 仅客户端存储（localStorage），refresh_token 同时存服务端 users 表
- **中间件设计**：`authMiddleware` 验证 access_token，`adminMiddleware` 检查 role=admin

---

## 风险

1. refresh_token 泄露 → 需要在 refresh 接口验证 token 家族（每次刷新生成新 refresh_token，旧 token 失效）
2. 密钥泄露 → 紧急轮换 JWT_SECRET 会使所有 token 失效
3. 暴力破解 → 登录接口加 rate limiting（非本 Phase 范围）
