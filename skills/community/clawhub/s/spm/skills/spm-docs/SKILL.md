---
name: spm-docs
version: 1.0.0
description: 文档规范 — Agent 要么不写文档，要么写垃圾文档。本技能给最低文档标准+ADR格式。SPM Phase 2/5 自动引用。
---

# SPM Docs — 文档规范

## 自动检测

SPM Phase 2 写 spec/plan 时和 Phase 5 交付时自动引用本技能。

## 独立使用

不走 SPM 也可以直接说："按 spm-docs 规范写 README。"

---

## Agent 文档 5 大反模式

| # | 反模式 | 症状 |
|---|--------|------|
| 1 | **零文档** | "代码自解释"——实际上谁也看不懂 |
| 2 | **复述代码** | "`getUser(id)` 通过 id 获取用户"——不需要文档 |
| 3 | **过时文档** | 代码改了三版，README 还是第一版 |
| 4 | **只有 happy path** | "运行 `npm start` 就行"——没说 Node 版本/环境变量/常见错误 |
| 5 | **鬼话连篇** | "采用先进的微服务架构实现高可用"——0 信息量 |

---

## 必写文档（按优先级）

### 1. README.md

```markdown
# Project Name
一句话说清做什么。

## Quick Start
```bash
git clone ...
cp .env.example .env   # 填你的密钥
npm install
npm run dev
```

## Prerequisites
- Node.js ≥ 18
- PostgreSQL 15+
- Redis (optional)

## 项目结构
src/components/    # React 组件
src/routes/        # API 路由
tests/             # 测试

## Environment Variables
| 变量 | 必需 | 默认 | 说明 |
|------|------|------|------|
| DATABASE_URL | 是 | - | PostgreSQL 连接串 |
| JWT_SECRET | 是 | - | 随机 64 字符 |

## Common Issues
- "port 3000 in use" → `kill -9 $(lsof -t -i:3000)`
```

### 2. API 文档

如果项目有 API，文档必须包含：
- 每个端点：URL + method + 请求体 + 响应体 + 状态码
- 认证方式
- 示例 curl 命令

### 3. Architecture Decision Records (ADR)

重大技术决策用 ADR 格式记录：

```markdown
# ADR 001: 选择 PostgreSQL 而非 MongoDB

**Status**: Accepted | Deprecated | Superseded by [ADR 003]
**Date**: 2026-05-10
**Context**: 需要强一致性和复杂查询支持
**Decision**: 使用 PostgreSQL 作为主数据库
**Consequences**: 
  - ✅ ACID、JOIN、成熟的迁移工具
  - ❌ 水平扩展不如 MongoDB
  - ❌ Schema 变更需要迁移脚本
```

---

## 什么该写、什么不该写

| ✅ 写 WHY | ❌ 不写 WHAT |
|-----------|-------------|
| "用 Redis 缓存是为了减轻 DB 压力" | "`cache.get(key)` 获取缓存值" |
| "JWT 而不是 Session 是因为服务要无状态" | "调用 `jwt.sign()` 生成 token" |
| "拒绝 WebSocket 是因为当前 MVP 不需要实时" | "`app.get('/api/users')` 返回用户列表" |

**代码告诉 WHAT，文档告诉 WHY。**

---

## 文档更新规则

```
✅ 改 API → 同步更新 API 文档
✅ 改 schema → 同步更新 README 的环境变量表
✅ 改架构 → 写新的 ADR
✅ 废弃旧方案 → 标记旧 ADR 为 Deprecated

❌ "等做完再补文档" → 永远不会补
❌ "这个太简单了不需要文档" → 新人不觉得简单
```

**铁律：改代码的同时改文档。不同步 = 文档死亡。**
