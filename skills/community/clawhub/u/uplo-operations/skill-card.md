## Description: <br>
AI-powered operations knowledge management. Search process documentation, capacity plans, resource allocation data, and KPI dashboards with structured extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RooJenkins](https://clawhub.ai/user/RooJenkins) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations teams, managers, and authorized employees use this skill to search organizational process documentation, SOPs, runbooks, capacity plans, vendor SLAs, incident records, and KPI data through UPLO. It supports incident response, capacity planning, operational reviews, onboarding, and documentation maintenance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an assistant broad access to sensitive company operations data. <br>
Mitigation: Install only for authorized users, use a least-privilege UPLO token, and respect classification tiers for confidential or restricted records. <br>
Risk: Org-context export, incident or directive retrieval, conversation logging, and knowledge-base updates may expose or persist sensitive operational information. <br>
Mitigation: Require user confirmation before exporting org context, retrieving sensitive incident or directive data, logging conversations, or changing knowledge-base records. <br>
Risk: A misconfigured or untrusted MCP package or UPLO instance could route requests to the wrong service. <br>
Mitigation: Verify the npm MCP package and UPLO instance URL before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/RooJenkins/uplo-operations) <br>
- [UPLO](https://uplo.ai) <br>
- [UPLO schemas](https://uplo.ai/schemas) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with MCP tool calls, search guidance, and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include organization-specific operations data retrieved through the configured UPLO MCP server.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
