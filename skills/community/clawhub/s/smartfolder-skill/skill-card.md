## Description:

SmartFolder helps agents organize, analyze, and clean local files with commands for categorization, duplicate detection, disk usage analysis, and cleanup workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zaosusu](https://clawhub.ai/user/zaosusu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide local folder organization, duplicate-file review, disk usage analysis, and file cleanup tasks. It is most useful when an agent needs to propose or run scoped file-management commands with preview-first handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can move files during organization workflows.

Mitigation: Use dry-run mode first, run only on small explicitly chosen folders, and review planned moves before execution.

Risk: Duplicate detection and disk analysis can recursively scan sensitive folders more broadly than intended.

Mitigation: Avoid scanning the whole home directory or system locations; choose narrow target directories for each run.

Risk: The dependency list includes an unnecessary pathlib package for modern Python versions.

Mitigation: Review or remove the dependency before installation in managed environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zaosusu/skills/smartfolder-skill)
- [OpenClaw](https://openclaw.ai)
- [Artifact README](artifact/README.md)
- [Artifact skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include local Python commands that scan or move files when the user chooses to execute them.]

## Skill Version(s):

0.1.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
