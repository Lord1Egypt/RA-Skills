## Description: <br>
Discover, pay, and fetch data from x402-enabled APIs on the Coinbase x402 Bazaar. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cariohca-ux](https://clawhub.ai/user/cariohca-ux) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search Coinbase x402 Bazaar resources, fetch paid API responses, and monitor daily spend while using a Base USDC wallet for x402 payments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can spend Base USDC from a configured wallet on user-invoked paid x402 API requests. <br>
Mitigation: Use a low-balance wallet, set DAILY_BUDGET_USD conservatively, and treat fetch or resolve commands as spending actions. <br>
Risk: Request URLs and query data are sent to external x402 services. <br>
Mitigation: Avoid sending sensitive URLs, wallet context, or confidential query data unless the selected provider is trusted. <br>
Risk: A private wallet key is required for payment signing. <br>
Mitigation: Store WALLET_KEY only in local environment configuration, keep the file out of git, and rotate the key if it is exposed. <br>


## Reference(s): <br>
- [x402 Bazaar Bridge on ClawHub](https://clawhub.ai/cariohca-ux/x402-bazaar-bridge) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON command output and Markdown usage guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search and fetch commands may call external x402 services, sign payment payloads when WALLET_KEY is configured, cache responses, and track daily budget state.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
