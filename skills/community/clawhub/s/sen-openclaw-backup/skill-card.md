## Description: <br>
Backup OpenClaw data to desktop with quick backups that exclude skills or full backups that include skills, and support scheduled automatic backups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sen-platotech](https://clawhub.ai/user/Sen-platotech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and operators use this skill to back up local OpenClaw state for safekeeping or migration, then restore that state on the same or another machine. It is intended for user-created archives that may include conversations, memory, configuration, encrypted credentials, and optionally installed skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Restore can replace active OpenClaw state and extract an unvalidated archive into the home directory. <br>
Mitigation: Use restore only with backups you created and trust, inspect archives from shared storage or other people before restoring, and keep the existing-data backup created during restore. <br>
Risk: Backups may contain sensitive credentials, conversation history, memory, and configuration data. <br>
Mitigation: Store backup archives in an encrypted or private location and limit access to trusted operators. <br>
Risk: Restore may sync skills after extraction, changing the local OpenClaw environment. <br>
Mitigation: Review restored state and synced skills before using the restored OpenClaw installation for sensitive work. <br>


## Reference(s): <br>
- [ClawHub listing for OpenClaw Backup](https://clawhub.ai/Sen-platotech/sen-openclaw-backup) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration guidance] <br>
**Output Format:** [Markdown with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local backup archive paths and environment variables such as INCLUDE_SKILLS.] <br>

## Skill Version(s): <br>
1.1.2 (source: ClawHub release evidence; artifact frontmatter reports 1.1.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
