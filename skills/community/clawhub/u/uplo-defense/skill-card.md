## Description: <br>
AI-powered defense knowledge management. Search mission documentation, logistics records, personnel data, and ITAR-controlled information with structured extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RooJenkins](https://clawhub.ai/user/RooJenkins) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Defense program teams, logistics officers, export-control staff, and security/compliance users use this skill to search structured mission, logistics, personnel, clearance, and ITAR/EAR knowledge while preserving access-control context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles highly sensitive defense, personnel, clearance, and ITAR/EAR data. <br>
Mitigation: Install only in an approved UPLO environment for the data sensitivity, confirm server-side clearance and need-to-know enforcement, and use least-privilege tokens. <br>
Risk: The skill includes broad export and logging workflows, including export_org_context and compliance logs. <br>
Mitigation: Restrict export_org_context, define logging retention and redaction rules, and control audit-log access before connecting mission, personnel, clearance, or export-controlled data. <br>
Risk: The MCP server package is installed through an npm command at runtime. <br>
Mitigation: Pin and review the MCP package version before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/RooJenkins/uplo-defense) <br>
- [UPLO](https://uplo.ai) <br>
- [UPLO schemas](https://uplo.ai/schemas) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline tool calls, shell commands, and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May query an MCP server and produce search results, audit-oriented summaries, organizational context exports, outdated-document flags, or update proposals depending on available tools and user authorization.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
