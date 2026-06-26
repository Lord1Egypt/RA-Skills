---
name: super-dev
description: "Super Dev pipeline governance: research-first, commercial-grade AI coding delivery with 10 expert roles, quality gates, and audit artifacts."
user-invocable: true
metadata: {"openclaw":{"requires":{"bins":["super-dev"]},"homepage":"https://superdev.goder.ai","install":[{"id":"pip","kind":"uv","formula":"super-dev","bins":["super-dev"],"label":"pip install super-dev"}]}}
---

# Super Dev - AI 开发治理 Skill

> `pip install super-dev` → `openclaw plugins install @super-dev/openclaw-plugin`

## 定位

- **插件（Plugin）**：桥梁，将 13 个 Tool 注册到 OpenClaw，每个 Tool 调用本地 `super-dev` CLI
- **技能（Skill）**：引导 OpenClaw Agent 按治理协议工作，确保流程不被跳过
- **CLI**：核心治理引擎，提供流程编排、质量门禁、审计产物

**OpenClaw Agent 负责**：模型调用、联网搜索、文件读写、代码生成。
**Super Dev 负责**：流程规范、质量门禁、设计约束、交付标准。

## 触发

用户输入 `/super-dev <需求>` 或 `super-dev: <需求>` 时，进入流水线模式。

## 知识库契约（强制）

每个阶段开始前，**必须**检查并读取项目知识库：

1. 读取 `knowledge/` 目录中与当前阶段相关的知识文件
2. 读取 `output/knowledge-cache/*-knowledge-bundle.json`（若存在）
3. 知识库中的标准 = **硬约束**（必须遵循）
4. 知识库中的检查清单 = **门禁**（必须逐项通过）
5. 知识库中的反模式 = **禁止项**（必须回避）
6. 读取 `output/*-ai-prompt.md` 中的"知识推送"章节（含阶段约束和反模式）

阶段-知识域映射：
- research/docs → product, architecture, design, security
- frontend → frontend, design, development (按技术栈过滤)
- backend → backend, data, security (按技术栈过滤)
- quality → testing, security, operations

## 流水线（使用 Plugin Tool）

### Step 1: 启动流水线
```
调用 super_dev_pipeline Tool:
  description: "用户的需求描述"
  frontend: "react"
  backend: "node"
```
产出: `output/*-research.md`, `output/*-prd.md`, `output/*-architecture.md`, `output/*-uiux.md`

### Step 2: 文档确认门禁 — 强制暂停
```
三份核心文档已完成。请查看后确认。
调用 super_dev_review Tool:
  type: "docs"
  status: "confirmed"
  comment: "用户已确认"
```
**未经确认不得编码。**

### Step 3: Spec 创建
```
调用 super_dev_spec Tool:
  action: "propose"
  changeId: "feature-name"
  title: "功能标题"
  description: "功能描述"
```

### Step 4: 前端实现
由 OpenClaw Agent 按 `output/*-uiux.md` 和 tasks.md 实现前端，然后验证：
```
调用 super_dev_run Tool:
  command: "run frontend"
```

### Step 5: 预览确认门禁 — 强制暂停
请用户预览前端效果。不满意则 UI 返工。

### Step 6: 后端实现
由 OpenClaw Agent 实现后端 + 测试。

### Step 7: 质量检查
```
调用 super_dev_quality Tool:
  type: "all"
```
必须 >= 80 分才能继续。未达标则修复后重跑。

### Step 8: 部署配置
```
调用 super_dev_deploy Tool:
  cicd: "github"
  docker: true
```

### Step 9: 交付
```
调用 super_dev_release Tool:
  action: "proof-pack"
```

## 可用 Tool 速查

| Tool | 用途 | 关键参数 |
|------|------|----------|
| `super_dev_pipeline` | 启动完整流水线 | description, frontend, backend |
| `super_dev_init` | 初始化项目 | name, frontend, backend |
| `super_dev_status` | 查看状态 | 无 |
| `super_dev_quality` | 质量门禁 | type: all/code/prd |
| `super_dev_spec` | Spec 管理 | action: list/propose/validate |
| `super_dev_review` | 门禁确认 | type: docs/ui/architecture |
| `super_dev_release` | 发布管理 | action: readiness/proof-pack |
| `super_dev_expert` | 专家咨询 | role: PM/ARCHITECT/SECURITY... |
| `super_dev_deploy` | 部署配置 | cicd, docker, rehearsal |
| `super_dev_analyze` | 项目分析 | 无 |
| `super_dev_doctor` | 环境诊断 | host |
| `super_dev_config` | 配置管理 | action: list/get/set |
| `super_dev_run` | 通用命令 | command: 任意 CLI 命令 |

## 首轮响应

用户首次触发时，回复：
```
Super Dev 流水线已激活。

当前阶段：research
顺序：research → 三文档 → 确认 → Spec → 前端 → 后端 → 质量 → 交付
三文档完成后暂停等确认。

正在启动...
```
然后立即调用 `super_dev_pipeline` Tool。

## UI 强制规则

- 禁止 emoji 充当功能图标
- 禁止紫/粉渐变主视觉
- 必须先定义设计 Token 再实现页面
- 组件需完整状态（hover/focus/loading/empty/error）

## 返工

| 场景 | 操作 |
|------|------|
| UI 不满意 | 更新 uiux.md → 重做前端 → `super_dev_review type:ui status:confirmed` |
| 架构变更 | 更新 architecture.md → 同步 tasks → `super_dev_review type:architecture status:confirmed` |
| 质量不达标 | 修复 → `super_dev_quality` → `super_dev_review type:quality status:confirmed` |

## 恢复

```
super_dev_status             → 查看当前状态
super_dev_run command:"run --resume"  → 从中断处继续
```

## System Flow Contract
- PHASE_CHAIN: research>docs>docs_confirm>spec>frontend>preview_confirm>backend>quality>delivery
- DOC_CONFIRM_GATE: required
- PREVIEW_CONFIRM_GATE: required
