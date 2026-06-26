## Description: <br>
Polymarket sports prediction markets for live odds, prices, order books, events, series, and market search across major sports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[antonelli182](https://clawhub.ai/user/antonelli182) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to look up Polymarket sports prediction markets, compare implied probabilities, inspect current prices and order books, and find relevant event or market identifiers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet-enabled trading commands can place or cancel orders when the optional trading dependency and private key are configured. <br>
Mitigation: Use read-only market lookup commands by default; require explicit user confirmation for each market, side, amount, price, and order type before any trading action. <br>
Risk: Supplying POLYMARKET_PRIVATE_KEY gives the agent access to wallet-backed trading operations. <br>
Mitigation: Do not provide POLYMARKET_PRIVATE_KEY unless trading is intentionally enabled, and keep private keys out of shared logs, prompts, and files. <br>
Risk: Using a market_id where a CLOB token_id is required can return errors or incorrect price/order book lookups. <br>
Mitigation: Call get_market_details first and use clobTokenIds for price, order book, price history, and last trade queries. <br>


## Reference(s): <br>
- [Polymarket API Reference](references/api-reference.md) <br>
- [Polymarket APIs](references/api.md) <br>
- [Valid Commands and Common Mistakes](references/commands.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/antonelli182/sports-skills-polymarket) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured market summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read commands need no authentication; trading actions require an optional dependency and a configured wallet.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
