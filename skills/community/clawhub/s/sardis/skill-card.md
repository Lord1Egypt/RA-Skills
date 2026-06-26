## Description: <br>
Payment OS for AI agents that creates MPC wallets, executes stablecoin payments with automatic policy enforcement, sets spending rules in natural language, checks balances across chains, and issues virtual cards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[efedurmaz16](https://clawhub.ai/user/efedurmaz16) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and agent builders use this skill to let agents create payment wallets, enforce spending policies, check balances, issue virtual cards, and initiate stablecoin payments through Sardis infrastructure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents can initiate actions against live payment infrastructure. <br>
Mitigation: Use a dedicated low-limit or least-privilege API key and require explicit human approval for each payment, bridge, escrow release, card issuance, and card reveal. <br>
Risk: API keys and full card details may be exposed through prompts, logs, traces, or transcripts. <br>
Mitigation: Keep credentials and card data out of agent context and operational logs; rotate keys if exposure is suspected. <br>
Risk: Public exposure of the skill server could widen access to financial operations. <br>
Mitigation: Run the FastAPI server only in a private, access-controlled environment and prefer sandbox or testnet flows before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/efedurmaz16/sardis) <br>
- [Sardis website](https://sardis.sh) <br>
- [Sardis API reference](https://api.sardis.sh/api/v2/docs) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SARDIS_API_KEY; payment, card, bridge, escrow, and wallet operations can affect live financial infrastructure.] <br>

## Skill Version(s): <br>
1.1.0 (source: SKILL.md frontmatter and server release metadata; pyproject.toml lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
