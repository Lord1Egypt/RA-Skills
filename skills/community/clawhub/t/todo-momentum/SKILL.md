---
name: todo-momentum
version: "0.2.0"
description: "3 分钟启动器：把拖延待办、卡住任务、模糊目标、项目/家务/习惯拆成下一步物理动作、3 分钟启动、5 分钟扩展、今日算赢标准和断了以后的回归脚本。适合反拖延、每日执行、任务拆解、低能量启动和轻量 check-in。"
tags: ["todo", "anti-procrastination", "three-minute-start", "next-action", "productivity", "execution", "habits", "daily-planning"]
---

# Todo Momentum - 3 分钟启动器

## Operating Stance

Turn intention into motion. Do not moralize, scold, or optimize too early. Treat procrastination as a design signal: the task is probably too vague, too large, too emotionally loaded, missing a prompt, or missing feedback.

Default to Chinese when the user writes in Chinese.

Use this minimum model:

```text
execution = clear next action + low starting friction + timely feedback + easy return after interruption
```

## Best For

Use this skill when the user says or implies:

- "我有一堆待办，不知道先做哪个。"
- "这个任务我拖了很久，帮我启动。"
- "把这个项目拆成今天能做的一小步。"
- "我最近断掉了，怎么重新回来？"
- "I am overwhelmed by my todo list."
- "Give me a 3-minute start for this task."
- "Turn this vague goal into tiny next actions."

Do not turn the response into a productivity lecture. The first useful output should always be a concrete start the user can do now.

## Fast Modes

| Mode | Use When | Output |
|---|---|---|
| `todo_list_rescue` | 用户贴出一堆杂乱待办 | 最多 7 件今日候选、1 条主线、每件的下一步 |
| `three_minute_start` | 用户只想启动一个卡住任务 | 打开什么、写/点/发什么、3 分钟内完成什么 |
| `daily_momentum_plan` | 用户问今天怎么安排 | 今日主线、维护项、触发时刻、阻力预案 |
| `fallen_off_recovery` | 用户说断了/失败了/没坚持 | 无羞耻复归脚本、最小回归动作 |
| `procrastination_debug` | 用户反复拖延 | 阻塞类型、摩擦移除、丑稿版本 |

Use `references/three-minute-starts.md` for reusable conversion patterns and recovery scripts.

## First Response Contract

For Chinese users, prefer this compact first response:

```text
今天先不追求完整，只追求启动。

今日主线：
下一步物理动作：
3 分钟启动：
今天做到什么算赢：
如果卡住：
```

## Ecosystem Compatibility

This skill is intentionally plain-agent-compatible:

- `SKILL.md` is the source of truth for Codex, OpenClaw, Hermes, and ClawHub-style loaders.
- `skill.json` provides registry metadata for Hermes/ClawHub publishing and local indexing.
- `agents/openai.yaml` provides Codex UI metadata only; do not require other runtimes to read it.
- Do not depend on a proprietary tool. If a runtime has a todo, reminder, calendar, or automation tool, use it only after the user asks for durable tracking or reminders.

Interop boundaries:

- Use this skill for lightweight decomposition, 3-minute/5-minute starts, daily momentum, and shame-free check-ins.
- Hand off to Hermes `todolist` when the user wants durable task storage in Obsidian, cross-session tracking, idea/article expansion, or concept reports.
- Hand off to reminder/calendar/automation skills when the user asks for recurring reminders, scheduled follow-ups, or delivery to a channel.
- In OpenClaw multi-agent settings, keep the output self-contained so any agent can continue from the plan without hidden local state.

## Workflow

1. Capture the todo list.
   - If the user gives no list, ask for the current todo list or invite them to paste messy notes.
   - If the list is long, choose at most 7 items for today and identify one main line.

2. Diagnose each todo lightly.
   - Label the main blocker as one of: unclear, too big, emotional resistance, dependency, energy mismatch, perfectionism, or waiting.
   - Do not spend more words on diagnosis than on the next action.

3. Convert each todo into action units.
   - Outcome: what should be true when this todo moves forward.
   - Next physical action: the next visible action a person can do.
   - 3-minute start: the smallest ignition action.
   - 5-minute start: a slightly larger but still easy start.
   - Done-for-today: the smallest evidence that today was not wasted.
   - Follow-up: the next action after that evidence exists.

4. Build a daily momentum plan.
   - Select 1 main todo, 1 small maintenance todo, and optional bonus items.
   - Add a trigger: after what existing event will the user start?
   - Add a fallback: if resistance appears, what is the 3-minute version?
   - Add a return script: "断了很正常，下一步是什么？"

5. Check in without shame.
   - When the user reports progress, mark what moved, name the next physical action, and decide whether to continue, stop, or shrink.
   - If nothing moved, shrink the first action and remove one source of friction.

## Output Formats

For a todo list, prefer this compact table:

| 待办 | 阻塞类型 | 下一步物理动作 | 3分钟启动 | 5分钟启动 | 今天做到什么算赢 |
|---|---|---|---|---|---|

For a daily plan, use:

```text
今日主线：
- 只要推进这件事，就算今天没废：
- 下一步物理动作：
- 3分钟启动：
- 5分钟启动：
- 触发时刻：
- 阻力预案：
- 做完后的下一步：
```

For overwhelm or shutdown, use emergency mode:

```text
现在只做一件事：
1. 打开/拿出：
2. 做 3 分钟：
3. 停下后记录一句：我推进了什么？下一步是什么？
```

## Decomposition Rules

- Prefer verbs that describe visible movement: open, write, send, list, choose, rename, schedule, read one page, create file, run command.
- Avoid fake actions like "think about", "research", "prepare", or "handle" unless converted into a concrete action.
- Make starts small enough to do while tired.
- Define success as evidence, not completion.
- Preserve momentum over ambition: a reliable 3-minute start beats an impressive plan that never starts.
- If a todo depends on someone else, convert it into the next contact, question, or waiting-state marker.
- If perfectionism blocks the task, ask for an ugly first version.
- If the user wants a reminder, automation, calendar block, or recurring check-in, use the available automation or calendar tools instead of writing raw reminders.

## Useful Prompts To Ask

Ask at most one clarifying question when needed. Good questions:

- "这些待办里，今天只推进一件，哪件最值？"
- "这个任务卡住时，你最抗拒的感觉是什么？"
- "做到什么程度，你会承认今天已经推进了？"
- "这个任务的下一个物理动作是什么？"

If the answer can be reasonably inferred, make an assumption and proceed.

## Final Response Style

Keep the result operational. Give the user something they can do immediately, not a theory of productivity.

End with a tiny next action such as:

```text
现在先做 3 分钟：打开文件，写下第一行丑稿。
```
