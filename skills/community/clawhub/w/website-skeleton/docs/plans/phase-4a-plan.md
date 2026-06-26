# Phase 4A 实施计划 — 多租户隔离

> **方案版本：** v6 Final
> **状态：** 🟢 进行中
> **更新日期：** 2026-05-06

---

## W1：JWT 扩展 + 向下兼容 + Cloud 中间件 + Edge RBAC

### 状态：✅ 完成

| 交付项 | 文件 | 状态 | 说明 |
|--------|------|------|------|
| JWT tenant 字段扩展 | `sharing/jwt-helper.js` | ✅ | signJWT 增加 tenant/role/jti；verifyJWT 增加旧 token users 表反查 |
| 移除 @edge-runtime/primitives | `sharing/jwt-helper.js` | ✅ | 删除 import，使用全局 crypto.subtle |
| Cloud 统一租户中间件 | `cloud-functions/middleware/tenant-context.js` | ✅ **新建** | withTenant() + withTenantAudit() |
| db.js 强制 {tenant} + 事务 | `cloud-functions/utils/db.js` | ✅ **新建** | query/queryOne/execute + withTransaction |
| Edge RBAC 中间件 | `edge-functions/middleware/rbac.js` | ✅ **新建** | requireRole/requireSuperadmin/requireAdmin |
| transition.js SQL 迁移 | `cloud-functions/api/order/transition.js` | ✅ | 迁移到 withTransaction + {tenant} |
| order-cron.js SQL 迁移 | `cloud-functions/cron/order-cron.js` | ✅ | 迁移到 withTransaction + {tenant} |

### 涉及文件清单

| 文件 | 操作类型 | 行数 |
|------|---------|------|
| sharing/jwt-helper.js | 修改 | 删除1行，新增20行 |
| cloud-functions/middleware/tenant-context.js | **新建** | 93行 |
| cloud-functions/utils/db.js | **新建** | 120行 |
| edge-functions/middleware/rbac.js | **新建** | 98行 |
| cloud-functions/api/order/transition.js | 重写 | 从220行精简到165行 |
| cloud-functions/cron/order-cron.js | 重写 | 从179行精简到145行 |

---

## W2：KV 动态租户前缀 + 配额限制（共享模块化）

### 状态：✅ 完成

| 交付项 | 文件 | 状态 | 说明 |
|--------|------|------|------|
| KV 动态前缀强制 tenant 检查 | `sharing/kv-keys.js` | ✅ | makeKey() 增加 tenant 非空检查（IMA S3） |
| 共享配额模块 | `sharing/quota.js` | ✅ **新建** | checkQuota + incrementQuota + resetQuota |
| 软/硬限制双层防护 | `sharing/quota.js` | ✅ | 硬限制 * 0.9 软限制，边界值提前告警 |
| fail-open 告警 | `sharing/quota.js` | ✅ | KV 故障时允许通过 + 上报告警 |

---

## W3：MySQL 租户隔离 + 权限分层 + 审计日志

### 状态：✅ 完成

| 交付项 | 文件 | 状态 | 说明 |
|--------|------|------|------|
| MySQL 迁移脚本 | `db/migrations/003_tenant_isolation.sql` | ✅ **新建** | 6 表 + 复合索引 + ALGORITHM=INSTANT |
| 独立回滚文件 | `db/migrations/003_rollback.sql` | ✅ **新建** | 可独立执行（架构专家 D5） |
| 权限分层 + 权限矩阵 | `sharing/constants.js` | ✅ **新建** | ROLES + PERMISSIONS + checkPermission() |
| 审计日志中间件 | `cloud-functions/middleware/audit.js` | ✅ **新建** | auditLog + queryAuditLogs + 90 天保留 |

---

## W4：管理后台 + 支付回调加固

### 状态：✅ 完成

| 交付项 | 文件 | 状态 | 说明 |
|--------|------|------|------|
| 租户管理 API | `edge-functions/api/admin/tenants.js` | ✅ **新建** | CRUD + invite + 启用/停用，requireRole superadmin |
| 支付回调 KV 反查 | `edge-functions/api/pay/wx-notify.js` | ✅ **新建** | KV 反查 tenant（P0-2），零 SQL 绕过 |
| 租户停用处理 | tenants.js status API | ✅ | PUT /api/admin/tenants/:id/status → active/suspended |

---

## W5：集成测试（14 条）

### 状态：✅ 完成

| 交付项 | 文件 | 状态 | 说明 |
|--------|------|------|------|
| 集成测试文档 | `references/integration-tests.md` | ✅ **新建** | 14 条用例（F1-F6 + S-01~S-08），含步骤+预期+执行顺序 |
| 可执行测试脚本 | `tests/integration/phase4a.test.js` | ✅ **新建** | Node.js fetch 自动化测试，输出 JSON 报告 |

### 后置修复

| 文件 | 问题 | 修复 |
|------|------|------|
| `edge-functions/api/pay/wx-notify.js` | import ../../utils/db.js 解析路径错误（Edge Functions 无法 import Cloud Functions） | 移至 **cloud-functions/api/pay/wx-notify.js**，使用正确相对路径 |
| 语法检查 | — | **21/21 全部通过** |
| Phase 4 新增文件 import 路径 | — | **8/8 全部正确** |

### 测试用例覆盖

| 类型 | 编号 | 测试项 |
|------|------|--------|
| 功能 | F1 | 跨租户数据隔离 |
| 功能 | F2 | KV 租户隔离 |
| 功能 | F3 | 旧 token 兼容 |
| 功能 | F4 | 角色权限（superadmin vs tenant_admin） |
| 功能 | F5 | 支付回调 KV 反查 |
| 功能 | F6 | SQL 强制 {tenant} |
| 安全 | S-01 | JWT tenant 篡改 |
| 安全 | S-02 | X-Tenant-ID Header 注入 |
| 安全 | S-03 | 超配额限制 |
| 安全 | S-04 | superadmin 提权尝试 |
| 安全 | S-05 | 支付回调伪造 |
| 安全 | S-06 | SQL 注入 tenant_id |
| 安全 | S-07 | RBAC 绕过 |
| 安全 | S-08 | 并发配额攻击 |

### Phase 4A 全部完成 ✅

| 周次 | 内容 | 状态 |
|------|------|------|
| W1 | JWT扩展 + 中间件 + db.js + RBAC | ✅ |
| W2 | KV动态前缀 + 配额限制 | ✅ |
| W3 | MySQL迁移 + 权限分层 + 审计日志 | ✅ |
| W4 | 管理后台 + 支付回调KV反查 | ✅ |
| W5 | 14条集成测试 | ✅ |
