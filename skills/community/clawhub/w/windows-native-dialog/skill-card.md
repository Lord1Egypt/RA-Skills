## Description: <br>
Handles native Windows file picker dialogs from WSL2 using exec and PowerShell. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Owlock](https://clawhub.ai/user/Owlock) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users working in WSL2 use this skill to handle Windows-native file picker dialogs that browser automation cannot see, especially upload workflows that require a local Windows file selection step. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to run a Windows PowerShell command from WSL2, which could be broadened into unrelated host commands if adapted carelessly. <br>
Mitigation: Review the exact PowerShell command before first use, keep it scoped to the intended file-selection workflow, and do not allow the agent to repurpose it for unrelated host actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Owlock/windows-native-dialog) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance is scoped to Windows 10 with WSL2 and a Windows PowerShell file-selection workflow.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
