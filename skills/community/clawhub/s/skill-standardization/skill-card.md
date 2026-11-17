## Description:

Audits, creates, updates, refactors, versions, and reviews agent skills against R-01 to R-26 standardization rules, including permission scanning and data-directory compliance checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ldxs001](https://clawhub.ai/user/ldxs001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to audit and standardize agent skill packages before release or during maintenance. It helps review structure, metadata, permissions, changelogs, reference documentation, and supported create/update/refactor workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents through repeated file modifications and fix loops on target skills.

Mitigation: Start with read-only audit modes, review planned changes before allowing update or refactor workflows, and keep an external backup of target skill directories.

Risk: Cleanup and reporting behavior may affect files or generated reports in ways that are not fully disclosed to the user.

Mitigation: Review deletion targets and generated report paths before running cleanup, update, refactor, or automatic fix operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ldxs001/skills/skill-standardization)
- [Publisher profile](https://clawhub.ai/user/ldxs001)
- [SKILL.md](artifact/SKILL.md)
- [Usage guide](artifact/references/guide.md)
- [Audit rules](artifact/references/rules.md)
- [Permissions and testing](artifact/references/permissions.md)
- [Architecture](artifact/references/architecture.md)
- [Changelog](artifact/references/changelog.md)
- [License](artifact/references/LICENSE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples, audit findings, generated or updated files, and optional JSON/HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and modify target skill files when update, refactor, cleanup, or fix workflows are used.]

## Skill Version(s):

2.103.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
