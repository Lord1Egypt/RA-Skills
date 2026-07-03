## Description: <br>
Upcoming token unlock events that may create sell pressure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents, developers, and crypto traders use this skill to query APEX Runner's token-unlock signal before trades, filtering for upcoming unlock events that may create sell pressure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks an agent to use an EVM private key for automatically paid calls that can spend USDC. <br>
Mitigation: Use only a dedicated low-balance wallet and avoid configuring a primary trading or custody wallet as EVM_PRIVATE_KEY. <br>
Risk: Agent usage can create repeated paid calls without an account, API key, or subscription gate. <br>
Mitigation: Apply external controls on agent usage and spending before deployment. <br>


## Reference(s): <br>
- [Token Unlock on ClawHub](https://clawhub.ai/kynto2001-ctrl/skills/token-unlock) <br>
- [APEX Runner Token Unlock Signal](https://apexrunner.ai/signals/token-unlock) <br>
- [APEX Runner Pricing Tier Check](https://apexrunner.ai/signals/my-pricing) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, API calls, JSON] <br>
**Output Format:** [Markdown instructions with a Python request example and JSON response shape] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an EVM_PRIVATE_KEY for x402 payment; calls may spend USDC on Base mainnet.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
