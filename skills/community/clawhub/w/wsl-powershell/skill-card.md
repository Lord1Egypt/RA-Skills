## Description: <br>
Control Windows PowerShell from WSL by executing commands and scripts on the Windows host using mounted Windows executables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TYzzt](https://clawhub.ai/user/TYzzt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents working inside WSL use this skill to run Windows PowerShell commands, execute PowerShell script files, inspect Windows system state, and manage Windows files, processes, services, and network information from a Linux agent session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad control over Windows PowerShell on the host from WSL. <br>
Mitigation: Install only when host-level Windows control is intended, review commands before execution, and require explicit approval for file changes, process control, program launches, execution-policy bypasses, or administrator prompts. <br>
Risk: PowerShell scripts or commands from untrusted sources can alter system files or run unwanted programs. <br>
Mitigation: Avoid untrusted scripts, prefer the reviewed ClawHub package over live downloads, and test commands before production use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/TYzzt/wsl-powershell) <br>
- [Windows Subsystem for Linux documentation](https://docs.microsoft.com/en-us/windows/wsl/) <br>
- [PowerShell project](https://github.com/PowerShell/PowerShell) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash and PowerShell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include Windows command results, process or service listings, filesystem changes, and command diagnostics from PowerShell.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
