# Execution Tracker — 执行追踪与进度可视化

## 核心职责

让用户实时看到编排器的执行过程，从"黑盒运行"变为"透明可见"。

## 追踪数据结构

```typescript
interface ExecutionTrace {
  sessionId: string;           // 本次编排会话 ID
  startTime: number;            // 开始时间戳
  tasks: TaskState[];           // 任务状态列表
  events: TraceEvent[];          // 事件日志
}

interface TaskState {
  id: string;
  description: string;
  skill: string;
  status: "pending" | "running" | "completed" | "failed" | "skipped";
  progress: number;             // 0-100 预估进度
  startedAt?: number;
  completedAt?: number;
  duration?: number;            // 耗时 ms
  result?: string;              // 结果摘要（截取前 200 字）
  error?: string;
}

interface TraceEvent {
  timestamp: number;
  type: "task_start" | "task_complete" | "task_fail" | "checkpoint" | "merge";
  taskId?: string;
  message: string;
}
```

## 用户可见的追踪 UI（Markdown 格式）

在编排过程中，主 Agent 向用户输出以下格式的追踪界面：

```
═══════════════════════════════════════════════════
⚙️  技能编排器 · 执行中
═══════════════════════════════════════════════════
Session ID: orch-20260414-0908-a3f2
Started:    09:08:12
Duration:   正在计时...

───────────────────────────────────────────────────
📊 执行进度   ████████░░░░░░░░  3/7 任务完成 (43%)
───────────────────────────────────────────────────

✅ [step-1] 意图解析          0.3s  完成  [产品总监 + 财务顾问]
🔄 [step-2a] 产品规划          运行中 (67%)    [产品总监]
🔄 [step-2b] 财务评估          运行中 (45%)    [财务顾问]
⏳ [step-3]  技术选型          等待中          -
⏳ [step-4]  风险分析          等待中          -
⏳ [step-5]  综合报告          等待中          -

───────────────────────────────────────────────────
📡 最新事件
───────────────────────────────────────────────────
09:08:13  启动 step-2a、step-2b（并联执行）
09:08:14  检测到 step-3 依赖 step-2a，已加入等待队列
09:08:15  step-2b 完成，正在合并中间结果...

═══════════════════════════════════════════════════
```

## 进度计算规则

```
总任务数 = T
完成数 = C
失败数 = F
跳过数 = S

进度 = (C + F * 0.5) / T * 100%

说明：失败任务计 50% 进度（已执行但失败），避免进度条卡在 80%
```

## 事件通知阈值

```yaml
立即通知的事件：
  - 任何任务失败
  - 任何任务完成
  - 到达 checkpoint（人工确认节点）

定期摘要（每 60 秒）：
  - 汇总当前运行中的任务数量
  - 预计剩余时间估算
```

## 记忆持久化

编排完成后，追踪数据写入工作记忆：

```markdown
## 2026-04-14 编排记录

Session: orch-20260414-0908-a3f2
任务：AI 简历工具创业方案
调用 Skill：[产品总监, 财务顾问, 技术选型]
执行时长：4.2 秒
结果：综合方案（5 页）
冲突：1 个（定价分歧，已裁决）
满意度：✅
```
