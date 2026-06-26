## Description: <br>
SSH远程自动化工具 - 会话管理、隧道、文件传输。使用场景：需要远程执行命令、建立SSH隧道、传输文件时。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YKaiXu](https://clawhub.ai/user/YKaiXu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, operators, and agents use this skill to automate SSH sessions, run approved remote commands, create SSH tunnels, and transfer files with SFTP. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent run commands and transfer files on remote machines. <br>
Mitigation: Use a least-privilege SSH account, avoid root access, and approve each command and file operation before execution. <br>
Risk: SSH credentials or private keys may be exposed if hardcoded into code or test configuration. <br>
Mitigation: Store secrets in environment variables or key files, avoid passwords where possible, and do not commit real host, user, password, or key material. <br>
Risk: Remote port forwarding can expose services more broadly than intended. <br>
Mitigation: Review every tunnel request, bind forwarded ports narrowly, and verify the remote bind address before enabling remote forwarding. <br>
Risk: Host identity is not proven by this context. <br>
Mitigation: Verify SSH server fingerprints outside the agent workflow before allowing the skill to connect. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/YKaiXu/rssh2) <br>
- [ssh2 dependency package](https://registry.npmjs.org/ssh2/-/ssh2-1.17.0.tgz) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with JavaScript code snippets and SSH/SFTP operation results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces remote command results, tunnel configuration guidance, and file transfer operation outputs.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
