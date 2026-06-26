## Description: <br>
AI-powered DevOps knowledge management for searching runbooks, infrastructure documentation, CI/CD pipelines, and incident response procedures with structured extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RooJenkins](https://clawhub.ai/user/RooJenkins) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SREs, platform engineers, and on-call responders use this skill to query UPLO-backed DevOps knowledge for runbooks, incident history, infrastructure documentation, CI/CD configurations, and migration planning. It helps answer operational questions from the organization's indexed knowledge while respecting access tiers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose broad internal infrastructure context through searches and organization exports. <br>
Mitigation: Install only with a least-privilege UPLO token, use a trusted UPLO instance, respect classification tiers, and avoid full organization exports unless there is an approved need. <br>
Risk: Incident logging or knowledge-base state changes can retain sensitive operational details. <br>
Mitigation: Require user confirmation before logging incident details, proposing updates, or changing knowledge-base state. <br>
Risk: The MCP server is installed from an external npm package. <br>
Mitigation: Review the MCP server provenance and pin an audited package version for production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/RooJenkins/uplo-devops) <br>
- [UPLO](https://uplo.ai) <br>
- [UPLO schemas](https://uplo.ai/schemas) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with tool-backed DevOps knowledge, runbook steps, incident summaries, and configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a trusted UPLO instance URL and least-privilege API key; responses depend on the connected organization's indexed knowledge and access tiers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
