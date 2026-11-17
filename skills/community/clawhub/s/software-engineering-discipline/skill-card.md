## Description:

Engineering discipline for AI coding agents working on maintained code, covering feature work, bug fixes, refactoring, code review, test strategy, scoped trade-offs, verified APIs, and executed checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wujiaming88](https://clawhub.ai/user/wujiaming88)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to guide AI coding agents during feature implementation, bug fixing, refactoring, review, and test planning. It emphasizes contract awareness, bounded scope, verified APIs, risk-based tests, and honest handoff evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make agents spend more effort reading code, verifying APIs, and reporting test evidence before claiming work is done.

Mitigation: Use it when stricter coding-agent discipline is desired and expect the additional verification work as part of normal operation.

Risk: Guidance-only skills can still lead to incorrect or misleading engineering recommendations if the agent applies them without checking the repository context.

Mitigation: Review the agent's proposed changes and require executed checks or clearly labeled blockers before accepting implementation claims.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/wujiaming88/skills/tree/main/software-engineering-discipline)
- [ClawHub skill page](https://clawhub.ai/wujiaming88/skills/software-engineering-discipline)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown or plain text with code and shell command blocks when implementation or review work requires them]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should report verification evidence, remaining risks, and any unverified assumptions.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
