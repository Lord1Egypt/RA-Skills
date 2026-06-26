---
name: sdd-global-init
description: "初始化 SDD 工作区，选择工作目录，扫描代码库生成项目概述、架构全景、技术约束、已有功能清单等全局文档。"
---

# SDD Global Init — 工作区初始化与全局 Spec 生成

## Overview

初始化 SDD 工作区：
1. 让用户选择或创建工作区目录
2. 在工作区创建 `spec/global/` 知识库目录
3. 扫描工作区中的代码库生成完整的全局文档集合（概述、架构、约束、功能清单、索引）
4. 包含配图生成

**触发方式：** 手动触发，用户运行 `/sdd-global-init`

## 关键概念

- **工作区 (Workspace)：** 用户指定的用于存放所有 SDD 文档和代码的根目录
- **工作区配置：** 初始化时在工作区根目录创建 `.sdd-workspace` 文件，记录工作区路径，供后续 SDD skill 使用

## Step 0: 获取工作区路径

### 0.1 检查是否存在已有工作区配置

检查当前 OpenClaw workspace 中是否存在 `.sdd-workspace` 配置文件：
- 如果存在，读取其中的 `workspace_path` 作为默认工作区
- 询问用户是继续使用现有工作区还是新建工作区

### 0.2 选择或创建工作区

如果无现有配置，或用户选择新建，使用 `AskUserQuestion` 展示选项：

1. **使用 OpenClaw 当前 workspace** — 使用 `/home/maqb11/.openclaw/workspace/` 作为工作区
2. **指定已有目录** — 用户输入一个已有的目录路径
3. **创建新目录** — 用户输入新目录名，在 OpenClaw workspace 下创建

**选项展示：**
```
📂 请选择工作区目录：

1. 使用当前 workspace: /home/maqb11/.openclaw/workspace/
2. 指定已有目录（请输入路径）
3. 创建新目录（请输入目录名）
```

使用 `AskUserQuestion` 让用户选择，然后验证目录是否存在：
- 选择 1：使用当前 workspace
- 选择 2：验证目录是否存在，不存在则提示错误
- 选择 3：创建新目录 `{workspace}/{dirname}/`

### 0.3 记录工作区配置

在选定的工作区根目录创建 `.sdd-workspace` 配置文件：

```json
{
  "workspace_path": "/path/to/workspace",
  "initialized_at": "2026-03-16T17:00:00+08:00",
  "sdd_version": "1.0"
}
```

后续所有 SDD skill 都通过读取这个配置文件获取工作区路径。

## Step 1: 模型检查

检查当前模型是否为 Opus（检查 system prompt 中的模型信息）。如果**不是** Opus，输出以下纯文本提示并继续（非阻塞）：

```
⚠️ 当前模型不是 Opus，全局 spec 初始化需要较强的理解和摘要能力，建议切换到 Opus。输入 /model 切换模型。
```

## Step 2: 工作区存在性检查

从 `.sdd-workspace` 读取工作区路径 `{workspace}`，检查 `{workspace}/spec/global/` 目录是否存在：

- **如果存在：** 显示 "工作区 [{workspace}] 的全局 spec 目录已存在，无需重复初始化。如需修改全局文档，请使用 /sdd-global-change。" 并**停止**。
- **如果不存在：** 继续 Step 3。

## Step 3: 扫描项目

在**工作区目录**中扫描项目以构建全面的图景：

AI 扫描工作区中的代码库：
- **技术栈：** package.json, requirements.txt, go.mod, Cargo.toml 等
- **目录结构与模块边界：** src/, components/, routes/ 等
- **路由/页面/API 端点：** 推断功能模块
- **README, CLAUDE.md, 配置文件：** 推断业务目标、外部依赖
- **Docker/部署配置：** 推断系统边界和部署拓扑
- **框架选择、CI/CD 配置、编码规范**

> **注意：** 工作区目录下可能包含多个项目，优先扫描主要项目。

## Step 4: 生成大纲并确认

展示所有待生成文档的大纲（目录结构 + 每个文档的核心要点）。使用 `AskUserQuestion` 一次性让用户确认或请求修改。

大纲格式示例：
```
📋 全局 Spec 初始化大纲

{workspace}/spec/global/
├── constraints.md — 项目架构约束
│   ├── 技术栈: TypeScript, React, Express...
│   ├── 架构决策: Monorepo, RESTful...
│   └── 编码规范 / 部署方式 / 安全约束
├── overview.md — 项目概述
│   ├── 项目目标: ...
│   ├── 核心用户: ...
│   ├── 系统边界: ...（外部依赖）
│   └── 核心业务流程: ...
├── architecture.md — 架构全景
│   ├── 系统组件图: ...
│   ├── 模块划分: ...
│   ├── 数据流: ...
│   └── 部署拓扑: ...
├── features.md — 已有功能清单
│   ├── 模块A: 功能点1, 功能点2...
│   ├── 模块B: 功能点1, 功能点2...
│   └── ...
├── index.md — 归档索引（空表）
├── images/ — 配图目录
└── domains/ — 领域目录（空）
```

