## Description: <br>
Use when Cartograph CLI or MCP is available and you need repository orientation, task-scoped context, or doc inputs with minimal token cost. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anthony-maio](https://clawhub.ai/user/anthony-maio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to prefer Cartograph for repository orientation, task-scoped context, and documentation inputs when the Cartograph CLI or MCP server is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cartograph may read repository contents, and provider-backed documentation generation may send relevant project context to the configured provider. <br>
Mitigation: Use Cartograph only where repository access is authorized, review provider settings before provider-backed documentation generation, and prefer static local commands for sensitive repositories. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill encourages passing run IDs and artifact references instead of long prose.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
