## Description: <br>
AI-powered customer lifecycle intelligence spanning sales, customer success, and retail. Unified search across pipeline data, account health, and customer analytics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RooJenkins](https://clawhub.ai/user/RooJenkins) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Revenue, customer success, and retail operations teams use this skill to query a unified customer knowledge base for account reviews, churn investigations, QBR preparation, and lifecycle analytics across sales, support, product usage, and retail data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects an external MCP server to sensitive customer and account data. <br>
Mitigation: Use only a trusted UPLO HTTPS endpoint with a least-privilege, rotatable API token. <br>
Risk: Broad organization-context exports, conversation logging, or shared knowledge-base flags can expose or change customer information. <br>
Mitigation: Require explicit user approval before exporting organization-wide context, logging customer-specific summaries, or creating flags or proposals in shared knowledge systems. <br>
Risk: The MCP server package is installed through an unpinned npx command. <br>
Mitigation: Review and pin the package version in deployment configuration where possible before installing in production. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/RooJenkins/uplo-customer-360) <br>
- [UPLO](https://uplo.ai) <br>
- [UPLO schemas](https://uplo.ai/schemas) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline MCP tool calls and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a trusted UPLO instance URL and API key; may invoke MCP searches and organization-context exports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
