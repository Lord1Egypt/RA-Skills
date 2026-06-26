## Description: <br>
Securely connect to remote systems via SSH for server management, file transfer, and tunneling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to have an agent prepare SSH client usage for connecting to remote hosts, running remote commands, forwarding ports, and transferring files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help form SSH commands that connect to remote systems or execute remote commands. <br>
Mitigation: Review the destination host and every remote command before allowing execution, especially for production systems. <br>
Risk: SSH usage can involve sensitive keys, credentials, or port forwarding. <br>
Mitigation: Use least-privilege SSH identities, protect private keys, and confirm any port-forwarding options before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dinghaibin/ssh-tool) <br>
- [Publisher profile](https://clawhub.ai/user/dinghaibin) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include SSH destinations, remote commands, port-forwarding options, and file-transfer command patterns for user review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
