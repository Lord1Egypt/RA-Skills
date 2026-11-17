# Startup Prompt Templates

Templates for the new conversation's opening prompt, adapted per IDE.
The goal: guide the new session's agent to **actively load** context that a platform-level "copy session" button would auto-inject.

---

## Universal Template (All IDEs)

```
This is a continuation of an existing project. Follow these steps:

Step 1: Load context
1. Read `docs/session-handoff.md` in the project root (project handoff document)
2. Read `docs/rules/coding-standards.md` (coding standards, if exists)
3. Read `docs/rules/processes.md` (process rules, if exists)

Step 2: Report to me
- What files you read and what you learned about the project
- Your understanding of the task I want to do
- Based on the project's current state and my task, what branchable directions are feasible

Step 3: Ask me
- Which direction I want to pursue
- Any technical details you're unsure about and need me to confirm

My task is: <TASK_DESCRIPTION>
```

---

## TRAE SOLO

```
This is a continuation of an existing project. Follow these steps:

Step 1: Load context (4 layers)
1. Read `docs/session-handoff.md` (project handoff document — 8-section structured summary)
2. Read `docs/rules/coding-standards.md` (coding standards, if exists)
3. Read `docs/rules/processes.md` (process rules, if exists)
4. OPTIONAL — Cross-project memory access (opt-in):
   Ask the user: "May I access your TRAE memory files (user profile, project memory, recent topics)? These may contain personal preferences and project-internal information. Declining is fine — I'll rely on TRAE's auto-injected memory and the handoff doc."
   - If user GRANTS consent:
     a. Read `user_profile.md` from your memory folder (cross-project preferences)
     b. Read `project_memory.md` from your memory projects folder (project conventions + lessons)
     c. Read the most recent `topics.md` from your memory projects folder (last 2 days of session topics)
     d. If the handoff doc references specific session_memory files, use Grep to search them by keyword
   - If user DECLINES: Skip this step. Rely on TRAE's auto-injected `<memory_item>` tags and the handoff doc only.

Step 2: Report to me
- What you learned from the handoff doc (summarize the 8 sections)
- Your understanding of the task I want to do
- Based on the project's current state, what branchable directions are feasible
- List any unfinished Todos from the handoff doc's "Current Work" section
- Do NOT report detailed user preferences from memory files — only acknowledge "memory context recovered" if applicable

Step 3: Ask me
- Which direction I want to pursue
- Any technical details you're unsure about and need me to confirm
- Whether the unfinished Todos should be continued or deprioritized

Note: Rules in `.trae/rules/` are auto-loaded — no need to read them manually.
Note: The handoff doc uses project-relative paths only. Do NOT construct absolute paths with usernames.
Note: Memory file reads are OPT-IN. Never silently read user_profile.md / project_memory.md / topics.md / session_memory files without explicit user consent.

My task is: <TASK_DESCRIPTION>
```

**TRAE SOLO adaptation notes**:
- Memory system is at `~/.trae-cn/memory/` — see `references/memory-guide.md` for full path structure
- TRAE auto-injects some memory via `<memory_item>` system reminders, but the new session should also explicitly read the files for completeness
- Rules in `.trae/rules/` are auto-loaded — do not include in the prompt
- `docs/knowledge/` contains deep knowledge files — load on demand, not upfront
- The handoff doc's "Current Work" section contains unfinished Todos — the new agent should offer to continue them

---

## WorkBuddy (Tencent)

