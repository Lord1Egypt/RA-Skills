## Description: <br>
Comprehensive token intelligence for Base blockchain, including risk scores, whale tracking, signal analysis, and safety checks for Base tokens. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[supah-based](https://clawhub.ai/user/supah-based) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, traders, and agent builders use this skill to query Base token risk scores, safety checks, market context, whale activity, portfolio risk, and signal feeds through the SUPAH API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send wallet addresses and token queries to the third-party SUPAH API. <br>
Mitigation: Only submit wallet addresses or token data that the user is comfortable sharing with api.supah.ai. <br>
Risk: The skill uses paid x402 API calls and the server security summary warns about insufficient upfront consent and risk controls. <br>
Mitigation: Use a dedicated low-balance wallet, confirm each paid API call manually, and review costs before execution. <br>
Risk: The artifact includes trading-oriented signal and automated trading examples. <br>
Mitigation: Treat outputs as informational analysis, require human approval before trades, and do not allow autonomous trade execution from signals alone. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/supah-based/supah-base-intelligence) <br>
- [SUPAH website](https://supah.ai) <br>
- [SUPAH API](https://api.supah.ai) <br>
- [SUPAH docs](https://docs.supah.ai) <br>
- [x402 protocol](https://www.x402.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples and JSON API result data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and curl; can send requests to api.supah.ai and may use x402 USDC payments on Base.] <br>

## Skill Version(s): <br>
1.3.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
