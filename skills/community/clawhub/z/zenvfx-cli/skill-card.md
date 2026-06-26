## Description: <br>
Helps agents create AI videos and manage ZenVFX canvases, nodes, files, and tasks through the ZenVFX CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lenzli](https://clawhub.ai/user/lenzli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative operators use this skill to authenticate ZenVFX, create AI video canvases, edit nodes and edges, upload project files, run generation tasks, and inspect task results from an agent session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and operates a third-party CLI that uses a ZenVFX account token. <br>
Mitigation: Install it only when you trust the ZenVFX/Tencent CLI and provide only the token needed for the intended ZenVFX work. <br>
Risk: File deletion and canvas node or edge removal commands can change or remove ZenVFX project assets. <br>
Mitigation: Verify target paths, canvas paths, node IDs, and edge IDs before running destructive commands. <br>
Risk: File upload commands can send local files into a ZenVFX project. <br>
Mitigation: Upload only files that belong in the project and avoid sensitive local files. <br>


## Reference(s): <br>
- [ZenVFX CLI on ClawHub](https://clawhub.ai/lenzli/zenvfx-cli) <br>
- [lenzli publisher profile](https://clawhub.ai/user/lenzli) <br>
- [Tencent npm registry used by install metadata](https://mirrors.tencent.com/npm/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the zenvfx CLI and ZENVFX_MCP_TOKEN on darwin or linux.] <br>

## Skill Version(s): <br>
1.0.19 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
