## Description:

Manage, track, and update enterprise WeCom tasks and goals with creation, progress updates, status reporting, filtering, and dependency handling for authorized agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jhzheng222](https://clawhub.ai/user/jhzheng222)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to coordinate WeCom-backed task and goal records, including task creation, lifecycle updates, dependency-aware next-task selection, reminders, filtering, and status reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify or delete shared WeCom task records.

Mitigation: Review before installing in any shared or production WeCom workspace and require explicit confirmation for delete operations.

Risk: Access controls are too weak for the authority granted to task and goal APIs.

Mitigation: Replace AGENT_ID-based authorization with a trusted runtime identity and add authorization checks to all goal APIs.

Risk: Hardcoded document and sheet fallbacks could target unintended shared records.

Mitigation: Remove hardcoded doc and sheet fallbacks and require explicit configuration for each workspace.

Risk: mcporter invocation behavior needs review before production use.

Mitigation: Change mcporter calls to use argument arrays with shell=False.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jhzheng222/skills/wecom-task-manager)
- [API reference](references/api.md)
- [Quickstart guide](QUICKSTART.md)
- [Priority levels](PRIORITY_LEVELS.md)
- [Enterprise WeChat smart sheet API](https://open.work.weixin.qq.com/devtool/query?e=2022034)
- [mcporter tool documentation](https://github.com/openclaw/mcporter)
- [OpenClaw AgentSkills specification](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples plus JSON configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call WeCom smart-sheet APIs through mcporter and may create, update, or delete shared task and goal records.]

## Skill Version(s):

1.2.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
