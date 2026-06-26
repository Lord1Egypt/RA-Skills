## Description: <br>
AI-powered media knowledge management. Search content production records, licensing agreements, distribution data, and audience analytics with structured extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RooJenkins](https://clawhub.ai/user/RooJenkins) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Media, rights, production, and distribution teams use this skill to search organizational knowledge about content rights, production records, licensing agreements, audience analytics, and related ownership context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive media, licensing, strategy, and talent information through the configured UPLO instance. <br>
Mitigation: Install only for trusted UPLO instances and MCP server packages, and use a least-privilege UPLO token. <br>
Risk: Automatic identity, directive, or broad organization-context lookups may expose more internal context than a task requires. <br>
Mitigation: Disable or narrow automatic lookups and broad organization exports unless the current task explicitly requires them. <br>
Risk: Rights, licensing, and talent information can be confidential or time-sensitive. <br>
Mitigation: Respect classification tiers, check validity or expiration fields, and verify material terms with the responsible owner before acting. <br>
Risk: Knowledge-base update proposals may introduce incorrect or misleading records if accepted without review. <br>
Mitigation: Review proposed updates and scan the skill before deployment or record changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/RooJenkins/uplo-media) <br>
- [UPLO](https://uplo.ai) <br>
- [UPLO schemas](https://uplo.ai/schemas) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and MCP tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a configured UPLO MCP server, UPLO instance URL, and least-privilege API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
