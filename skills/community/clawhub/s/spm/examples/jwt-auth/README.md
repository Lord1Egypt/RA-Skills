# 示例项目：JWT 用户认证系统

> 这是一个完整的 SPM 示例项目，展示了从 Phase 1 到 Phase 5 的完整产出物。
> 所有文件都是填好的真实内容，不是模板占位符。

## 项目概述

- **目标**：为 Web 应用添加 JWT 用户认证功能（注册/登录/Token刷新/权限中间件）
- **技术栈**：Node.js + Express + PostgreSQL + jsonwebtoken
- **项目类型**：`code`
- **执行模式**：`subagent`

## Phase 产出物

| Phase | 文件 | 说明 |
|-------|------|------|
| Phase 1 | `specs/2026-05-09-jwt-auth-design.md` | 需求设计文档（灵魂拷问 + 架构 + API 契约） |
| Phase 2 | `plans/2026-05-09-jwt-auth-plan.md` | 实施计划（WBS 6 任务） |
| Phase 2 | `ledger.md` | WBS 台账（含 Context Brief + Eval Delta） |
| Phase 2 | `reviews/2026-05-09-plan-review.md` | 对抗性计划审查报告 |
| Phase 4 | `reviews/2026-05-09-verification.md` | 标准化验证报告 |

## 项目结构（最终产出）

```
jwt-auth/
├── src/
│   ├── models/user.js          # User 模型 + DB Schema
│   ├── middleware/auth.js       # JWT 验证中间件
│   ├── routes/auth.js           # 注册/登录/刷新路由
│   └── utils/token.js           # Token 签发/验证工具
├── tests/
│   ├── auth.test.js             # 认证路由测试
│   └── token.test.js            # Token 工具测试
├── migrations/
│   └── 001_create_users.sql     # 用户表迁移
├── docs/spm/
│   ├── specs/                   # 设计文档
│   ├── plans/                   # 实施计划
│   ├── reviews/                 # 审查报告
│   └── ledger.md                # WBS 台账
└── package.json
```

---

## 如何使用此示例

1. 阅读文件顺序：spec → plan → ledger → plan-review → verification
2. 对比你自己的 SPM 项目，看每个 Phase 应该产出什么
3. 模板占位符参考：`templates/prd-template.md` 和 `references/task-ledger-template.md`
