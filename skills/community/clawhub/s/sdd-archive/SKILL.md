---
name: sdd-archive
description: "将已完成的 feature spec 归档到全局知识库。提取关键决策，更新约束和领域索引，然后将 feature 目录移到 spec/archive/。"
---

# SDD Archive — Feature 归档与领域综合

## Overview

将已完成的 feature spec 归档到项目的全局知识库（`spec/global/`）。此技能从 feature 的设计文档**和**实际代码中提取关键决策，使用 4 部分领域文档结构执行增量领域综合，更新全局约束和概述文档，然后将整个 feature 目录移到 `spec/archive/`。

**触发方式：** 手动触发，用户运行 `/sdd-archive`

**启动时声明：** "我正在使用 sdd-archive 技能来归档 feature spec。"

## Step 0: 模型检查

检查当前模型是否为 Opus（检查 system prompt 中的模型信息）。如果**不是** Opus，输出以下纯文本提示并继续（非阻塞）：

```
⚠️ 当前模型不是 Opus，归档提取需要较强的理解和摘要能力，建议切换到 Opus。输入 /model 切换模型。
```

## Step 1: 前置条件检查

检查 `spec/global/` 目录是否存在。

- **如果不存在：** 显示 "全局 spec 目录不存在，请先运行 /sdd-global-init 初始化。" 并**停止**。
- **如果存在：** 继续 Step 2。

## Step 2: Feature 选择

1. 扫描 `spec/` 中匹配 `feature_*` 模式的目录
2. **排除：** `spec/archive/` 和 `spec/global/`
3. 按目录修改时间排序（最新优先）
4. 通过 `AskUserQuestion` 展示**最新的 3 个** feature 目录：
   - 每个选项显示目录名
   - 用户可以通过 "Other" 输入自定义路径
   - 所有问题文本用中文："选择要归档的 feature："
5. 读取选中 feature 的 `spec-design.md`

### 边界情况：未找到 feature 目录

显示："未找到可归档的 feature 目录。`spec/` 下没有 `feature_*` 目录。"
停止。

### 边界情况：未找到 spec-design.md

显示："所选 feature 目录中未找到 `spec-design.md`，无法提取摘要。请确认该 feature 已完成设计阶段。"
停止。

## Step 3: 完成度检查（严格模式）

检查 feature 的完成状态：

### 3.1 检查 spec-plan.md

- 如果存在，读取 `spec/{feature}/spec-plan.md`
- 统计总复选框数（`- [ ]` 和 `- [x]`）和已完成复选框数（`- [x]`）
- 计算完成百分比

### 3.2 检查 spec-human-verify.md

- 如果存在，读取 `spec/{feature}/spec-human-verify.md`
- 检查 `[!]`（失败）和 `[ ]`（待处理）项目
- 汇总：通过/失败/待处理数量

### 3.3 决策逻辑

- **全部完成（计划 100% + 验证全部通过）：** 静默继续
- **部分完成或存在失败：** 显示警告：
  ```
  ⚠️ 该 feature 尚未完全完成：
  - 执行计划完成度: XX%
  - 验收结果: X 通过 / Y 失败 / Z 待验收
  ```
  使用 `AskUserQuestion`：「继续归档」/「取消」
  - 如果取消 → 停止
- **没有计划或验证文件：** 显示警告：
  ```
  ⚠️ 该 feature 缺少执行计划或验收文件，可能尚未经过完整 SDD 流程。
  ```
  使用 `AskUserQuestion`：「继续归档」/「取消」
  - 如果取消 → 停止

## Step 4: 知识提取 + 用户确认

读取 feature 的 `spec-design.md` **并扫描与 feature 相关的实际代码文件**。

### 4.1 信息来源

- **spec-design.md：** 设计决策、架构选择、权衡的主要来源
- **实际代码文件：** 扫描实现文件以验证决策并发现设计文档中未捕获的实现细节（例如实际文件路径、组件名称、工具函数、使用的模式）

### 4.2 一句话摘要

描述此 feature 做什么的简洁中文句子（最多 30 个字符）。

### 4.3 关键决策列表

提取 feature 中做出的 3-7 个关键技术或设计决策。每个决策是一个短bullet point，例如：
- 认证方式: JWT + Refresh Token
- 存储: Redis 缓存 token，PostgreSQL 存用户

从 spec-design.md 和实际代码模式中获取决策。

### 4.4 领域分类

- 确定**主要领域**（例如 auth、marketplace、payment、user、notification 等）
- 如果 feature 跨领域边界，识别**相关领域**
- 领域名使用小写英文 kebab-case

### 4.5 展示给用户确认

展示提取结果，使用 `AskUserQuestion`：「确认」/「需要修改」

如果用户选择 "需要修改"：
- 询问要修改什么（纯文本）
- 应用修改
- 通过 `AskUserQuestion` 重新确认

## Step 5: 约束演进检查

