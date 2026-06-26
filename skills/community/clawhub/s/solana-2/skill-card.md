## Description: <br>
Query Solana blockchain data with USD pricing for wallet balances, token portfolios, transaction details, NFTs, whale detection, network stats, and price lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AgungPrabowo123](https://clawhub.ai/user/AgungPrabowo123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to inspect Solana wallets, tokens, transactions, NFTs, large transfers, network status, and token prices from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried public wallet addresses, token mints, and transaction signatures are sent to Solana RPC providers and sometimes CoinGecko. <br>
Mitigation: Use a trusted RPC endpoint for sensitive analysis and pass --no-prices when CoinGecko price lookups are not needed. <br>
Risk: An untrusted SOLANA_RPC_URL could expose queries to an unexpected RPC provider. <br>
Mitigation: Set SOLANA_RPC_URL only to RPC endpoints you trust. <br>
Risk: Public RPC and CoinGecko free APIs may rate-limit requests or return incomplete price coverage. <br>
Mitigation: Use --no-prices for faster RPC-only runs or configure a private RPC endpoint for production use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/AgungPrabowo123/solana-2) <br>
- [Publisher Profile](https://clawhub.ai/user/AgungPrabowo123) <br>
- [Solana Public RPC Endpoint](https://api.mainnet-beta.solana.com) <br>
- [CoinGecko Solana Token Price API](https://api.coingecko.com/api/v3/simple/token_price/solana) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include live Solana RPC and CoinGecko results; price lookups can be disabled with --no-prices.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
