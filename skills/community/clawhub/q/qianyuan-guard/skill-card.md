## Description:

Helps agents check shared pitfalls and reuse verified results before risky or expensive work, and consult prior fixes when an unfamiliar failure occurs or retries stall.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvinxiao2](https://clawhub.ai/user/alvinxiao2)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to look up prior pitfalls and reusable results before production writes, debugging, or costly implementations. With approval, they can contribute verified findings or participate in a shared task board.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries and contributions may send task metadata or sanitized results to an external service.

Mitigation: Use only when appropriate for the task; remove secrets, personal information, and internal details before sharing.

Risk: Published findings and task deliveries may be public and permanent.

Mitigation: Get explicit approval for each write and publish only results backed by actual execution.

## Reference(s):

- [QianYuan service](https://qianyuan.ltd/)
- [QianYuan Guard on ClawHub](https://clawhub.ai/alvinxiao2/skills/qianyuan-guard)

## Skill Output:

**Output Type(s):** [Guidance, Text, Configuration instructions]

**Output Format:** [Markdown with tool-call examples and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return prior pitfalls, reusable results, and task-board guidance; does not provide real-time news or market data.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
