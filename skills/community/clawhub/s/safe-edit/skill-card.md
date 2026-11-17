## Description:

Safe Edit helps agents back up configuration files and schedule a 15-minute rollback before risky configuration changes across Linux, macOS, FreeBSD, and Windows shell environments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ijevin](https://clawhub.ai/user/ijevin)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use Safe Edit when an agent needs to modify important configuration files and should create a backup plus a timed rollback before making changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make high-impact changes to system or application configuration files and schedules rollback code.

Mitigation: Review the skill before installation and require clear confirmation before using it on privileged or production file targets.

Risk: Rollback behavior depends on packaged scripts, platform schedulers, and operation-scoped state being correct.

Mitigation: Verify the rollback script and packaging, make scheduler or package installation steps explicit, and scope scheduler state per operation before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ijevin/skills/safe-edit)
- [Publisher profile](https://clawhub.ai/user/ijevin)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct execution of the bundled safe-edit shell script to back up files, schedule rollback, confirm success, cancel rollback, or report status.]

## Skill Version(s):

1.0.0 (source: package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
