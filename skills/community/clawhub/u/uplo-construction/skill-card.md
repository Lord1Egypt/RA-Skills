## Description: <br>
AI-powered construction knowledge management. Search project documents, safety compliance records, permits, building codes, and RFIs with structured extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RooJenkins](https://clawhub.ai/user/RooJenkins) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Construction project teams use this skill to search project documentation, safety records, permits, building codes, RFIs, submittals, change orders, and related organizational context. It supports field and office workflows such as change order review, pre-pour verification, onboarding, and compliance checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access confidential construction project data, including cost data, bid information, safety incidents, and litigation-sensitive records. <br>
Mitigation: Use least-privilege UPLO tokens and preserve classification tiers when answering or exporting information. <br>
Risk: The skill can guide agents to log conversations, mark documents outdated, or export organizational context, which may alter or disclose project records. <br>
Mitigation: Require explicit user approval before logging conversations, flagging documents, or exporting organizational context. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/RooJenkins/uplo-construction) <br>
- [UPLO](https://uplo.ai) <br>
- [UPLO Schemas](https://uplo.ai/schemas) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, MCP tool calls, and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference project names, document revisions, dates, statuses, responsible parties, and deadlines when grounded in the connected knowledge base.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
