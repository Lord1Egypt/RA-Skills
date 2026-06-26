## Description: <br>
智能助理核心技能，支持 20 轮对话上下文、情感识别、主动提醒、日程管理，集成飞书/钉钉/企业微信。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pengong101](https://clawhub.ai/user/pengong101) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and workflow agents use this skill to interpret workplace messages, maintain short conversation context, suggest responses, and coordinate reminders or schedule-related actions across configured collaboration platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can be configured with workplace messaging and calendar bot tokens, which may allow broad message sending or schedule changes if scopes are too permissive. <br>
Mitigation: Use dedicated least-privilege bot tokens, restrict channel and calendar scopes, and rotate tokens if the skill is tested in shared environments. <br>
Risk: The skill describes proactive reminders, schedule management, memory, and user profiling behavior without clear confirmation controls. <br>
Mitigation: Require explicit user confirmation before sending messages, notifying others, creating reminders, or changing calendar entries. <br>
Risk: The skill may report that an action was handled even when a connected backend has not actually performed it. <br>
Mitigation: Verify action completion in the target messaging or calendar backend before treating the result as final. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pengong101/secretary-core) <br>
- [Publisher profile](https://clawhub.ai/user/pengong101) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Context manager design](artifact/CONTEXT_MANAGER.md) <br>
- [Intent understanding design](artifact/INTENT_UNDERSTANDING.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, Python response dictionaries, CLI examples, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include suggested actions, intent and emotion labels, reminder or schedule instructions, and platform token configuration guidance.] <br>

## Skill Version(s): <br>
4.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
