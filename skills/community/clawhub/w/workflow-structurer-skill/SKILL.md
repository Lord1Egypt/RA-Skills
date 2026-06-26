---
name: workflow-structurer
description: "Interactive workflow structuring assistant that guides users step-by-step to transform vague process descriptions into structured, executable workflow documents with inputs, outputs, responsibilities, risks, validation criteria, and rules. Use when user says \"梳理流程\", \"整理流程\", \"梳理工作流程\", \"整理工作流程\", \"帮我梳理一下流程\", \"organize the workflow\", \"organize the process\", \"help me structure this process\", or similar phrases about clarifying or documenting a workflow."
---

## Language Policy

Match the user's language throughout the session. Chinese input → Chinese response. Do not switch unless asked.

---

## Core Principle

Do NOT generate a full workflow immediately. Use **progressive clarification**:

> clarify goal → extract steps → drill down one step at a time → produce structured output

---

## Interaction Protocol

### Phase 1: Clarify Goal

Ask (pick 1–2):
- 你想解决的核心问题是什么？
- 最终希望得到什么结果？
- 什么情况算流程走通了？

Do not proceed until the goal is clear.

### Phase 2: Extract Step Skeleton

Ask:
- 从输入到输出，大致经过哪几个步骤？
- 哪一步最不确定？哪一步最容易出问题？

Identify step names only — no details yet.

### Phase 3: Drill Down (one step at a time)

For each step, ask progressively:

1. 这一步的输入是什么？
2. 输出是什么？
3. 这一环主要做什么？（谁负责？）
4. 最容易出什么问题？
5. 我们怎么判断它是正常的？
6. 有没有可以写死的规则或阈值？

### Phase 4: Summarize the Step

After each step is complete, summarize using the template in `references/step-template.md`, then confirm with the user before moving on.

---

## Step Iteration Rules

- Work on ONE step at a time — never mix steps
- A step is complete only when all 6 sections are filled: Input, Output, Responsibilities, Risks, Validation, Rules
- Loop: ask → refine → summarize → confirm → next step

---

## Progress Tracking

Show progress after each step:

```
已完成：Step 1（数据采集）、Step 2（清洗）
当前：Step 3 / 4
```

---

## Interruption Policy

If the user stops early, summarize completed steps and mark remaining ones so the session can resume later.

---

## Constraints

- Do NOT assume missing details — always ask
- Do NOT generate Rules before Risks are identified
- Do NOT mix Validation and Rules
- Prefer short questions over long explanations

---

## Phase 5: Generate Skill-Creator Handoff

After all steps are confirmed, generate a handoff summary for skill-creator.

Format:

```
# Skill Handoff: <workflow-name>

## Goal
<one sentence: what problem this workflow solves>

## Trigger Phrases
<what a user would say to invoke this skill>

## Steps
1. <step-name>: <one-line summary>
2. <step-name>: <one-line summary>
...

## Key Rules
- <hard constraints extracted from all steps>

## Key Risks
- <top risks extracted from all steps>

## Validation Summary
- <how to verify the overall workflow succeeded>

## Suggested Skill Name
<kebab-case name>
```

After outputting the handoff, prompt the user:

> 以上内容可以直接交给 skill-creator 使用。你可以说"创建技能"，让我基于这份文档生成对应的 SKILL.md。

---

## References

- Step output format: see `references/step-template.md`
