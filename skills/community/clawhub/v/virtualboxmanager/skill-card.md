## Description: <br>
Control and manage VirtualBox virtual machines directly from OpenClaw using VBoxManage for VM lifecycle, configuration, snapshots, cloning, networking, shared folders, and monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xFratex](https://clawhub.ai/user/0xFratex) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to administer local VirtualBox virtual machines from an agent workflow. It helps inspect VM state, start and stop guests, create snapshots, clone machines, configure networking and shared folders, and monitor VM resources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper script can turn VM names or file paths into unintended shell commands on the host. <br>
Mitigation: Review exact commands before execution and avoid untrusted VM names, file paths, snapshot names, or rule names until the helper uses argument arrays and input validation. <br>
Risk: VirtualBox administration actions can delete VMs, power off or reset guests, change networking, add shared folders, import or export appliances, or run guestcontrol operations. <br>
Mitigation: Confirm destructive or privileged VM operations before running them, keep backups or snapshots for important guests, and limit use to environments where the agent is intended to administer VirtualBox. <br>


## Reference(s): <br>
- [VirtualBox VBoxManage Manual](https://www.virtualbox.org/manual/ch08.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and TypeScript code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires VBoxManage on the host; generated commands may alter VM state, networking, storage, and shared folders.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
