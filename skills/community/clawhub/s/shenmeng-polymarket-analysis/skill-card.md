## Description: <br>
Analyzes Polymarket prediction market data by fetching market listings, odds, volume, liquidity, and sentiment signals to generate structured analysis reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenmeng](https://clawhub.ai/user/shenmeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to inspect Polymarket markets, identify popular categories, compare odds, volume, and liquidity, and produce a concise market analysis report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled analysis script can contact SkillPay and attempt a 0.001 USDT charge when it runs. <br>
Mitigation: Review before installing; remove or disable billing credentials, separate billing from analysis, or require explicit confirmation before any charge. <br>
Risk: The skill has a suspicious security verdict because billing can be attempted without explicit confirmation. <br>
Mitigation: Use only if the SkillPay integration is acceptable for the deployment environment and users understand the billing behavior. <br>


## Reference(s): <br>
- [Polymarket Gamma API](https://gamma.polymarket.com) <br>
- [Polymarket CLOB API](https://clob.polymarket.com) <br>
- [Polymarket Leaderboard](https://polymarket.com/leaderboard) <br>
- [Polymarket Predictions](https://polymarket.com/predictions) <br>
- [SkillPay](https://skillpay.me) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style analysis reports and terminal text output; market detail mode can emit JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include market overviews, category highlights, detailed market data, risk notes, and user-oriented suggestions.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
