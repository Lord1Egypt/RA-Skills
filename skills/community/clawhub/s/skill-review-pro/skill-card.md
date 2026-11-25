## Description:

Reviews agent skills through static analysis, type-aware policies, scoring, adversarial checks, and actionable improvement guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[z-zihan](https://clawhub.ai/user/z-zihan)

### License/Terms of Use:

MIT-0

## Use Case:

Skill authors and reviewers use it to assess skill quality, produce scored review reports, and plan improvements. It also supports repository audits and read-only ClawHub release checks when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security review reports a benign result with medium confidence and partial scanner coverage.

Mitigation: Review the skill files and their behavior before installation; treat the scanner result as limited coverage.

Risk: Unpinned package references may change over time.

Mitigation: Review package sources and versions before using the related checks.

Risk: The remote CI rerun option can trigger a remote workflow.

Mitigation: Confirm the target workflow and intended retry before initiating a rerun.

Risk: Generic fix triggers could activate outside a skill review.

Mitigation: Confirm the target skill and requested fix action before applying changes.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/z-zihan/skills/skill-review-pro)
- [Project homepage](https://github.com/z-Zihan/awesome-skills)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance, Files]

**Output Format:** [Markdown review reports, scores, recommendations, and structured checklists; optional user-confirmed skill-file edits.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese or English, following the user's language.]

## Skill Version(s):

2.3.2 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
