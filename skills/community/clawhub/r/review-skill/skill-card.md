## Description:

Reviews PRs that add or modify Agent Skills for structural validity, design quality, and marketplace consistency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and marketplace reviewers use this skill to review pull requests that add or modify Agent Skills, producing severity-calibrated findings for structural validity, design quality, and marketplace consistency.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Caller-controlled branch arguments and output paths can create unsafe command execution or file overwrite behavior in an untrusted harness.

Mitigation: Use only in controlled review environments, validate git refs before command construction, restrict output paths to a safe workspace directory, and avoid overwriting existing files without explicit approval.

Risk: Automated review findings may be incorrect if the reviewer relies on diffs or partial context.

Mitigation: Require full skill-file reads, line-specific evidence, and human review of Critical and Major findings before acting on the verdict.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anderskev/skills/review-skill)
- [Publisher profile](https://clawhub.ai/user/anderskev)
- [Structural checks](references/structural-checks.md)
- [Design checks](references/design-checks.md)
- [Marketplace checks](references/marketplace-checks.md)

## Skill Output:

**Output Type(s):** [markdown, guidance, shell commands]

**Output Format:** [Markdown review report with severity sections, file-line findings, confidence labels, and readiness verdict.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Structured findings are written to the caller-provided output path.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
