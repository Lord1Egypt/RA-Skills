## Description:

Smart Money Miner helps an agent discover and filter high-performing Solana and BNB Chain wallet addresses from PumpFun, Four Meme, or user-provided token data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackydai-bc](https://clawhub.ai/user/jackydai-bc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to mine potentially profitable crypto wallet addresses from token trading data and produce structured results for review. It supports PumpFun on Solana, Four Meme on BNB Chain, and manually supplied token addresses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends token and wallet addresses to third-party crypto data APIs.

Mitigation: Use it only for intended wallet-analysis tasks and avoid submitting addresses that should not be shared with those services.

Risk: The skill saves detailed wallet-analysis output to smart_money_results.json in the working directory.

Mitigation: Run it in a directory where that output file is expected and acceptable.

Risk: Dependency installation may pull current package versions if users install requests themselves.

Mitigation: Pin dependencies in managed environments before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jackydai-bc/skills/smart-money-miner)
- [PumpFun token API endpoint](https://frontend-api-v3.pump.fun/coins)
- [OKX Web3 trader ranking API endpoint](https://web3.okx.com/priapi/v1/dx/market/v2/pnl/top-trader/ranking-list)
- [OKX Web3 token PnL API endpoint](https://web3.okx.com/priapi/v1/dx/market/v2/pnl/token-list)
- [Four Meme token query API endpoint](https://four.meme/meme-api/v1/private/token/query)
- [Binance wallet narrative API endpoint](https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/token/ai/narrative/query)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON files]

**Output Format:** [Markdown guidance with shell commands and local JSON result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are saved to smart_money_results.json and may include filtered wallet addresses, source tokens, profit metrics, chain labels, and full analysis data.]

## Skill Version(s):

1.0.0 (source: server release metadata; skill frontmatter and release changelog describe 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
