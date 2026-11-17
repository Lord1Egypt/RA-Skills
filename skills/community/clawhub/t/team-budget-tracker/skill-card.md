## Description:

团队预算管理工具 - 帮助小型团队规划和追踪项目预算。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuhaichao87](https://clawhub.ai/user/wuhaichao87)

### License/Terms of Use:

MIT-0

## Use Case:

Small team members and project leads use this skill to create project budgets, allocate category amounts, track spending against plan, receive overspend warnings, and prepare monthly or quarterly budget reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release declares an install-time shell command for an installer file that is not included in the artifact.

Mitigation: Review installation before use and prefer a release that removes the lifecycle script or includes a clearly documented, narrowly scoped installer.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wuhaichao87/skills/team-budget-tracker)
- [README](README.md)
- [Guide](GUIDE.md)
- [Changelog](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance, shell commands]

**Output Format:** [Markdown with budget structures, report text, configuration references, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses bash for installation according to release metadata and package scripts.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter, CHANGELOG.md, and package.json report 0.9.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
