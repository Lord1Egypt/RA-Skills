## Description: <br>
Transform AI agents from task-followers into proactive partners that anticipate needs and continuously improve with memory, proactive check-ins, security hardening, self-healing, and verification patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure an assistant with persistent memory, proactive check-ins, onboarding, self-healing workflows, security review habits, and approval gates for external actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory and profile logging can capture sensitive personal or workspace information. <br>
Mitigation: Require explicit opt-in before enabling memory files, define what may be recorded, and regularly review or purge generated memory. <br>
Risk: Proactive monitoring of mailboxes, calendars, files, apps, logs, tools, and accounts can exceed the user's intended scope. <br>
Mitigation: Limit the skill to a documented allowlist of sources and accounts before use. <br>
Risk: Crons and autonomous sub-agents can take action without sufficient oversight. <br>
Mitigation: Disable autonomous schedules by default or require human approval before enabling them. <br>


## Reference(s): <br>
- [Proactive Agent on ClawHub](https://clawhub.ai/yuyonghao-123/yuyonghao-proactive-agent) <br>
- [Onboarding Flow Reference](references/onboarding-flow.md) <br>
- [Security Patterns Reference](references/security-patterns.md) <br>
- [Hal 9001 profile](https://x.com/halthelobster) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes starter memory, onboarding, heartbeat, agent-rules, and security-audit artifacts for an agent workspace.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and package.json; artifact skill text describes 3.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
