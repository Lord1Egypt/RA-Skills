## Description: <br>
Perform triangular arbitrage on Hedera using SaucerSwap to find, calculate, and execute profitable multi-hop token swaps atomically. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HarleysCodes](https://clawhub.ai/user/HarleysCodes) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and trading agents use this skill to evaluate SaucerSwap triangular arbitrage paths on Hedera, calculate expected profit across pools, and prepare multi-hop swap transactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mainnet swap guidance can move real funds without clear confirmation boundaries. <br>
Mitigation: Use a testnet or dry-run workflow first, require explicit confirmation before any swap, and manually verify slippage, fees, and liquidity. <br>
Risk: Wallet permissions or funded accounts used for arbitrage can expose assets to loss. <br>
Mitigation: Use least-privilege wallet access and never give a wallet more authority or funds than the user is prepared to risk. <br>


## Reference(s): <br>
- [SaucerSwap mainnet route API](https://mainnet-api.saucerswap.fi/route?from=${tokenA}&to=${tokenB}&amount=${amountIn}) <br>
- [ClawHub skill page](https://clawhub.ai/HarleysCodes/saucerswap-arbitrage) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown with TypeScript code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes quote-fetching, profit calculation, swap execution, slippage, fee, and liquidity guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
