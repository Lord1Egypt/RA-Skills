## Description: <br>
AI-powered consulting knowledge management. Search engagement records, methodology frameworks, deliverable templates, and best practices with structured extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RooJenkins](https://clawhub.ai/user/RooJenkins) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Consulting teams use this skill to retrieve institutional knowledge from engagement records, methodology frameworks, proposal archives, deliverable templates, and lessons learned. It supports proposal development, engagement kickoff, staffing research, onboarding, and knowledge-gap reporting through the connected UPLO knowledge base. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad access to sensitive consulting knowledge, including proposal, client, engagement, and organizational context. <br>
Mitigation: Use a least-privilege UPLO token, enforce classification tiers, and avoid using the skill with confidential client or proposal data unless retention, access, and deletion policies are approved. <br>
Risk: Tools such as export_org_context, get_directives, proposal logging, knowledge-base writes, and stale-marking actions can expose or alter sensitive firm knowledge. <br>
Mitigation: Require explicit user approval before org-context exports, directives retrieval, proposal logging, knowledge-base write actions, or stale-marking actions. <br>
Risk: The MCP server is launched through an npm package at install time. <br>
Mitigation: Verify and pin the MCP server package where possible before installing in a real firm environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/RooJenkins/uplo-consulting) <br>
- [UPLO](https://uplo.ai) <br>
- [UPLO schemas](https://uplo.ai/schemas) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline MCP tool calls, JSON configuration examples, and consulting guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an UPLO instance URL and API key. Agent outputs may include retrieved engagement summaries, methodology references, directives, organizational context, and proposed knowledge-base updates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
