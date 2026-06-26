# Result Merger — 结果合并与冲突裁决

## 核心职责

将多个子 Agent 的输出合并为统一的综合方案，处理内容重复、结论冲突、格式不一致等问题。

## 合并场景

### 场景 1：独立维度分析（无冲突）

```
Task-A 输出：产品定位报告（Markdown）
Task-B 输出：财务评估报告（Markdown）
Task-C 输出：技术选型报告（Markdown）
      ↓
合并策略：直接拼接 + 添加分隔标题
```

**合并格式：**

```markdown
# 综合方案报告

## 📦 一、产品规划
[Task-A 内容]

## 💰 二、财务评估
[Task-B 内容]

## ⚙️ 三、技术选型
[Task-C 内容]

## 🎯 四、整合建议
[主 Agent 交叉分析]
```

### 场景 2：同一问题给出不同结论（冲突）

```
Task-A："定价策略建议走高端路线，单价 ¥299"
Task-B："建议走性价比路线，单价 ¥99"
      ↓
裁决规则：
1. 若两结论差距 < 10%，取均值或合并
2. 若两结论差距 > 50%，标注"存在分歧"并列呈现
3. 主 Agent 给出裁决理由
```

**输出格式：**

```markdown
## ⚠️ 定价策略（存在分歧）

| 方案 | 建议方 | 理由 |
|---|---|---|
| 高端路线 ¥299 | 产品总监 | 品牌溢价、毛利空间 |
| 性价比路线 ¥99 | 市场专家 | 快速获客、市场渗透 |

**主 Agent 裁决**：综合考虑冷启动阶段的不确定性，建议采用
分层定价策略——基础版 ¥99（获客），高级版 ¥299（转化）。
```

### 场景 3：格式不一致

```
Task-A 输出：JSON
Task-B 输出：纯文本
Task-C 输出：Markdown 表格
      ↓
统一转换为结构化 Markdown
```

## 合并算法

```typescript
interface MergeResult {
  merged: string;           // 合并后的综合内容
  conflicts: Conflict[];    // 检测到的冲突列表
  summary: string;           // 一句话总结
  nextSteps: string[];      // 建议的后续行动
  confidence: number;      // 合并置信度 0-1
}

function mergeResults(taskResults: TaskResult[]): MergeResult {
  const conflicts = detectConflicts(taskResults);
  const merged = conflicts.length > 0
    ? mergeWithConflictNote(taskResults, conflicts)
    : simpleConcat(taskResults);

  return {
    merged,
    conflicts,
    summary: generateSummary(taskResults),
    nextSteps: generateNextSteps(taskResults),
    confidence: conflicts.length === 0 ? 0.95 : 0.7
  };
}
```

## 冲突检测规则

```yaml
冲突类型:
  - 名称: "数字结论冲突"
    检测: "两输出包含同一个数字指标但值不同"
    例: "Task-A 说成本 5 万，Task-B 说成本 15 万"
    
  - 名称: "方向结论冲突"
    检测: "两输出包含相斥的 action verb"
    例: "Task-A 建议扩张，Task-B 建议收缩"
    
  - 名称: "前提假设冲突"
    检测: "两输出的 base assumption 互相矛盾"
    例: "Task-A 以'目标用户是 Z 世代'为前提，Task-B 以'目标用户是职场人群'为前提"

裁决优先级:
  1. 有数据支撑 > 无数据支撑
  2. 最近数据 > 历史数据
  3. 更专业的 Skill > 更通用的 Skill
  4. 无法裁决 → 呈现双方 + 主 Agent 判断
```

## 长上下文与溯源

窗口变长后，仍优先向下游传递 **结构化摘要 + `step_id` +短证据摘录**（≤200 字/条），而非无脑拼接全文；冲突条目在 `machine-contract.md` 的 `evidence_snippet` 中落地，便于审计与人工复核。

## 输出格式规范

最终合并输出必须包含：

```yaml
final_output:
  task_overview: "一句话描述任务"
  skill_invocations: ["skill-A", "skill-B"]
  sub_task_results: [...]
  merged_content: "## 合并后内容..."
  conflicts_handled: [...]
  next_steps: ["建议1", "建议2"]
  confidence: 0.85
```
