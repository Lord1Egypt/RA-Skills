## Description: <br>
Build full-stack web applications using 语构's chat-driven development platform. Manages conversations, sends development instructions, monitors build progress, extracts results (generated files, summaries, task status), publishes applications, and manages versions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yugoo](https://clawhub.ai/user/yugoo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to create, iterate, publish, and manage full-stack web applications through Yugoo's chat-driven platform and CLI workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends app prompts and selected files to a third-party Yugoo/Creo4u service. <br>
Mitigation: Install only when use of that service is intended, and avoid uploading secrets or private business data. <br>
Risk: The skill requires sensitive credentials. <br>
Mitigation: Use a revocable, least-privilege CREO4U_SKILL_API_KEY and rotate it if exposure is suspected. <br>
Risk: The skill can publish applications publicly and the security evidence notes no clear user confirmation step. <br>
Mitigation: Require explicit user approval before publishing applications or sharing production URLs. <br>
Risk: The CLI supports an --insecure option that disables TLS certificate verification. <br>
Mitigation: Use --insecure only in controlled test environments and never with real credentials. <br>


## Reference(s): <br>
- [Creo4u homepage](https://creo4u.com) <br>
- [ClawHub skill page](https://clawhub.ai/yugoo/yugoo-app-builder) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON-line CLI responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CREO4U_SKILL_API_KEY and may use uploaded files, remote project state, and publish actions through the Yugoo service.] <br>

## Skill Version(s): <br>
1.0.5 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
