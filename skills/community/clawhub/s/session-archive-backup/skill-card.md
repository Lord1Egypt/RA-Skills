## Description: <br>
OpenClaw session reset, archive, and backup workflow that helps manage token-overrun, idle-timeout, and manual-reset scenarios with structured archives and GitHub or OneDrive backups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NevereveN619](https://clawhub.ai/user/NevereveN619) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External OpenClaw users and developers use this skill to configure session lifecycle management that archives chat history, synchronizes long-term memory, records reset activity, and backs up workspace data before token-limit, idle-timeout, or manual-reset events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist full chat history, long-term memory, and OpenClaw configuration files across sessions. <br>
Mitigation: Enable it only for data you intend to archive, add exclusions or deletion rules for secrets and personal data, and periodically review stored transcripts and memory files. <br>
Risk: Backup automation may copy sensitive workspace data to GitHub or OneDrive destinations. <br>
Mitigation: Use private or encrypted backup destinations, verify repository and OneDrive paths before use, and avoid embedding GitHub tokens in remote URLs. <br>
Risk: Generated PowerShell backup scripts can modify files and transfer data. <br>
Mitigation: Review generated scripts before execution and keep PowerShell execution policy restrictive. <br>


## Reference(s): <br>
- [Configuration Templates](references/config-templates.md) <br>
- [Troubleshooting Guide](references/troubleshooting.md) <br>
- [Workflow Diagram](references/workflow-diagram.md) <br>
- [ClawHub Release Page](https://clawhub.ai/NevereveN619/session-archive-backup) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JSON, JSONL, and PowerShell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce archive templates, HEARTBEAT.md configuration guidance, PowerShell backup script examples, status files, and troubleshooting steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
