## Description: <br>
Automates monitoring and self-repair of OpenClaw Gateway on Windows using Task Scheduler, with AI diagnosis and Telegram alert notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aichiafranco](https://clawhub.ai/user/aichiafranco) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators who run OpenClaw Gateway on Windows use this skill to deploy scheduled monitoring, trigger repair workflows, inspect status and logs, and configure alerting for failures that need manual attention. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent PowerShell automation is installed through Windows Task Scheduler and can restart services or run repair workflows. <br>
Mitigation: Review the PowerShell scripts before installation, test first on non-sensitive systems, and keep a documented way to disable or remove the scheduled tasks. <br>
Risk: The repair workflow is described as having broad authority to stop, edit, disable, restart, and send alerts externally. <br>
Mitigation: Use limited credentials, scope file and process permissions narrowly, and confirm exactly what actions the installed scripts can perform. <br>
Risk: Environment files hold API keys and Telegram alert credentials. <br>
Mitigation: Restrict permissions on the environment file, use least-privilege tokens, and avoid placing secrets on shared or high-sensitivity machines. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aichiafranco/windows-healing-gateway) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with PowerShell command snippets and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Targets Windows 10/11, PowerShell 5.1+, OpenClaw CLI, Task Scheduler access, and environment-file based credential configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
