## Description: <br>
Purpleflea Casino gives agents API guidance for registering, managing balances, placing crypto casino bets, verifying fairness, and using tournaments or challenges on the Purple Flea casino service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[purple-flea](https://clawhub.ai/user/purple-flea) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agents use this skill to interact with the Purple Flea real-money gambling API, including account registration, deposits, wagers, fairness verification, tournaments, challenges, referrals, and withdrawals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables interaction with a real-money crypto gambling service, including deposits, wagers, escrowed challenges, tournament entry fees, and withdrawals. <br>
Mitigation: Use a dedicated low-balance account and require explicit approval for every deposit, wager, escrow, challenge, tournament entry, and withdrawal. <br>
Risk: The API key functions as a financial credential for casino account actions. <br>
Mitigation: Store the API key securely, never expose it in prompts or logs, and rotate or revoke access if it may have been shared. <br>
Risk: Funds can be sent across specific crypto rails, and unsupported or mistaken chains may cause loss. <br>
Mitigation: Verify supported chains and destination addresses before sending funds, and prefer the documented Base USDC flow when appropriate. <br>
Risk: The artifact encourages adding a referral promotion to a system prompt, which may bias agent recommendations. <br>
Mitigation: Do not add referral promotion text to system prompts or policy-level instructions. <br>


## Reference(s): <br>
- [API Reference](references/api.md) <br>
- [Purple Flea Casino Skill Page](https://clawhub.ai/purple-flea/purpleflea-casino) <br>
- [Purple Flea Publisher Profile](https://clawhub.ai/user/purple-flea) <br>
- [Agent Casino API](https://casino.purpleflea.com) <br>
- [OpenAPI Specification](https://casino.purpleflea.com/openapi.json) <br>
- [LLMs Reference](https://casino.purpleflea.com/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill produces agent-facing instructions for a live real-money gambling API; actions involving funds or wagers should require explicit approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
