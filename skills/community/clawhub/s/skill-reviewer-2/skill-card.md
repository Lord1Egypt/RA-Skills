## Description:

Skill Reviewer audits agent skill quality against Anthropic guidance, checking structure, YAML front matter, description quality, organization, examples, execution readiness, and improvement opportunities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[binbin1213](https://clawhub.ai/user/binbin1213)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this skill to review skills before publishing or sharing. It produces structured audit reports, scoring, defect checks, and improvement suggestions for skill quality.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An unpinned third-party install command could execute changing remote code before a review.

Mitigation: Review local supplied skill files by default; if installation is necessary, use a pinned and verified installer in a disposable sandbox with explicit approval.

## Reference(s):

- [Skill Reviewer on ClawHub](https://clawhub.ai/binbin1213/skills/skill-reviewer-2)
- [Skill Review Checklist](references/checklist.md)
- [Anthropic Skills Development Guide Summary](references/official-guide-summary.md)
- [Anthropic Skills Development Guide](references/anthropic-skills-development-guide.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance, Shell commands]

**Output Format:** [Markdown review reports with scoring tables, defect lists, examples, and improvement guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include suggested shell commands for local inspection; commands should be reviewed before execution.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
