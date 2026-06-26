## Description: <br>
Financial enablement and accounting platform for bots, agents, and OpenClaw, with methods for enabling and managing agentic spending and purchases across wallets with consolidated accounts and guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codejika](https://clawhub.ai/user/codejika) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to register and operate CreditClaw wallets, check balances and spending permissions, request top-ups, generate payment links, and make purchases through owner-configured payment rails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables real-money wallet and marketplace actions, including purchases, transfers, listings, top-up requests, and approval-sensitive workflows. <br>
Mitigation: Use a low-balance dedicated wallet and require manual approval for purchases, transfers, haggle acceptance, listings, and top-up requests. <br>
Risk: Exposure of CREDITCLAW_API_KEY could allow unauthorized wallet or payment actions. <br>
Mitigation: Store the key in a secure secrets manager or protected environment variable, avoid plaintext storage, and only send it to creditclaw.com API endpoints. <br>
Risk: The recurring heartbeat and downloadable helper files can influence agent behavior around balances, top-ups, and spending checks. <br>
Mitigation: Inspect downloaded heartbeat or CLI files before use and keep owner spending limits, blocked categories, and approval settings enforced. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/codejika/usd) <br>
- [Publisher profile](https://clawhub.ai/user/codejika) <br>
- [CreditClaw homepage](https://creditclaw.com) <br>
- [CreditClaw skill reference](https://creditclaw.com/skill.md) <br>
- [CreditClaw heartbeat routine](https://creditclaw.com/heartbeat.md) <br>
- [CreditClaw skill metadata](https://creditclaw.com/skill.json) <br>
- [CreditClaw API base](https://creditclaw.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown documentation with curl commands and JSON request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY and owner-configured CreditClaw wallet or payment rail access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 2.0.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
