## Description: <br>
Traffic Monitor helps an agent inspect local server network traffic with vnstat, generate monthly usage reports, and warn when usage approaches a configured 2 TB monthly limit. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binyuli](https://clawhub.ai/user/binyuli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and server operators use this skill to check monthly, daily, and real-time traffic on a local network interface and to surface threshold warnings for bandwidth-limited servers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local traffic-reporting commands and service-administration commands on the target server. <br>
Mitigation: Install it only on servers where local traffic monitoring is intended, and run systemctl commands only when administering the vnstat service. <br>
Risk: Traffic reports can be misleading if vnstat is not installed, trusted, running, or tracking the intended network interface. <br>
Mitigation: Verify that vnstat is trusted, active, and configured for the intended interface before relying on monthly usage reports. <br>
Risk: Heartbeat mode stores a small local state file that can affect repeated alert behavior. <br>
Mitigation: Clear the heartbeat state file if alert behavior appears stale or after intentionally resetting reporting state. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/binyuli/traffic-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documentation and human-readable terminal output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports inbound, outbound, total, remaining, and threshold status for the configured interface when vnstat data is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
