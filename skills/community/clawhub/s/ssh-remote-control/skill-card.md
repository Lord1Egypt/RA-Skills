## Description: <br>
Enables an AI agent running on a server to connect to and operate authorized remote Mac/Linux computers over SSH without installing agent software on the controlled machine. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lixiang92229](https://clawhub.ai/user/lixiang92229) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and operators use this skill to let an AI agent connect to authorized macOS or Linux machines over SSH for file operations, application control, system monitoring, and development tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an AI agent powerful SSH remote-control capability over configured machines. <br>
Mitigation: Install only for machines you own or are explicitly authorized to administer, and use a dedicated restricted account and dedicated SSH key. <br>
Risk: Using root/admin access or a reused private key can broaden the impact of agent mistakes or key exposure. <br>
Mitigation: Avoid root/admin access, use a dedicated key for this skill, and revoke or rotate the key when the agent no longer needs access. <br>
Risk: Leaving SSH tunneling available when it is not needed can keep a remote access path open. <br>
Mitigation: Keep tunneling off except when needed and monitor SSH logs for unexpected access. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lixiang92229/ssh-remote-control) <br>
- [Project Homepage](https://github.com/lixiang92229/skill-ssh-remote-control) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with SSH and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SSH target environment variables and a private-key path; remote effects depend on the permissions of the SSH account.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
