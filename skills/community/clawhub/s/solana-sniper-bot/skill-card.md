## Description: <br>
Autonomous Solana token sniper and trading bot that monitors new Raydium and Jupiter token launches, evaluates rugpull risk with LLM analysis, auto-buys promising launches, and manages exit strategies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[srikanthbellary](https://clawhub.ai/user/srikanthbellary) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and trading automation users use this skill to configure and run an autonomous Solana trading bot that monitors new pools, scores token risk, and submits Jupiter swap transactions. Users should treat it as high-risk financial automation because it can trade from a wallet private key without a confirmation or dry-run safety gate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a wallet private key to attempt autonomous live trades without a confirmation or dry-run safety gate. <br>
Mitigation: Use only a dedicated low-balance wallet, start with tiny trade amounts, prefer dry-run or manual approval before live use, and assume all allocated funds can be lost. <br>
Risk: The documented stop-loss and auto-sell protections should not be relied on without implementation and testing. <br>
Mitigation: Review and test exit behavior before enabling live transactions, and monitor positions actively while the bot is running. <br>
Risk: New Solana token and memecoin trading is extremely high risk and many assets can lose all value. <br>
Mitigation: Limit capital exposure, set conservative position sizes and thresholds, and avoid using a primary wallet or funds needed for other purposes. <br>


## Reference(s): <br>
- [Solana Sniper Bot on ClawHub](https://clawhub.ai/srikanthbellary/solana-sniper-bot) <br>
- [Publisher profile](https://clawhub.ai/user/srikanthbellary) <br>
- [Publisher homepage](https://github.com/srikanthbellary) <br>
- [Jupiter Aggregator API](references/jupiter-api.md) <br>
- [Raydium Pool Monitoring](references/raydium-pools.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell commands, environment configuration, and Python code references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SOLANA_PRIVATE_KEY and LLM_API_KEY; may also use RPC_URL, HELIUS_API_KEY, BUY_AMOUNT_SOL, TAKE_PROFIT, STOP_LOSS, MAX_POSITIONS, MIN_LIQUIDITY, and SLIPPAGE_BPS.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
