## Description:

Collects public Xiaohongshu post comments in paid, user-approved steps and can export the collected comments as CSV.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cuiyunhai](https://clawhub.ai/user/cuiyunhai)

### License/Terms of Use:

MIT-0

## Use Case:

Users and analysts collect public Xiaohongshu comments page by page, inspect replies and engagement, and export comments for feedback or sentiment review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default HTTP connection can expose account tokens, note links, and collected comments in transit.

Mitigation: Use a trusted HTTPS service URL before logging in and avoid insecure=true, which disables certificate verification.

Risk: Each comment page or reply expansion can consume paid credits without reliable automatic consent enforcement.

Mitigation: Show the estimated page count and credit cost, then obtain explicit user approval before every paid collection step.

Risk: Exported comments can contain identifiable nicknames and IP locations.

Mitigation: Collect only for authorized purposes; protect exported CSV files and delete them when no longer needed.

## Reference(s):

- [ClawHub skill release: xhs-comments](https://clawhub.ai/cuiyunhai/skills/xhs-comments)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, CSV files]

**Output Format:** [Step-by-step guidance and comment summaries; downloadable CSV export]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Comments may include nicknames, content, likes, IP locations, and reply counts.]

## Skill Version(s):

2.0.1 (source: release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
