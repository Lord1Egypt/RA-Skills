## Description: <br>
Task Protection helps agents and shell scripts register, track, log, analyze failures, retry, and report recurring, critical, external, user-delegated, or long-running tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alfredming-2026](https://clawhub.ai/user/alfredming-2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and AI agent users use this skill to add lifecycle tracking, logs, status files, failure analysis, retries, and reports to recurring system tasks, critical operations, external notifications, delegated one-time tasks, and long-running work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled news script includes an embedded Tavily API key. <br>
Mitigation: Remove and rotate the embedded key, then provide credentials through explicit user configuration or environment variables before running the script. <br>
Risk: The bundled news script uses a fixed Feishu recipient ID. <br>
Mitigation: Replace the hard-coded recipient with user-controlled configuration and confirm the target before enabling notifications. <br>
Risk: The scripts assume absolute /home/admin workspace paths. <br>
Mitigation: Review and update paths for the deployment environment before installation or scheduled execution. <br>
Risk: Task names, descriptions, logs, errors, generated reports, and newsletters can persist locally. <br>
Mitigation: Treat local task artifacts as retained operational data and apply review, retention, and cleanup practices appropriate for the user's environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/alfredming-2026/task-protection) <br>
- [Quickstart](docs/QUICKSTART.md) <br>
- [Task Trigger Criteria](docs/task-trigger-criteria.md) <br>
- [AI Task Registration](docs/ai-task-registration.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration, Markdown, Files] <br>
**Output Format:** [Markdown guidance with bash examples, JSON task status files, log files, and generated Markdown reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local task registry, task status, log, newsletter, and report files when its scripts are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
