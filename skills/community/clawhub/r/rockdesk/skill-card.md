## Description:

Lets an agent operate an authorized remote computer through RockDesk, including its shell, files, screen, clipboard, and device connections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rockdesk-io](https://clawhub.ai/user/rockdesk-io)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to operate a RockDesk-enabled computer they own or are authorized to control, including running commands, transferring files, and managing remote peripherals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation guidance includes advice that could bypass executable screening, while some downloads are unpinned and the scan was incomplete.

Mitigation: Do not bypass executable screening; verify the publisher and integrity of installers and packages, and consider the incomplete scan before installing.

Risk: Remote shell, file, clipboard, and device operations can affect or expose data on another computer.

Mitigation: Operate only machines you own or are authorized to control, follow the peer's permission settings, and treat clipboard history as sensitive.

Risk: A background service may remain enabled and keep running.

Mitigation: Review whether you want the service enabled to keep running before installation or activation.

## Reference(s):

- [RockDesk download page](https://rockdesk.io/#download)
- [RockDesk Remote Control on ClawHub](https://clawhub.ai/rockdesk-io/skills/rockdesk)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands operate through the RockDesk application on the local and remote machines.]

## Skill Version(s):

1.0.21 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
