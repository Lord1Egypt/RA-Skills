## Description: <br>
SignalRadar monitors Polymarket prediction markets for probability changes and sends alerts when configured thresholds are crossed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vahnxu](https://clawhub.ai/user/vahnxu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use SignalRadar to add, list, check, and remove Polymarket market monitors, configure threshold-based alerts, and manage recurring market checks through the provided CLI workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically create recurring background market checks after the first market is added. <br>
Mitigation: Review the schedule immediately after setup and use the documented schedule disable command if recurring monitoring is not desired. <br>
Risk: Alert payloads and routing metadata may be sent to webhook targets or stored for later delivery. <br>
Mitigation: Configure only trusted webhook URLs or file paths, and verify delivery status before assuming background alerts are active. <br>
Risk: The authoritative security verdict is suspicious because persistence and routing storage are part of normal behavior. <br>
Mitigation: Install only when recurring monitoring and stored routing data are acceptable for the intended workspace. <br>


## Reference(s): <br>
- [SignalRadar ClawHub listing](https://clawhub.ai/vahnxu/signalradar) <br>
- [Configuration Reference](artifact/references/config.md) <br>
- [Runtime Protocol Reference](artifact/references/protocol.md) <br>
- [Operations Reference](artifact/references/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Natural-language guidance with CLI commands, structured JSON status output, and markdown alert or digest text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local watchlist, baseline, audit, schedule, and delivery state during normal CLI operation.] <br>

## Skill Version(s): <br>
1.2.0 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
