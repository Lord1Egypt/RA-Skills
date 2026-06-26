## Description: <br>
Use when helping SMBcrm customers with Private Integration Tokens, REST API v2, workflows, custom webhooks, MCP, or Agent Studio API for troubleshooting, automation design, data sync, AI assistant setup, or tasks involving SMBcrm service endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[section5media](https://clawhub.ai/user/section5media) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External SMBcrm customers, operators, and developers use this skill to design and troubleshoot advanced CRM automations, API v2 integrations, workflow webhooks, MCP clients, and Agent Studio API usage with secure implementation patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated examples may use overly broad token scopes, expose secrets, or be applied directly to production CRM data. <br>
Mitigation: Review token scopes, keep secrets out of prompts and logs, use test or sandbox data first, and store Private Integration Tokens in a secret manager. <br>
Risk: CRM writes, payments, public content actions, or long-running automations may create unintended customer or business impact. <br>
Mitigation: Manually approve high-impact actions, validate behavior with a test plan, and review rollback steps before production use. <br>


## Reference(s): <br>
- [SMBcrm Developer Documentation](https://developers.smbcrm.com/) <br>
- [SMBcrm Services API Base URL](https://services.smbcrm.com) <br>
- [SMBcrm Skill Release Page](https://clawhub.ai/section5media/smbcrm) <br>
- [section5media Publisher Profile](https://clawhub.ai/user/section5media) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code blocks, shell commands, JSON examples, and implementation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include CRM API examples, workflow steps, MCP configuration snippets, test plans, and failure-mode guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
