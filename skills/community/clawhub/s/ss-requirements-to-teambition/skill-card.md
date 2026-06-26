## Description: <br>
Collects tagged SaleSmartly customer-support conversations, uses AI analysis to extract product requirements, and creates Teambition tasks for customer feedback management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zpeng6834-arch](https://clawhub.ai/user/zpeng6834-arch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Customer-support and product operations teams use this skill to turn tagged SaleSmartly conversations into structured Teambition requirement tasks. It supports a workflow from conversation collection through AI-assisted requirement extraction and task creation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Customer-support conversations and local transcript exports may expose customer or personal data. <br>
Mitigation: Use only in an environment approved for customer-support data, redact unnecessary customer fields before analysis or task creation, and keep retention short for generated session files. <br>
Risk: SaleSmartly and Teambition credentials are required for collection and task creation. <br>
Mitigation: Restrict credential permissions and store tokens outside plaintext project files where possible. <br>
Risk: Automated Teambition task creation can create unwanted or duplicate work items if run unattended. <br>
Mitigation: Keep duplicate checks enabled and review retention, access controls, and task approval behavior before enabling cron automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zpeng6834-arch/ss-requirements-to-teambition) <br>
- [AI analysis and task creation template](references/analysis_template.md) <br>
- [Configuration fields guide](references/config_fields.md) <br>
- [Teambition MCP setup guide](references/tb_mcp_setup.md) <br>
- [Teambition user MCP page](https://open.teambition.com/user-mcp) <br>
- [SaleSmartly API endpoint](https://api.salesmartly.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON files, API calls] <br>
**Output Format:** [Markdown guidance, shell commands, JSON session exports, and Teambition task creation requests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local SaleSmartly session exports, AI analysis notes, duplicate-aware Teambition task creation requests, and optional cron automation guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
