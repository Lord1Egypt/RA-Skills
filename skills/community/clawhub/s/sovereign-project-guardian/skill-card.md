## Description:

Project health and best practices enforcer that checks security, quality, documentation, CI/CD, and dependencies, then produces a letter grade with actionable fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryudi84](https://clawhub.ai/user/ryudi84)

### License/Terms of Use:

MIT

## Use Case:

Developers and maintainers use this skill to audit repositories for project health gaps across security, quality, documentation, CI/CD, dependencies, and code hygiene. It returns a graded report and prioritized remediation plan.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may surface sensitive repository content, including secrets it detects, in the agent conversation.

Mitigation: Use it only on repositories whose contents may be reviewed in chat, and remove or rotate exposed secrets before broader sharing.

Risk: Suggested package remediation commands may change dependencies or development tooling.

Mitigation: Review generated npm, npx, or other shell commands before execution, prefer pinned versions, and keep lock files under review.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ryudi84/skills/sovereign-project-guardian)
- [Artifact README](artifact/README.md)
- [Examples](artifact/EXAMPLES.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with tables, categorized findings, and prioritized action items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes an A-F project health grade and security-first remediation priorities.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
