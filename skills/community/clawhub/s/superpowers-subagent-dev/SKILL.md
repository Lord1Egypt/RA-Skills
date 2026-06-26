---
name: superpowers-subagent-dev
description: Use when executing implementation plans with independent tasks - coordinates task execution by dispatching subagents per task with verification checkpoints, adapted for OpenClaw's isolated session model
---

# Superpowers Subagent 开发（OpenClaw 适配版）

## 概述

通过为每个任务 dispatch 独立 subagent 来执行计划，每个任务后进行两阶段审查：先审查规格合规，再审查代码质量。

**为什么用 subagent：** 将任务委托给专门 agent，隔离上下文。通过精确构造指令和上下文，确保它们专注并成功完成。Subagent 不应继承 session 历史——精确构造它们需要的上下文。

**核心原则：** 每个任务新鲜 subagent + 两阶段审查（规格合规 → 代码质量）

## OpenClaw 适配说明

Superpowers 原版设计基于 Claude Code 的 Task/subagent 级联模型。OpenClaw 使用 `sessions_spawn` 创建独立 session，无法做到原生级联。

**OpenClaw 适配方案：**
- 主 agent 作为 controller，协调所有工作
- 用 `sessions_spawn(mode="run")` dispatch 一次性任务 subagent
- Subagent 结果通过 session 历史或文件系统传递
- 审查在主 session 内 inline 执行（或 spawn 独立审查 session）
- 复杂审查任务用 `sessions_spawn`

## 使用条件

```
有实现计划？
  → 任务大多独立？
    → 在本 session 内工作？
      → 用 subagent-dev（这个技能）
    → 并行独立 session？
      → 用 sessions_spawn 并行 dispatch
  → 手动执行或先 brainstorming
```

## 流程

### 每次任务

1. **读取计划，提取所有任务**
   - 读取计划文件一次
   - 提取所有任务及其完整文本和上下文
   - 创建任务列表

2. **Dispatch 实现者 subagent**
   ```
   使用 sessions_spawn:
   - mode: "run"（一次性任务）
   - task: 完整任务文本 + 上下文
   - cwd: 项目目录
   ```
   
3. **Subagent 提问处理**
   - 如果 subagent 提问 → 回答问题，提供上下文
   - 重新 dispatch 或继续

4. **Subagent 实现、测试、commit、自审**
   - 实现者完成工作
   - 运行测试
   - Commit
   - 自审

5. **规格合规审查（主 session inline 或 spawn）**
   - 检查实现是否满足计划中的规格
   - 发现问题 → 反馈给实现者修复 → 重新审查
   - 通过 → 继续

6. **代码质量审查**
   - 检查代码质量：DRY、命名、测试设计
   - 发现问题 → 修复
   - 通过 → 继续

7. **标记任务完成，继续下一个**

### 任务后

所有任务完成后：
- 做最终代码审查
- 调用 `superpowers-finishing-branch` 完成工作

## 模型选择

用能处理任务的最弱模型，节省成本增加速度：

| 任务类型 | 示例 | 模型 |
|---------|------|------|
| 机械实现任务 | 孤立函数、清晰规格、1-2 文件 | 快速便宜模型 |
| 集成和判断任务 | 多文件协调、模式匹配、调试 | 标准模型 |
| 架构设计和审查任务 | 需要设计判断或广泛代码库理解 | 最强模型 |

## 处理 Subagent 状态

Subagent 报告四种状态之一。适当处理：

**DONE：** 继续规格合规审查。

**DONE_WITH_CONCERNS：** 实现者完成但标记了疑虑。先读关注点再继续。如果关注点涉及正确性或范围，先解决再审查。

**NEEDS_CONTEXT：** 实现者需要未提供的信息。提供缺失上下文并重新 dispatch。

**BLOCKED：** 实现者无法完成任务。评估阻塞：
1. 如果是上下文问题，提供更多上下文并用相同模型重新 dispatch
2. 如果任务需要更多推理，用更强模型重新 dispatch
3. 如果任务太大，拆成更小的块
4. 如果计划本身有问题，上报给主人

**永远不要**忽略升级或强制相同模型重试而不做变更。

## Red Flags

**永远不要：**
- 在 main/master 分支上开始实现（没有主人明确同意）
- 跳过审查（规格合规或代码质量）
- 有未修复问题时继续
- 同时 dispatch 多个实现 subagent（冲突）
- 让 subagent 读计划文件（直接提供完整文本）
- 跳过场景设置上下文（subagent 需要理解任务在哪里_fit）
- 忽略 subagent 的提问（先回答再让他们继续）
- 接受"差不多"的规格合规（审查发现问题 = 没完成）
- 跳过审查循环（审查发现问题 = 实现者修复 = 重新审查）
- 让实现者自审替代实际审查（两者都需要）
- **在规格合规通过前开始代码质量审查**（顺序错误）
- 有公开问题时继续下一个任务

## 集成

**必需的工作流技能：**
- `superpowers-writing-plans` — 创建这个技能执行的计划
- `superpowers-finishing-branch` — 所有任务完成后的收尾
- `superpowers-tdd` — Subagent 每个任务遵循 TDD

**替代工作流：**
- `sessions_spawn` 并行 dispatch — 用于独立问题的并行调查
- 顺序执行 — 在主 session 内按批次执行
