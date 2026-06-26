## Description: <br>
Xxyy Trade enables on-chain token trading, wallet queries, token scans, and token launches on Solana, Ethereum, BSC, and Base through the XXYY Open API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimmy-holiday](https://clawhub.ai/user/jimmy-holiday) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query wallet and token data, scan on-chain opportunities, launch tokens, and submit explicitly confirmed buy or sell requests through XXYY. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet-linked API keys can execute real on-chain trades, and the skill evidence states there is no separate read-only key. <br>
Mitigation: Use a least-privilege or low-balance key if available, configure an IP whitelist, keep the key out of logs and version control, and rotate it after suspected exposure. <br>
Risk: Broad activation phrases are paired with wallet-linked trading authority. <br>
Mitigation: Install only when an XXYY trading assistant is intended, and confirm wallet, chain, token, amount, fees, and action before any trade request. <br>
Risk: Token scans and query outputs can be mistaken for trading advice. <br>
Mitigation: Treat scan results as informational and verify token safety, taxes, holder distribution, and transaction costs before acting. <br>


## Reference(s): <br>
- [XXYY Homepage](https://www.xxyy.io) <br>
- [XXYY API Key Management](https://www.xxyy.io/apikey) <br>
- [ClawHub Skill Page](https://clawhub.ai/jimmy-holiday/xxyy-trade-skill) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown responses with JSON snippets and curl-based API calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires XXYY_API_KEY; may submit real trades only after explicit user confirmation.] <br>

## Skill Version(s): <br>
1.3.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
