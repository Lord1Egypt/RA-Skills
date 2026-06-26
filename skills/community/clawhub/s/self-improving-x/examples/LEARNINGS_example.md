# 学习日志

在开发过程中捕获的纠正、见解和知识差距。

**类别**: correction | insight | knowledge_gap | best_practice
**领域**: frontend | backend | infra | tests | docs | config
**状态**: pending | in_progress | resolved | wont_fix | promoted | promoted_to_skill

## 前言

### 状态定义

| 状态 | 含义 |
|--------|---------|
| `pending` | 尚未处理 |
| `in_progress` | 正在积极处理 |
| `resolved` | 问题已修复或知识已整合 |
| `wont_fix` | 决定不处理（在解析中注明原因） |
| `promoted` | 已提升到 CLAUDE.md、AGENTS.md 或 copilot-instructions.md |
| `promoted_to_skill` | 已提取为可重用技能 |

### 技能提取字段

当学习内容被提升为技能时，添加以下字段：

```markdown
**状态**: promoted_to_skill
**技能路径**: skills/skill-name
```

---

## [LRN-20250115-001] 纠正

**记录时间**: 2025-01-15T10:30:00Z
**优先级**: high
**状态**: pending
**领域**: tests

### 摘要
错误地假设 pytest fixtures 默认是函数作用域的

### 详情
在编写测试 fixtures 时，我假设所有 fixtures 都是函数作用域的。
用户纠正说，虽然函数作用域是默认值，但代码库
约定使用模块作用域的 fixtures 用于数据库连接以
提高测试性能。

### 建议操作
创建涉及昂贵设置（数据库、网络）的 fixtures 时，
在默认使用函数作用域之前，检查现有 fixtures 的作用域模式。

### 元数据
- 来源: user_feedback
- 相关文件: tests/conftest.py
- 标签: pytest, testing, fixtures

---


## [LRN-20250115-002] 知识差距

**记录时间**: 2025-01-15T14:22:00Z
**优先级**: medium
**状态**: resolved
**领域**: config

### 摘要
项目使用 pnpm 而不是 npm 进行包管理

### 详情
尝试运行 `npm install`，但项目使用 pnpm workspaces。
锁文件是 `pnpm-lock.yaml`，不是 `package-lock.json`。

### 建议操作
在假设使用 npm 之前，检查 `pnpm-lock.yaml` 或 `pnpm-workspace.yaml`。
为此项目使用 `pnpm install`。

### 元数据
- 来源: error
- 相关文件: pnpm-lock.yaml, pnpm-workspace.yaml
- 标签: package-manager, pnpm, setup

### 解析
- **已解决**: 2025-01-15T14:30:00Z
- **提交/PR**: N/A - 知识更新
- **备注**: 已添加到 CLAUDE.md 以供将来参考

---

## [LRN-20250115-003] 最佳实践

**记录时间**: 2025-01-15T16:00:00Z
**优先级**: high
**状态**: promoted
**领域**: backend
**已提升**: AGENTS.md

### 摘要
API 响应必须包含请求头中的 correlation ID

### 详情
所有 API 响应都应该回显请求中的 X-Correlation-ID 头。
这是分布式追踪所必需的。没有此头的响应
会破坏可观察性管道。

### 建议操作
始终在 API 处理器中包含 correlation ID 直通。

### 元数据
- 来源: user_feedback
- 相关文件: src/middleware/correlation.ts
- 标签: api, observability, tracing

---

## [LRN-20250116-001] 最佳实践

**记录时间**: 2025-01-16T09:00:00Z
**优先级**: high
**状态**: promoted
**领域**: backend
**已提升**: AGENTS.md

### 摘要
OpenAPI 规范更改后必须重新生成 API 客户端

### 详情
修改 API 端点时，必须重新生成 TypeScript 客户端。
忘记这一点会导致运行时才出现的类型不匹配。
生成脚本也会运行验证。

### 建议操作
添加到智能体工作流：任何 API 更改后，运行 `pnpm run generate:api`。

### 元数据
- 来源: error
- 相关文件: openapi.yaml, src/client/api.ts
- 标签: api, codegen, typescript

---

## [LRN-20250118-001] 最佳实践

**记录时间**: 2025-01-18T11:00:00Z
**优先级**: high
**状态**: promoted_to_skill
**领域**: infra
**技能路径**: skills/docker-m1-fixes

### 摘要
Docker build 在 Apple Silicon 上因平台不匹配而失败

### 详情
在 M1/M2 Mac 上构建 Docker 镜像时，构建失败，因为
基础镜像没有 ARM64 变体。这是一个常见问题
影响许多开发者。

### 建议操作
在 docker build 命令中添加 `--platform linux/amd64`，或在 Dockerfile 中使用
`FROM --platform=linux/amd64`。

### 元数据
- 来源: error
- 相关文件: Dockerfile
- 标签: docker, arm64, m1, apple-silicon
- 另请参阅: ERR-20250115-A3F, ERR-20250117-B2D

---
