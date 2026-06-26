## Description: <br>
Guides immutable OS management for Fedora Atomic and Bazzite systems using rpm-ostree layering, rollbacks, rebasing, and system upgrades. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[silverod](https://clawhub.ai/user/silverod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, Linux workstation users, and system administrators use this skill to inspect, update, layer packages on, roll back, clean up, and rebase Fedora Atomic or Bazzite rpm-ostree systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested rpm-ostree commands can make privileged system-management changes. <br>
Mitigation: Review commands before execution, inspect current deployments first, and run them only on intended rpm-ostree systems. <br>
Risk: Remote RPM installs or rebase targets can change the trusted system base. <br>
Mitigation: Verify remote RPM sources, signing expectations, and rebase image references before applying them. <br>
Risk: Cleanup, rollback, upgrade, or rebase operations can affect bootable deployments and require rebooting. <br>
Mitigation: Keep a recovery or rollback option available and confirm pending deployments before cleanup or reboot. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/silverod/rpm-ostree-toolkit) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands often require root or wheel privileges and may require rebooting to apply rpm-ostree deployment changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
