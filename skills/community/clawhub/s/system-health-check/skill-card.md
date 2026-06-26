## Description: <br>
System health validator that checks skill files, paths, permissions, binaries, backup freshness, and encryption, then produces pass/fail reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[satoshistackalotto](https://clawhub.ai/user/satoshistackalotto) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw operators, system administrators, and accounting support teams use this skill to run read-only health checks before critical operations or on a schedule. It reports missing skill files, unexpected directories, insecure permissions, stale backups, stale locks, missing dependencies, and integrity or encryption concerns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads system and accounting configuration state during diagnostics. <br>
Mitigation: Review the configured data root and run it only in environments where diagnostic reads of OpenClaw state are authorized. <br>
Risk: The skill may write local diagnostic reports or failure logs despite being described as read-only. <br>
Mitigation: Confirm report generation settings before installation, and disable or redirect saved reports when a strict no-write posture is required. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/satoshistackalotto/system-health-check) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/satoshistackalotto) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell command examples and JSON report examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local diagnostic reports or failure logs when report generation is enabled.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
