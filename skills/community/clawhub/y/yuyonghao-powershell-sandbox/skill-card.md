## Description: <br>
Runs PowerShell scripts through a restricted sandbox workflow with command allowlisting, timeout controls, output limits, static checks, and working-directory isolation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to run or prepare PowerShell script execution with timeout, output, command, and path controls. Review is required before relying on it for untrusted scripts because server security evidence says the sandbox implementation is missing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package is marked suspicious because it claims to sandbox untrusted PowerShell, but server security evidence says the actual src/sandbox.ps1 implementation is missing. <br>
Mitigation: Do not rely on it for untrusted script execution until the implementation and meaningful security tests are supplied and reviewed. <br>
Risk: PowerShell execution can affect the host environment if the sandbox boundary is incomplete or bypassed. <br>
Mitigation: Experiment only with trusted scripts in a VM or operating-system sandbox, and require explicit approval before any PowerShell execution. <br>
Risk: The documented configuration can allow network access and customize allowed commands. <br>
Mitigation: Keep network access disabled by default and review any allowlist changes before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yuyonghao-123/yuyonghao-powershell-sandbox) <br>
- [Artifact Skill Documentation](artifact/SKILL.md) <br>
- [Artifact Test Results](artifact/TEST_RESULTS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with PowerShell command examples and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes configurable timeout, output limit, working directory, network access, and command allowlist options.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata, package.json, artifact/SKILL.md, artifact/TEST_RESULTS.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
