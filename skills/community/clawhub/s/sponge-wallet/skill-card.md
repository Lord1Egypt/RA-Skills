## Description: <br>
Manages crypto wallets, transfers tokens, swaps on DEXes, checks balances, and accesses paid APIs (search, image gen, prediction markets, web scraping, document parsing, sales prospecting) via x402 micropayments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rishabluthra](https://clawhub.ai/user/rishabluthra) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent inspect wallet balances, transfer supported tokens, perform Solana swaps, and access paid API services through x402 micropayments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can delegate wallet write and transaction-signing authority, including transfers, swaps, withdrawals, and x402 payments. <br>
Mitigation: Use testnet or low-balance wallets and verify recipient, chain, token, amount, slippage, and payment recipient before each action. <br>
Risk: Paid API calls can spend funds automatically when payment is enabled. <br>
Mitigation: Review costs where possible and use payment preview behavior such as disabling automatic payment before approving paid API calls. <br>
Risk: Overriding the wallet API endpoint can redirect authenticated wallet operations to a different service. <br>
Mitigation: Avoid overriding SPONGE_API_URL unless the endpoint is fully trusted. <br>
Risk: Stored or environment-provided credentials can continue granting wallet access after use. <br>
Mitigation: Use logout or rotate credentials when finished. <br>


## Reference(s): <br>
- [README.md](README.md) <br>
- [REFERENCE.md](REFERENCE.md) <br>
- [Sponge Wallet ClawHub page](https://clawhub.ai/rishabluthra/sponge-wallet) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, API Calls, Guidance] <br>
**Output Format:** [JSON responses and Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Wallet and paid API actions require authentication and may move funds or incur micropayment costs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
