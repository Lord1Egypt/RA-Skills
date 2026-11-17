## Description:

Control and manage VirtualBox virtual machines from OpenClaw using the VBoxManage CLI for lifecycle, configuration, snapshot, cloning, shared folder, network, and monitoring workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xfratex](https://clawhub.ai/user/0xfratex)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to inspect, create, configure, start, stop, snapshot, clone, export, import, and monitor local VirtualBox virtual machines through VBoxManage commands and helper functions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can turn VM names, paths, snapshot names, and descriptions into host shell commands.

Mitigation: Use only trusted values and change the helper to argument-array execution such as execFile or spawn before accepting untrusted inputs.

Risk: VM delete, hard poweroff, snapshot restore, and snapshot delete actions can destroy state or data.

Mitigation: Require explicit user confirmation before destructive VM lifecycle or snapshot operations.

Risk: Guest control examples may expose credentials when passwords are placed directly in commands.

Mitigation: Avoid inline passwords and use safer credential handling appropriate to the host environment.

## Reference(s):

- [VirtualBox VBoxManage Manual](https://www.virtualbox.org/manual/ch08.html)
- [Virtual Box Manager on ClawHub](https://clawhub.ai/0xfratex/skills/virtualboxmanager)
- [0xfratex ClawHub Profile](https://clawhub.ai/user/0xfratex)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and TypeScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires VBoxManage to be installed and accessible to the user.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
