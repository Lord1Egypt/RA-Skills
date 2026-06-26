## Description: <br>
AI-powered facilities knowledge management. Search building management records, maintenance schedules, space planning data, and vendor service documentation with structured extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RooJenkins](https://clawhub.ai/user/RooJenkins) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Facilities teams use this skill to query building records, maintenance schedules, space planning documents, vendor service contracts, inspections, and operational directives through UPLO-backed knowledge tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Full organizational context exports can expose sensitive facilities and operational information. <br>
Mitigation: Install only with a UPLO token scoped to facilities data, prefer targeted searches over full organization exports, and handle exported context as sensitive operational information. <br>
Risk: Facilities records may include restricted building security configurations, access-control data, overdue inspections, or expiring vendor contracts. <br>
Mitigation: Respect UPLO classification tiers, confirm identity and classification controls, and surface only knowledge-base-backed information with relevant dates and responsible owners. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/RooJenkins/uplo-facilities) <br>
- [UPLO](https://uplo.ai) <br>
- [UPLO schemas](https://uplo.ai/schemas) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, MCP tool calls] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call UPLO MCP tools for search, GraphRAG, directives, organizational context export, and document flagging.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
