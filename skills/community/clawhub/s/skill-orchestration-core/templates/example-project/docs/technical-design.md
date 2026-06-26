# 技术方案

## 架构设计

采用分层架构：

```
┌─────────────┐
│   Frontend  │  React SPA
├─────────────┤
│   API Layer │  FastAPI REST
├─────────────┤
│  Service    │  业务逻辑层
├─────────────┤
│  Data Layer │  PostgreSQL + Redis
└─────────────┘
```

## 数据模型

### User
- id: UUID (PK)
- email: VARCHAR(255) UNIQUE
- phone: VARCHAR(20) UNIQUE NULLABLE
- password_hash: VARCHAR(255)
- role: ENUM(admin, editor, viewer)
- status: ENUM(active, locked, disabled)
- created_at: TIMESTAMP
- updated_at: TIMESTAMP

### AuditLog
- id: BIGSERIAL (PK)
- user_id: UUID (FK)
- action: VARCHAR(100)
- resource: VARCHAR(100)
- timestamp: TIMESTAMP
- details: JSONB

## API 设计

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| POST | /api/v1/auth/register | 用户注册 | No |
| POST | /api/v1/auth/login | 用户登录 | No |
| GET | /api/v1/users/me | 获取当前用户 | Yes |
| PUT | /api/v1/users/{id}/role | 修改角色 | Admin |
| GET | /api/v1/audit-logs | 审计日志 | Admin |

## 安全设计

- JWT Token 认证（access + refresh）
- bcrypt 密码哈希（cost=12）
- RBAC 中间件鉴权
- Rate Limiting：100 req/min per IP
- CORS 白名单
