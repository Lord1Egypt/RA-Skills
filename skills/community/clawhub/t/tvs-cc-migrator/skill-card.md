## Description: <br>
Backs up, packages, and helps restore Claude Code configuration from ~/.claude, including rules, skills, commands, agents, plugins, and settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[inksnowhailong](https://clawhub.ai/user/inksnowhailong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Claude Code users use this skill to scan local Claude Code configuration, create a portable backup, and restore selected configuration on another machine. The workflow is most relevant when changing computers, exporting settings, or recovering a Claude Code setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backup archives may include sensitive Claude Code settings or local configuration. <br>
Mitigation: Prefer clearing sensitive settings fields before backup, keep generated archives private, and review backup contents before sharing or restoring them. <br>
Risk: Restore instructions may execute reinstall commands supplied by a backup manifest. <br>
Mitigation: Only restore from trusted backups and review manifest-provided reinstall commands before approving execution. <br>


## Reference(s): <br>
- [Restore Guide](artifact/RESTORE_GUIDE.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/inksnowhailong/tvs-cc-migrator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON backup manifests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces backup archives and manifest-driven restore instructions for Claude Code configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
