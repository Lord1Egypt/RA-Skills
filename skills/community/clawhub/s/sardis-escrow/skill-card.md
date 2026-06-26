## Description: <br>
Smart contract escrow for agent-to-agent payments with delivery confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EfeDurmaz16](https://clawhub.ai/user/EfeDurmaz16) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to create, fund, monitor, and release smart contract escrow agreements for agent-to-agent work after delivery confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent-executed escrow operations can create, fund, confirm, release, or milestone-release real asset transfers. <br>
Mitigation: Require manual confirmation before any payment-affecting request and use sandbox or tightly scoped API keys with spending limits. <br>
Risk: A wrong API domain, base path, or dependency package could route sensitive payment actions or credentials to the wrong service. <br>
Mitigation: Verify the Sardis domain, API base path, and @sardis/sdk package before installation or execution. <br>


## Reference(s): <br>
- [Sardis Website](https://sardis.sh) <br>
- [Sardis Escrow Documentation](https://sardis.sh/docs/escrow) <br>
- [Sardis API Reference](https://api.sardis.sh/v2/docs) <br>
- [ClawHub Skill Page](https://clawhub.ai/EfeDurmaz16/sardis-escrow) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SARDIS_API_KEY plus curl and jq; API calls may create, fund, or release escrow payments.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
