## Description: <br>
Automated backup, integrity monitoring, and self-healing for AI agent workspaces. Detects unexpected changes, creates automatic backups, self-heals from corruption. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheShadowRose](https://clawhub.ai/user/TheShadowRose) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agent operators, and AI agent users use Sentinel to monitor important workspace files, create local backups, detect file-level corruption, and restore selected state or configuration files after accidental changes or data loss. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic restore can overwrite current agent memory, configuration, or state. <br>
Mitigation: Keep WORKSPACE_ROOT and CRITICAL_FILES narrowly scoped, store backups in a protected location, and disable or avoid automatic restore until the baseline is trusted. <br>
Risk: Backups are local copies and may be stored as plain files. <br>
Mitigation: Use protected backup directories and disk encryption for sensitive state, and pair Sentinel with separate off-site backup if disaster recovery is required. <br>
Risk: Sentinel detects file-level corruption and hash changes, not semantic or schema-level mistakes. <br>
Mitigation: Use application-level validation for critical structured files before treating a restored or unchanged file as correct. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TheShadowRose/sentinel) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/TheShadowRose) <br>
- [README.md](artifact/README.md) <br>
- [LIMITATIONS.md](artifact/LIMITATIONS.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Code, Guidance, Markdown] <br>
**Output Format:** [Markdown with Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local file-monitoring, backup, manifest, and restore guidance for user-configured workspaces.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
