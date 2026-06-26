## Description: <br>
Read-only balance checking and spending analytics for Sardis agent wallets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EfeDurmaz16](https://clawhub.ai/user/EfeDurmaz16) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to inspect Sardis wallet balances, spending summaries, transaction history, vendor spend, and remaining budgets without executing payments or modifying wallet state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose sensitive wallet balances, vendors, budgets, and transaction history. <br>
Mitigation: Use a read-only Sardis API key scoped only to wallets the agent is allowed to inspect, and treat returned financial data as sensitive. <br>
Risk: A broadly scoped API key could allow the agent to inspect more wallets than intended. <br>
Mitigation: Provision a least-privilege API key for the intended wallet set before enabling the skill. <br>


## Reference(s): <br>
- [Sardis Website](https://sardis.sh) <br>
- [Sardis Balance API Documentation](https://sardis.sh/docs/balance-api) <br>
- [Sardis API Reference](https://api.sardis.sh/v2/docs) <br>
- [ClawHub Skill Page](https://clawhub.ai/EfeDurmaz16/sardis-balance) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses SARDIS_API_KEY and read-only Sardis API endpoints; requires curl and jq.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
