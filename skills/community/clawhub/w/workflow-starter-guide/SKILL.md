---
name: openclaw-workflow-starter
description: OpenClaw 工作流快速入门指南 - 含业务流程处理（TaskFlow）与数字资源入库（ClawHub）的端到端实操步骤，适用于新用户在 30 分钟内完成从内容创作到资源发布的完整链路
metadata:
  clawdbot:
    emoji: "🚀"
    requires:
      - bins: [openclaw, clawhub]
      - install:
          - id: node
            kind: node
            package: clawhub
            bins: [clawhub]
            label: Install ClawHub CLI
  author: terrycarter1985
  created: "2026-08-16"
  version: "1.0.0"
  tags:
    - guide
    - workflow
    - openclaw
    - taskflow
    - digital-resource
    - onboarding
---

# OpenClaw 工作流快速入门指南 v1.0.0

## 概述

本指南面向 OpenClaw 新用户，提供从**业务流程处理**到**数字资源入库**的端到端实操流程。读完本指南后，你将能够：

1. 使用 TaskFlow 编排多步骤业务工作流
2. 使用 ClawHub 将数字资源发布到资源中心
3. 掌握两个工具串联配合的标准作业流程（SOP）

---

## 第一部分：业务流程处理（TaskFlow）

### 用途
TaskFlow 是 OpenClaw 内置的**持久化工作流编排引擎**。它不负责业务逻辑本身，而是为多步骤、跨会话、可能需要人工介入的工作流提供统一的状态管理、子任务链接和生命周期控制。

### 适用场景
- 多步骤后台任务，需在多个会话间保持上下文
- 需要等待外部系统或人类回复的工作流
- 子智能体（subagent / ACP）编排
- 需要持久化状态的插件或工具

### 前置条件
- OpenClaw 运行时环境
- 工具上下文 `ctx` 含有效 `sessionKey`
- 对 `api.runtime.tasks.flow` 的访问权限

### 基本步骤
```text
步骤 1: 创建托管流 (createManaged)
        ↓
步骤 2: 运行子任务 (runTask)
        ↓
步骤 3: 等待外部输入 (setWaiting) -- 可选
        ↓
步骤 4: 恢复执行 (resume) -- 从 waiting 恢复
        ↓
步骤 5: 完成或失败 (finish / fail)
```

### 核心 API 速查
```typescript
// 1. 创建工作流
const created = taskFlow.createManaged({
  controllerId: "your-plugin/id",     // 控制器标识
  goal: "人类可读的目标描述",         // 工作流目标
  currentStep: "step1_classify",      // 当前步骤
  stateJson: { /* 持久化状态 */ }     // 初始状态
});

// 2. 运行子任务（如 ACP / subagent）
const child = taskFlow.runTask({
  flowId: created.flowId,
  runtime: "acp",                     // "acp" 或 "subagent"
  task: "子任务描述",
  status: "running",
  startedAt: Date.now(),
  lastEventAt: Date.now(),
});

// 3. 等待外部输入（如 Slack 回复、表单提交）
const waiting = taskFlow.setWaiting({
  flowId: created.flowId,
  expectedRevision: created.revision,  // 必须携带最新 revision
  currentStep: "await_external",
  stateJson: { /* 更新状态 */ },
  waitJson: { kind: "reply", channel: "slack", threadKey: "..." },
});

// 4. 恢复工作流
const resumed = taskFlow.resume({
  flowId: waiting.flow.flowId,
  expectedRevision: waiting.flow.revision,
  status: "running",
  currentStep: "finalize",
  stateJson: waiting.flow.stateJson,
});

// 5. 完成
taskFlow.finish({
  flowId: resumed.flow.flowId,
  expectedRevision: resumed.flow.revision,
  stateJson: resumed.flow.stateJson,
});
```

---

## 第二部分：数字资源入库与管理（ClawHub）

### 用途
ClawHub 是 OpenClaw 生态的**数字资源注册表**。用于发布、发现、安装和更新 Agent Skills、指南、模板等数字资源。

### 适用场景
- 发布 Agent Skill 到公共/私有注册表
- 管理团队内部知识资产
- 同步技能到最新版本
- 搜索和发现可用的数字资源

### 前置条件
- Node.js 环境
- ClawHub CLI: `npm i -g clawhub`
- 登录凭证: `clawhub login`
- 待发布资源的目录结构

