## Description: <br>
Execute token swaps using the 0x API with support for price quotes, gasless meta-transactions, and on-chain trade history retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aviclaw](https://clawhub.ai/user/aviclaw) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and crypto automation operators use this skill to fetch 0x token swap quotes, execute ERC-20 swaps from a configured wallet, and inspect swap history on supported EVM chains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can spend real funds and gas through irreversible cryptocurrency transactions. <br>
Mitigation: Use a dedicated low-balance hot wallet and review chain, token addresses, amount, spender, and transaction target before every swap. <br>
Risk: The swap flow uses a raw wallet private key. <br>
Mitigation: Never use a primary wallet key; store only a dedicated hot-wallet key in the runtime environment and rotate it if exposed. <br>
Risk: swap.js can submit a transaction without an explicit human confirmation or dry-run step. <br>
Mitigation: Add a confirmation or dry-run gate before allowing an agent to execute swap.js. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aviclaw/zeroex-swap) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/aviclaw) <br>
- [0x developer dashboard](https://dashboard.0x.org/) <br>
- [0x Swap API endpoint](https://api.0x.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and JavaScript execution output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZEROEX_API_KEY and a wallet private key; swap execution can submit irreversible on-chain transactions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
