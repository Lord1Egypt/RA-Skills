## Description:

Queries real-time stock and market-index quotes for A-shares, Hong Kong stocks, and US stocks, with batch lookups supported.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuli4](https://clawhub.ai/user/liuli4)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve current A-share, Hong Kong, US stock, and market-index quotes by code. It supports single-symbol checks and small batch comparisons for chat-based market lookup workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hong Kong quote lookups can read an Eastmoney API key from a shared local vault and run another installed skill with broad environment access.

Mitigation: Install only when the publisher, host environment, and mx-finance-data dependency are trusted; prefer a revised release that clearly discloses and scopes credentials and dependencies.

Risk: The security review verdict is suspicious because the Hong Kong stock path silently depends on local credentials and another skill.

Mitigation: Review before installing, and disable or isolate the Hong Kong lookup path unless those credential and dependency behaviors are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liuli4/skills/stock-price-query-mx)
- [Stock query API docs](references/api-docs.md)
- [Tencent Finance quote endpoint](https://qt.gtimg.cn/q={symbol})

## Skill Output:

**Output Type(s):** [text, markdown, shell commands]

**Output Format:** [JSON from the query script plus concise Markdown or plain-text quote summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-stock queries return one JSON object; batch queries return a JSON array for up to 20 symbols.]

## Skill Version(s):

1.1.4 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
