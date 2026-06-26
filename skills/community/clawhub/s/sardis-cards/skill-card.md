## Description: <br>
Virtual card issuance and management for AI agents to make real-world purchases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EfeDurmaz16](https://clawhub.ai/user/EfeDurmaz16) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and purchasing agents use this skill to issue and manage Sardis virtual cards for agent purchases, including spending limits, merchant controls, transaction monitoring, freezing, and termination. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad authority over real payment cards, including card creation, unfreezing, limit changes, and card deletion. <br>
Mitigation: Use the narrowest Sardis API key available, enforce hard spend limits and merchant allowlists outside the agent, and require manual confirmation before card creation, unfreezing, limit increases, or deletion. <br>
Risk: The skill includes a workflow for revealing full card credentials. <br>
Mitigation: Require manual confirmation before revealing card details, prefer masked card data when possible, and do not log or display full card numbers or CVVs. <br>
Risk: Unattended use could allow unintended purchases or delayed response to suspicious activity. <br>
Mitigation: Monitor transactions, freeze cards on anomalies, and fail closed when fraud detection or approval checks are uncertain. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/EfeDurmaz16/sardis-cards) <br>
- [Sardis website](https://sardis.sh) <br>
- [Sardis virtual cards documentation](https://sardis.sh/docs/virtual-cards) <br>
- [Sardis API reference](https://api.sardis.sh/v2/docs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with curl and jq command examples and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SARDIS_API_KEY, curl, and jq; examples target the Sardis API and include sensitive card-management operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
