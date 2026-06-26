## Description: <br>
Start VS Code Remote Tunnel in Docker containers for remote terminal access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[listky](https://clawhub.ai/user/listky) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to start, stop, inspect, and log VS Code Remote Tunnel sessions inside Linux Docker containers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable VS Code Remote Tunnel access to the current container. <br>
Mitigation: Install and run it only when that access is intended, authorize with the correct Microsoft account, and use the stop or status commands when finished. <br>
Risk: Authorization codes and tunnel logs may be sensitive. <br>
Mitigation: Treat displayed authorization information and log output as sensitive and avoid sharing them outside the intended operator workflow. <br>
Risk: The script downloads and executes the VS Code CLI at runtime. <br>
Mitigation: Use it only in environments where runtime downloads from the VS Code CLI endpoint are allowed by policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/listky/vscode-tunnel) <br>
- [VS Code CLI download endpoint](https://code.visualstudio.com/sha/download?build=stable&os=cli-alpine-x64) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and terminal output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May surface VS Code Remote Tunnel authorization details and live tunnel logs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