1. 读取 `spec/global/constraints.md`
2. 将 feature 的关键决策与现有约束比较
3. 识别：
   - 约束中不存在的新技术/模式（例如 feature 引入了 Redis 但约束中未提及）
   - 与现有约束的冲突（例如 feature 使用 GraphQL 但约束规定 RESTful）
   - 无变化 — feature 与所有现有约束一致

### 如果发现新技术或冲突：

显示每个发现：
```
🔍 约束演进检查：
- [新增] 缓存技术: Redis（当前约束中未记录）
- [冲突] API 风格: feature 使用 GraphQL，但约束记录为 RESTful
```

对于每个发现，使用 `AskUserQuestion`：
- **新技术：** 「更新约束」/「跳过（不更新）」
- **冲突：** 「更新为新值」/「保留原值」/「两者并存」

将确认的更改应用到 `spec/global/constraints.md` 并追加更新页脚：
```
---
*最后更新: YYYY-MM-DD — 由 {feature_directory_name} 归档时更新*
```

### 如果无变化：

显示："约束检查通过，无需更新。"

## Step 5.5: 概况文档演进检查

约束演进检查后，对概况文档进行轻量级检查。

1. 读取 `spec/global/overview.md`、`spec/global/architecture.md`、`spec/global/features.md`
2. 将新归档 feature 的关键决策和范围与这些文档比较
3. 识别潜在更新：
   - **新模块或功能点** → 更新 `features.md`
   - **新外部依赖或系统边界变化** → 更新 `overview.md` 和/或 `architecture.md`
   - **架构变化（新组件、新数据流）** → 更新 `architecture.md`

### 如果检测到变化：

显示每个发现：
```
🔍 概况文档演进检查：
- [features.md] 新增功能点: {description}
- [architecture.md] 新组件: {description}
- [overview.md] 新外部依赖: {description}
```

对于每个需要更新的文档，使用 `AskUserQuestion`：「更新」/「跳过」

对于确认的更新：
- 将更改应用到对应文档
- 更新页脚：`*最后更新: YYYY-MM-DD — 由 {feature_directory_name} 归档时更新*`

### 如果无变化：

显示："概况文档检查通过，无需更新。"

## Step 6: 写入全局 Spec 文件 + 领域综合

### 6.1 更新 spec/global/index.md

在功能表**顶部**插入新行（最新优先）：

```markdown
| [{feature_id}](../archive/{feature_dir}/) | {一句话摘要} | {primary_domain} | {YYYY-MM-DD} |
```

更新底部的领域索引部分 — 添加或更新具有正确 feature 计数的领域条目。

### 6.2 使用 4 部分结构更新/创建领域文件

**文件：** `spec/global/domains/{primary_domain}.md`

#### 如果文件不存在 — 创建新领域文档

使用**领域文档模板**（见下面的模板部分）创建新的领域文档，所有 4 个部分根据此 feature 填充。

#### 如果文件已存在 — 增量综合

执行增量领域综合：

1. **Feature 附录：** 在 `## Feature 附录` 下追加新的 feature 条目
2. **领域综述：** 如果新 feature 改变了领域的范围、责任或边界，审查并调整概述
3. **核心流程：** 如果新 feature 添加或修改了工作流，审查并更新核心流程
4. **技术方案总结：** 如果新 feature 引入了新的技术选择、模式或更改了现有技术，审查并更新

目标是**当前状态的快照** — 不是演进历史。每个部分应该作为领域的**当前状态**连贯描述，而不是变更日志。

### 6.3 微领域合并检测

确定目标领域后，检查该领域是否**≤2 个 feature**（包括正在归档的）。如果是：

1. 识别可以吸收该领域的相关领域
2. 通过 `AskUserQuestion` 展示建议：
   ```
   💡 领域 "{domain}" 目前仅有 {N} 个 feature，建议合并到 "{suggested_domain}" 领域。
   ```
   选项：「合并」/「保持独立」

如果用户确认合并：
- 将小领域的所有 feature 条目移到目标领域
- 更新目标领域的概述/流程/技术部分
- 删除小领域文件
- 更新 index.md 领域引用
- 更新其他领域文件中的交叉引用

### 6.4 跨领域引用

对于每个**相关领域**（非主要领域）：
- 打开/创建 `spec/global/domains/{related_domain}.md`
- 在 `## 相关 Feature` 部分下添加交叉引用：

```markdown
- → [{primary_domain}.md#{feature_dir}](./{primary_domain}.md#{feature_dir}) — {一句话摘要}
```

## Step 7: 同步配图生成

写入/更新所有全局 spec 文件后，收集配图需求并逐一生成配图。

### 7.1 收集配图清单

评估哪些文档被修改需要更新配图：
- 新或更新的领域文档 → 领域概览配图
- 更新的 index.md → 领域拓扑配图
- 更新的 constraints.md → 技术栈配图
- 任何匹配配图触发规则的新内容部分 → 额外配图

对于每个需要的配图，如果文档中尚未存在，在文档中插入 `![描述](./images/NN-type.png)` 引用，并添加到清单：

