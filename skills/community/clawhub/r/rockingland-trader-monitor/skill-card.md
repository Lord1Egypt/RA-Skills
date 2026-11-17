## Description:

Monitors a configured Xiaohongshu (RedNote) user's latest posts for target keywords and sends WeChat notifications when matching posts appear.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shawntribbiani](https://clawhub.ai/user/shawntribbiani)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure keyword-based monitoring for a Xiaohongshu account and receive WeChat alerts when matching posts appear. It is suited to periodic checks of trader or seller updates after the user supplies their own account credentials and target keywords.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses authenticated Xiaohongshu session cookies and account tokens.

Mitigation: Store cookies in a private user-owned directory, treat them like passwords, and rotate or remove them when no longer needed.

Risk: The local MCP service exposes account-control capabilities on port 18060.

Mitigation: Run only on a trusted single-user machine, keep the service bound to loopback, do not expose the port, and stop the service after checks complete.

Risk: The monitoring helper depends on downloaded Xiaohongshu MCP binaries.

Mitigation: Download binaries only from the expected release source and verify their integrity before use.

Risk: The security evidence reports broader authenticated account-control capabilities beyond monitoring.

Mitigation: Prefer a constrained deployment that removes write, publish, like, favorite, and comment tools when only monitoring is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shawntribbiani/skills/rockingland-trader-monitor)
- [Publisher profile](https://clawhub.ai/user/shawntribbiani)
- [xiaohongshu-mcp GitHub releases](https://github.com/xpzouying/xiaohongshu-mcp/releases)
- [Trader monitoring rules](artifact/trader_rules.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided Xiaohongshu cookies, a target user ID, an xsec_token, keyword settings, and a WeChat target ID; produces local state and log files during monitoring.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
