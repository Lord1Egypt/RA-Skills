## Description: <br>
Create VS Code Copilot custom Agent (.agent.md) files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create VS Code Copilot custom agent files, configure roles and tool permissions, and define handoff workflows for workspace or user-level agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated or adapted agent files may grant broad tool, MCP, handoff, or hook access. <br>
Mitigation: Review each generated agent's tools, MCP access, handoffs, and hooks before using it. <br>
Risk: User-level agents under ~/.copilot/agents can persist across workspaces. <br>
Mitigation: Use workspace-level agents when scope should be limited, and audit user-level agents before relying on them across projects. <br>


## Reference(s): <br>
- [VS Code Custom Agent Complete Format Reference](references/agent-format.md) <br>
- [ClawHub release page](https://clawhub.ai/openlark/vscode-agent-creator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with YAML frontmatter examples and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
