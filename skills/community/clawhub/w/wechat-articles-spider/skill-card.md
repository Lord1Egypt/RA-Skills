## Description:

WeChat Official Account article crawler with x402 micropayments. Requires Chrome browser and interactive WeChat QR login on first use. Harvest articles for research and analysis with pay-as-you-go Base USDC pricing.

This skill is for research and development only.

## Publisher:

[kehongpeng](https://clawhub.ai/user/kehongpeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to crawl WeChat Official Account article titles, URLs, publish times, account histories, and keyword-ranked article sets for monitoring, archiving, and content analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid Base USDC flows may involve real funds while the security evidence flags payment verification as unsafe.

Mitigation: Use the free tier or testnet first, and do not run paid mainnet USDC flows unless the payment verification bugs are fixed.

Risk: WeChat session credentials are stored locally in weixin_credentials.py.

Mitigation: Treat weixin_credentials.py like a password, protect or remove it when not needed, and use a secondary WeChat account.

Risk: Automated WeChat crawling can expose the user account to platform enforcement or blocking.

Mitigation: Use a secondary account, reduce crawl frequency, avoid concurrent crawls, and review WeChat platform terms before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kehongpeng/skills/wechat-articles-spider)
- [WeChat Official Accounts Platform](https://mp.weixin.qq.com/)
- [Google Chrome](https://www.google.com/chrome/)
- [BaseScan](https://basescan.org)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; crawler runs may create local Excel and JSON output files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3, Google Chrome, USER_ID, interactive WeChat QR login, and local credential and queue storage.]

## Skill Version(s):

2.0.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
