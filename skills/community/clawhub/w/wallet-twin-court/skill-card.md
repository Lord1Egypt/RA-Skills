## Description: <br>
Use this skill when the user wants to put a Solana wallet on trial, identify the action most likely to cause regret tomorrow, return a verdict, and only then preview execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[richard7463](https://clawhub.ai/user/richard7463) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to assess one Solana wallet before trading, identify the action most likely to cause regret, and receive a single verdict before any execution preview. The skill supports court-style pre-trade review using the disclosed Court API and wallet, market, quote, and receipt evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried Solana wallet addresses are sent to the disclosed Court API and may reveal or correlate wallet activity with a third-party service. <br>
Mitigation: Use only wallet addresses whose activity you are comfortable sharing with the Court API, and avoid submitting wallets that require privacy from third-party analysis. <br>
Risk: Execution previews can be mistaken for completed trades. <br>
Mitigation: Treat previews as informational until a wallet-connected client signs, broadcasts, and confirms the transaction with a receipt. <br>
Risk: Trading steps could be acted on without sufficient user intent. <br>
Mitigation: Require explicit user approval before broadcast, and stop at preview when the client environment cannot sign and broadcast safely. <br>


## Reference(s): <br>
- [Wallet Twin Court Skill Page](https://clawhub.ai/richard7463/wallet-twin-court) <br>
- [Court API](https://todays-orders.vercel.app/api/todays-orders) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, API Calls, Shell commands, Guidance] <br>
**Output Format:** [Markdown with structured verdict sections and optional inline bash command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs a preview report unless execution is explicitly approved and confirmed with a receipt.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