将 `...` 占位符替换为扫描发现的实际信息。

如果用户选择 "需要修改"，询问要修改什么，调整大纲后重新确认。

## Step 5: 生成所有文档

用户确认大纲后，一次性生成所有文档——不逐个文档确认：

1. 创建 `{workspace}/spec/` 目录
2. 创建 `{workspace}/spec/global/` 目录
3. 创建 `{workspace}/spec/global/domains/` 目录（空）
4. 创建 `{workspace}/spec/global/images/` 目录（空）
5. 创建 `{workspace}/spec/global/domains/images/` 目录（空）
6. 使用约束模板写入 `{workspace}/spec/global/constraints.md`，填入发现的信息。无法确定的维度使用 `"（未检测到）"`。
7. 使用概述模板写入 `{workspace}/spec/global/overview.md`，填入发现的信息。
8. 使用架构模板写入 `{workspace}/spec/global/architecture.md`，填入发现的信息。
9. 使用功能清单模板写入 `{workspace}/spec/global/features.md`，填入发现的信息。
10. 使用索引模板写入 `{workspace}/spec/global/index.md`，包含空的功能表。

**constraints.md 与 architecture.md 的区别：**
- **constraints.md** = "约束规则" — 应该如何做（技术栈选择、编码规范、API 风格规则、安全约束）
- **architecture.md** = "实际现状" — 系统实际是如何组织的（组件图、模块边界、数据流、部署拓扑、外部集成技术细节）

**配图占位：** 每个文档模板都包含 `![描述](./images/NN-type.png)` 引用。在文档写作时根据配图触发规则插入这些引用。

## Step 6: 同步配图生成

所有文档写完后，收集配图需求并逐一生成配图。

### 6.1 收集配图清单

扫描所有生成的文档中的 `![...](./images/...)` 引用。为每个引用构建清单条目：

```json
{
  "description": "描述文字（用于图片生成 prompt）",
  "type": "architecture|feature-relationship|tech-stack|concept",
  "style": "根据 Style Mapping 确定",
  "aspect_ratio": "16:9 或 1:1",
  "output_path": "spec/global/images/NN-type.png"
}
```

配图始终输出到 `{workspace}/spec/global/images/` 或 `{workspace}/spec/global/domains/images/`。

### 6.2 同步配图生成

遍历清单，逐一生成配图：

对于清单中的每个配图：
1. 显示进度：`🖼️ 正在生成第 X/N 张：{description}...`
2. 调用 `/gen-image` skill，参数：prompt={description + style prefix}, aspect_ratio, size=1K, output={workspace}/spec/global/images/{filename}
3. 成功时：显示 `✅ 已保存: {output_path}`
4. 失败时：重试一次。如果仍然失败，显示 `⚠️ 生成失败: {description}，已跳过` 并继续下一个配图

所有配图处理完后，显示总结：
- 全部成功：`🖼️ 配图全部生成完成（{N} 张）`
- 部分失败：`🖼️ 配图生成完成: {X} 张成功，{Y} 张失败`

## Step 7: 输出总结

用中文显示简洁总结：

```
✅ SDD 工作区初始化完成

📂 工作区: {workspace}
📁 生成目录: {workspace}/spec/global/
📝 生成的文件:
  - spec/global/index.md（归档索引）
  - spec/global/overview.md（项目概述）
  - spec/global/architecture.md（架构全景）
  - spec/global/features.md（已有功能清单）
  - spec/global/constraints.md（架构约束）
🖼️ 配图: X 张生成成功
  {或: 🖼️ 配图: X 张成功，Y 张失败（{失败文件列表}）}

💡 工作区已记录到 .sdd-workspace 配置文件
💡 后续所有 SDD 操作将在此工作区进行
💡 如需修改全局文档，请使用 /sdd-global-change。
```

## 工作区配置说明

### .sdd-workspace 文件

在工作区根目录创建 `.sdd-workspace` JSON 配置文件：

```json
{
  "workspace_path": "/absolute/path/to/workspace",
  "initialized_at": "2026-03-16T17:00:00+08:00",
  "sdd_version": "1.0"
}
```

### 读取工作区路径

后续所有 SDD skill（sdd-brainstorming, sdd-writing-plans 等）在执行时必须：

1. 首先检查当前 OpenClaw workspace 中是否存在 `.sdd-workspace`
2. 如果存在，读取 `workspace_path` 作为工作区根目录
3. 所有 `spec/` 相关路径都基于工作区路径：`{workspace}/spec/...`

