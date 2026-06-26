---
name: superpowers-parallel-agents
description: Use when facing 2 or more independent tasks that can be worked on without shared state - dispatches parallel subagents using sessions_spawn for concurrent investigation and execution, adapted for OpenClaw
---

# Superpowers Parallel Agents（OpenClaw 适配版）

## 概述

当面临 2+ 个独立任务时，将它们分配给专门的并行 subagent，同时工作。OpenClaw 用 `sessions_spawn` 创建独立 session 实现并行分发。

**核心原则：** 每个独立问题域分配一个 agent，让它们并发工作。

## OpenClaw 适配

Superpowers 原版用 Claude Code 的 `Task` 工具并发派发。OpenClaw 用 `sessions_spawn`：
- `sessions_spawn(mode="run")` — 一次性任务，并发执行
- `sessions_spawn(mode="session")` — 持久 session，可多轮交互
- 主 session 协调，subagent 结果通过 session 历史或文件系统汇总

## 使用条件

```
有多个失败/独立任务？
  → 它们独立？（不同根因、无共享状态）？
    → 可以并行工作？
      → 用 parallel-agents（这个技能）✅
    → 顺序更合适？
      → 用 systematic-debugging 单独处理
  → 需要全面上下文理解？
    → 单一 agent 处理
```

**适用场景：**
- 3+ 个测试文件失败，根因不同
- 多个子系统独立损坏
- 每个问题可以在不理解其他问题上下文的情况下理解
- 调查之间无共享状态

**不适用：**
- 失败互相关联（修一个可能修其他）
- 需要理解完整系统状态
- Agents 会互相干扰（编辑同一文件、共用资源）

## 流程

### 1. 识别独立问题域

按问题分组：
- 测试文件 A：工具审批流程
- 测试文件 B：批处理完成行为
- 测试文件 C：中止功能

每个问题域独立——修工具审批不影响中止测试。

### 2. 为每个 Agent 创建专注任务

每个 agent 获得：
- **明确范围：** 一个测试文件或子系统
- **清晰目标：** 让这些测试通过 / 修复这个 bug
- **约束：** 不要改其他代码
- **预期输出：** 发现什么、修复什么的摘要

### 3. 并行 dispatch

用 `sessions_spawn` 同时派发所有 agent：

```javascript
// OpenClaw: sessions_spawn 并行派发
sessions_spawn({
  task: "修复 src/agents/agent-tool-abort.test.ts 的 3 个失败测试...",
  runtime: "subagent",
  mode: "run",
  cwd: "/path/to/project"
})
sessions_spawn({
  task: "修复 src/batch/completion.test.ts 的 2 个失败测试...",
  runtime: "subagent",
  mode: "run",
  cwd: "/path/to/project"
})
sessions_spawn({
  task: "修复 src/tools/race-conditions.test.ts 的 1 个失败测试...",
  runtime: "subagent",
  mode: "run",
  cwd: "/path/to/project"
})
```

### 4. 审查和整合

当 agents 返回：
- 读每个摘要
- 验证修复不冲突
- 运行完整测试套件
- 整合所有变更

## Agent 提示词结构

好的 agent 提示词：
1. **专注** — 一个清晰的问题域
2. **自包含** — 理解问题所需的全部上下文
3. **输出具体** — agent 应该返回什么？

```markdown
修复 src/agents/agent-tool-abort.test.ts 中 3 个失败的测试：

1. "should abort tool with partial output capture" - 期望消息中有 'interrupted at'
2. "should handle mixed completed and aborted tools" - 快速工具被中止而非完成
3. "should properly track pendingToolCount" - 期望 3 个结果但得到 0

这些是时序/竞态条件问题。你的任务：

1. 读测试文件，理解每个测试验证什么
2. 识别根因——时序问题还是实际 bug？
3. 修复：
   - 用事件等待替代任意 timeout
   - 如发现 bug 则修复 abort 实现
   - 如测试的是变化的行为则调整测试期望

不要只加 timeout——找真正的问题。

返回：你发现了什么，修复了什么。
```

## 常见错误

**❌ 范围太广：** "修所有测试" — agent 会迷失
**✅ 具体：** "修 agent-tool-abort.test.ts" — 专注范围

**❌ 无上下文：** "修竞态条件" — agent 不知道在哪里
**✅ 有上下文：** 粘贴错误信息和测试名

**❌ 无约束：** Agent 可能重构一切
**✅ 有约束：** "不要改其他代码" 或 "只修测试"

**❌ 输出模糊：** "修好了" — 不知道改了啥
**✅ 输出具体：** "返回根因和变更摘要"

## 何时不用

**相关失败：** 修一个可能修其他——先一起调查
**需要完整上下文：** 理解需要看到整个系统
**探索性调试：** 还不知道哪里坏了
**共享状态：** Agents 会互相干扰（编辑同一文件、用同一资源）

## 关键优势

1. **并行化** — 多个调查同时进行
2. **专注** — 每个 agent 范围窄，跟踪的上下文少
3. **独立性** — Agents 不互相干扰
4. **速度** — 3 个问题用 1 个问题的时间解决

## 验证

Agents 返回后：
1. **审查每个摘要** — 理解改了什么
2. **检查冲突** — Agents 编辑了同一代码吗？
3. **运行完整套件** — 验证所有修复一起工作
4. **抽查** — Agents 可能犯系统性错误