```json
{
  "description": "描述文字（用于图片生成 prompt）",
  "type": "architecture|feature-relationship|tech-stack|concept",
  "style": "根据 Style Mapping 确定",
  "aspect_ratio": "16:9 或 1:1",
  "output_path": "spec/global/images/NN-type.png（全局文档）或 spec/global/domains/images/NN-type.png（领域文档）"
}
```

根据源 md 文件确定输出目录：
- 全局文档（index/overview/architecture/features/constraints）→ `spec/global/images/`
- 领域文档（domains/*.md）→ `spec/global/domains/images/`

### 7.2 智能重新生成检查

- 仅在内容更改使现有配图过时时才重新生成
- 如果配图目录已有配图且对应文档内容没有实质性变化，跳过重新生成
- 重新生成时，覆盖现有配图文件（相同文件名）

### 7.3 同步配图生成（如果需要配图）

如果清单非空，遍历清单逐一生成配图：

对于清单中的每个配图：
1. 显示进度：`🖼️ 正在生成第 X/N 张：{description}...`
2. 调用 `/gen-image` skill，参数：prompt={description + style prefix}, aspect_ratio, size=1K, output={output_path}
3. 成功时：显示 `✅ 已保存: {output_path}`
4. 失败时：重试一次。如果仍然失败，显示 `⚠️ 生成失败: {description}，已跳过` 并继续下一个配图

所有配图处理完后，显示总结：
- 全部成功：`🖼️ 配图全部生成完成（{N} 张）`
- 部分失败：`🖼️ 配图生成完成: {X} 张成功，{Y} 张失败`

如果不需要配图，跳到 Step 8。

## Step 8: 执行归档

1. 如果不存在，创建 `spec/archive/` 目录
2. 移动整个 feature 目录：`spec/{feature_dir}/` → `spec/archive/{feature_dir}/`
   - 保留原始目录名
   - 使用 Bash `mv` 命令

## Step 9: 输出归档总结

用中文显示简洁总结：

```
✅ 归档完成

📁 归档位置: spec/archive/{feature_dir}/
📝 更新的全局文件:
  - spec/global/index.md（新增条目）
  - spec/global/domains/{primary_domain}.md（领域综合更新）
  {- spec/global/domains/{related_domain}.md（新增交叉引用）  // 仅适用时}
  {- spec/global/constraints.md（更新约束: ...）  // 仅约束更改时}
  {- spec/global/overview.md（更新: ...）  // 仅更改时}
  {- spec/global/architecture.md（更新: ...）  // 仅更改时}
  {- spec/global/features.md（新增功能点: ...）  // 仅更改时}
🖼️ 配图: X 张生成成功
  {或: 🖼️ 配图: X 张成功，Y 张失败（{失败文件列表}）}
  {或: （无需更新配图）}
```

不要执行任何 git 操作。

## 模板

### 领域文档模板（4 部分结构）

```markdown
# {Domain} 领域

![{Domain} 领域概览](./images/{domain}-overview.png)

## 领域综述
{概念模型、核心职责、与其他领域的边界}

## 核心流程
{当前该领域的主要工作流，基于实际代码}

## 技术方案总结
{跨 feature 的技术选型汇总：存储方案、组件复用、设计模式}

## Feature 附录

### {feature_directory_name}
**摘要:** {一句话摘要}
**关键决策:** {bullet list}
**归档:** [链接](../../archive/{feature_dir}/)
**归档日期:** {YYYY-MM-DD}

---

## 相关 Feature
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

- **手动触发** — 永不自动调用，用户必须运行 `/sdd-archive`
- **前置条件：spec/global/ 必须存在** — 如果未初始化则用 "请先运行 /sdd-init-global" 拒绝
- **AI 提取，人类确认** — 所有提取结果在写入前展示给用户审核
- **约束冲突需要用户决定** — 永不自动解决冲突
- **归档保留原始目录名** — 不重命名
- **索引按归档日期降序排序** — 最新条目在顶部
- **跨领域引用** — 涉及多个领域的 feature 在相关领域文件中添加交叉引用
- **领域文档是快照，不是日志** — 每个部分作为当前状态阅读，不是演进历史
- **增量综合** — 归档时，根据新 feature 调整现有领域文档部分（概述、流程、技术），不只是追加
- **代码扫描** — 知识提取读取 spec-design.md **和**实际代码文件
- **微领域合并** — 建议合并 ≤2 个 feature 的领域，用户确认
- **同步配图生成** — 逐一生成配图并显示进度
- **智能重新生成** — 仅在内容更改使现有配图过时时才重新生成
- **使用 /gen-image skill** — 不内联 gen-image 逻辑，只调用 skill
- **无 git 操作** — 不进行 branch、commit、merge、push
- **中文输出** — 所有用户-facing 信息用中文
- **英文指令** — SKILL.md 内部逻辑用英文
- **全局文档内容用中文** — constraints.md、index.md、domains/*.md 内容用中文撰写
- **配图存储在 md 文件的 `./images/` 相对路径** — 全局文档用 `spec/global/images/`，领域文档用 `spec/global/domains/images/`
- **配图文字用中文** — 除非是技术英文术语
- **配图分辨率: 1K** — 草稿质量