## 模板

### spec/global/index.md 模板

```markdown
# 项目全局 Spec 索引

![全局领域拓扑](./images/01-domain-topology.png)

## 项目概况
→ [overview.md](./overview.md) — 项目概述
→ [architecture.md](./architecture.md) — 架构全景
→ [features.md](./features.md) — 已有功能清单
→ [constraints.md](./constraints.md) — 架构约束

## 已归档 Feature

| Feature ID | 摘要 | 领域 | 归档日期 |
|-----------|------|------|----------|

## 领域索引
```

### spec/global/overview.md 模板

```markdown
# 项目概述

![项目全景](./images/02-project-overview.png)

## 项目目标
{项目是什么、解决什么问题}

## 核心用户
{目标用户群体及其核心需求}

## 系统边界
{系统与哪些外部服务交互，业务视角}
- **{外部服务名}:** {作用描述}

## 核心业务流程
{主要的 1-3 个业务流程简述}

---
*最后更新: YYYY-MM-DD — 初始化生成*
```

### spec/global/architecture.md 模板

```markdown
# 架构全景

![系统架构](./images/03-system-architecture.png)

## 系统组件
{各组件及其职责}

## 模块划分
{代码中的核心模块、它们的边界和职责}

## 数据流
![数据流](./images/04-data-flow.png)

{核心数据如何在组件间流动}

## 外部集成
{技术层面的外部服务集成细节：端口、协议、认证方式等}

## 部署拓扑
{各服务如何部署、容器编排等}

---
*最后更新: YYYY-MM-DD — 初始化生成*
```

### spec/global/features.md 模板

```markdown
# 已有功能清单

![功能模块概览](./images/05-feature-modules.png)

## {模块名}
- **{功能点}:** {一句话描述}
- **{功能点}:** {一句话描述}

## {模块名}
...

---
*最后更新: YYYY-MM-DD — 初始化生成*
```

### spec/global/constraints.md 模板

```markdown
# 项目架构约束

![技术栈概览](./images/06-tech-stack.png)

## 技术栈
- **语言:** ...
- **前端框架:** ...
- **后端框架:** ...
- **数据库:** ...
- **缓存:** ...
- **构建工具:** ...
- **包管理器:** ...

## 架构决策
- **目录结构:** ...
- **分层架构:** ...
- **状态管理:** ...
- **通信模式:** ...

## API 风格
- **风格:** RESTful / GraphQL / ...
- **认证方式:** ...
- **错误处理:** ...

## 编码规范
- **命名约定:** ...
- **文件组织:** ...

## 部署方式
- **环境:** ...
- **CI/CD:** ...

## 安全约束
- ...

---
*最后更新: YYYY-MM-DD — 初始化生成*
```

## 配图触发规则

### 强制触发（始终生成配图）
- 3 个以上组件交互
- 多步骤流程
- 多分支决策逻辑
- 系统边界/集成图
- 跨模块数据流

### AI 补充（根据内容复杂程度决定是否生成）
- 密集的技术解释
- 跨领域关系
- 前后对比

### Style Mapping

| 配图类型 | Style prefix | 宽高比 |
|-----------|-------------|-------------|
| 架构/数据流 | Technical diagram, vector style | 16:9 |
| 功能关系 | Clean flat flowchart, minimal | 16:9 |
| 技术栈概览 | Technical diagram, vector style | 16:9 |
| 概念图示 | Flat design, soft pastel | 1:1 或 16:9 |

## 规则

- **手动触发** — 永不自动调用，用户必须运行 `/sdd-global-init`
- **工作区优先** — 首先让用户选择或创建工作区目录，所有后续操作都在工作区中进行
- **记录配置** — 在工作区根目录创建 .sdd-workspace 配置文件，供后续 skill 读取
- **一次性使用** — 如果工作区的 `spec/global/` 已存在，拒绝并停止
- **AI 扫描，人类确认大纲** — 生成文档前展示大纲供用户审核
- **大纲确认后一次性生成所有文档** — 不逐个文档确认
- **同步配图生成** — 逐一生成配图并显示进度
- **使用 /gen-image skill** — 不内联 gen-image 逻辑，只调用 skill
- **无 git 操作** — 不进行 branch、commit、merge、push
- **中文输出** — 所有用户-facing 信息使用中文
- **英文指令** — SKILL.md 内部逻辑使用英文
- **全局文档内容用中文** — 所有生成的文档内容用中文撰写
- **配图文字用中文** — 除非是技术英文术语
- **配图分辨率: 1K** — 草稿质量
- **配图存储在 md 文件的 `./images/` 相对路径** — 相对于工作区的 `spec/global/images/`
