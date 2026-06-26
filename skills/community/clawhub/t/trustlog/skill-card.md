## Description: <br>
Create, summarize, or verify local human-readable receipts for AI agent work using the @builtbyecho/trustlog CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[builtbyecho](https://clawhub.ai/user/builtbyecho) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and agent operators use trustlog to create local JSON and Markdown receipts after verification commands, summarize what ran or changed, and verify receipts before sharing handoffs, PR evidence, tickets, or chat updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Receipts may include secrets or sensitive project details even with redaction. <br>
Mitigation: Review .trustlog files before sharing them outside the local workspace. <br>
Risk: The optional Vaultline workflow sends a receipt to an external service. <br>
Mitigation: Use the local receipt workflow by default and upload only when intentionally sharing with a scoped, revocable API key. <br>
Risk: The skill runs referenced npm tools and wraps user-selected commands. <br>
Mitigation: Install only when comfortable running the referenced npm packages, prefer non-destructive commands, and verify receipts before using them as final evidence. <br>


## Reference(s): <br>
- [trustlog on ClawHub](https://clawhub.ai/builtbyecho/trustlog) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JavaScript upload snippet] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local .trustlog JSON and Markdown receipt files through the referenced CLI; optional Vaultline upload requires VAULTLINE_API_KEY.] <br>

## Skill Version(s): <br>
0.2.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
