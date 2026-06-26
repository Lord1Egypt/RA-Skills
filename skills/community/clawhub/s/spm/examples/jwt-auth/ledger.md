# WBS Task Ledger — JWT 用户认证系统

## Task Summary

- Assignment: 为 Web 应用添加完整的 JWT 用户认证功能
- Requested outcome: 注册/登录/Token刷新 + 权限中间件，全部通过测试
- Success criteria: 4 个 API 端点 + 2 个中间件，覆盖率 ≥ 80%

## WBS

| ID | Work Package | Dependencies | Context Brief | Exit Criteria | Evidence | Status |
|----|-------------|-------------|---------------|---------------|----------|--------|
| 1 | DB Schema + 迁移脚本 | - | Cold-start: 创建 users 表 (id, username, password_hash, refresh_token, role, timestamps)。文件: migrations/001_create_users.sql。约束: bcrypt 12 rounds, role 默认 'user'。 | 迁移脚本可执行，表创建成功 | `psql -f migrations/001_create_users.sql` → OK | done |
| 2 | Token 工具模块 | 1 | Cold-start: Task 1 完成了 users 表。新建 src/utils/token.js 实现 signToken/verifyToken。约束: HS256, access 24h, refresh 7d。JWT_SECRET 从 env 读。文件: src/utils/token.js, tests/token.test.js。 | sign 返回有效 JWT, verify 正确解析 payload, 过期 token 抛错 | `npm test tests/token.test.js` → 5/5 pass | done |
| 3 | User 模型 + 密码哈希 | 1 | Cold-start: Task 1 完成了 users 表。新建 src/models/user.js 实现 createUser/findByUsername/updateRefreshToken。约束: bcrypt salt=12, 密码不存明文。文件: src/models/user.js, tests/user.test.js。 | 密码 bcrypt 哈希存储, 用户名唯一约束, 查找正确 | `npm test tests/user.test.js` → 4/4 pass | done |
| 4 | 认证路由 (register/login/refresh) | 2,3 | Cold-start: Task 2 完成了 token 工具, Task 3 完成了 User 模型。新建 src/routes/auth.js 实现 POST /register /login /refresh。约束: 注册返回 201, 登录返回 access+refresh token, refresh 验证并替换旧 token。文件: src/routes/auth.js, tests/auth.test.js。 | register 201, login 返回 token, refresh 返回新 token, 旧 refresh_token 失效 | `npm test tests/auth.test.js` → 8/8 pass | done |
| 5 | Auth 中间件 + 权限中间件 | 2 | Cold-start: Task 2 完成了 token 工具。新建 src/middleware/auth.js 实现 authMiddleware(验证token→req.user), adminMiddleware(检查role)。约束: 无 token→401, 无效 token→401, 非 admin→403。文件: src/middleware/auth.js, tests/auth.test.js。 | 有效 token 通过, 无/无效 token→401, 非 admin→403 | `npm test` → 全部 17/17 pass | done |
| 6 | 集成测试 + 覆盖率验证 | 4,5 | Cold-start: Task 4 完成了路由, Task 5 完成了中间件。完善集成测试覆盖所有错误路径, 运行全量测试+覆盖率。约束: 覆盖率≥80%。文件: tests/integration.test.js。 | 全量测试通过, 覆盖率≥80%+ Eval Delta 正向 | 见 verification report | done |

## Mutation Log

| Time | Type | Affected | Reason | New IDs |
|------|------|---------|--------|---------|
| - | - | - | 无变更 | - |

## Heartbeat Log

| Time | Active item | Evidence added |
|------|-----------|----------------|
| 2026-05-09 10:15 | Task 1 | migration executed ✓ |
| 2026-05-09 10:45 | Task 2 | token.test.js: 5/5 pass |
| 2026-05-09 11:15 | Task 3 | user.test.js: 4/4 pass |
| 2026-05-09 12:00 | Task 4 | auth.test.js: 8/8 pass |
| 2026-05-09 12:30 | Task 5 | middleware tests: all pass |
| 2026-05-09 13:00 | Task 6 | coverage 85%, Eval Delta: +17 tests, +0 regressions |

## Delivery Summary

- Completed work: 6/6 tasks done. 注册/登录/刷新/权限中间件全部实现
- Evidence package: verification-report.md, test outputs, coverage report
- Remaining blockers: 无
- Residual risks: refresh_token 家族追踪（超出 MVP 范围，已记录在 spec 风险中）
- Final handoff: `npm install && npm test` → 全部通过。`JWT_SECRET=xxx npm start` → 4 个 API 端点可用。