```
这是一个已有项目的支线任务。请按以下步骤启动：

第一步：加载上下文
1. 读取 `.workbuddy/session-handoff.md`（项目交接文档 — 必读）
2. 如交接文档中引用了编码规范和流程规范，一并读取

【可选 — 需要你的明确同意】
在读取身份和记忆文件前，请先问我：
"是否允许我访问你的 WorkBuddy 身份文件（SOUL.md/IDENTITY.md/USER.md）和项目记忆（MEMORY.md）？这些文件可能包含你的个人偏好和项目内部信息。拒绝也没关系，我会基于交接文档继续。"

- 如果我同意：
  3. 读取 `~/.workbuddy/SOUL.md`（你的身份定义）
  4. 读取 `.workbuddy/memory/MEMORY.md`（项目记忆）
- 如果我拒绝：跳过身份/记忆文件读取，仅基于交接文档继续

第二步：向我汇报
- 你读取了哪些文件，了解到项目的什么状态
- 你对我要做的任务有什么理解
- 基于项目当前状态和我的任务，有哪些可行的支线方向
- 交接文档中是否有未完成的任务列表
- 不要汇报身份/记忆文件中的详细偏好内容，只确认"身份和记忆上下文已恢复"

第三步：问我
- 在你建议的方向中，我想走哪一条
- 有没有你不确定的技术细节需要我确认
- 未完成的任务是否应该继续

我的任务是：<任务描述>
```

**WorkBuddy adaptation notes**:
- Handoff doc saved to `.workbuddy/session-handoff.md` (aligns with memory system)
- Identity files (SOUL.md/IDENTITY.md/USER.md) and memory files (MEMORY.md) are OPT-IN — must ask user for explicit consent before reading
- Use Chinese prompts
- Use relative paths
- Do NOT report detailed personal preferences recovered from identity/memory files — only acknowledge that context was recovered

---

## Cursor

```
This is a continuation of an existing project. Follow these steps:

Step 1: Load context
1. Read `docs/session-handoff.md` in the project root
2. Read `docs/rules/coding-standards.md` (if exists)
3. Read `docs/rules/processes.md` (if exists)

Step 2: Report to me
- What you read and what you learned about the project state
- Your understanding of the task
- What directions are feasible given the current state
- Any unfinished Todos from the handoff doc

Step 3: Ask me
- Which direction I want to pursue
- Any technical details you need confirmed

My task is: <TASK_DESCRIPTION>
```

**Cursor adaptation notes**:
- `.cursor/rules/` is auto-loaded — equivalent to TRAE's `.trae/rules/`
- If the project has `.cursorrules`, mention it in the handoff doc
- Use project-relative paths only

---

## Claude Code

```
This is a continuation of an existing project. Follow these steps:

Step 1: Load context
1. Read `docs/session-handoff.md` in the project root
2. Read `docs/rules/coding-standards.md` (if exists)
3. Read `docs/rules/processes.md` (if exists)

Step 2: Report to me
- What you read and what you learned about the project state
- Your understanding of the task
- What directions are feasible given the current state
- Any unfinished Todos from the handoff doc

Step 3: Ask me
- Which direction I want to pursue
- Any technical details you need confirmed

My task is: <TASK_DESCRIPTION>
```

**Claude Code adaptation notes**:
- `CLAUDE.md` provides project-level rules — mention it in the handoff doc if it exists
- Use project-relative paths only

---

## Customization Guide

To adapt for a new IDE:

1. Check if the IDE auto-loads rules files (if yes, don't include them in the prompt)
2. Use project-relative paths only (never absolute paths with usernames)
3. Check the IDE's preferred language (Chinese IDEs may prefer Chinese prompts)
4. Check if the IDE has a memory/identity system (like WorkBuddy's SOUL.md/MEMORY.md or TRAE's memory folder)
5. If a memory system exists, add explicit "read memory files **with user consent (OPT-IN)**" instructions to Step 1 — never silently read identity/memory files; always ask the user first and provide a clear "decline is fine" alternative
6. When reporting recovered memory context, limit to project conventions and recent topics — do NOT report detailed personal preferences (language, security sensitivity, work style details); only acknowledge "memory context recovered"
7. Determine the handoff document save location (project docs/ vs IDE-specific directory)
8. Add the new template to this file and update SKILL.md's `target_ide` config