### 基本步骤
```text
步骤 1: 准备资源目录（含 SKILL.md 和 _meta.json）
        ↓
步骤 2: 质量检查（核对清单见下）
        ↓
步骤 3: 元数据填写（name, description, version, tags）
        ↓
步骤 4: 发布到注册表（clawhub publish）
        ↓
步骤 5: 验证发布结果（clawhub search / clawhub list）
```

### 质量检查清单
- [ ] `SKILL.md` 存在且格式正确
- [ ] `_meta.json` 包含必填字段
- [ ] 描述在 10-200 字之间，包含关键术语
- [ ] 标签 3-8 个，覆盖宽泛+具体维度
- [ ] 无敏感信息
- [ ] 链接可访问（如有）
- [ ] 版本号遵循 SemVer (x.y.z)

### 常用命令
```bash
# 搜索资源
clawhub search "数字资源管理"
clawhub search "workflow"

# 安装资源
clawhub install <skill-slug>
clawhub install <skill-slug> --version 1.0.0

# 更新资源
clawhub update <skill-slug>
clawhub update --all

# 发布资源
clawhub publish ./my-skill \
  --slug my-skill-slug \
  --name "显示名称" \
  --version 1.0.0 \
  --changelog "变更说明"

# 查看已安装
clawhub list
```

---

## 第三部分：串联配合 — 从内容处理到资源入库的完整流程

### 流程总览
```
[内容创作] → [TaskFlow 流程编排] → [ClawHub 发布入库] → [资源中心]
      │            │                        │
      │            │                        │
      │            └─ 质量检查、元数据填写  ─┘
      │                     │
      └─────────────────────┘
```

### 端到端执行顺序（可复现）

#### 阶段 A：使用 TaskFlow 处理数字内容（流程编排）

```text
A.1 创建资源工作流实例
    目标：为本次入库任务创建独立的工作流上下文

    调用：taskFlow.createManaged({
      controllerId: "digital-resource/ingest",
      goal: "发布新数字资源到 ClawHub",
      currentStep: "prepare_content",
      stateJson: {
        resourceName: "openclaw-workflow-starter",
        author: "terrycarter1985",
        steps: { prepare: false, review: false, publish: false, verify: false }
      }
    })

A.2 运行内容准备子任务
    目标：确保资源目录结构完整、SKILL.md 格式正确

    调用：taskFlow.runTask({
      flowId: <flowId>,
      runtime: "subagent",
      task: "Verify resource directory structure and SKILL.md format",
      status: "running",
      startedAt: Date.now(),
      lastEventAt: Date.now(),
    })

A.3 更新状态：内容准备完成
    调用：taskFlow.resume({
      flowId: <flowId>,
      expectedRevision: <revision>,
      currentStep: "quality_review",
      stateJson: { ..., steps: { prepare: true, ... } }
    })

A.4 设置等待状态（如需人工审核）
    目标：暂停工作流等待人类审核元数据

    调用：taskFlow.setWaiting({
      flowId: <flowId>,
      expectedRevision: <revision>,
      currentStep: "await_human_review",
      waitJson: {
        kind: "human",
        resource: "openclaw-workflow-starter",
        checklist: ["metadata", "tags", "sensitive-info"]
      }
    })

A.5 恢复工作流并标记审核通过
    调用：taskFlow.resume({
      flowId: <flowId>,
      expectedRevision: <revision>,
      currentStep: "publish_to_clawhub",
      stateJson: { ..., steps: { review: true, ... } }
    })
```

#### 阶段 B：使用 ClawHub 发布入库

```text
B.1 确认资源目录结构
    路径：~/workspace/assets/resource-center-example/
    ├── SKILL.md          # 技能描述文档（必填）
    ├── _meta.json        # 元数据文件（必填）
    ├── reference/        # 参考资料（可选）
    └── assets/           # 媒体资源（可选）

B.2 核对元数据（_meta.json）
    {
      "name": "openclaw-workflow-starter",
      "version": "1.0.0",
      "description": "...",
      "author": "terrycarter1985",
      "created": "2026-08-16",
      "tags": ["guide", "workflow", "openclaw"]
    }

B.3 执行发布命令
    命令：
    clawhub publish ./assets/resource-center-example \
      --slug openclaw-workflow-starter \
      --name "OpenClaw 工作流快速入门指南" \
      --version 1.0.0 \
      --changelog "初始版本：TaskFlow + ClawHub 端到端流程"

B.4 更新 TaskFlow 状态为发布完成
    调用：taskFlow.resume({
      flowId: <flowId>,
      expectedRevision: <revision>,
      currentStep: "verify_release",
      stateJson: { ..., steps: { publish: true } }
    })

B.5 验证发布结果
    命令：
    clawhub search "openclaw-workflow"
    clawhub list

B.6 完成工作流
    调用：taskFlow.finish({
      flowId: <flowId>,
      expectedRevision: <revision>,
      stateJson: { ..., steps: { verify: true }, status: "published" }
    })
```

