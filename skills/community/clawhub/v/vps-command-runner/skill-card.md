## Description: <br>
Run commands across multiple VPS simultaneously to execute SSH commands, deploy updates, check logs, and manage services across servers from one place. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chmikiro](https://clawhub.ai/user/chmikiro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage their own VPS fleet by running SSH commands, status checks, service updates, and deployment tasks across one or more hosts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad remote command execution can change services, containers, files, users, firewall rules, or deployments across multiple VPS hosts. <br>
Mitigation: Require explicit approval for state-changing commands and test commands on one host before running them across the fleet. <br>
Risk: Password-based sshpass flows and disabled host key checking weaken SSH credential and host authenticity protections. <br>
Mitigation: Replace password flows with least-privilege SSH keys or a secure secret source and keep host key verification enabled. <br>
Risk: Host inventory and credentials may be exposed if edited directly into shared skill scripts. <br>
Mitigation: Store host inventory and secrets outside the shared skill and inject them from a secure local source at runtime. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and shell script references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-supplied VPS inventory and SSH credentials before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
