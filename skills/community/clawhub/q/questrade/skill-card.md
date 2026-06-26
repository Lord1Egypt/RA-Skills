## Description: <br>
Query a Questrade brokerage account and Canadian/US market data via the Questrade REST API for account information, balances, positions, orders, executions, activities, Level 1 quotes, historical candles, and symbol search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JoseMiguelHerrera](https://clawhub.ai/user/JoseMiguelHerrera) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent inspect Questrade account data and Canadian/US market data, including balances, positions, orders, executions, activities, quotes, candles, and symbol metadata. Users with Questrade partner API access can expose order placement and cancellation commands, which should remain under explicit human approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive Questrade account data and local token files. <br>
Mitigation: Install only when the publisher and skill are trusted, protect the local OpenClaw credential and token cache files, and revoke Questrade tokens if a shared or compromised machine may have exposed them. <br>
Risk: Order placement and cancellation commands can affect real brokerage activity when partner API access is available. <br>
Mitigation: Keep QUESTRADE_READ_ONLY=true, require explicit human approval for order changes, and do not allow an agent to run cancellation or trading commands autonomously. <br>
Risk: The --force option bypasses confirmation prompts and price-sanity checks for orders. <br>
Mitigation: Avoid --force in agent workflows and require review of order summaries before submitting any trade. <br>


## Reference(s): <br>
- [Questrade API Reference](references/api.md) <br>
- [Questrade REST API Documentation](https://www.questrade.com/api/documentation/getting-started) <br>
- [Questrade Skill on ClawHub](https://clawhub.ai/JoseMiguelHerrera/questrade) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and JSON printed by CLI commands, with setup guidance in Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Questrade refresh token and writes rotated token material to local OpenClaw credential and cache files.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
