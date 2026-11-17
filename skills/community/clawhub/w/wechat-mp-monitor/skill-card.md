## Description:

Fetch and summarize supplied WeChat MP article URLs, maintain a local watchlist, and send Feishu/Lark notifications while account monitoring remains demo-level.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[lwd815813](https://clawhub.ai/user/lwd815813)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to fetch summaries for WeChat MP articles, maintain a watchlist, and configure Feishu/Lark alerts while evaluating whether the demo account-checking behavior fits their workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches user-supplied article URLs and the security review flags unrestricted URL fetching.

Mitigation: Run it in an isolated environment and provide only trusted WeChat article URLs.

Risk: Webhook values and article history may be stored in local plaintext files.

Mitigation: Prefer the FEISHU_WEBHOOK environment variable, avoid the command-line webhook option, and review or delete ~/.wechat_mp_monitor when it may contain sensitive data.

Risk: The release overstates account monitoring because check-all is demo-level and requires an RSS or search API source.

Mitigation: Treat account monitoring as demonstration functionality and verify behavior manually before relying on scheduled checks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lwd815813/skills/wechat-mp-monitor)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local watchlist and history files under ~/.wechat_mp_monitor and can send Feishu/Lark webhook notifications when configured.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
