## Description:

AI Token消耗监控优化工具，面向QClaw/OpenClaw用户读取会话日志、统计Token消耗、检测异常模式、提供优化建议并生成消耗趋势报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QClaw/OpenClaw users use this skill to review local session log token consumption, identify abnormal spikes or repeated failures, and receive concise optimization guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local QClaw/OpenClaw session logs, which may contain sensitive usage context.

Mitigation: Install and run it only when local session-log access is acceptable for the environment.

Risk: The documented token_stats.py helper script is referenced by commands but is not included in the reviewed artifact.

Mitigation: Inspect the actual local helper script before executing the example commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/qclaw-token-monitor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks and tabular token-usage summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference generated local token-usage JSON files and local session-log paths.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
