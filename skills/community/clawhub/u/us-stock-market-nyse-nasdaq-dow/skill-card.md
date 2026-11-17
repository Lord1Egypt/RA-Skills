## Description:

Get US stock market data (NYSE, NASDAQ, and major indices) via FinanceAgent on OneKey Gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to query US stock market symbols through the OneKey Gateway and receive stock quote responses for NYSE, NASDAQ, DOW, and major-index workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing an unpinned npm gateway package, especially globally, can introduce unexpected package changes.

Mitigation: Review the provider and npm package before installing, prefer a pinned project-local package version, and avoid global installation when possible.

Risk: Verbose curl examples that include X-OneKey can expose DEEPNLP_ONEKEY_ROUTER_ACCESS in logs or screenshots.

Mitigation: Remove curl -v when using the access key, keep the key out of logs and screenshots, and rotate the key if it was ever captured.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ai-hub-admin/skills/us-stock-market-nyse-nasdaq-dow)
- [DeepNLP OneKey Agent Router endpoint](https://agent.deepnlp.org/agent_router)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration instructions]

**Output Format:** [JSON responses with Markdown usage examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DEEPNLP_ONEKEY_ROUTER_ACCESS and a symbol_list array of US stock tickers.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
