# Orchestration Engine — 任务编排引擎

> **运行说明**：若宿主提供子 Agent / Task 类工具，可按下文「并发启动」执行；否则由**同一模型**按任务图分步模拟（逻辑不变，仅无真实并行进程）。

**数据交换**：可序列化 JSON 字段见 `references/machine-contract.md`（与下述 TypeScript 接口互补）。

## 核心职责

将复杂任务拆解为可执行的子任务图（Task Graph），并通过 Task 工具驱动并行/串联执行。

## 任务图结构

```typescript
interface OrchestrationTask {
  id: string;                    // 唯一标识 "step-1", "step-2a"
  description: string;           // 人类可读的任务描述
  skill: string;                // 调度的目标 Skill 名称
  prompt: string;               // 给子 Agent 的完整指令
  dependencies: string[];        // 前置任务 ID 列表（串联依赖）
  parallelGroup: string | null;  // 所属并行组（同组内并发执行）
  mode: "acceptEdits" | "bypassPermissions" | "default" | "plan";
  status: "pending" | "running" | "completed" | "failed" | "skipped";
  result?: any;                 // 执行结果
  error?: string;               // 错误信息
  startedAt?: number;
  completedAt?: number;
}
```

## 编排策略

### 并联编排（Parallel）

```
用户："帮我分析竞品，从产品、技术、口碑三个维度"
      ↓
  Task-A（产品分析）──┐
  Task-B（技术分析）──┼──→ Merge → 综合报告
  Task-C（口碑分析）──┘

parallelGroup = "竞品分析"
dependencies = []  ← 无依赖，全部并发
```

### 串联编排（Sequential）

```
用户："先写代码，再写测试，最后部署"
      ↓
Task-1（写代码）→ Task-2（写测试）→ Task-3（部署）
dependencies = ["step-1"]（每步依赖上一步）
```

### 混合编排（Hybrid）

```
Task-A ──┐
Task-B ──┼──→ Task-E（汇总）→ Task-F（发布）
Task-C ──┘

A/B/C 并联 → E 串联 → F 串联
```

## 执行器伪代码

```javascript
async function executeOrchestration(taskGraph) {
  const pending = [...taskGraph];
  const running = [];
  const completed = {};

  // 启动所有无依赖的任务（并发启动）
  const initialTasks = pending.filter(t => t.dependencies.length === 0);
  for (const task of initialTasks) {
    task.status = "running";
    task.startedAt = Date.now();
    const agent = launchSubAgent(task);  // 调用 Task 工具
    running.push({ task, agent });
  }

  // 事件循环：等待任务完成，触发后续任务
  while (running.length > 0 || pending.length > 0) {
    const done = await waitForAny(running.map(r => r.agent));
    
    for (const [agent, result] of done) {
      const entry = running.find(r => r.agent === agent);
      entry.task.status = "completed";
      entry.task.result = result;
      completed[entry.task.id] = result;
      
      // 移除已完成任务
      running.splice(running.indexOf(entry), 1);
      
      // 检查是否有任务现在可以启动
      const newlyUnblocked = pending
        .filter(t => t.dependencies.every(d => completed[d]))
        .filter(t => t.dependencies.every(d => completed[d]?.status !== "failed"));
      
      for (const task of newlyUnblocked) {
        task.status = "running";
        task.startedAt = Date.now();
        const newAgent = launchSubAgent(task);
        running.push({ task, newAgent });
      }
    }
  }

  return completed;
}
```

## 执行模式

| 模式 | 适用场景 | 说明 |
|---|---|---|
| `default` | 常规任务 | 标准权限，必要时暂停等待用户批准 |
| `acceptEdits` | 快速执行 | 自动接受文件编辑，适合已确认安全的任务 |
| `bypassPermissions` | 后台任务 | 跳过所有批准，适合纯分析任务 |
| `plan` | 高风险任务 | 先输出计划，用户确认后再执行 |

## 超时与重试

```
超时策略：
- 默认子任务超时：10 分钟
- 复杂任务（step > 5）：20 分钟
- 纯分析任务：5 分钟

重试策略：
- 失败后自动重试 1 次（`default` 模式）
- 重试失败则标记 `skipped`，继续其他并行分支
- 主 Agent 接管失败任务的兜底输出
```

## 上下文传递

子 Agent 的 prompt 中自动注入以下上下文：

```
=== 编排上下文 ===
当前任务编号：{current_step}/{total_steps}
并行组：{parallelGroup}（{current_parallel}/{total_parallel}）
已完成任务结果：
{previous_results_json}
=== 以下是你的任务 ===
{task_prompt}
```

这样每个子 Agent 都能感知整体进度和上游输出。
