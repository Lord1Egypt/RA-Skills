## Description: <br>
AI-powered enterprise IT intelligence spanning DevOps, cybersecurity, and engineering. Unified search across infrastructure, security, and architecture documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RooJenkins](https://clawhub.ai/user/RooJenkins) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SREs, security analysts, and enterprise IT teams use this skill to search infrastructure, cybersecurity, architecture, incident, and compliance documentation through a configured UPLO knowledge base. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can retrieve sensitive infrastructure, security, and architecture documentation from the configured UPLO instance. <br>
Mitigation: Install it only with scoped MCP credentials, confirm classification-tier enforcement, and match access to the user's team and clearance. <br>
Risk: Operational recommendations may be incomplete or stale when the underlying knowledge base has gaps or outdated entries. <br>
Mitigation: Check current directives and source context before acting, and use knowledge-gap or outdated-entry reporting for missing or stale documentation. <br>
Risk: The supplied security telemetry reports no issues but notes low-confidence review conditions. <br>
Mitigation: Review the skill files and requested MCP access before installation, as recommended by the security guidance. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/RooJenkins/uplo-enterprise-it) <br>
- [UPLO](https://uplo.ai) <br>
- [UPLO Schemas](https://uplo.ai/schemas) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with inline tool calls and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a configured UPLO MCP server and should respect identity context and classification tiers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
