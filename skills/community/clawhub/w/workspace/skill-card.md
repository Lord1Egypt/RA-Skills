## Description: <br>
Workspace helps agents manage self-hosted Jira work logs by logging time, creating daily templates, listing issues, testing connections, and setting Apple Reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[polarali](https://clawhub.ai/user/polarali) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and individual contributors use this skill to manage time tracking against self-hosted Jira from an agent-assisted CLI workflow. It supports testing Jira connectivity, listing issues, creating daily work logs, logging time, and setting reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled real credentials or sensitive Jira configuration could expose account or project access. <br>
Mitigation: Remove real credentials before installation, use local example configuration or a secret store, and rotate any exposed Jira API tokens. <br>
Risk: Unrelated Google Docs and Word automation may perform actions outside the Jira logging use case. <br>
Mitigation: Review the package before installing and run those automation files only when those actions are intentional. <br>
Risk: LaunchAgent or background tracker installers may create persistent local services that write logs or send reminders. <br>
Mitigation: Install persistent services only after reviewing their behavior, and disable or remove them when reminder automation is not required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/polarali/workspace) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create daily log files, Jira work-log API requests, reminders, and local service setup commands when the user intentionally runs those workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
