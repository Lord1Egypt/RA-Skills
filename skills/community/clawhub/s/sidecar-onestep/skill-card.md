## Description: <br>
Control SidecarOneStep, a macOS Sidecar enhancement tool for one-click iPad connection, remote control, virtual display management, and MCP-based automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zy84338719](https://clawhub.ai/user/zy84338719) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Mac users and automation-focused developers use this skill to let an agent inspect and control SidecarOneStep connections, web console state, logs, and virtual display settings through mcporter and MCP. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional web control server may expose Sidecar controls if it is not localhost-only or otherwise protected. <br>
Mitigation: Check the web console's binding and protection before use, run it only on trusted networks, and stop it when finished. <br>
Risk: The skill depends on a locally installed SidecarOneStep app and its release source. <br>
Mitigation: Install only when you trust the SidecarOneStep app and the release source identified by the server evidence. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zy84338719/sidecar-onestep) <br>
- [Publisher Profile](https://clawhub.ai/user/zy84338719) <br>
- [SidecarOneStep Website](https://sidecaronestep.app.murphyyi.com/) <br>
- [SidecarOneStep Releases](https://github.com/yi-nology/sidecarOneStep/releases/latest) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and MCP tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide users through mcporter configuration and SidecarOneStep MCP calls; no generated files by default.] <br>

## Skill Version(s): <br>
1.4.1 (source: server release evidence and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
