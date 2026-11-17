---
name: write-goal
description: >
  Help the user craft a well-specified goal objective for autonomous mode — turn a rough intention
  into a completion contract with a clear finish line, proof, boundaries, and stop rule. Use when the
  user asks for help writing, refining, or improving a goal, wants to set a structured objective for
  autonomous execution, or when a request is vague and would benefit from structured decomposition
  before execution. Triggers: "帮我写个 goal", "write a goal", "设定目标", "set a goal", "create a goal",
  "目标模式", "/goal".
---

# Write Goal

Turn a rough user intention into a well-specified goal with a verifiable end state.

## Anatomy of a Good Goal

| Part | Description |
|------|-------------|
| **Objective** | One sentence: what will be true when done. Specific, actionable, verifiable. |
| **Completion Criterion** | How to check it's met. Concrete tests, commands, or observable outcomes. |
| **Boundary** | What is explicitly out of scope. Prevents scope creep. |
| **Budget** | Optional hard limit on turns, tokens, or time. |

## Workflow

### 1. Extract Intent

Identify from the user's request:
- **What** they want to achieve (the deliverable)
- **Constraints** — time, scope, tools, style

If already specific and verifiable, skip to step 3.

### 2. Identify Ambiguity

| Gap | Action |
|-----|--------|
| No clear deliverable | Ask: "What should exist when this is done?" |
| No validation path | Ask: "How will you know it works?" |
| Too broad | Break into sub-goals or pick the most important slice |
| No scope boundary | Ask: "What is explicitly NOT part of this goal?" |
| Subjective quality | Replace with measurable criteria |

If intent is clear from context, infer rather than ask.

### 3. Draft the Objective

Rules:
- **One sentence**, imperative mood
- **Specific**: name the deliverable, not the process
- **Verifiable**: completion criterion must be mechanically checkable
- **Scoped**: include boundary clause for broad requests
- **Self-contained**: a fresh agent with no context should understand it

Good:
```
"为 UserService 添加 JWT 认证中间件，实现登录/登出/token 刷新，所有现有测试保持通过。"
"Fix the memory leak in WebSocket handler — heap usage must stay stable over 10k messages."
```

Bad:
```
"改进代码质量"       — vague, no deliverable
"让页面好看一点"     — subjective, no validation
```

### 4. Define Completion Criterion

Prefer (in order):
1. **Command**: `npm test` passes, `tsc --noEmit` clean
2. **File existence**: specific file exists with expected content
3. **Observable output**: endpoint returns expected JSON
4. **Manual check**: only as last resort, must be specific

### 5. Commit the Goal

**If goal management tools are available** (e.g., `CreateGoal`, `SetGoalBudget`):

- Call the goal creation tool with the refined `objective` and `completionCriterion`.
- If the user specified a budget constraint, also set it:
  - "20 turns 内完成" → turns limit
  - "不要超过 500k tokens" → token limit
  - "30 分钟搞定" → time limit
- If an active goal already exists and the user wants to replace it, use the replace option.
- Do NOT set a budget unless the user explicitly asks.

**If no goal tools are available**:

- Present the structured goal as formatted text with clear sections: Objective, Completion Criterion, Boundary, Budget.
- Ask the user to confirm or adjust before proceeding with execution.

### 6. Present to User

Show the user:
- The objective (one line)
- The completion criterion (bullet list)
- Any budget set
- How to modify: "随时说 '修改目标' 或 '取消目标' 来调整"

## Refinement

When improving an existing goal:

- **If goal tools available**: read the current goal state, identify weaknesses, propose a revised version, apply after approval.
- **If no goal tools**: ask the user for the current goal text, identify weaknesses using the anatomy table, show the diff, proceed after approval.

## Multi-Goal Decomposition

For large requests:
1. Identify independent slices
2. Order by dependency
3. Focus on the first goal only — complete before next
4. Tell the user the full sequence

## Anti-Patterns

Do NOT:
- Create goals for greetings, questions, or non-executable requests
- Describe the process instead of the outcome
- Use subjective completion criteria
- Set budgets the user didn't ask for
- Make the objective so narrow it's a single tool call

## Language

Match the user's language. Technical terms and code identifiers stay in original form.
