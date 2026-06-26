## Description: <br>
Buy, sell, and launch tokens on Pump.fun using the PumpPortal API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PlaydaDev](https://clawhub.ai/user/PlaydaDev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and operators use this skill to configure an agent for Pump.fun token buys, sells, and launches through the PumpPortal API. It requires a Solana private key and should be used only with explicit review of wallet impact before each transaction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests a Solana private key and can initiate high-impact crypto trades or token launches. <br>
Mitigation: Use only a dedicated low-balance wallet, never a main wallet, and set SOLANA_PRIVATE_KEY only after reviewing and trusting the implementation. <br>
Risk: Incorrect token mint, amount, slippage, fee, or launch parameters could create unintended wallet impact. <br>
Mitigation: Manually verify token mint, amount, slippage, fees, and wallet impact before every trade or token launch. <br>
Risk: Server security evidence reports insufficient visible implementation or transaction safeguards for the claimed trading authority. <br>
Mitigation: Review the package before installing and do not use it for real transactions unless the implementation and transaction controls are inspectable and acceptable. <br>


## Reference(s): <br>
- [Pump.fun](https://pump.fun) <br>
- [ClawHub skill page](https://clawhub.ai/PlaydaDev/pump-fun) <br>
- [Publisher profile](https://clawhub.ai/user/PlaydaDev) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with command examples and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SOLANA_PRIVATE_KEY; optional SOLANA_RPC_URL, PUMP_PRIORITY_FEE, and PUMP_DEFAULT_SLIPPAGE settings are documented.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
