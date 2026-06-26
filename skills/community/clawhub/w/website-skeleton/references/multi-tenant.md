# 多租户隔离参考文档

> **版本：** v1.0 · **Phase：** 4A  
> **职责：** 租户上下文解析、数据隔离、KV 前缀规则、迁移脚本

---

## 一、架构概览

```
┌────────────────────────────────────────────────────────────┐
│                    JWT (payload.tenant)                    │
│  Edge Middleware / Cloud tenant-context 解析              │
│  → { tenant, userId, role } 注入到请求上下文               │
└────────────────────────────────────────────────────────────┘
                              ↓
┌────────────────────────────────────────────────────────────┐
│                    D1 数据隔离                              │
│  所有 SQL 强制包含 {tenant} 占位符                         │
│  db.js 在运行时自动注入租户 ID → 参数化绑定                 │
└────────────────────────────────────────────────────────────┘
                              ↓
┌────────────────────────────────────────────────────────────┐
│                    KV Key 前缀                              │
│  所有 KV Key 格式: {tenant}:{resource}:{id}               │
│  kv-keys.js 统一生成，防止跨租户访问                       │
└────────────────────────────────────────────────────────────┘
```

---

## 二、三层角色模型

| 角色 | 权限范围 | JWT 中表示 |
|------|---------|-----------|
| **superadmin** | 跨租户，全权限（创建/管理租户） | `role: "superadmin"` |
| **tenant_admin** | 本租户内管理（用户/商品/订单） | `role: "tenant_admin"` |
| **user** | 本租户内个人数据 | `role: "user"` |
| **guest** | 未登录（仅公开 API） | `role: "guest"`, `userId: null` |

### 权限矩阵

| 操作 | superadmin | tenant_admin | user |
|------|:---:|:---:|:---:|
| 创建/管理租户 | ✅ | — | — |
| 管理本租户用户 | ✅ | ✅ | — |
| CRUD 商品 | ✅ | ✅ | — |
| 查看/管理订单 | ✅ | ✅ | ✅（自己） |
| 购物车/下单 | ✅ | ✅ | ✅ |

---

## 三、租户上下文解析

### 3.1 Cloud Functions（`middleware/tenant-context.js`）

```javascript
import { withTenant } from '../middleware/tenant-context.js';

export async function onRequest(request, env) {
  const ctx = await withTenant(request, env);
  if (ctx instanceof Response) return ctx; // 401

  const { tenant, userId, role } = ctx;
  // tenant: 从 JWT payload.tenant 解析，旧 token 降级为 "default"
  // userId: JWT payload.sub
  // role: user / tenant_admin / superadmin
}
```

### 3.2 租户来源优先级

1. **JWT `payload.tenant`**（新 token，Phase 3+ RS256）
2. **从 users 表反查**（旧 HS256 token，30天兼容窗口）
3. **`"default"`**（无 token 时，公开 API 兜底）

> ⚠️ **安全设计**：不再接受 `X-Tenant-ID` 请求头，防止租户伪造。

---

## 四、D1 数据隔离

### 4.1 {tenant} 强制注入

所有 SQL 语句必须包含 `{tenant}` 占位符。`db.js` 在运行时：
1. 检查 SQL 中是否含 `{tenant}`
2. 用 `?` 替换 `{tenant}`
3. 将租户 ID 作为第一个参数绑定

```javascript
// ❌ 错误：无租户隔离
query(env, 'SELECT * FROM orders WHERE id = ?', [orderId]);

// ✅ 正确
query(env, 'SELECT * FROM orders WHERE tenant_id = {tenant} AND id = ?', [orderId], tenant);
```

### 4.2 数据库 Schema

```sql
-- 每张业务表都包含 tenant_id 字段
CREATE TABLE orders (
  id         BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  tenant_id  VARCHAR(32) NOT NULL,       -- 租户隔离字段
  user_id    BIGINT UNSIGNED NOT NULL,
  -- ...
  INDEX idx_tenant (tenant_id)
);

CREATE TABLE products (
  id         BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  tenant_id  VARCHAR(32) NOT NULL,
  -- ...
);
```

### 4.3 迁移脚本

```bash
# 执行租户隔离迁移
edgeone d1 execute my-database --file=db/migrations/003_tenant_isolation.sql

# 回滚（谨慎！）
edgeone d1 execute my-database --file=db/migrations/003_rollback.sql
```

---

## 五、KV Key 前缀规则

### 5.1 Key 格式

```
{tenant}:{resource}:{identifier}

示例：
  default:session:abc123        — Session
  tenant_a:cart:user456         — 购物车
  tenant_a:rt:user789:meta       — Refresh Token
  superadmin:tenant:meta:xyz    — 租户管理
```

### 5.2 kv-keys.js 统一管理

```javascript
import { sessionKey, cartKey, orderTenantKey } from '../sharing/kv-keys.js';

// 自动拼接租户前缀
const key = sessionKey(tenant, userId);
// → "tenant_a:session:user123"
```

---

## 六、支付回调的租户反查

支付回调（`/api/pay/wx-notify`）没有 JWT，需要从 KV 反查租户：

```
支付回调 → out_trade_no → KV.get("order_tenant:{out_trade_no}")
         → 拿到 tenant → 连接对应 D1 数据库
```

```javascript
// cloud-functions/api/pay/wx-notify.js
const meta = JSON.parse(await env.KV.get(`order_tenant:${orderId}`) || '{}');
const tenant = meta.tenant;
```

---

## 七、安全验证清单

| 检查项 | 验证方法 |
|--------|---------|
| 租户 A 用户无法访问租户 B 数据 | 用 TOKEN_A 调用带 TOKEN_B 数据的 API，期望 403/404 |
| X-Tenant-ID Header 无效 | 请求携带 `X-Tenant-ID: tenant_b`，仍按 JWT.tenant 执行 |
| SQL 缺少 {tenant} 报错 | 删除 {tenant} 占位符，期望抛出 Error |
| 支付回调无 tenant 返回 404 | 伪造回调发往 `/api/pay/wx-notify`，期望 404 |
| superadmin 可跨租户操作 | superadmin token 访问任意租户数据 |

---

## 八、测试数据

```sql
-- 插入测试租户
INSERT INTO tenants (id, name, status, quota_limit) VALUES
('tenant_a', '租户 A', 'active', 1000),
('tenant_b', '租户 B', 'active', 500);

-- 插入测试商品（带租户隔离）
INSERT INTO products (tenant_id, name, price, stock) VALUES
('tenant_a', '商品 A-1', 99.00, 100),
('tenant_b', '商品 B-1', 199.00, 50);
```
