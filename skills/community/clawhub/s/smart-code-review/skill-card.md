## Description:

Code Review helps agents review code snippets, diffs, and PR changes across security, performance, maintainability, logic, and style, then produce structured findings with risk ratings and fix suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caingao](https://clawhub.ai/user/caingao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to ask an agent for full, PR, security-focused, or quick code reviews before merge or release. It is designed to surface prioritized issues and practical remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask the agent to inspect proprietary or sensitive source code and diffs.

Mitigation: Use it only with code the user is authorized to share, and keep review input within the intended agent or workspace boundary.

Risk: Generated findings and fix snippets may be incomplete or wrong even when the security scan verdict is clean.

Mitigation: Treat results as review assistance and have a developer validate security, logic, and generated fixes before merging.

Risk: The artifact is Chinese-first, which may be unsuitable for teams expecting English review output.

Mitigation: Request English output explicitly when needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/caingao/skills/smart-code-review)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown review reports with prioritized findings, summaries, and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-first output by default; users can request English output explicitly.]

## Skill Version(s):

1.0.0 (source: server release metadata, OpenClaw metadata, README)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
