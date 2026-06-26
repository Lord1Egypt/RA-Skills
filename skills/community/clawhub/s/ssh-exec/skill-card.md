## Description: <br>
Run a single command on a remote Tailscale node via SSH without opening an interactive session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Xejrax](https://clawhub.ai/user/Xejrax) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to have an agent run one-off SSH commands or pipe a local script to a configured remote Tailscale host. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables remote command execution over SSH, so an agent could run an unintended command or target the wrong host if inputs are not reviewed. <br>
Mitigation: Use least-privilege SSH keys and accounts, verify the target host and port, and review each command or local script before allowing execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Xejrax/ssh-exec) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an ssh binary and SSH access to the configured remote host.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
