# Machine Contract — 机器可读附录

可选 JSON 供宿主、脚本或评测解析；**人类仍以 Markdown 为主**。在 Step 3（计划）、Step 6/7（合并与终稿）后可选用下列结构，放在 Markdown 代码围栏内并标注语言为 `json`。

## 会话与计划

```json
{
  "schema": "skill-orchestrator.bundle@v1",
  "session_id": "orch-20260414-a3f2",
  "user_goal_one_liner": "一句话用户目标",
  "intent": {
    "task_type": "综合方案 | 分析评估 | 内容生成 | 指导建议 | 信息查询",
    "domains": ["产品", "财务"],
    "complexity": "single | multi | complex",
    "constraints": ["时间紧", "无预算"]
  },
  "plan": {
    "steps": [
      {
        "id": "step-1",
        "skill": "builtin|skill-name",
        "mode": "default|acceptEdits|plan|bypassPermissions",
        "depends_on": [],
        "parallel_group": null,
        "risk_tier": "low|medium|high"
      },
      {
        "id": "step-2a",
        "skill": "产品总监",
        "mode": "acceptEdits",
        "depends_on": [],
        "parallel_group": "phase-2",
        "risk_tier": "low"
      }
    ]
  }
}
```

## 执行轨迹（可增量追加）

```json
{
  "session_id": "orch-20260414-a3f2",
  "events": [
    {
      "ts": "ISO8601",
      "step_id": "step-2a",
      "type": "task_start|task_complete|task_fail|checkpoint|merge",
      "message": "人类可读一句",
      "error_class": "timeout|refusal|tool_error|null"
    }
  ]
}
```

## 合并结果

```json
{
  "session_id": "orch-20260414-a3f2",
  "merge": {
    "summary": "一句话结论",
    "confidence": 0.88,
    "conflicts": [
      {
        "topic": "定价策略",
        "positions": [
          { "from_step": "step-2a", "claim": "¥299 高端", "evidence_snippet": "≤200 字摘录" },
          { "from_step": "step-2b", "claim": "¥99 性价比", "evidence_snippet": "≤200 字摘录" }
        ],
        "resolution": "分层定价 | 保留分歧 | 待用户裁决",
        "resolution_confidence": 0.82
      }
    ],
    "next_steps": ["建议 1", "建议 2"]
  }
}
```

## 使用约定

- 字段名可扩展，**勿删** `schema` / `session_id`（若输出 JSON）。
- `risk_tier`与 Registry 中 Skill 声明对齐时，利于自动 Checkpoint。
- 与 `orchestration-engine.md` 中 TypeScript 接口互补：接口偏实现，本文件偏**可交换数据**。