---

## 第四部分：输入输出关系与关键注意事项

### TaskFlow ↔ ClawHub 数据流

| 阶段 | TaskFlow 状态 (stateJson) | ClawHub 操作 |
|------|--------------------------|--------------|
| 内容准备 | `steps.prepare: true` | 目录创建、SKILL.md 编写 |
| 质量审核 | `steps.review: true` | 核对清单、元数据校验 |
| 发布执行 | `steps.publish: true` | `clawhub publish` |
| 验证完成 | `steps.verify: true` | `clawhub search/list` |

### 关键注意事项

**TaskFlow 侧**
1. **Revision 必须正确传递**：每次 mutation 必须携带 `expectedRevision`，否则会失败
2. **状态只存必要数据**：`stateJson` 只保留能恢复工作流的最小集合
3. **Waiting 必须明确**：`waitJson` 要清晰记录等待的原因和恢复条件
4. **不持有业务逻辑**：条件判断、分支决策放在上层，TaskFlow 只管状态和生命周期

**ClawHub 侧**
1. **slug 唯一**：`--slug` 参数决定资源唯一标识，发布后无法更改
2. **版本号递增**：同一 slug 下每次发布必须使用更高的 SemVer 版本号
3. **标签影响发现率**：用 3-8 个标签，避免太泛或太窄
4. **描述要具体**：描述包含关键术语会显著提高搜索排名

**串联配合侧**
1. **错误处理**：ClawHub 发布失败时，TaskFlow 应 `fail` 而非 `finish`
2. **可追溯性**：在 TaskFlow stateJson 中记录 ClawHub 发布结果（slug、version、发布时间）
3. **幂等性**：同一内容的重复发布应有检测机制，避免重复工作

---

## 第五部分：他人可复现的执行清单

### 准备环境
```bash
# 1. 安装 ClawHub CLI
npm i -g clawhub

# 2. 登录
clawhub login

# 3. 验证登录
clawhub whoami
```

### 执行步骤（按顺序）

| # | 操作 | 命令 / API | 预期结果 |
|---|------|-----------|----------|
| 1 | 创建资源目录 | `mkdir -p <path>/reference <path>/assets` | 目录创建成功 |
| 2 | 编写 SKILL.md | 参照本指南格式 | 文件存在且格式正确 |
| 3 | 填写 _meta.json | 填写必填字段 | JSON 校验通过 |
| 4 | 启动 TaskFlow | `taskFlow.createManaged(...)` | 返回 `flowId` 和 `revision` |
| 5 | 运行内容校验 | `taskFlow.runTask(...)` | 子任务创建成功 |
| 6 | 更新状态 | `taskFlow.resume(...)` | 返回更新后的 `revision` |
| 7 | 等待人工审核 | `taskFlow.setWaiting(...)` | 流程进入 waiting 状态 |
| 8 | 恢复流程 | `taskFlow.resume(...)` | 流程回到 running |
| 9 | 发布到 ClawHub | `clawhub publish ...` | 返回发布成功消息 |
| 10 | 验证搜索 | `clawhub search "<slug>"` | 资源出现在结果中 |
| 11 | 完成工作流 | `taskFlow.finish(...)` | 流程标记为 finished |

### 验证入库结果
```bash
# 1. 本地已安装
clawhub list | grep openclaw-workflow-starter

# 2. 注册表可搜索
clawhub search "openclaw workflow starter"

# 3. 远程验证
curl -s https://clawhub.com/skills/openclaw-workflow-starter | head -c 200
```

---

## 参考资源

- TaskFlow 官方文档: `skills/taskflow/SKILL.md`
- TaskFlow 示例: `skills/taskflow/examples/inbox-triage.lobster`
- ClawHub 注册表: https://clawhub.com
- 数字资源管理指南: `skills/digital-resource-management-guide/SKILL.md`

---

**入库记录**
- 发布时间: 2026-08-16
- 发布者: terrycarter1985
- 资源中心: ClawHub Registry
- 状态: 已发布
