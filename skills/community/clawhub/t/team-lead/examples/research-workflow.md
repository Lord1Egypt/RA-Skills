# 示例：市场研究报告工作流

## 用户请求

```
帮我做一份 2026 年 AI 芯片市场分析报告，包括主要玩家、市场规模、趋势预测
```

## Team Lead 执行流程

### Step 1: 任务分析

**识别结果：**
```json
{
  "taskType": "research",
  "complexity": "high",
  "requiredCapabilities": ["市场研究", "数据分析", "报告撰写"],
  "estimatedSubtasks": 4
}
```

**分析过程：**
- 关键词匹配：`研究`、`分析`、`报告` → research 模板
- 复杂度评估：涉及多个子领域 → high
- 预计需要：数据搜索 + 分析 + 撰写

---

### Step 2: 任务分解

**分解结果：**
```json
{
  "template": "research",
  "subtasks": [
    {
      "id": "step-0",
      "type": "search",
      "label": "信息搜索",
      "suggestedAgentType": "search",
      "dependsOn": [],
      "parallel": true,
      "priority": 2,
      "input": {
        "task": "帮我做一份 2026 年 AI 芯片市场分析报告...",
        "instruction": "搜索 2026 年 AI 芯片市场规模、增长率、主要数据，提供来源链接"
      },
      "estimatedTime": 60
    },
    {
      "id": "step-1",
      "type": "search",
      "label": "厂商调研",
      "suggestedAgentType": "search",
      "dependsOn": [],
      "parallel": true,
      "priority": 2,
      "input": {
        "instruction": "搜索 AI 芯片主要厂商：NVIDIA、AMD、Intel、华为海思等，市场份额和产品线"
      },
      "estimatedTime": 60
    },
    {
      "id": "step-2",
      "type": "analyze",
      "label": "数据分析",
      "suggestedAgentType": "analysis",
      "dependsOn": ["step-0", "step-1"],
      "parallel": false,
      "priority": 3,
      "input": {
        "instruction": "分析市场趋势、竞争格局、技术发展方向"
      },
      "estimatedTime": 90
    },
    {
      "id": "step-3",
      "type": "writing",
      "label": "报告撰写",
      "suggestedAgentType": "writing",
      "dependsOn": ["step-2"],
      "parallel": false,
      "priority": 1,
      "input": {
        "instruction": "整合为结构化报告，包含执行摘要、市场分析、趋势预测"
      },
      "estimatedTime": 120
    }
  ],
  "executionPlan": [
    { "type": "parallel", "tasks": [0, 1] },
    { "type": "sequential", "tasks": [2] },
    { "type": "sequential", "tasks": [3] }
  ],
  "estimatedTotalTime": 330
}
```

---

### Step 3: Agent 发现与分发

**Agent 匹配结果：**

| 子任务 | 所需能力 | 匹配 Agent | 匹配度 |
|--------|----------|-----------|--------|
| step-0 | search | search-agent (dynamic) | 1.0 |
| step-1 | search | search-agent (dynamic) | 1.0 |
| step-2 | analysis | analysis-agent (dynamic) | 0.95 |
| step-3 | writing | writing-agent (dynamic) | 0.92 |

**分发策略：**
- 并行组 1：step-0, step-1 同时执行
- 串行：step-2 等待并行组完成
- 串行：step-3 等待 step-2 完成

---

### Step 4: 执行过程

```
[10:00:00] 开始任务 task-1710410400000
[10:00:01] 任务分解完成，4 个子任务
[10:00:02] 并行执行：step-0, step-1
[10:01:02] step-0 完成 (60s)
[10:01:03] step-1 完成 (61s)
[10:01:04] 开始执行 step-2 (等待依赖完成)
[10:02:34] step-2 完成 (90s)
[10:02:35] 开始执行 step-3
[10:04:35] step-3 完成 (120s)
[10:04:36] 质量检查通过 (85/100)
[10:04:37] 结果聚合完成
[10:04:38] 任务完成，总耗时 278s
```

---

### Step 5: 质量检查

**质量报告：**
```json
{
  "summary": {
    "total": 4,
    "passed": 4,
    "failed": 0,
    "avgScore": 0.85,
    "passRate": 1.0
  },
  "details": [
    {
      "subtaskId": "step-0",
      "overallScore": 0.88,
      "passed": true,
      "feedback": ["内容完整", "有数据来源"]
    },
    {
      "subtaskId": "step-1",
      "overallScore": 0.82,
      "passed": true,
      "feedback": ["覆盖主要厂商", "建议添加更多细节"]
    },
    {
      "subtaskId": "step-2",
      "overallScore": 0.90,
      "passed": true,
      "feedback": ["分析深入", "洞察有价值"]
    },
    {
      "subtaskId": "step-3",
      "overallScore": 0.85,
      "passed": true,
      "feedback": ["结构清晰", "表达流畅"]
    }
  ]
}
```

---

### Step 6: 结果聚合

**聚合策略：** `merge`（合并互补信息）

**最终输出结构：**
```markdown
# 2026 年 AI 芯片市场分析报告

## 执行摘要
[由 step-3 生成]

## 市场规模
[整合自 step-0]
- 2026 年全球市场规模：XXX 亿美元
- 年复合增长率：XX%
- 主要驱动因素：...

## 主要厂商
[整合自 step-1]
### NVIDIA
- 市场份额：XX%
- 主要产品：...

### AMD
- 市场份额：XX%
- 主要产品：...

[其他厂商...]

## 竞争格局分析
[整合自 step-2]
- 市场集中度：...
- 竞争态势：...

## 趋势预测
[整合自 step-2 和 step-3]
### 技术趋势
- ...

### 市场趋势
- ...

## 数据来源
[整合自所有步骤]
1. ...
2. ...
```

---

### Step 7: 最终交付

**交付结果：**
```json
{
  "taskId": "task-1710410400000",
  "status": "completed",
  "duration": 278000,
  "quality": 0.87,
  "result": {
    "type": "merged",
    "sections": 4,
    "totalLength": 5200,
    "format": "markdown"
  },
  "stats": {
    "subtasksCompleted": 4,
    "subtasksTotal": 4,
    "agentsUsed": ["search-agent", "analysis-agent", "writing-agent"],
    "parallelGroups": 1,
    "sequentialSteps": 2
  }
}
```

---

## 关键指标

| 指标 | 数值 | 说明 |
|------|------|------|
| 总耗时 | 278s | 比串行执行节省约 120s |
| 质量评分 | 87/100 | 良好 |
| Agent 使用数 | 3 | 动态创建 |
| 并行度 | 2 | 最多 2 个任务同时执行 |
| 用户满意度 | 高 | 结构化报告，数据详实 |

---

## 经验教训

### ✅ 做得好的
1. 任务分解合理，依赖关系清晰
2. 并行执行节省时间
3. 质量检查确保输出质量

### ⚠️ 可改进的
1. step-1 可以要求更多细节
2. 可以添加事实核查步骤
3. 可以考虑使用缓存加速类似任务

---

## 复用建议

同样的工作流可以应用于：
- 其他行业市场分析报告
- 竞品分析报告
- 技术趋势研究报告
- 投资尽职调查

只需修改任务分解模板中的具体指令即可。
