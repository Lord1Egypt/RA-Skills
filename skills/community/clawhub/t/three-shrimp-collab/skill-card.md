## Description: <br>
三只虾协作系统 is a multi-agent task coordination framework for role-based task assignment, file-based monitoring, heartbeat checks, and completion notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AyangAI](https://clawhub.ai/user/AyangAI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to coordinate OpenClaw-style multi-agent work through shared task queues, role responsibilities, macOS file monitoring, scheduled heartbeat checks, and Feishu task completion notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent macOS launchd and fswatch monitoring can run in the background with weak scoping and hard-coded local paths. <br>
Mitigation: Inspect the scripts and plist configuration before loading services, replace hard-coded paths with environment-specific paths, and enable monitoring only for intended task files. <br>
Risk: Feishu notifications can expose task details, private links, credentials, or other sensitive work product to the wrong recipient or webhook. <br>
Mitigation: Verify the Feishu webhook and recipient before use, redact sensitive queue details, and avoid placing secrets or customer data in task queues or notification messages. <br>
Risk: Automatic task queue, memory, and notification workflows may overwrite or remove operational context. <br>
Mitigation: Keep backups or version control for queue and memory files before enabling automated cleanup or recurring background workflows. <br>
Risk: The release evidence does not include server-resolved source provenance. <br>
Mitigation: Treat the artifact files as the review boundary and do not infer GitHub origin, maintainership, or upstream history from the skill text. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AyangAI/three-shrimp-collab) <br>
- [Publisher profile](https://clawhub.ai/user/AyangAI) <br>
- [Skill overview](artifact/SKILL.md) <br>
- [Detailed documentation](artifact/README.md) <br>
- [Automation flow](artifact/docs/shrimp-automation-flow.md) <br>
- [Collaboration protocol](artifact/docs/shrimp-collaboration-protocol.md) <br>
- [Heartbeat configuration](artifact/docs/shrimp-heartbeat-config.md) <br>
- [Task notification guide](artifact/docs/shrimp-task-notification.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces task queue conventions, role coordination guidance, launchd setup steps, and notification workflow instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
