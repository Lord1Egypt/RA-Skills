## Description: <br>
AI-powered engineering knowledge management. Search architecture docs, API specs, incident reports, runbooks, and infrastructure documentation with structured extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RooJenkins](https://clawhub.ai/user/RooJenkins) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to search organizational architecture documents, API specifications, runbooks, incident reports, repository metadata, and technical decision records for engineering research, onboarding, incident review, and technical debt investigation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote token-backed MCP access may expose broad internal engineering context. <br>
Mitigation: Use scoped tokens, least-privilege document access, and avoid broad organization exports unless they are required for the task. <br>
Risk: Identity, clearance lookup, and activity logging may process sensitive organizational information. <br>
Mitigation: Confirm logging, retention, redaction, clearance, and audit controls with the publisher and the connected UPLO instance before deployment. <br>
Risk: Outdated or incomplete engineering documentation can mislead incident response, RFC review, or operational decisions. <br>
Mitigation: Cross-check high-impact answers against current runbooks, service owners, directives, and source systems before making production changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/RooJenkins/uplo-engineering) <br>
- [UPLO](https://uplo.ai) <br>
- [UPLO schemas](https://uplo.ai/schemas) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/RooJenkins) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include service names, repository paths, team ownership, runbook steps, escalation contacts, and links returned from the connected knowledge base.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
