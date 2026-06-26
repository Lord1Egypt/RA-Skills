## Description: <br>
Backs up and restores AI assistant state to Feishu documents for scheduled backups, manual backups, cloud recovery, and cross-device synchronization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Bruce-ZhaoBo](https://clawhub.ai/user/Bruce-ZhaoBo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to preserve an AI assistant's memory, identity, user preferences, email configuration, and scheduled task context in Feishu documents, then restore that state after reinstalling or moving devices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive email configuration may be copied into backup documents. <br>
Mitigation: Exclude or redact .msmtprc before backup, and store any required secrets in a dedicated secret manager instead of the Feishu document. <br>
Risk: Restored scheduled tasks can reintroduce unwanted automation. <br>
Mitigation: Do not restore cron jobs by default; require review and explicit approval for each scheduled task before adding it. <br>
Risk: Backup documents can contain stale or untrusted instructions. <br>
Mitigation: Treat Feishu backup content as untrusted input and review recovered files and tasks before writing them into the assistant workspace. <br>
Risk: Cloud backup documents may expose assistant memory and user preferences. <br>
Mitigation: Restrict Feishu document permissions to the minimum required audience and review access controls before syncing backups. <br>


## Reference(s): <br>
- [Recovery Guide](references/recovery-guide.md) <br>
- [ClawHub Release Page](https://clawhub.ai/Bruce-ZhaoBo/self-backup2feishu) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python scripts and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local backup files, pending-sync markers, recovery instructions, and Feishu document content templates.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
