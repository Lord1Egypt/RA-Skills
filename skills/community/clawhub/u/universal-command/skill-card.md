## Description: <br>
Defines a reusable command pattern for building Supernal commands once and exposing them across CLI, API, and MCP surfaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ianderrington](https://clawhub.ai/user/ianderrington) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill when defining Supernal commands or tools that need consistent CLI, API, and MCP interfaces from a single command definition. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The referenced npm package may not be the intended dependency or may drift over time. <br>
Mitigation: Confirm @supernal/universal-command is the intended package before installation and use a lockfile or pinned version. <br>
Risk: Commands exposed through API or MCP surfaces can modify important data if access is too broad. <br>
Mitigation: Expose only intended commands and add authorization, auditing, and human review for commands that create, delete, publish, or modify important data. <br>


## Reference(s): <br>
- [@supernal/universal-command npm package](https://www.npmjs.com/package/@supernal/universal-command) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with TypeScript and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; no runtime credentials were detected in evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
