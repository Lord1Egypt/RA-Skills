## Description:

Pre-execution security layer for AI agents that checks tool calls before execution and monitors tool results for threats across OpenClaw and Claude Code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wow-leeroy-jenkins05](https://clawhub.ai/user/wow-leeroy-jenkins05)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add pre-execution checks and post-execution monitoring for dangerous tool calls, prompt injection patterns, out-of-scope writes, runaway loops, and data exfiltration indicators.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad monitoring over every agent tool call and depends on local Shoofly binaries.

Mitigation: Review and trust the binaries in ~/.shoofly/bin before enabling the skill, and deploy it only when session-wide monitoring is intended.

Risk: Tool activity may be logged or forwarded through external notification channels.

Mitigation: Disable or tightly control notification channels and confirm logs are redacted and retained according to local policy.

Risk: The checker fails open when unavailable or slow.

Mitigation: Treat Shoofly as an advisory layer, monitor checker availability, and keep independent safeguards for high-risk tool execution.

## Reference(s):

- [Shoofly Advanced on ClawHub](https://clawhub.ai/wow-leeroy-jenkins05/skills/shoofly-advanced)
- [wow-leeroy-jenkins05 ClawHub publisher profile](https://clawhub.ai/user/wow-leeroy-jenkins05)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSONL log examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires locally installed Shoofly binaries and uses jq and curl when available.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
