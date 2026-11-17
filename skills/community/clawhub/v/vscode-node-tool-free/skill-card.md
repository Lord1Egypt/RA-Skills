## Description: <br>
VSCode节点工具免费版 helps agents operate a connected VSCode or Cursor IDE through a node protocol for file operations, language feature lookup, editor state inspection, diagnostics, and basic Git queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to let an agent inspect and operate a connected VSCode or Cursor workspace for routine development tasks such as reading files, applying edits, looking up definitions or references, checking diagnostics, and reviewing Git status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents using this skill can write, edit, delete, or rename files through connected IDE nodes. <br>
Mitigation: Keep gateway allowCommands narrow, default to read-only commands, and require explicit user approval before file-changing operations. <br>
Risk: The skill's remote IDE control surface may affect sensitive repositories if connected broadly. <br>
Mitigation: Install only for intended VSCode or Cursor workspaces and avoid connecting repositories that should not be modified by an agent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/vscode-node-tool-free) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, markdown] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce commands that invoke connected IDE nodes and structured JSON responses from those node operations.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
