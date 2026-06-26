## Description: <br>
Roo Code guides agents in using the Roo Code VS Code AI programming assistant, including agent modes, file and terminal workflows, MCP integration, and model setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangifonly](https://clawhub.ai/user/zhangifonly) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to configure and operate Roo Code in VS Code for multi-step coding, architecture review, debugging, project setup, and MCP-assisted workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill describes use of a coding agent with access to the user's workspace and selected external services. <br>
Mitigation: Install only when that access is intended, and review file changes and commands before allowing them to run. <br>
Risk: MCP servers can extend the agent's reach into external tools and services. <br>
Mitigation: Use trusted MCP servers and avoid exposing high-privilege secrets. <br>
Risk: Credential-bearing integrations such as GitHub access can increase impact if tokens are over-scoped. <br>
Mitigation: Scope tokens narrowly and avoid exposing high-privilege secrets. <br>


## Reference(s): <br>
- [Roo Code on ClawHub](https://clawhub.ai/zhangifonly/roo-code) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes examples for VS Code commands, .roomodes definitions, and MCP server configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
