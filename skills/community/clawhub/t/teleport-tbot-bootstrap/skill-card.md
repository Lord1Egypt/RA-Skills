## Description: <br>
Bootstrap a persistent Teleport Machine ID (tbot) setup on macOS using LaunchAgent and tbot configure identity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[webvictim](https://clawhub.ai/user/webvictim) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to configure a local macOS Teleport Machine ID bot, install a user-level LaunchAgent, and verify refreshed SSH identity output for OpenClaw or agent host access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill configures a persistent macOS Teleport bot identity for the current user account. <br>
Mitigation: Install it only on accounts that should maintain automation identity refresh, and review the generated LaunchAgent plist and tbot configuration before relying on them. <br>
Risk: Onboarding tokens, registration secrets, tbot state, and identity outputs are sensitive credentials. <br>
Mitigation: Use least-privilege Teleport roles, label-scoped node access, secure secret delivery, and restricted filesystem permissions for the tbot directory and files. <br>
Risk: Cleanup commands remove LaunchAgent and tbot paths. <br>
Mitigation: Confirm removal paths point only to this skill's LaunchAgent and tbot directory before running cleanup. <br>


## Reference(s): <br>
- [Teleport tbot CLI Reference](https://goteleport.com/docs/reference/cli/tbot/) <br>
- [Teleport YAML examples](references/teleport-prereq-examples.yaml) <br>
- [LaunchAgent notes for tbot](references/launchagent-notes.md) <br>
- [ClawHub skill page](https://clawhub.ai/webvictim/teleport-tbot-bootstrap) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline shell commands and configuration file guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup steps for tbot identity configuration, LaunchAgent installation, first-run verification, and cleanup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
