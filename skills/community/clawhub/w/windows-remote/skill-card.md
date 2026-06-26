## Description: <br>
Control remote Windows machines via SSH for command execution, GPU checks, script runs, and file transfer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoyaner0201](https://clawhub.ai/user/xiaoyaner0201) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to administer a configured Windows host over SSH, including running commands and scripts, checking NVIDIA GPU status, and uploading or downloading files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can execute commands and transfer files on a remote Windows machine. <br>
Mitigation: Install only for intentional Windows administration, use a dedicated least-privilege SSH account and key, and review commands and file transfers before execution. <br>
Risk: The SSH and SCP helper scripts disable host identity checks. <br>
Mitigation: Use trusted networks or a private overlay where appropriate, and consider editing the scripts to enforce known_hosts verification before use. <br>


## Reference(s): <br>
- [Windows Remote on ClawHub](https://clawhub.ai/xiaoyaner0201/windows-remote) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ssh plus WINDOWS_SSH_HOST and WINDOWS_SSH_USER environment configuration; optional SSH port, key path, and timeout settings are supported.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
