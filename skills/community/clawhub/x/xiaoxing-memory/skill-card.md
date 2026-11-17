## Description:

记忆模块管理系统，让 AI Agent 拥有持久化记忆能力。当需要保存跨会话信息、检索历史记录、建立个人知识库、或执行记忆相关操作（搜索/读取/保存）时触发本技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[crater18098077-svg](https://clawhub.ai/user/crater18098077-svg)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to give an agent persistent, file-backed memory for saving session history, searching prior work, and maintaining a personal knowledge base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables persistent storage and search over private or long-term memory, which may retain sensitive personal data without clear consent or retention controls.

Mitigation: Define allowed memory categories before use, exclude secrets and sensitive personal data, and require explicit approval before reading private memory or saving psychological or profile-like notes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/crater18098077-svg/skills/xiaoxing-memory)
- [Publisher profile](https://clawhub.ai/user/crater18098077-svg)
- [记忆系统架构详解](references/architecture.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Configuration, Guidance]

**Output Format:** [Markdown and file-structure guidance for memory index and topic files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses persistent workspace memory files such as MEMORY.md and memory/*.md; users should control what private information may be stored.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
