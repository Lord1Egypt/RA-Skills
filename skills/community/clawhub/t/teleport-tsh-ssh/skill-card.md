## Description: <br>
Use Teleport tsh CLI with a Machine ID (tbot) identity file to SSH into Teleport-managed hosts or run remote commands through Teleport access controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[webvictim](https://clawhub.ai/user/webvictim) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to access Teleport-managed SSH nodes, run remote commands, list nodes, and transfer files with an explicit Machine ID identity and resolved Teleport proxy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to run remote commands or copy files through Teleport with the access granted to the selected Machine ID identity. <br>
Mitigation: Confirm the identity file and proxy before use, keep the Machine ID identity narrowly scoped, and review remote command or file-copy requests before execution. <br>
Risk: Machine ID identity files, bot state, tokens, or registration secrets could expose privileged access if committed or shared. <br>
Mitigation: Keep identity material out of source control and use explicit paths with least-privilege role mappings for automation identities. <br>


## Reference(s): <br>
- [tsh ssh reference](references/tsh-ssh-reference.md) <br>
- [Teleport tsh ssh CLI reference](https://goteleport.com/docs/reference/cli/tsh/#tsh-ssh) <br>
- [ClawHub skill page](https://clawhub.ai/webvictim/teleport-tsh-ssh) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include command output summaries, troubleshooting steps, node discovery results, and file transfer command patterns.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
