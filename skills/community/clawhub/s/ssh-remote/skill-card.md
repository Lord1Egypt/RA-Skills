## Description: <br>
Connect to remote Linux servers through SSH and execute commands non-interactively. Covers password authentication, key authentication, file transfer, and cross-platform usage on Windows with Git Bash, macOS, and Linux. Use when the user needs remote server login or remote command execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agilebuilder](https://clawhub.ai/user/agilebuilder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to prepare SSH, SCP, key-authentication, and remote-command workflows for Linux servers from non-interactive agent sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote SSH guidance can target the wrong host, user, or command if connection details are not reviewed. <br>
Mitigation: Review every hostname, username, and command before execution, and prefer non-root accounts where possible. <br>
Risk: Bypassing host key checks can expose a connection to man-in-the-middle risk. <br>
Mitigation: Verify host keys for production servers and reserve host-key bypass options for temporary access where the user accepts the risk. <br>
Risk: Plaintext passwords in temporary scripts or command lines can be exposed. <br>
Mitigation: Prefer SSH keys for long-term access, avoid hard-coded passwords, restrict temporary password files, and delete them immediately after use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agilebuilder/skills/ssh-remote) <br>
- [Server-resolved GitHub provenance](https://github.com/agilebuilder/dev-skills/tree/master/skills/ssh-remote) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell and PowerShell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes SSH host key, password handling, and temporary file safety guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
