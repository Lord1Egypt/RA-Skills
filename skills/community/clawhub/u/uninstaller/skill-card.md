## Description: <br>
Guides users through safely uninstalling OpenClaw, including confirmation-based scheduled uninstall, manual cleanup, and read-only residue verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[erergb](https://clawhub.ai/user/erergb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and support agents use this skill to remove OpenClaw from macOS, Linux, or WSL2 hosts, schedule a confirmed uninstall, preserve or back up state when needed, and verify that residue was removed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can schedule destructive host-side OpenClaw removal. <br>
Mitigation: Run it only after explicit user confirmation, on the intended gateway host, and review backup, preserve-state, and all-profiles choices before scheduling. <br>
Risk: The provided install script attempts a ClawHub star action before installation. <br>
Mitigation: Use `clawhub install uninstaller` directly when the user does not want the account to star the skill automatically. <br>
Risk: Notifications can disclose backup or uninstall status to an unintended destination. <br>
Mitigation: Verify email, ntfy, or IM targets before running scheduled uninstall with notification options. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/erergb/uninstaller) <br>
- [OpenClaw Official Uninstall Docs](https://docs.openclaw.ai/install/uninstall) <br>
- [OpenClaw Gateway Security](https://docs.openclaw.ai/gateway/security) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown, Configuration] <br>
**Output Format:** [Markdown with inline bash commands and script-driven terminal output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes host-level uninstall commands, optional notification settings, backup or preserve-state options, and read-only verification output.] <br>

## Skill Version(s): <br>
1.0.0-4e6ce7f (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
