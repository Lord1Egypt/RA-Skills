## Description:

Skill Release Audit is a pre-publish quality and safety auditor for AI agent skills that runs static checks for syntax, feature coverage, edge cases, data safety, dependencies, and documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songhonglei](https://clawhub.ai/user/songhonglei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use this skill as a final local release gate before publishing or updating agent skills. It reports machine-checkable quality, safety, dependency, metadata, and documentation issues without editing files or publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional --auto-install mode can change the active Python environment and may fetch dependencies for the skill being audited.

Mitigation: Use the default report-only mode for untrusted skills, and enable --auto-install only after explicitly consenting to dependency installation.

Risk: Audit findings and suggested fixes can be wrong or incomplete for a specific release context.

Mitigation: Review the full report before changing files; the skill's documented behavior requires explicit user confirmation before edits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/songhonglei/skills/skill-release-audit)
- [Dependency Detection Patterns](references/dep-patterns.md)
- [Skill Registry / Hub Specifications](references/hub-specs.md)
- [Safe Data Path Guidelines for Skills](references/safe-paths.md)

## Skill Output:

**Output Type(s):** [analysis, markdown, JSON, shell commands, guidance]

**Output Format:** [Structured console or JSON report with suggested fixes and optional Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default mode is report-only; --format json emits machine-readable evidence, and fixes require explicit user confirmation.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
