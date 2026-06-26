---
name: sdd-global-change
description: "通过自然语言修改全局 spec 文档。解析需求，展示变更计划，执行修改，并生成配图。"
---

# SDD Global Change — 全局文档修改

## Overview

根据用户的自然语言需求修改全局 spec 文档（`spec/global/`）。解析请求，展示变更计划以供确认，执行修改，并生成任何需要的配图。

**触发方式：** 手动触发，用户运行 `/sdd-global-change <自然语言需求>`

**启动时声明：** "我正在使用 sdd-global-change 技能来修改全局文档。"

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

检查当前模型是否为 Opus（检查 system prompt 中的模型信息）。如果**不是** Opus，输出以下纯文本提示并继续（非阻塞）：

```
⚠️ 当前模型不是 Opus，全局文档修改需要较强的理解和摘要能力，建议切换到 Opus。输入 /model 切换模型。
```

## Step 1: 前置条件检查

检查 `{workspace}/spec/global/` 目录是否存在。

- **如果不存在：** 显示 "全局 spec 目录不存在，请先运行 /sdd-global-init 初始化。" 并**停止**。
- **如果存在：** 继续 Step 2。

## Step 2: 解析用户需求

从用户的自然语言输入中提取：
- **目标文档：** 需要修改哪些全局文档（overview.md、architecture.md、constraints.md、features.md、index.md、domains/*.md）
- **变更类型：** 添加、更新、删除或重组内容
- **范围：** 具体部分或整个文档
- **内容详情：** 具体需要更改什么

如果用户需求不明确，使用 `AskUserQuestion` 澄清后再继续。

## Step 3: 读取相关文档

读取变更可能影响的所有全局文档：
- 直接目标文档
- 可能需要一致性更新的相关文档（例如更改架构可能影响约束）

## Step 4: 展示变更计划

显示结构化的变更计划，展示：
- 将修改哪些文档
- 每个文档将做什么具体更改（添加/更新/删除哪些部分）
- 需要哪些跨文档一致性更新

示例格式：
```
📋 变更计划

1. spec/global/architecture.md
   - [更新] 系统组件: 新增 Redis 缓存层描述
   - [更新] 数据流: 更新缓存读写路径

2. spec/global/constraints.md
   - [新增] 技术栈 > 缓存: Redis 6.x

3. spec/global/overview.md
   - （无需修改）
```

使用 `AskUserQuestion`：「确认执行」/「需要调整」

如果用户选择 "需要调整"：
- 询问要修改什么（纯文本）
- 调整计划
- 通过 `AskUserQuestion` 重新确认

## Step 5: 执行修改

应用所有已确认的更改：
1. 使用 Edit 工具编辑每个目标文档
2. 更新每个修改文档的页脚：
   ```
   ---
   *最后更新: YYYY-MM-DD — 由 /sdd-global-change 更新*
   ```
3. 确保跨文档一致性

## Step 6: 同步配图生成

所有文档修改完成后，评估配图需求并逐一生成配图。

### 6.1 评估配图需求

对于每个修改的文档：
- 检查现有配图是否仍与内容更改后的情况一致
- 检查新内容部分是否需要配图（根据配图触发规则）
- 在需要的地方插入 `![描述](./images/NN-type.png)` 引用

根据源 md 文件确定输出目录：
- 全局文档（index/overview/architecture/features/constraints）→ `spec/global/images/`
- 领域文档（domains/*.md）→ `spec/global/domains/images/`

### 6.2 收集配图清单

构建需要生成/重新生成的配图清单：

```json
[
  {
    "description": "描述文字（用于图片生成 prompt）",
    "type": "architecture|feature-relationship|tech-stack|concept",
    "style": "根据 Style Mapping 确定",
    "aspect_ratio": "16:9 或 1:1",
    "output_path": "spec/global/images/NN-type.png（全局文档）或 spec/global/domains/images/NN-type.png（领域文档）"
  }
]
```

### 6.3 同步配图生成（如果需要配图）

如果清单非空，遍历清单逐一生成配图：

对于清单中的每个配图：
1. 显示进度：`🖼️ 正在生成第 X/N 张：{description}...`
2. 调用 `/gen-image` skill，参数：prompt={description + style prefix}, aspect_ratio, size=1K, output={output_path}
3. 成功时：显示 `✅ 已保存: {output_path}`
4. 失败时：重试一次。如果仍然失败，显示 `⚠️ 生成失败: {description}，已跳过` 并继续下一个配图

所有配图处理完后，显示总结：
- 全部成功：`🖼️ 配图全部生成完成（{N} 张）`
- 部分失败：`🖼️ 配图生成完成: {X} 张成功，{Y} 张失败`

如果不需要配图，跳到 Step 7。

## Step 7: 输出总结

用中文显示简洁总结：

```
✅ 全局文档修改完成

📝 修改的文件:
  - spec/global/architecture.md（更新: 系统组件、数据流）
  - spec/global/constraints.md（新增: 缓存技术栈）
🖼️ 配图: X 张生成成功
  {或: 🖼️ 配图: X 张成功，Y 张失败（{失败文件列表}）}
  {或: （无需更新配图）}
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

- **手动触发** — 永不自动调用，用户必须运行 `/sdd-global-change <需求>`
- **前置条件：spec/global/ 必须存在** — 如果未初始化则拒绝
- **执行前展示变更计划** — 永远不要在没有用户确认的情况下修改
- **跨文档一致性** — 修改一个文档时，检查并更新相关文档
- **同步配图生成** — 逐一生成配图并显示进度
- **智能重新生成** — 仅当内容更改使现有配图过时时才重新生成
- **使用 /gen-image skill** — 不内联 gen-image 逻辑，只调用 skill
- **无 git 操作** — 不进行 branch、commit、merge、push
- **中文输出** — 所有用户-facing 信息用中文
- **英文指令** — SKILL.md 内部逻辑用英文
- **全局文档内容用中文** — 所有文档内容用中文撰写
- **配图文字用中文** — 除非是技术英文术语
- **配图分辨率: 1K** — 草稿质量
- **配图存储在 md 文件的 `./images/` 相对路径** — 全局文档用 `spec/global/images/`，领域文档用 `spec/global/domains/images/`
