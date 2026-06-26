## Description: <br>
WSL to Windows bridge for OpenClaw agents that proposes shell commands and configuration for invoking Windows Python, PowerShell, CMD, path conversion, and file copy workflows from WSL2. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deaconhan](https://clawhub.ai/user/deaconhan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure WSL2 environments so agents can call Windows-side tools, run Windows Python scripts, execute PowerShell or CMD commands, and move files across WSL and Windows paths. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives WSL agents broad Windows command and file access that is not well bounded or clearly controlled. <br>
Mitigation: Install only when this host-level access is intentional, review setup.sh first, and require explicit approval before destructive file changes, Windows process control, trading tools, or account-related directories. <br>
Risk: The reviewed package advertises win-* wrappers that are not included in the artifact. <br>
Mitigation: Verify the installed package contents and wrapper availability before relying on the commands in production workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/deaconhan/wsl-windows-bridge) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that execute Windows programs or modify Windows-accessible files when run by an agent.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
