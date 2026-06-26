# 示例条目

## 学习：纠正

```markdown
## [LRN-20260326-001] correction

- Agent: agent1
- Logged: 2026-03-26T10:30:00+08:00
- Priority: high
- Status: pending
- Area: tests

### 摘要
错误地假设 pytest fixtures 默认为函数作用域

### 详情
编写测试 fixtures 时，我假设所有 fixtures 都是函数作用域的。用户纠正说虽然函数作用域是默认的，但代码库约定对数据库连接使用模块作用域的 fixtures 以提高测试性能。

### 建议行动
创建涉及昂贵设置（DB、网络）的 fixtures 时，在默认为函数作用域之前检查现有 fixtures 的作用域模式。

### 元数据
- Source: user_feedback
- Related Files: tests/conftest.py
- Tags: pytest, testing, fixtures

---
```

## 学习：知识缺口（已解决）

```markdown
## [LRN-20260326-002] knowledge_gap

- Agent: agent1
- Logged: 2026-03-26T14:22:00+08:00
- Priority: medium
- Status: resolved
- Area: config

### 摘要
项目使用 pnpm 而不是 npm 进行包管理

### 详情
尝试运行 `npm install` 但项目使用 pnpm workspaces。锁文件是 `pnpm-lock.yaml`，而不是 `package-lock.json`。

### 建议行动
在假设 npm 之前检查 `pnpm-lock.yaml` 或 `pnpm-workspace.yaml`。为此项目使用 `pnpm install`。

### 元数据
- Source: error
- Related Files: pnpm-lock.yaml, pnpm-workspace.yaml
- Tags: package-manager, pnpm, setup

### 解决方案
- **Resolved**: 2026-03-26T14:30:00Z
- **Commit/PR**: N/A - 知识更新
- **Notes**: 已添加到 CLAUDE.md 以供将来参考

---
```

## 学习：提升到 SOUL.md

```markdown
## [LRN-20260326-003] best_practice

- Agent: agent1
- Logged: 2026-03-26T16:00:00+08:00
- Priority: high
- Status: promoted
- Promoted: SOUL.md
- Promoted-By: agent1
- Area: backend

### 摘要
API 响应必须包含请求头中的关联 ID

### 详情
所有 API 响应应该回传请求中的 X-Correlation-ID 头。这是分布式跟踪所必需的。没有此头的响应会破坏可观察性管道。

### 建议行动
始终在 API 处理程序中包含关联 ID 传递。

### 元数据
- Source: user_feedback
- Related Files: src/middleware/correlation.ts
- Tags: api, observability, tracing

---
```

## 错误条目

```markdown
## [ERR-20260326-A3F] docker_build

- Agent: agent1
- Logged: 2026-03-26T09:15:00+08:00
- Priority: high
- Status: pending
- Area: infra

### 摘要
Docker 构建在 M1 Mac 上因平台不匹配而失败

### 错误
```
error: failed to solve: python:3.11-slim: no match for platform linux/arm64
```

### 上下文
- 命令：`docker build -t myapp .`
- Dockerfile 使用 `FROM python:3.11-slim`
- 在 Apple Silicon (M1/M2) 上运行

### 建议修复
添加平台标志：`docker build --platform linux/amd64 -t myapp .`
或更新 Dockerfile：`FROM --platform=linux/amd64 python:3.11-slim`

### 元数据
- Reproducible: yes
- Related Files: Dockerfile

---
```

## 功能需求

```markdown
## [FEAT-20260326-001] export_to_csv

- Agent: agent1
- Logged: 2026-03-26T16:45:00+08:00
- Priority: medium
- Status: pending
- Area: backend

### 请求的能力
导出分析结果为 CSV 格式

### 用户上下文
用户运行每周报告，需要与非技术利益相关者在 Excel 中共享结果。目前手动复制输出。

### 复杂度估算
simple

### 建议实现
为 analyze 命令添加 `--output csv` 标志。使用标准 csv 模块。可以扩展现有的 `--output json` 模式。

### 元数据
- Frequency: recurring
- Related Features: analyze command, json output

---
```
