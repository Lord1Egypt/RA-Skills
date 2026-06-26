## Description: <br>
QMD Memory enables local hybrid memory search and embedding for OpenClaw workspaces using QMD, local models, and optional shared MCP access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[asabovetech](https://clawhub.ai/user/asabovetech) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure local memory search, refresh indexes and embeddings, estimate API cost savings, and optionally run a shared QMD MCP server for multiple agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local indexing can include sensitive markdown files from an OpenClaw workspace. <br>
Mitigation: Keep secrets out of indexed folders and review the configured QMD collections before relying on search results. <br>
Risk: Setup performs a global npm install and downloads roughly 2GB of local model files. <br>
Mitigation: Review setup.sh first, run it as a normal user rather than root, and confirm disk and network expectations before installation. <br>
Risk: The optional MCP server shares local memory over a localhost service. <br>
Mitigation: Start the server only when shared agent access is intended and confirm how to stop or remove it before enabling ongoing use. <br>


## Reference(s): <br>
- [QMD Memory on ClawHub](https://clawhub.ai/asabovetech/qmd-memory) <br>
- [QMD project](https://github.com/tobi/qmd) <br>
- [As Above Technologies](https://asabove.tech) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May configure local QMD collections, refresh local indexes, start an optional local MCP server, and report estimated savings.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release version and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
