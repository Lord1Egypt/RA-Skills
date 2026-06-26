# Migration Guide

## Phase 3 → Phase 4A

### 概述

Phase 4A 引入了多租户隔离，所有 Phase 3 的存量数据需要迁移。本指南涵盖数据库、JWT token、KV key 三方面的迁移。

### 1. 数据库迁移

```bash
# 前置条件：MySQL 8.0.12+
# 小表迁移（ALGORITHM=INSTANT）
mysql -u root -p < db/migrations/003_tenant_isolation.sql

# 大表迁移（使用 gh-ost）
gh-ost --alter="ADD COLUMN tenant_id VARCHAR(64) NOT NULL DEFAULT 'default'" \
       --table=orders \
       --execute

# 迁移后校验
mysql -u root -p -e "
  SELECT COUNT(*) AS total_rows,
         COUNT(DISTINCT tenant_id) AS tenant_count
  FROM orders;
"
```

**回滚：**
```bash
mysql -u root -p < db/migrations/003_rollback.sql
```

### 2. JWT Token 迁移

Phase 4A 的 JWT 向下兼容策略：
- **新 token**（Phase 4A 签发）：payload 含 `tenant`/`role`/`jti` 字段，RS256 签名
- **旧 token**（Phase 3 签发）：自动从 `users` 表按 `sub` 反查真实 `tenant_id`

**无需重新登录。** 用户下次登录时将自动获得含 `tenant` 字段的新 token。

### 3. KV Key 迁移

Phase 3 → Phase 4A 的 KV key 前缀变化：

| Phase 3 | Phase 4A | 说明 |
|---------|---------|------|
| `session:xxx` | `{tenant}:session:xxx` | 新 key 自动带前缀 |
| `rt:{uid}:meta` | `{tenant}:rt:{uid}:meta` | 旧 session 会自然过期 |
| `cart:{uid}` | `{tenant}:cart:{uid}` | 迁移不涉及 KV 数据复制 |

Phase 3 旧 KV key 无 tenant 前缀的会自动过期（TTL 到期），无需手动迁移。

### 4. API 变更

| API | Phase 3 | Phase 4A |
|-----|---------|---------|
| 订单创建 | 无租户概念 | 自动从 JWT 提取 tenant |
| 管理员接口 | 仅 role=admin | role=superadmin/tenant_admin |
| 支付回调 | `out_trade_no.split('_')[0]` | 从 KV `order_tenant:{id}` 反查 |

### 5. 权限表

| 操作 | 旧角色 | 新角色 |
|------|--------|--------|
| 管理后台 | admin | superadmin |
| 租户内管理 | admin | tenant_admin |
| 普通操作 | user | user |

### 6. 零停机部署步骤

```
1. 部署新代码（兼容旧 token）
2. 执行数据库迁移（003_tenant_isolation.sql，ALGORITHM=INSTANT）
3. 用户自动获取新 token（无需重新登录）
4. 验证旧 token 正常运行（resolveLegacyTenant）
5. 30 天后可移除 HS256 兼容代码（JWT Phase 3 过渡期结束）
```
