## Description: <br>
Manages Solana portfolios by tracking balances, token distribution, and asset valuation across connected wallets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liji3597](https://clawhub.ai/user/liji3597) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to add, list, remove, and review public Solana wallet holdings for a Telegram-linked user. It summarizes portfolio value, holdings, PnL, and educational rebalancing signals without asking for private keys. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill links public Solana wallet addresses and portfolio data to a Telegram identity. <br>
Mitigation: Add only wallet addresses the user is comfortable associating with that Telegram identity, and limit access to portfolio outputs. <br>
Risk: Wallet add and remove actions depend on the host runtime binding the Telegram user ID to the actual caller. <br>
Mitigation: Deploy only in runtimes that provide a trusted caller identity and do not accept arbitrary user-supplied Telegram IDs for another account. <br>
Risk: Users may confuse portfolio tracking or rebalancing summaries with trade execution or investment advice. <br>
Mitigation: Treat outputs as informational, verify balances and prices independently, and do not provide private keys or seed phrases. <br>
Risk: Storage, authorization, and portfolio-fetching behavior lives in shared service modules outside the visible skill scripts. <br>
Mitigation: Review those shared modules before relying on the skill for production portfolio tracking. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liji3597/solana-portfolio) <br>
- [Publisher profile](https://clawhub.ai/user/liji3597) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Conversational Markdown and command output, with JSON used for missing-parameter responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and SOLANA_NETWORK; scripts rely on shared service modules for storage, authorization, portfolio fetching, and formatting.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence and target metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
