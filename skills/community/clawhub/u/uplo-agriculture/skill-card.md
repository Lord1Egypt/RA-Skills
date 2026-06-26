## Description: <br>
AI-powered agricultural knowledge management for searching crop management records, livestock data, compliance documentation, and sustainability reports with structured extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RooJenkins](https://clawhub.ai/user/RooJenkins) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agriculture teams and their agents use this skill to query organizational farming knowledge, including crop plans, livestock records, compliance materials, sustainability reports, and responsible knowledge owners. It is intended to ground answers in the connected UPLO knowledge base rather than generate unsupported agriculture guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access broad organizational agriculture records, including farm operations, livestock, compliance, financial, and proprietary data. <br>
Mitigation: Use a least-privilege UPLO token, enforce classification tiers, and require approval before full organizational context export. <br>
Risk: Conversation summaries may be persisted without clear user or tenant consent. <br>
Mitigation: Require explicit consent before logging conversations and avoid storing sensitive record details in summaries. <br>
Risk: The skill depends on an external MCP package for knowledge-base access. <br>
Mitigation: Verify and approve the MCP package before installation, and pin or otherwise control the package version in managed environments. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/RooJenkins/uplo-agriculture) <br>
- [UPLO](https://uplo.ai) <br>
- [UPLO schemas](https://uplo.ai/schemas) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses should cite UPLO sources, respect classification levels, and state when the knowledge base does not contain an answer.] <br>

## Skill Version(s): <br>
1.0.0 (source: skill.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
