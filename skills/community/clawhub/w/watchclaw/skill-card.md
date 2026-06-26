## Description: <br>
Auto-recovery watchdog for OpenClaw gateway. Monitors health, detects bad config changes, and recovers via git stash/revert. Supports native and Docker restart modes with pluggable alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jarvis4wang](https://clawhub.ai/user/jarvis4wang) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use WatchClaw to monitor OpenClaw gateways, detect unhealthy configuration changes, and recover service through git-based rollback, native restarts, or Docker restarts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The normal install path runs unpinned remote code and downloads executables at install time. <br>
Mitigation: Review the installer and downloaded files before use, pin them to a specific commit or release, and verify checksums where possible. <br>
Risk: The daemon can modify gateway configuration state and restart services during recovery. <br>
Mitigation: Run it against a dedicated, backed-up OpenClaw config repository and validate recovery behavior before relying on it for production operations. <br>
Risk: Custom alert commands can execute shell behavior from configuration. <br>
Mitigation: Avoid custom alert commands unless the configuration file is protected and write access is restricted. <br>


## Reference(s): <br>
- [WatchClaw ClawHub page](https://clawhub.ai/jarvis4wang/watchclaw) <br>
- [jarvis4wang publisher profile](https://clawhub.ai/user/jarvis4wang) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>
- [WatchClaw install script URL](https://raw.githubusercontent.com/jarvis4wang/watchclaw/main/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with bash commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
