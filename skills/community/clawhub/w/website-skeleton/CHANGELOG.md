# Changelog

> 语义化版本（SemVer）：<https://semver.org/>
> 所有包在 Phase 4 期间 lockstep 发布补丁版本

## 3.2.0 (2026-05-26)

### 🚀 Phase 5 — 工程完缮

#### 新增
- **商品详情独立页**：`/products/:id` 独立页面（图片、描述、价格、库存、加购）
- **227 项测试**：sharing/* 166 项 + cloud/utils 61 项（db.js + order-state-machine）
- **init-site.js + 模板联动**：从 `templates/*.json` 读取配置，功能开关自动预配置
- **migrate.js**：D1 迁移自动执行脚本（按序 001→002→003，D1 语法适配）
- **sample-data.js --hash-passwords**：bcrypt 密码哈希自动生成
- **vitest** 测试框架集成（CI 自动运行）

#### 工程
- middleware.js async/await + try-catch（修复 HTTP 545 运行时崩溃）
- EdgeOne Pages 部署验证通过（首页/SPA/API 均返回 200）

## 3.1.2 (2026-05-26)

### 🚀 Phase 4D — 工程补齐完缮

#### 新增
- **SPA 补齐 7 页面**：checkout（结算）、order-detail（订单详情）、ai-chat（AI 对话）、profile（个人中心）、admin/dashboard/orders/products（管理后台 CRUD）
- **脚本补齐**：`scripts/init-site.js`（交互式初始化向导）、`scripts/sample-data.js`（示例数据生成）、`db/seed.sql`（SQL 种子数据）
- **CI Node 22**：test.yml + deploy.yml 升级到 Node 22，新增 `.nvmrc`
- **Dependabot**：`.github/dependabot.yml` 自动依赖更新（npm + Actions）

#### 修复
- `db/migrations/001_init.sql` 建表脚本创建（6 张核心表 + 索引 + 约束）
- `deploy.yml` 新增 `on: push: branches: [main]` 自动触发
- 内联 CSS 555 行抽取为独立 `client/src/styles/main.css` 文件

#### 文档
- GitHub About（Description + Homepage）设置
- README 版本号同步更新

## 3.1.1 (2026-05-26)

### 🚀 Phase 4C — 代码补齐 & 工程加固

#### 新增
- **前端 SPA 完整实现**（20 个文件）：index.html（入口）、app.js、router、event-bus、storage、escape-html + 6 页面（home/login/register/products/cart/orders）+ 2 组件（navbar/toast）+ 3 服务（api/auth/cart/ai SSE）
- **Edge Functions API 14 端点**：auth（login/me/refresh/logout）、products（list/[id]/categories）、cart（add/get/update/remove）、orders（list/[id]）、ai（history）
- **Cloud Functions API 13 端点**：auth（register）、pay（create-order/query/close）、admin（products/orders/users/stats）、order（create/detail/cancel）、ai（chat-stream SSE）

#### 修复
- 添加 LICENSE（MIT No Attribution）
- 修复 English README 空白段（Features / Demo）
- 修复 quota.js 每日不重置（缺少 expirationTtl 参数）
- 修复 Edge API 14 个文件导入路径（`../../../sharing/` → `../../sharing/`）
- 修复 CI 集成测试无服务器环境 fetch 失败（添加 serverReachable 健康检查）

#### 工程
- GitHub Topics 设置 16 个标签
- `continue-on-error` 移除，测试失败阻断 CI
- 计划文件移至 `docs/plans/`
- `.gitignore` 增强，`reports/` 取消跟踪

## 3.0.0 (2026-05-06)

### 🎉 Phase 4A — 多租户隔离

#### 重大变更
- **JWT 扩展**：新 token 包含 `tenant`/`role`/`jti` 字段，旧 token 自动从 `users` 表反查
- **数据库迁移**：6 张核心表增加 `tenant_id` 列 + 复合索引
- **所有 SQL 必须包含 `{tenant}` 占位符**：通过 `db.js` 接口强制执行
- **权限分层**：从单一 `admin` 拆分为 `superadmin`/`tenant_admin`/`user`

#### 新增
- 多租户中间件（Cloud: `tenant-context.js`, Edge: `rbac.js`）
- 数据库事务支持（`db.js` → `withTransaction()`）
- 共享配额模块（`quota.js` → 软/硬限制 + fail-open）
- 审计日志（`audit.js` → 90 天 KV 保留）
- 租户管理 API（CRUD + 邀请 + 启用/停用）
- 14 条集成测试（功能 6 + 安全 8）

#### 修复
- 移除 `@edge-runtime/primitives` 导入（EdgeOne V8 不兼容）
- 支付回调改为 KV 反查（修复 `{tenant}` 鸡生蛋问题）

#### 依赖
- `@website-skeleton/shared` → 3.0.0
- `@website-skeleton/payment` → 1.0.0
- `@website-skeleton/admin` → 1.0.0

## 2.2.0 (2026-04-26)

### Phase 3 — 工程化完善
- RS256 双轨 JWT 迁移
- 订单状态机完整实现
- SEO / i18n / Analytics 模块
- 多租户 KV 前缀铺垫
- 5 篇 reference 文档补充

## 2.1.0 — Phase 2 — 核心功能增强
## 2.0.0 — Phase 1 — 基础骨架搭建
## 1.0.0 — 初始版本
