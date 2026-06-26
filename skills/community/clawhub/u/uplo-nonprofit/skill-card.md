## Description: <br>
AI-powered nonprofit knowledge management. Search grant documentation, donor records, program reports, and compliance data with structured extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RooJenkins](https://clawhub.ai/user/RooJenkins) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Nonprofit staff, grant writers, development teams, finance staff, and program leaders use this skill to search organizational knowledge, extract grant and program data, prepare reports, and identify missing documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive donor, grant, board, compliance, and funder information through a connected UPLO deployment. <br>
Mitigation: Install only for trusted UPLO deployments, use least-privilege UPLO tokens, and confirm classification-tier enforcement before use. <br>
Risk: Full organizational exports and relationship notes may expose confidential information beyond the immediate task. <br>
Mitigation: Restrict full organizational exports, avoid unnecessary logging of donor or funder call notes, and apply clear retention and access-control rules. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/RooJenkins/uplo-nonprofit) <br>
- [UPLO](https://uplo.ai) <br>
- [UPLO schemas](https://uplo.ai/schemas) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with MCP tool calls, configuration snippets, and structured text responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May surface sensitive nonprofit records according to the connected UPLO deployment and access controls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
