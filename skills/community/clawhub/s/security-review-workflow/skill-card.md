## Description:

Use when the current branch or PR needs a focused security review that minimizes false positives and only reports concrete, exploit-relevant issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wimi321](https://clawhub.ai/user/wimi321)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review branch or pull-request diffs for concrete, exploit-relevant security issues while filtering out low-confidence noise.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow causes the agent to inspect repository diffs and related code context.

Mitigation: Use it only in repositories where agent access to that code context is acceptable.

Risk: Security review output can be incomplete or incorrect if relevant context is missing.

Mitigation: Have a human reviewer confirm reported findings and assess whether additional review is needed before relying on the results.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wimi321/skills/security-review-workflow)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown security findings with severity, exploit path, and fix recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [High-signal findings only; speculative or general code review comments are filtered out.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
