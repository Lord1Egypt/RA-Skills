## Description:

StockEarning helps agents query stock market data, review portfolio performance, and record stock trades through the StockEarning REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hareluya](https://clawhub.ai/user/hareluya)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use StockEarning to connect an AI assistant to mystockearning.cn for stock lookup, portfolio summaries, profit/loss review, broker fee checks, and user-confirmed trade record updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change financial account records by creating trade records or editing position quantities.

Mitigation: Review every trade or position-adjustment confirmation carefully before allowing write actions, and verify portfolio data after corrections.

Risk: The skill handles an API key, portfolio data, and transaction payloads, and the security evidence flags unsafe shell handling around credentials and transaction data.

Mitigation: Use a least-privilege API key when available, keep the API-key file private with restrictive permissions, and prefer a version that parses credentials safely and serializes JSON with a proper encoder.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hareluya/skills/secn)
- [StockEarning Website](https://www.mystockearning.cn)
- [Root Skill Instructions](artifact/SKILL.md)
- [Plugin Manifest](artifact/plugin.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries and tables, with shell commands and JSON API responses when scripts are run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke HTTPS REST API calls requiring STOCK_API_KEY; trade and position changes require explicit user confirmation.]

## Skill Version(s):

1.0.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
