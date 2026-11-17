## Description:

WatchClaw is an auto-recovery watchdog for OpenClaw gateways that monitors health, detects bad config changes, recovers via git stash or revert, and supports native or Docker restart modes with pluggable alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jarvis4wang](https://clawhub.ai/user/jarvis4wang)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use WatchClaw to monitor an OpenClaw gateway, detect unhealthy configuration changes, recover with git stash or revert, restart native or Docker deployments, and send alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer fetches executable files from a mutable GitHub branch before the runtime can be reviewed.

Mitigation: Install only from a trusted, pinned release or locally reviewed checkout, and verify checksums before use.

Risk: WatchClaw can modify an OpenClaw configuration repository by stashing or reverting changes during recovery.

Mitigation: Run it against a dedicated OpenClaw config repository with reviewed git history and tested rollback behavior.

Risk: Docker restart mode and custom alert commands can affect host services or run operator-defined commands.

Mitigation: Avoid elevated privileges, review Docker access, and allow only trusted alert commands.

## Reference(s):

- [ClawHub WatchClaw skill page](https://clawhub.ai/jarvis4wang/skills/watchclaw)
- [jarvis4wang publisher profile](https://clawhub.ai/user/jarvis4wang)
- [OpenClaw project](https://github.com/openclaw/openclaw)
- [WatchClaw install command source](https://raw.githubusercontent.com/jarvis4wang/watchclaw/main/install.sh)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs operational commands, configuration settings, recovery-mode guidance, and status/log inspection guidance for WatchClaw.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
