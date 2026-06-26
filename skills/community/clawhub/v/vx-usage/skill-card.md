## Description: <br>
Teaches AI agents how to use vx, the universal development tool manager, for tool execution, project setup, token-efficient workflows, MCP integration, and GitHub Actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loonghao](https://clawhub.ai/user/loonghao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to guide AI agents working in vx-managed projects, including tool execution, project setup, Git/GitHub workflows, MCP configuration, and CI usage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can steer agents toward vx commands that install tools, update local caches, change project files, or alter CI/MCP configuration. <br>
Mitigation: Confirm the project is vx-managed and approve environment-changing commands such as vx install, vx sync, vx setup, vx lock, and vx ai setup before execution. <br>
Risk: The skill includes Git and GitHub workflows that may mutate repositories or use token-bearing integrations. <br>
Mitigation: Review repository state, intended branch or pull request, and token scope before allowing vx git, vx gh, or GitHub Actions changes. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/loonghao/vx-usage) <br>
- [Publisher profile](https://clawhub.ai/user/loonghao) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell, TOML, JSON, YAML, Dockerfile, and Starlark examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; no executable payload is included in the artifact.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
