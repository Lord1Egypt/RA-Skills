## Description: <br>
Agent settles an invoice at the end of a multi-step task using CAI transfer after user confirms payee and amount. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bernardtai](https://clawhub.ai/user/bernardtai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to prepare, confirm, and settle CAI invoice payments at the end of multi-step agent work. It supports balance checks, recipient resolution, transfer execution after explicit user approval, and payment proof retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help prepare high-impact cryptocurrency or financial transfers. <br>
Mitigation: Install it only when CAI invoice payment assistance is intended, and require explicit user approval before any transfer. <br>
Risk: Incorrect payee, address, amount, asset, or chain details can lead to an irreversible transfer. <br>
Mitigation: Independently verify all transfer details against the invoice and CAI recipient resolution before approving payment. <br>
Risk: The skill requires sensitive CAI credentials to operate. <br>
Mitigation: Store CAI_API_KEY only through the agent secret manager and avoid placing credentials in prompts, files, or logs. <br>


## Reference(s): <br>
- [CAI Skill Reference](https://cai.com/skill.md) <br>
- [Agent Payment Workflow](https://cai.com/skill-references/agent-payment-workflow.md) <br>
- [CAI Developers](https://cai.com/developers.html) <br>
- [ClawHub Skill Page](https://clawhub.ai/bernardtai/settle-agent-invoice) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Markdown with inline shell commands and tool-call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a CAI_API_KEY secret and explicit user confirmation before transfer.] <br>

## Skill Version(s): <br>
1.0.15 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
