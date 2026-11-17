## Description:

Backs up and restores AI assistant state through Feishu documents, including memory, identity, user preferences, behavior guidance, email configuration, and scheduled tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bruce-zhaobo](https://clawhub.ai/user/bruce-zhaobo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to back up an AI assistant's working state to Feishu, trigger manual or scheduled backups, and recover the assistant state after reinstalling or switching devices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may collect and restore highly sensitive assistant state, email configuration, and scheduled tasks.

Mitigation: Remove .msmtprc and unrelated cron data from the backup scope before use, and require explicit approval for each restore target.

Risk: Restoring behavior-rule files or cron entries from a Feishu document can reintroduce untrusted state.

Mitigation: Verify the provenance and contents of the Feishu document before restoring cron jobs or behavior-rule files.

## Reference(s):

- [Recovery Guide](references/recovery-guide.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python scripts and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local backup content, pending-sync markers, and recovery instructions for Feishu-backed assistant state.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
