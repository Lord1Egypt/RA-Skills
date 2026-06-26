## Description: <br>
Automate Volkern CRM operations including lead management, appointment scheduling, task tracking, service catalog, WhatsApp messaging, sales pipeline, quotations, and contracts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DeXpertmx](https://clawhub.ai/user/DeXpertmx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External CRM operators and developers use this MCP server to let compatible AI agents query and update Volkern CRM records, schedule appointments, manage follow-up work, send WhatsApp messages, and prepare quotations or contracts through authenticated API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review was incomplete because the scanner reported that the supplied workspace did not expose the target skill artifact files referenced by the scanners. <br>
Mitigation: Inspect the artifact files before installation and rerun security review in an environment where the scanner can access the released artifact. <br>
Risk: Tool calls can create or change CRM records, schedule appointments, send WhatsApp messages, and share quote or contract links. <br>
Mitigation: Require explicit user confirmation for externally visible or state-changing actions, use least-privilege API credentials, and confirm appropriate customer consent before sending messages or links. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/DeXpertmx/volkern-skill) <br>
- [Volkern API base URL](https://volkern.app/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown guidance, JSON tool schemas, shell commands, and MCP tool call results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires VOLKERN_API_KEY and optionally VOLKERN_API_URL; tool calls may create or modify CRM records and send WhatsApp messages.] <br>

## Skill Version(s): <br>
1.1.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
