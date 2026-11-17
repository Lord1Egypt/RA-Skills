## Description:

Pre-release safety and scope checker for skills, repos, and export bundles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lethehades](https://clawhub.ai/user/lethehades)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release maintainers use this skill to inspect skill folders, repositories, or export bundles before publishing. It produces readiness decisions, findings, suggested exclusions, minimal publish surface guidance, identity leakage review, and action hints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner reads files in the target path, and the security review notes it can follow symlinks and read outside the selected folder.

Mitigation: Run it only on trusted, narrow target directories until symlink rejection, resolved-path containment checks, regular-file validation, and file-size limits are added.

## Reference(s):

- [Export Safety](references/export-safety.md)
- [Release Minimal](references/release-minimal.md)
- [Report Format](references/report-format.md)
- [Rules](references/rules.md)
- [Target Types](references/target-types.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style text report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports can include a readiness decision, blocking issues, warnings, suggested exclusions, minimal publish surface, identity leakage review, and action hints.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
