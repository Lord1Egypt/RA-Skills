---
name: superpowers-writing-plans
description: Use when you have a spec or requirements for a multi-step task, before touching code - guides writing comprehensive implementation plans with bite-sized tasks, TDD, and DRY/YAGNI principles
---

# Superpowers Writing Plans - 写实现计划

## 概述

写全面的实现计划，假设执行者对代码库零上下文、品味可疑。记录他们需要知道的一切：每个任务要修改的文件、代码、可能需要检查的测试和文档、如何测试。给出完整计划为小粒度任务。DRY。YAGNI。TDD。频繁 commit。

假设执行者是个有技能的开发者，但几乎不了解我们的工具集或问题领域。假设他们不太懂好的测试设计。

**开始时宣布：** "我正在用 writing-plans 技能创建实现计划。"

**上下文：** 这应该在专门的工作目录中运行（由 brainstorming 技能创建）。

**保存计划到：** `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`

## 范围检查

如果规格涵盖多个独立子系统，应该在 brainstorming 阶段已分解为子项目规格。如果没有，建议分解为独立计划——每个子系统一个。每个计划应产生可工作、可测试的软件。

## 文件结构

在定义任务之前，映射哪些文件将被创建或修改，每个文件负责什么。这是分解决策被锁定的地方。

- 用清晰边界和定义好接口的设计单元。每个文件应该有一个明确职责。
- 你能放进脑子里的代码你推理得最好，编辑也更可靠。偏好更小、专注的文件，不要大的什么都做的文件。
- 一起变更的文件应该放一起。按职责拆分，不是按技术层。
- 现有代码库中，遵循已有模式。如果代码库用大文件，不要单方面重构——但如果修改的文件已经长得太大，在计划中包含拆分是合理的。

这个结构指导任务分解。每个任务应该产生能独立理解的有意义的变更。

## 小粒度任务

**每步是一个动作（2-5 分钟）：**
- "写失败的测试" — 一步
- "运行确保它失败" — 一步
- "写最少代码让测试通过" — 一步
- "运行确保测试通过" — 一步
- "Commit" — 一步

## 计划文档头部

**每个计划必须以此头部开始：**

```markdown
# [功能名] 实现计划

**目标：** [一句话描述构建内容]

**架构：** [2-3 句话描述方法]

**技术栈：** [关键技术和库]

---
```

## 任务结构

```markdown
### 任务 N：[组件名]

**文件：**
- 创建：`exact/path/to/file.py`
- 修改：`exact/path/to/existing.py:123-145`
- 测试：`tests/exact/path/to/test.py`

- [ ] **步骤 1：写失败的测试**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

- [ ] **步骤 2：运行测试验证它失败**

运行：`pytest tests/path/test.py::test_name -v`
预期：FAIL，错误信息 "function not defined"

- [ ] **步骤 3：写最少的实现代码**

```python
def function(input):
    return expected
```

- [ ] **步骤 4：运行测试验证它通过**

运行：`pytest tests/path/test.py::test_name -v`
预期：PASS

- [ ] **步骤 5：Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
```

## 无占位符

每步必须包含执行者需要的实际内容。以下是**计划失败**——永远不要写：
- "TBD"、"TODO"、"稍后实现"、"填细节"
- "添加适当的错误处理"/"添加验证"/"处理边界情况"
- "为上述写测试"（没有实际测试代码）
- "类似于任务 N"（重复代码——执行者可能按顺序读任务）
- 描述做什么而不展示怎么做的步骤（代码步骤必须有代码块）
- 引用任何任务中未定义的类型、函数或方法

## 自审

写完完整计划后，用新眼光看规格并检查计划：

**1. 规格覆盖：** 浏览规格每个部分/需求。能指向实现它的任务吗？列出任何缺口。

**2. 占位符扫描：** 在计划中搜索红旗——上述"无占位符"部分的任何模式。修复它们。

**3. 类型一致性：** 在后续任务中使用的类型、方法签名和属性名与前面定义的一致吗？任务 3 中的 `clearLayers()` 和任务 7 中的 `clearFullLayers()` 是 bug。

发现问题，内联修复。不需要重新审查——修复并继续。如果发现规格需求没有任务，加任务。

## 工作目录说明（OpenClaw 适配）

Superpowers 原版使用 git worktree 做隔离工作区。在 OpenClaw 环境中：
- 使用 git branch 创建特性分支
- 在分支上工作，完成后 merge 或 PR
- 保持工作目录整洁，与主分支隔离

**工作流程：**
```bash
# 从当前分支创建特性分支
git checkout -b feature/<feature-name>

# 实现（按计划任务）
# ...

# 完成时
git checkout main && git merge feature/<feature-name>
```

## 执行移交

保存计划后，提供执行选择：

**"计划写完保存到 `docs/superpowers/plans/<filename>.md`。两种执行选项：**

**1. 子 Agent 驱动（推荐）** — 我为每个任务 dispatch 新的 subagent，任务间审查，快速迭代

**2. 顺序执行** — 在本 session 按批次执行任务，有审查检查点

**选择哪种？"**

**如果选择子 Agent 驱动：**
- 需要 `superpowers-subagent-dev` 技能
- 每个任务新鲜 subagent + 两阶段审查

**如果选择顺序执行：**
- 在本 session 按计划任务顺序执行
- 每个任务后运行验证
- 完成后调用 `superpowers-finishing-branch` 清理
