<p align="center">
  <img src="https://img.shields.io/badge/version-v3.2.0-blue?style=flat-square" alt="version">
  <img src="https://img.shields.io/badge/EdgeOne_Pages-ready-brightgreen?style=flat-square" alt="EdgeOne Pages">
  <img src="https://img.shields.io/badge/license-MIT_No_Attribution-green?style=flat-square" alt="license">
  <img src="https://img.shields.io/badge/status-stable-brightgreen?style=flat-square" alt="status">
  <img src="https://img.shields.io/badge/Phase_5_工程完缮-%E2%9C%85-success?style=flat-square" alt="Phase 5">
  <a href="https://website-skeleton-demo-8mv8fitk.edgeone.cool?eo_token=587119f1f48590b7dded3b65f6001030&eo_time=1779867268"><img src="https://img.shields.io/badge/demo-live-purple?style=flat-square" alt="Demo"></a>
</p>

# Website Skeleton Skill

> **One sentence to build a full-stack website.** Generate auth, payments, AI chat, and admin panel — deploy to EdgeOne Pages.

[English](#english) · [中文](#chinese) · [Demo](https://website-skeleton-demo-8mv8fitk.edgeone.cool?eo_token=587119f1f48590b7dded3b65f6001030&eo_time=1779867268)

---

## English

**website-skeleton-skill** is an EdgeOne Pages skill that scaffolds full-stack websites from a single prompt. It combines 5 reusable modules (Auth, Cart, Payment, AI Chat, Admin) across 3 scene templates (E-commerce, AI Assistant, SaaS Admin).

### Quick Start

```bash
npm install -g edgeone
edgeone login --site china
edgeone pages deploy -n my-site
```


### Features

| Feature | Status | Description |
|---------|--------|-------------|
| 🔐 Auth | ✅ | JWT dual-track (RS256 + HS256), bcrypt, KV Session, RT rotation |
| 🛒 Cart & Payment | ✅ | WeChat/Alipay, Edge idempotency lock, multi-tenant KV cart |
| 🤖 AI Chat | ✅ | SSE streaming via Cloud Functions, KV history, rate-limited |
| 📊 Admin Panel | ✅ | RBAC (superadmin/tenant_admin/user), CRUD, stats, audit logs |
| 🏢 Multi-tenant | ✅ | Phase 4A: {tenant} forced SQL, KV prefix isolation, quotas |
| 📦 npm Packages | ✅ | Phase 4B: @website-skeleton/{shared,payment,admin} |
| 🌍 i18n | ✅ | Chinese + English, extensible |
| 🔍 SEO | ✅ | JSON-LD structured data, meta tags |
| 📈 Analytics | ✅ | KV-based event tracking, opt-out support |

### Demo

[Live Demo →](https://website-skeleton-demo-8mv8fitk.edgeone.cool?eo_token=587119f1f48590b7dded3b65f6001030&eo_time=1779867268)

Deploy your own with a single command: `edgeone pages deploy -n my-site`

---

## Chinese

# website-skeleton-skill

> 一句话描述需求 → AI 生成完整前后端网站 → 自动部署到 EdgeOne Pages 全球 CDN。

**版本：** v3.2.0 · **Phase 5（工程完缮）已全部完成**

---

## 目录

- [一、快速开始](#一快速开始)
- [二、架构](#二架构)
- [三、功能特性](#三功能特性)
- [四、Phase 4 变更概要](#四phase-4-变更概要)
- [五、目录结构](#五目录结构)
- [六、安全设计](#六安全设计)
- [七、评审历程](#七评审历程)
- [八、版本历史](#八版本历史)
- [九、License](#九license)

---

## 一、快速开始

```bash
# 1. 安装 EdgeOne CLI
npm install -g edgeone

# 2. 登录
edgeone login --site china

# 3. 部署（交互式引导）
edgeone pages deploy -n my-site

# 4. 按提示选择场景模板、填写配置、执行数据库迁移
```

### 场景模板

| 模板 | 适用场景 | 包含模块 | 快速命令 |
|------|---------|---------|---------|
| **🛒 电商** | 独立电商、品牌官网 | Auth + Cart + Payment (微信/支付宝) + Orders + Admin | `帮我搭一个电商网站` |
| **🤖 AI 助手** | AI 客服、AI 工具站 | Auth + AI Chat (SSE流式) + Admin | `帮我做一个AI客服站` |
| **📊 SaaS 管理后台** | B2B SaaS、管理后台 | Auth + RBAC + Stats + Subscription | `帮我建一个管理后台` |

---

## 二、架构

### 双运行时设计

```
┌──────────────────────────────────────────────────────────────────┐
│  Platform Middleware                                              │
│  CORS · CSP · 支付回调 IP 白名单（直接 return，不进 Edge）         │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│  Edge Functions (V8 + KV)                                        │
│  JWT 校验 · KV Session · 限流 · 商品列表 · 幂等锁 · 租户路由     │
│  延迟敏感、无密钥、轻量操作                                       │
└──────────────────────────────────────────────────────────────────┘
                              ↓（写操作/密钥操作）
┌──────────────────────────────────────────────────────────────────┐
│  Cloud Functions (Node.js + D1)                               │
│  bcrypt · 支付创建/回调 · 订单状态机 · Admin CRUD · AI SSE 流     │
│  密钥操作、复杂事务、SELECT FOR UPDATE                            │
└──────────────────────────────────────────────────────────────────┘
```

### 核心设计决策

| 决策 | 选择 | 理由 |
|------|------|------|
| 数据库 | **D1 (EdgeOne Pages 原生)** | EdgeOne Pages 原生支持，`SELECT FOR UPDATE` 事务需求 |
| 认证 | **JWT RS256 + 30天 HS256 兼容窗口** | 安全性（RS256）与迁移平滑兼顾 |
| 支付幂等 | **Edge `putIfNotExists` 24h TTL** | 微信重试窗口 72h，Edge 原子操作保证 |
| 会话 | **KV Session** | 无状态、低延迟，适合 Edge 运行时 |
| 前端 | **SPA (Vanilla JS) + History API** | 无需构建工具链，Skill 生成零依赖 |

---

## 三、功能特性

### 已实现功能

| 功能 | 状态 | 说明 |
|------|------|------|
| 🔐 Auth | ✅ | JWT 双轨 (RS256 + HS256)、bcrypt、KV Session、RT 轮换 |
| 🛒 购物车与支付 | ✅ | 微信/支付宝、Edge 幂等锁、多租户 KV 购物车 |
| 🤖 AI 对话 | ✅ | Cloud Functions SSE 流式、KV 历史、限流 |
| 📊 管理后台 | ✅ | RBAC (superadmin/tenant_admin/user)、CRUD、统计、审计日志 |
| 🏢 多租户隔离 | ✅ | Phase 4A: {tenant} 强制 SQL、KV 前缀隔离、配额限制 |
| 📦 npm 包 | ✅ | Phase 4B: @website-skeleton/{shared,payment,admin} |
| 🌍 国际化 | ✅ | 中英双语，可扩展 |
| 🔍 SEO | ✅ | JSON-LD 结构化数据、meta 标签 |
| 📈 数据分析 | ✅ | KV 事件追踪、opt-out 支持 |

---

## 四、Phase 4 变更概要

### Phase 4A：多租户隔离（5 周）

| 周次 | 内容 | 关键文件 |
|------|------|----------|
| W1 | JWT 扩展 tenant/role + Cloud 中间件 + Edge RBAC + db.js {tenant} 强制 + 事务 | `jwt-helper.js`, `tenant-context.js`, `rbac.js`, `db.js` |
| W2 | KV 动态前缀 + 共享配额模块（软/硬限制 + fail-open） | `kv-keys.js`, `quota.js` |
| W3 | D1 迁移（6 表 + 复合索引）+ 权限分层 + 审计日志 + 回滚脚本 | `003_tenant_isolation.sql`, `003_rollback.sql` |
| W4 | 租户管理 API + 支付回调 KV 反查 | `admin/tenants.js`, `pay/wx-notify.js` |
| W5 | 集成测试（14 条）+ KV 热 key 分散 | 测试用例, `kv-keys.js` |

### Phase 4B：npm 包化 + 增强（4 周）

| 交付项 | 文件 | 状态 |
|--------|------|------|
| @website-skeleton/shared | `packages/shared/package.json` + src/index.js | ✅ v3.0.0 |
| @website-skeleton/payment | `packages/payment/package.json` + src/index.js | ✅ v1.0.0 |
| @website-skeleton/admin | `packages/admin/package.json` + src/index.js | ✅ v1.0.0 |
| 构建同步 | `scripts/sync-sharing.js` | ✅ --check/--sync/--ci 三种模式 |
| Edge auth 内联 | `package.json scripts` | ✅ npm run build 自动同步 |

### 5 项 P0 前置修复

| P0 | 内容 | 来源 |
|----|------|------|
| P0-1 | 移除 `@edge-runtime/primitives` 导入，改用全局 `crypto.subtle` | 平台专家 |
| P0-2 | 支付回调租户识别从 4B 提前到 4A W4（KV 反查） | 架构 + 安全专家 |
| P0-3 | db.js 新增 `withTransaction()` 事务接口 | 平台专家 |
| P0-4 | Edge Functions RBAC 中间件 `rbac.js` | 架构专家 |
| P0-5 | 旧 token 从 users 表反查真实 tenant（渐进路径，无需轮换 SECRET） | 安全专家 + IMA 第三轮 |

---

## 五、目录结构

```
website-skeleton-skill/
├── SKILL.md                    # Core Skill 指令文件
├── README.md                   # 本文件
├── LICENSE                     # MIT No Attribution
├── CONTRIBUTING.md             # 贡献指南
├── CHANGELOG.md                # 版本变更日志
├── MIGRATION.md                # 升级迁移指南
│
├── templates/                  # 场景预设模板
│   ├── e-commerce.json         # 电商场景
│   ├── ai-assistant.json       # AI 助手场景
│   └── saas-admin.json         # SaaS 管理后台场景
│
├── sharing/                    # 跨运行时共享（构建时同步到 Edge + Cloud）
│   ├── jwt-helper.js           # JWT 签发/验证（RS256 + HS256 兼容）
│   ├── kv-keys.js              # KV key 命名（FNV-1a 64 分区）
│   ├── constants.js            # 角色/状态/权限常量
│   ├── validators.js           # 输入校验
│   └── i18n/                   # 国际化（中/英）
│
├── edge-functions/             # Edge Functions（V8 + KV）
│   ├── api/                    # API 端点
│   │   ├── auth/              # 登录/注册/me
│   │   ├── products/          # 商品列表/详情
│   │   ├── cart/              # 购物车
│   │   ├── orders/            # 订单读取
│   │   └── ai/                # AI 历史
│   ├── middleware/             # 中间件
│   │   ├── rbac.js            # ✅ Phase 4 新增：RBAC 权限检查
│   │   └── quota.js           # ✅ Phase 4 新增：KV 配额限制
│   └── pages/                  # SPA 入口
│
├── cloud-functions/            # Cloud Functions（Node.js + D1）
│   ├── api/
│   │   ├── auth/              # 注册（bcrypt）
│   │   ├── pay/               # 支付创建/回调
│   │   ├── admin/             # 管理后台 CRUD
│   │   ├── order/             # 订单创建/取消/状态机
│   │   └── ai/                # AI SSE 流
│   ├── middleware/
│   │   └── tenant-context.js  # ✅ Phase 4 新增：Cloud 统一租户解析
│   ├── utils/
│   │   └── db.js              # ✅ Phase 4 增强：{tenant} 强制 + 事务 + 不导出 db
│   └── cron/                   # 定时任务（订单超时取消）
│
├── db/                         # 数据库迁移
│   ├── migrations/
│   │   ├── 001_init.sql        # 建表脚本
│   │   ├── 002_order_logs.sql  # 订单审计表
│   │   ├── 003_tenant_isolation.sql  # ✅ Phase 4 新增：租户隔离
│   │   └── 003_rollback.sql    # ✅ Phase 4 新增：回滚脚本
│   └── seed.sql                # 测试数据
│
├── client/                     # 前端 SPA
│   ├── src/
│   │   ├── app.js             # 启动 + History API 路由
│   │   ├── utils/
│   │   │   ├── auth.js        # JWT 客户端
│   │   │   ├── analytics.js   # 埋点 SDK（含 opt-out）
│   │   │   ├── seo.js         # JSON-LD 生成
│   │   │   └── event-bus.js   # 事件总线
│   │   └── services/
│   │       └── ai.js          # AI SSE 客户端
│   │
│   └── index.html             # SPA 入口
│
├── packages/                   # ✅ Phase 4 新增：npm 包源码
│   ├── payment/               # @website-skeleton/payment
│   ├── admin/                 # @website-skeleton/admin
│   └── shared/                # @website-skeleton/shared
│
├── scripts/
│   └── sync-sharing.js        # ✅ Phase 4 增强：构建同步（哈希校验 + CI 阻断）
│
├── references/                 # 按需加载的参考文档
│   ├── auth-module.md
│   ├── payment-module.md
│   ├── ai-chat-module.md
│   ├── admin-module.md
│   ├── order-state-machine.md
│   ├── edge-functions.md
│   ├── cloud-functions.md
│   ├── middleware.md
│   ├── kv-storage.md
│   └── deployment.md
│
└── .github/                    # CI
    ├── workflows/
    │   └── validate.yml        # SKILL.md 校验 + 链接检查
    └── ISSUE_TEMPLATE/
        ├── bug_report.md
        └── feature_request.md
```

---

## 六、安全设计

### 安全措施一览

| 类别 | 措施 | 实现 |
|------|------|------|
| **支付** | 幂等原子锁 | Edge `putIfNotExists` 24h TTL（小于微信 72h 重试窗口） |
| **支付** | 回调 IP 白名单 | Platform Middleware 直接 return |
| **支付** | KV 反查租户 | `order_tenant:{orderId}`，不走 SQL（零绕过） |
| **并发** | RT 乐观锁 | KV version 校验，并发刷新仅第一个成功 |
| **订单** | 防超卖 | `SELECT FOR UPDATE` + 乐观锁 + D1 CHECK 约束（三重） |
| **金额** | 服务端唯一来源 | D1 价格字段，前端不可篡改 |
| **密码** | bcrypt | cost=12，暴力破解成本极高 |
| **Session** | JWT 短期+轮换 | Access Token 15min + Refresh Token 7d |
| **Cookie** | 安全标记 | HttpOnly + Secure + SameSite=Strict |
| **数据库** | 租户隔离 | `DELETE FROM orders WHERE tenant_id = {tenant}`（强制占位符）|
| **数据库** | 防绕过 | db 对象不导出，所有 SQL 走 `query()` / `execute()` 函数 |
| **API** | 租户配额 | KV 滑动窗口限流（单租户 API/存储/调用上限） |
| **API** | 角色鉴权 | Edge RBAC 中间件 + Cloud 租户中间件 |
| **AI** | 会话限流 | 未登录 10次/分，登录 60次/分 |
| **AI** | 所有权校验 | KV session 绑定 userId，防止跨用户读取 |
| **追踪** | 隐私 opt-out | localStorage + DNT 头支持 |

---

## 七、评审历程

本 Skill 经历了 **8 轮评审**：

| 轮次 | 评审方 | 评分 | 核心发现 |
|------|--------|------|---------|
| 1-4 | WorkBuddy + QClaw + Hermes + IMA（两轮） | — | 方案可行，8 项修正 |
| 5 | 🛡️ 独立安全专家 | **7.0/10** 有条件通过 | S-01~S-08 |
| 6 | 🏗️ 独立架构专家 | **7.2/10** 有条件通过 | C1~C3, D1~D5 |
| 7 | ⚙️ 独立平台专家 | **7.5/10** 有条件通过 | B-1~B-4, R-1~R-2 |
| 8 | IMA 第三轮 | 有条件通过 | C1 鸡生蛋修复 + I1 渐进路径 |

**最终结论：** 5 项 P0 前置修复全部完成，4A 可启动。Phase 4 已全部实施完毕，进入维护阶段。

---

## 八、版本历史

| 版本 | 日期 | 内容 |
|------|------|------|
| v1.0 | 2026-04-20 | Phase 1：基础骨架 + Mock Demo |
| v2.0 | 2026-04-23 | Phase 2：JWT 双轨 · 订单状态机 · 支付 |
| v2.2 | 2026-04-26 | Phase 3：RS256 迁移 · SEO · i18n · Analytics · 多租户铺垫 |
| v3.0 | 2026-05-06 | Phase 4A：多租户隔离 + Phase 4B：npm 包化 + 增强 |
| **v3.1.1** | **2026-05-26** | **Phase 4C：前端 SPA + API 端点 + 工程加固** |
| **v3.1.2** | **2026-05-26** | **Phase 4D：SPA 页面补齐 + 脚本 + CI + 文档完缮** |
| **v3.2.0** | **2026-05-26** | **Phase 5：商品详情页 + 227项测试 + 迁移/init-site/密码哈希** |


## 九、License

MIT No Attribution — 详见 [LICENSE](./LICENSE)。

---

*文档更新于 2026-05-26 · v3.2.0 — 工程完缮 + 227项测试 · 如需提交 Issue 或 Feature Request，请使用 [GitHub Issues](https://github.com/liuboacean/website-skeleton-skill/issues)*
