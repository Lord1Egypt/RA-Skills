## Description: <br>
Copies files from remote Windows, macOS, or Linux machines to a local Mac over SSH/SCP, with path conversion, connection diagnostics, and troubleshooting guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[taogehengq](https://clawhub.ai/user/taogehengq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical users use this skill to generate SSH/SCP transfer commands, convert remote paths across Windows, macOS, and Linux conventions, and diagnose failed remote-copy attempts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SSH commands may use unsafe defaults that weaken host authenticity checks. <br>
Mitigation: Review generated commands before execution and prefer verified host keys instead of disabling strict host key checking. <br>
Risk: Password-based examples can expose credentials when passwords are passed on the command line. <br>
Mitigation: Prefer key-based authentication and use interactive or otherwise secure credential handling when passwords are unavoidable. <br>
Risk: Remote SSH setup and firewall guidance can broaden access to the remote machine. <br>
Mitigation: Apply restricted firewall rules, enable SSH only where needed, and confirm the remote account and destination paths before transferring data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/taogehengq/remote-copy) <br>
- [Publisher profile](https://clawhub.ai/user/taogehengq) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include SSH diagnostics, OS-specific setup steps, SCP/rsync/tar command variants, and local destination paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact version section) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
