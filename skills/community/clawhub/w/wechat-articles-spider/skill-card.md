## Description: <br>
WeChat Official Account article crawler with x402 micropayments. Requires Chrome browser and interactive WeChat QR login on first use. Harvest articles for research and analysis with pay-as-you-go Base USDC pricing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kehongpeng](https://clawhub.ai/user/kehongpeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to collect WeChat Official Account article titles, links, publish times, account history, and keyword-ranked article results for monitoring, research, archiving, and reporting workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores reusable WeChat session credentials locally. <br>
Mitigation: Use a dedicated WeChat account, keep credential files out of version control, restrict local file permissions, and delete credentials after use. <br>
Risk: Paid x402 flows depend on the configured receiving address and payment verification settings. <br>
Mitigation: Review the receiving address before sending funds and enable on-chain verification before relying on paid crawls. <br>
Risk: Automated WeChat crawling can trigger account restrictions or bans. <br>
Mitigation: Use a secondary account, avoid VPN-related login failures, keep crawl volume low, and respect the built-in rate limits. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kehongpeng/wechat-articles-spider) <br>
- [Publisher profile](https://clawhub.ai/user/kehongpeng) <br>
- [Google Chrome download](https://www.google.com/chrome/) <br>
- [WeChat Official Accounts Platform](https://mp.weixin.qq.com/) <br>
- [BaseScan](https://basescan.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with inline shell commands; crawler runs can produce local Excel, JSON, and article-link data files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3, Google Chrome, USER_ID, interactive WeChat QR login, and optional Base payment verification settings.] <br>

## Skill Version(s): <br>
2.0.4 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
