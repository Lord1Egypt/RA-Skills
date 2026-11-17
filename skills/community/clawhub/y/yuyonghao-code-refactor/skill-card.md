## Description:

Analyzes JavaScript code quality issues and produces refactoring plans, previews, file changes, validation results, and rollback-aware reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to inspect JavaScript files for code smells, generate refactoring plans, preview diffs, apply supported changes, and validate results with tests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify files in the workspace.

Mitigation: Use dry-run mode first, inspect generated diffs, keep backups enabled, and apply changes only in trusted workspaces.

Risk: The validation flow can run caller-configured shell commands.

Mitigation: Use known-safe test commands and avoid running the skill against untrusted repositories until workspace path limits and safer test execution are enforced.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yuyonghao-123/skills/yuyonghao-code-refactor)
- [Publisher Profile](https://clawhub.ai/user/yuyonghao-123)
- [Artifact Skill Documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON analysis results, Markdown reports, JavaScript code changes, diffs, and CLI output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports dry-run previews, optional application of changes, backups, rollback, and caller-configured validation commands.]

## Skill Version(s):

0.1.0 (source: release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
