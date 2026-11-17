## Description:

3 分钟启动器：把拖延待办、卡住任务、模糊目标、项目/家务/习惯拆成下一步物理动作、3 分钟启动、5 分钟扩展、今日算赢标准和断了以后的回归脚本。适合反拖延、每日执行、任务拆解、低能量启动和轻量 check-in。

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and general agent users use this skill to turn overwhelming or delayed todos into immediate next physical actions, 3-minute starts, daily momentum plans, and low-shame recovery scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may produce productivity plans that are too broad if the user's todo list is vague or overloaded.

Mitigation: Ask at most one clarifying question when needed, choose no more than seven candidate items for today, and convert each item into a visible next physical action.

Risk: Users may treat generated starts as durable reminders or task storage.

Mitigation: Use reminder, calendar, automation, or durable todo tools only when the user explicitly asks for tracking, scheduling, or recurring follow-up.

Risk: Chinese-first behavior may surprise users who expect another response language.

Mitigation: Default to Chinese only when the user writes in Chinese and otherwise follow the user's language.

## Reference(s):

- [Three-Minute Starts](references/three-minute-starts.md)
- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/skills/todo-momentum)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Text]

**Output Format:** [Markdown or plain text with compact tables and action-plan templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-first responses when the user writes in Chinese; no code execution or durable tracking unless the user asks for an available external tool.]

## Skill Version(s):

0.2.0 (source: SKILL.md frontmatter, skill.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
