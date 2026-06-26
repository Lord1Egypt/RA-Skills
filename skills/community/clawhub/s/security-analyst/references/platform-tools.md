# Security Analyst — Platform Tool Mapping

The security analyst runs on **Claude Code**, **Cursor**, and **OpenAI Codex**. All platforms use the same agents-only orchestration pattern — no Teams (TeamCreate/TeamDelete/SendMessage).

## Orchestration Model

All platforms spawn agents via the `Task` tool with self-contained prompts. The Task tool **blocks** until the agent completes and returns its result. No polling, no messaging.

**Claude Code / Codex** additionally support TaskCreate/TaskList/TaskUpdate for progress tracking (checkbox UX). **Cursor** does not have these tools.

## Tool Availability by Platform

### Claude Code & Codex (agents + task tracking)

- `Task` — spawn subagent (generalPurpose, explore, shell, etc.); **blocks until agent returns**
- `TaskCreate` — create tasks for progress tracking
- `TaskGet` — get a task by ID
- `TaskList` — list tasks, check status
- `TaskUpdate` — mark task complete after agent returns
- `TaskOutput` — get output from running/completed background task
- `TaskStop` — stop a background task
- **NOT used:** TeamCreate, TeamDelete, SendMessage — agents return results via Task return value

### Cursor (agents only — no task tracking)

- `Task` — spawn subagent (generalPurpose, explore, shell, etc.); **blocks until agent returns**
- `TodoWrite` — optional progress tracking (different from TaskCreate)
- **NOT available:** TeamCreate, TaskCreate, TaskList, TaskUpdate, SendMessage, TaskOutput, TaskStop

## Universal Flow (all platforms)

### Per-stage pattern

1. **Prepare** — Read prompt templates, build full prompt for each agent with all placeholders replaced
2. **Track (Claude Code / Codex only)** — Create tasks via TaskCreate for each agent
3. **Spawn** — Call `Task` for each agent:
   - `subagent_type`: "generalPurpose"
   - `prompt`: Full self-contained instructions including "Write output to {PATH}. Return your LOD-0 + LOD-1 summary in your final message."
   - `description`: Short label (e.g., "Recon step 1: metadata")
   - Batch all independent Task calls in ONE message
4. **Collect** — Task returns when done. Extract LOD-0/LOD-1 from the return content.
5. **Verify** — Glob/Read to confirm output files were written
6. **Update (Claude Code / Codex only)** — Mark tasks as completed via TaskUpdate
7. **Proceed** — Move to next stage

### Agent Prompts

All agents get **self-contained prompts** with full task instructions inline. Agent prompts should:
- Include all necessary context and instructions
- Specify the output file path
- End with "Return your LOD-0 + LOD-1 summary in your final message"
- NOT reference TaskList, SendMessage, or claiming tasks

## Summary

| Action | Claude Code / Codex | Cursor |
|--------|---------------------|--------|
| Create tasks | TaskCreate per agent | Skip |
| Spawn agents | Task tool (no team_name) | Task tool (no team_name) |
| Wait for completion | Task blocks — no polling | Task blocks — no polling |
| Get agent results | Task return value | Task return value |
| Mark complete | TaskUpdate | N/A |
| Progress tracking | TaskCreate/TaskList | TodoWrite (optional) |
