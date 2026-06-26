# Dispatch Protocol: Three-Role Isolation

## Architecture

```
+-------------------------------------+
|        Orchestrator (You)            |
|  Steps 1-3: Profile + Generate Tasks|
|  Steps 6-7: Score + Report          |
|  NEVER executes test tasks           |
+----------+------------+-------------+
           |            |
    +------v------+ +--v--------------+
    | Sub-Agent A | | Sub-Agent B      |
    |  Baseline   | |  With-Skill      |
    | No skill    | | Reads skill first|
    +-------------+ +-----------------+
```

**Orchestrator**: Designs tasks and scores results. Reads skill content for task design only. NEVER answers any test task.

**Sub-Agent A (Baseline)**: Receives ONLY task prompts. No skill content, no skill name, no hint about the evaluation.

**Sub-Agent B (With-Skill)**: Receives task prompts AND the full skill content. Applies the skill before answering.

## Sub-Agent A Prompt Template

Copy this exactly. Replace `{TASK_LIST}` with `task_id + prompt` pairs. **MUST NOT** contain any skill content.

```
You are a task executor. Complete each task independently based on your own knowledge.

Rules:
- Answer each task independently
- Do NOT read, reference, or apply any external skill file
- Provide your best answer

Tasks:
{TASK_LIST}

Output: Return a JSON array:
[{"task_id": "...", "output": "your answer", "reasoning_summary": "your approach"}]
Return ONLY the JSON array.
```

## Sub-Agent B Prompt Template

Copy this exactly. Replace `{SKILL_CONTENT}` with full SKILL.md, `{TASK_LIST}` with the same tasks as Sub-Agent A.

```
You are a task executor. Read the skill below first, then apply its guidance to every task.

## Skill to Apply
{SKILL_CONTENT}

---

Rules:
- Understand the skill content FIRST
- Apply its methodology to each task
- Answer each task independently

Tasks:
{TASK_LIST}

Output: Return a JSON array:
[{"task_id": "...", "output": "your answer", "reasoning_summary": "approach + skill influence", "skill_applied": true, "skill_influence_notes": "what changed"}]
Return ONLY the JSON array.
```

## Constraints

| Constraint | Requirement |
|------------|-------------|
| Isolation | Sub-Agent A and B MUST be different sessions (different `session_id`) |
| Single-arm | NEVER run both arms in one sub-agent |
| Variable control | Same model, temperature, tools; only variable is skill on/off |
| Skill isolation | Sub-Agent A's prompt MUST NOT contain skill content |
| No self-execution | Orchestrator MUST NOT answer any test task |

## Evidence Requirements

Results must include `dispatch_evidence`:

```json
{
  "orchestrator_role": "prepare_and_score_only",
  "baseline_agent_session_id": "arm-a-session-id",
  "skill_agent_session_id": "arm-b-session-id",
  "baseline_prompt_contains_skill": false
}
```

Each task must also include per-arm evidence with distinct `session_id` values.
