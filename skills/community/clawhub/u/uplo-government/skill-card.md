## Description: <br>
AI-powered government knowledge management. Search policy documents, regulatory filings, public records, and inter-agency coordination data with structured extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RooJenkins](https://clawhub.ai/user/RooJenkins) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Government analysts, policy staff, counsel, budget offices, auditors, and congressional liaisons use this skill to search agency policy, regulatory, public-record, inter-agency, and coordination knowledge while preserving authoritative citations and classification-tier awareness. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive government or organizational knowledge through API-backed search and context export. <br>
Mitigation: Install only for authorized deployments, use narrowly scoped UPLO tokens, require HTTPS endpoints, and avoid confidential, restricted, regulated, or classified data unless the deployment is approved for that handling. <br>
Risk: The export_org_context capability may expose broad agency context if the connected knowledge base and token are not scoped appropriately. <br>
Mitigation: Confirm what export_org_context includes before use and restrict token permissions to the minimum organizational scope needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/RooJenkins/uplo-government) <br>
- [UPLO](https://uplo.ai) <br>
- [UPLO schemas](https://uplo.ai/schemas) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a UPLO instance URL and narrowly scoped UPLO MCP token for connected use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
