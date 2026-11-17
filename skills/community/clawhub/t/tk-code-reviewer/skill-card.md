## Description:

Automated code review for security vulnerabilities, performance issues, best practices, refactoring suggestions, documentation gaps, and PR-ready review comments across common programming languages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tktk-ai](https://clawhub.ai/user/tktk-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineering teams, maintainers, agencies, and students use this skill to review code or pull request diffs for security, performance, style, complexity, refactoring, and documentation issues before merge or handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reviewing pasted code or file paths may expose sensitive source content to the active AI agent.

Mitigation: Use approved agent environments for proprietary code, avoid submitting secrets or credentials, and review only the minimum code needed for the task.

Risk: AI-generated review comments or corrected code may be incomplete or incorrect for the project context.

Mitigation: Treat findings and fixes as review proposals, then validate them with project tests, security review, and maintainer judgment before merging.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tktk-ai/skills/tk-code-reviewer)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Guidance]

**Output Format:** [Markdown code review report with issue severity, category, location, remediation guidance, optional corrected code, and PR-ready comments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include an overall score, issue counts, positive observations, and before/after code snippets when requested.]

## Skill Version(s):

1.0.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
