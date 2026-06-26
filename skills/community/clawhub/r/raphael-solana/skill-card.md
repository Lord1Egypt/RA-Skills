## Description: <br>
Manage Solana and Polygon wallets, run Polymarket weather arbitrage, post to X/Twitter, and execute Raydium swaps from natural language. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[inspi-writer001](https://clawhub.ai/user/inspi-writer001) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to operate crypto wallets, Polymarket weather-arbitrage workflows, X/Twitter posting, and Raydium swaps through natural-language agent tools or CLI commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow can expose the master wallet password in terminal output or logs. <br>
Mitigation: Run setup only in a private local terminal, avoid shared shells and CI, and rotate the master password if it has already appeared in logs. <br>
Risk: Live trading, transfers, and swaps can spend wallet funds or place Polymarket orders. <br>
Mitigation: Use wallets funded only with amounts you are willing to risk, begin scanners in dry-run mode, and verify each live trade or transfer before execution. <br>
Risk: X/Twitter actions can publish posts or replies from the configured account. <br>
Mitigation: Start X workflows in dry-run mode, keep rate limits enabled, and verify live posting requests before allowing execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/inspi-writer001/raphael-solana) <br>
- [Source code link declared by skill](https://github.com/inspi-writer001/raphael-solana) <br>
- [Plugin tools source link declared by skill](https://github.com/inspi-writer001/raphael-solana/blob/main/src/plugin.ts) <br>
- [X developer portal](https://developer.x.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text tool responses and Markdown command/configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include transaction URLs, wallet addresses, balances, scanner status, tweet URLs, and error messages.] <br>

## Skill Version(s): <br>
1.1.2 (source: SKILL.md frontmatter and server release metadata; package.json reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
