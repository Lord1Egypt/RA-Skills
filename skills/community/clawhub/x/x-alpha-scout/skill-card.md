## Description: <br>
X/Twitter alpha scanner for crypto and NFTs, used for daily alpha reports and on-demand token, NFT, or project sentiment analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hammadbtc](https://clawhub.ai/user/hammadbtc) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agents use this skill to scan X/Twitter for crypto and NFT market signals, generate daily alpha reports, and summarize on-demand sentiment and red flags for a specific asset. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent and bird CLI to use sensitive X/Twitter session credentials. <br>
Mitigation: Use a dedicated low-risk X account, store X_AUTH_TOKEN and X_CT0 in a secret manager or secure environment, avoid pasting or logging them, and rotate them if exposed. <br>
Risk: Reports may be delivered to external channels such as Discord or Telegram. <br>
Mitigation: Confirm the destination before enabling delivery and review reports before sharing them outside the agent session. <br>
Risk: Crypto and NFT alpha reports can be speculative or misleading if treated as investment advice. <br>
Mitigation: Treat outputs as research notes, verify claims against primary sources, and keep NFA/DYOR disclaimers visible in generated reports. <br>


## Reference(s): <br>
- [X Alpha Scout on ClawHub](https://clawhub.ai/hammadbtc/x-alpha-scout) <br>
- [bird releases](https://github.com/steipete/bird/releases) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports and short-form text analysis with inline shell commands and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include external X/Twitter profile or status links when search results support them.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
