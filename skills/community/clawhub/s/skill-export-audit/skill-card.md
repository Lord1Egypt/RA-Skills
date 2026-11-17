## Description:

Use before ClawHub export: audit skill, fix local + public.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blueboyzx](https://clawhub.ai/user/blueboyzx)

### License/Terms of Use:

MIT-0

## Use Case:

Skill authors use it to audit a local skill before ClawHub export, verify its content and metadata, and ensure both local and published copies are correct.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan is partial and flags instructions to run bundled scripts on real inputs before review.

Mitigation: Review scripts first, then use a disposable, restricted environment with synthetic or sanitized inputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/blueboyzx/skills/skill-export-audit)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.2.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
