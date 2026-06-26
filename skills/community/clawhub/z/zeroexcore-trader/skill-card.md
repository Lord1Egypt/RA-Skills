## Description: <br>
Trade Solana tokens, track portfolio, bet on prediction markets, check NFT floors via the trader CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devatzeroxcore](https://clawhub.ai/user/devatzeroxcore) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent operate the trader CLI for Solana token swaps, portfolio tracking, prediction-market positions, perpetuals market views, and NFT floor checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent high-impact wallet and betting authority for real crypto trading. <br>
Mitigation: Use only a dedicated low-balance wallet and require explicit user approval for every wallet export, swap, bet, sell, close, or claim. <br>
Risk: The artifact includes guidance for geo-blocked prediction markets. <br>
Mitigation: Do not use the skill to bypass geo-restrictions or platform terms. <br>
Risk: The skill installs and runs a third-party npm CLI that can sign wallet transactions. <br>
Mitigation: Verify the npm package source and version before installation or execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/devatzeroxcore/zeroexcore-trader) <br>
- [Project homepage](https://github.com/zeroexcore/trader) <br>
- [Helius developer portal](https://dev.helius.xyz) <br>
- [Jupiter developer portal](https://portal.jup.ag) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Markdown] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples; CLI output is JSON by default with optional Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WALLET_PASSWORD and HELIUS_API_KEY; JUPITER_API_KEY is used for swaps and predictions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
