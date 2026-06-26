# Phase 4A 集成测试大纲 — 14 条

> 版本：v6 Final
> 更新日期：2026-05-06
> 前置条件：6 项 P0 修复全部完成 + W1-W4 实施完成

## 前置条件

运行测试前需确保：
1. `sharing/jwt-helper.js` 已移除 `@edge-runtime/primitives` 导入
2. `cloud-functions/utils/db.js` 已就位（含 {tenant} 强制 + withTransaction）
3. `edge-functions/middleware/rbac.js` 已就位
4. 数据库已执行 `003_tenant_isolation.sql` 迁移
5. `sharing/constants.js` 权限矩阵已配置
6. KV 中至少有两个测试租户（`tenant_a`, `tenant_b`）

## 功能测试（F1-F6）

### F1：租户隔离 — 跨租户数据不可见

| 项目 | 内容 |
|------|------|
| 验证 | 租户 A 的 token 无法读取租户 B 的订单 |
| 前置 | tenant_a 和 tenant_b 各有一个订单 |
| 步骤 | 1. 用 tenant_a 的 token 请求 `/api/order?id={tenant_b_order_id}`；2. 检查响应 |
| 预期 | 403 或空结果（不暴露 tenant_b 的数据）|
| 命令 | `curl -H "Authorization: Bearer {token_a}" {url}/api/order?id={order_b_id}` |

### F2：KV 租户隔离

| 项目 | 内容 |
|------|------|
| 验证 | tenant_b 无法访问 tenant_a 的 KV session |
| 步骤 | 1. tenant_a 创建一个 KV session；2. tenant_b 尝试读取 |
| 预期 | tenant_b 读不到 tenant_a 的 session |
| 说明 | KV key 前缀 `${tenant}:session:{id}` 天然隔离 |

### F3：旧 token 兼容

| 项目 | 内容 |
|------|------|
| 验证 | 旧 token（无 tenant 字段）自动归入正确租户 |
| 步骤 | 1. 用 Phase 3 签发的 token（HS256，无 tenant）请求；2. 检查响应 |
| 预期 | resolveLegacyTenant() 从 users 表反查到该用户的真实 tenant_id |
| 说明 | 旧 token 的 `_isLegacy` 标记为 true |

### F4：角色权限

| 项目 | 内容 |
|------|------|
| 验证 | superadmin 可跨租户，tenant_admin 只看本租户 |
| 步骤 | 1. superadmin 调用 `GET /api/admin/tenants`；2. tenant_admin 调用 |
| 预期 | superadmin → 200 + 租户列表；tenant_admin → 403 |

### F5：支付回调租户识别

| 项目 | 内容 |
|------|------|
| 验证 | 支付回调从 KV 反查到正确 tenant |
| 步骤 | 1. 创建订单时写入 `order_tenant:{orderId}` → `{tenant}` |
| 预期 | 回调时从 KV 反查 tenant 正确，订单状态更新到对应租户 |

### F6：SQL 强制 {tenant}

| 项目 | 内容 |
|------|------|
| 验证 | 不走 query() 的 SQL 操作直接报错 |
| 步骤 | 直接调用 `env.DB.prepare('SELECT ...')` 而不经过 db.js |
| 预期 | db 对象不导出，在模块作用域内不可访问，编译或运行时报错 |

## 安全测试（S-01 ~ S-08）

### S-01：JWT tenant 篡改

| 项目 | 内容 |
|------|------|
| 验证 | 篡改 JWT payload 中的 tenant → 验签失败 → 401 |
| 步骤 | 1. 获取一个有效 token；2. 手动修改 payload 中的 tenant 字段；3. 重新 base64 编码；4. 发送请求 |
| 预期 | token 签名不匹配，返回 401 |

### S-02：X-Tenant-ID Header 注入

| 项目 | 内容 |
|------|------|
| 验证 | 添加 X-Tenant-ID Header → 被忽略，以 JWT tenant 为准 |
| 步骤 | 1. 用 tenant_a 的 token；2. 添加 `X-Tenant-ID: tenant_b` header；3. 请求 |
| 预期 | tenant-context.js 不读取此 header，仍以 JWT 中的 tenant 为准 |

### S-03：超配额限制

| 项目 | 内容 |
|------|------|
| 验证 | 单租户超限 → 返回 429/403，不影响其他租户 |
| 步骤 | 1. 模拟一个租户的配额耗尽；2. 该租户请求被拒绝；3. 另一租户请求正常 |
| 预期 | 超限租户返回 `QUOTA_EXCEEDED`，其他租户正常 |

### S-04：superadmin 提权尝试

| 项目 | 内容 |
|------|------|
| 验证 | tenant_admin 尝试访问 superadmin API → 403 |
| 步骤 | 1. 用 tenant_admin 的 token；2. 调用 `GET /api/admin/tenants` |
| 预期 | rbac.js 校验角色 → 403 Forbidden |

### S-05：支付回调伪造

| 项目 | 内容 |
|------|------|
| 验证 | 伪造支付回调（无 KV 记录）→ 404 |
| 步骤 | 1. 构造一个假的微信回调请求（out_trade_no 在 KV 中无记录） |
| 预期 | wx-notify.js 从 KV 反查不到 tenant → 404 |

### S-06：SQL 注入 tenant_id

| 项目 | 内容 |
|------|------|
| 验证 | 构造恶意 tenant 值 → 被 {tenant} 占位符参数化绑定防御 |
| 步骤 | 1. 用 tenant 值 `' OR 1=1 --` 等注入字符串构造 token |
| 预期 | {tenant} → ? → bind(tenant, ...) 参数化，注入无效 |

### S-07：RBAC 绕过

| 项目 | 内容 |
|------|------|
| 验证 | 无 token 访问受保护路由 → 401 |
| 步骤 | 1. 不携带 Authorization header；2. 直接请求 `/api/admin/tenants` |
| 预期 | rbac.js 检测到无 token → 401 |

### S-08：并发配额攻击

| 项目 | 内容 |
|------|------|
| 验证 | 大量并发请求 → 配额定界不被突破 |
| 步骤 | 1. 并发发送 200 个请求（超过 kv_ops:10000 限制）；2. 检查配额计数 |
| 预期 | 并发请求不应突破硬限制的合理倍数（允许少量偏差）|
| 备注 | 此测试依赖 KV atomic counter 的实现，可能在 EdgeOne 环境中略有偏差 |

---

## 测试执行顺序

```
       F3 (旧token兼容)
       ↓
F1 ─→ F2 ─→ F5 ─→ F6    功能测试（先确保基础隔离正确）
                       ↓
S1 ─→ S2 ─→ S4 ─→ S7    安全测试（先验证认证机制）
↓
S3 ─→ S8                配额测试（最后测边界条件）
↓
S5 ─→ S6                边界测试（防御机制）
```

## 测试结果记录

| 用例 | 结果 | 日期 | 备注 |
|------|------|------|------|
| F1 | ⬜ | — | |
| F2 | ⬜ | — | |
| F3 | ⬜ | — | |
| F4 | ⬜ | — | |
| F5 | ⬜ | — | |
| F6 | ⬜ | — | |
| S-01 | ⬜ | — | |
| S-02 | ⬜ | — | |
| S-03 | ⬜ | — | |
| S-04 | ⬜ | — | |
| S-05 | ⬜ | — | |
| S-06 | ⬜ | — | |
| S-07 | ⬜ | — | |
| S-08 | ⬜ | — | |
