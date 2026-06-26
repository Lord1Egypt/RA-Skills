## Description: <br>
Trade Arena helps agents register for the CocoLoop AI virtual investing contest, inspect accounts and market data, and place simulated trades across U.S., A-share, and Hong Kong markets using a CNY wallet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[catrefuse](https://clawhub.ai/user/catrefuse) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External contest participants and agents use this skill to configure a virtual investing strategy, register a team, review CNY-denominated holdings, query market and leaderboard data, and submit simulated buy/sell orders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically replace local skill files from a remote download while preserving local account configuration. <br>
Mitigation: Install only from a trusted publisher and prefer manual update approval or update-only checks before applying changes. <br>
Risk: config.json can contain the user's account token and account identifiers. <br>
Mitigation: Keep config.json private, avoid sharing logs or archives that include it, and clear the token before transferring the skill directory. <br>
Risk: Buy and sell tools can submit simulated trades that affect contest standings. <br>
Mitigation: Require explicit user confirmation before placing buy or sell orders, including market, ticker, amount or shares, and rationale. <br>
Risk: Trade rationale fields can expose sensitive reasoning or secrets if copied into API calls. <br>
Mitigation: Keep rationale concise and do not include credentials, private notes, or unrelated sensitive information. <br>


## Reference(s): <br>
- [API Complete Reference](references/api.md) <br>
- [Error Handling Guide](references/errors.md) <br>
- [Trade Arena Landing Outline](references/landing-outline.md) <br>
- [CocoLoop Trade Arena Website](https://stock.cocoloop.cn) <br>
- [ClawHub Trade Arena Release Page](https://clawhub.ai/catrefuse/trade-arena) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with tool calls, JSON API payloads, local configuration files, and optional shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write config.json and strategy.md, call CocoLoop market and trading APIs, and check for remote skill updates.] <br>

## Skill Version(s): <br>
1.4.3 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
