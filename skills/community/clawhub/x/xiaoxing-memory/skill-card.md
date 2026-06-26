## Description: <br>
记忆模块管理系统，让 AI Agent 拥有持久化记忆能力。当需要保存跨会话信息、检索历史记录、建立个人知识库、或执行记忆相关操作（搜索/读取/保存）时触发本技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[crater18098077-svg](https://clawhub.ai/user/crater18098077-svg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to give an AI agent file-based long-term memory across sessions, including saving, indexing, searching, and retrieving remembered context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory files may retain passwords, tokens, financial details, sensitive personal information, or private context if users save them indiscriminately. <br>
Mitigation: Avoid saving sensitive secrets or personal data, and periodically inspect or delete MEMORY.md, USER.md, memory/, and private memory files. <br>
Risk: Long-term memory can preserve outdated or irrelevant context that later affects agent behavior. <br>
Mitigation: Use the documented periodic整理 workflow to consolidate useful daily logs into topic files and remove stale index entries. <br>


## Reference(s): <br>
- [Memory System Architecture](references/architecture.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with file templates and workflow steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guidance for maintaining MEMORY.md, USER.md, memory/, and optional private memory files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
