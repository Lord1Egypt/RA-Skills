---
name: sdd-writing-plans
description: "当有规格说明或需要多步骤任务的需求时，在编写代码之前使用。根据 spec-design.md 生成可执行的 spec-plan.md。"
---

# SDD Writing Plans — 编写执行计划

## Overview

读取 `spec-design.md` 文档，生成单一交付物：

**`spec-plan.md`** — 逐步执行计划。每个 Task 包含执行步骤和对应的验证检查清单。

计划保存到源 `spec-design.md` 所在的同一目录。

原则：DRY, YAGNI。保持计划简洁——描述意图和关键逻辑，而非样板代码。

**启动时声明：** "我正在使用 sdd-writing-plans 技能来创建执行和验证计划。"

## 关键概念

- **工作区 (Workspace)：** 通过 `.sdd-workspace` 配置文件中 `workspace_path` 指定的根目录
- **Spec 目录：** 所有 SDD 文档存储在 `{workspace}/spec/` 下

## Step 0: 读取工作区配置

在任何操作之前，必须读取工作区配置：

1. 检查当前 OpenClaw workspace 中是否存在 `.sdd-workspace`
2. 如果存在，读取 `workspace_path` 作为工作区根目录 `{workspace}`
3. 如果不存在，显示错误："请先运行 `/sdd-global-init` 初始化工作区。" 并**停止**

验证工作区目录存在，如果不存在提示用户重新初始化。

## Step 1: 模型检查

检查当前模型是否为 Opus。如果不是 Opus，输出以下纯文本消息并继续（非阻塞）：

```
⚠️ 当前模型不是 Opus，建议切换到 Opus 以获得最佳计划生成质量。输入 /model 切换模型。
```

## Step 1: 启动与 Feature 发现

### 前置条件

此技能运行前**必须**存在 `spec-design.md` 文件。

### 定位 spec-design

1. 如果用户提供了路径（例如 `/sdd-writing-plans {workspace}/spec/feature_xxx/spec-design.md`），直接使用。
2. 否则，扫描 `{workspace}/spec/` 中所有匹配 `feature_*/spec-design.md` 的目录。按修改时间排序（最新优先），向用户展示**最新的 3 个**通过 `AskUserQuestion` 选择（用户也可以通过 "Other" 输入自定义路径）。
3. 读取选中的 `spec-design.md` 作为输入上下文。

## Step 2: 执行清单

0. **模型检查** — 检测当前模型是否为 Opus（检查 system prompt 中的模型信息）；如果不是 Opus，输出纯文本建议（非阻塞：无论如何都继续）。
1. **声明** 技能激活。
2. **定位并读取** `spec-design.md`（参见启动与 Feature 发现）。
3. **探索项目背景** — 扫描相关源文件、现有模式和规范，为计划提供信息。
4. **一次性生成所有计划** — 为所有 Task 起草执行步骤和匹配的验证项目，**包括一个最终验收 Task，其端到端验证场景派生自 spec**。不要让用户逐个确认每个 Task。
5. **最终审核** — 输出下面的最终审核格式中定义的两个 Markdown 表，然后使用 `AskUserQuestion` 提供两个选项（确认/请求修改）。只有用户确认后，才继续写入文件。
6. **写入文件** — 将 `spec-plan.md` 保存到与 `spec-design.md` 相同的目录。

## 计划模板

````markdown
# [功能名称] 执行计划

**目标:** [一句话描述]

**技术栈:** [关键技术/库]

**设计文档:** [spec-design.md 的相对路径]

---

### Task N: [组件/模块名称]

**涉及文件:**
- 新建: `exact/path/to/file.ts`
- 修改: `exact/path/to/existing.ts`

**执行步骤:**
- [ ] [描述意图：做什么，为什么]
  - 关键代码或逻辑说明
- [ ] [下一步意图]
  - ...

**检查步骤:**
- [ ] 检查描述
  - `可执行的验证命令`
  - 预期: 预期输出描述
- [ ] 另一个检查
  - `curl/grep/script 命令`
  - 预期: 一句话描述预期输出

---

### Task [last]: [Feature Name] Acceptance

**前置条件:**
- 启动命令: `exact start command`
- 测试数据准备: `setup command or steps`
- 其他环境准备...

**端到端验证:**

1. [场景描述]
   - `curl/script 验证命令`
   - Expected: expected result description
   - On failure: check Task N [related module name]

2. [另一个场景]
   - `curl/script 验证命令`
   - Expected: expected result description
   - On failure: check Task N [related module name]

3. [Next scenario]
   - ...
````

## 检查步骤指南

所有检查步骤必须是可通过 CLI/curl/脚本自动执行的命令。
不要使用 `[HUMAN]` 标签 — 需要人工验证的场景由 sdd-plan-human-verify 技能单独处理。

每个检查步骤**必须**包含可执行命令和预期结果：

```
- [ ] 检查描述
  - `可执行的验证命令`
  - 预期: 预期输出描述
```

示例：
```
- [ ] 验证 API 返回正确的用户信息
  - `curl -s http://localhost:3001/api/auth/me -H 'Authorization: Bearer TOKEN' | jq .userCode`
  - 预期: 返回 "chenwx57"

- [ ] 验证前端构建无错误
  - `cd key-portal/web && npm run build 2>&1 | tail -5`
  - 预期: 输出包含 "built in" 且无 error
```

## 最终审核格式

写入文件前，输出以下两个 Markdown 表供用户审核。

**汇总表**（单行）：

| 功能 | Task 数量 | 新增文件数 | 修改文件数 |
|------|-----------|------------|------------|
| [spec title] | N | X | Y |

> 文件数必须去重 — 一个文件被多个 Task 触碰只计算一次。

**Task 列表表**：

| Task | 名称 | 执行概要 | 验收概要 |
|------|------|----------|----------|
| 1 | [name] | ≤30 char summary | ≤30 char summary |
| 2 | ... | ... | ... |
| **N** | **[Feature Name] Acceptance** | **End-to-end verification** | **N scenarios** |

输出表格后，使用 `AskUserQuestion` 提供两个选项：

- **确认写入** — 继续写入 `spec-plan.md`
- **需要修改** — 用户提供反馈；修改并重新显示表格

## 记住

- **开始时检测模型** — 检查模型，如果不是 Opus，输出纯文本建议；非阻塞，始终继续
- 精确的文件路径
- 使用 @ 语法引用相关技能
- 计划文件用中文撰写
- **不要逐个确认每个 Task** — 一次性生成所有 Task，确认一次后再写入文件
- 文件数去重 — 一个文件被多个 Task 触碰只计算一次
- **验收 Task** — 最后一个 Task 必须是端到端验收，动态命名为 "[Feature Name] Acceptance"；包含前置条件、可执行的验证命令和失败排查指针（引用相关 Task）；场景自动从 `spec-design.md` 派生
- 执行步骤使用 `- [ ]` 复选框格式（不是编号列表）
- 执行步骤和检查步骤是独立的列表，不需要 1:1 配对
- **无 [HUMAN] 标签** — 所有检查步骤必须可以通过 CLI/curl/script 自动化；人工验证由 sdd-plan-human-verify 技能单独处理

## 终止

所有 Task 确认并文件写入后：

1. 显示总结：Task 数量、`spec-plan.md` 路径。
2. **不要**创建 git commit。
3. **不要**自动调用任何其他技能。
4. 向用户输出（中文）："✅ 执行计划已写入 `{workspace}/spec/.../spec-plan.md`，共 N 个 Task。\n\n**建议下一步：** 运行 `/sdd-executing-plans` 自动执行计划。"
