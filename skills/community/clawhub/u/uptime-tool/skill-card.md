## Description: <br>
Prints a basic Linux system uptime duration for quick health checks and reboot verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill for quick uptime checks and reboot verification. The bundled script provides a basic Linux uptime duration, so broader monitoring features described in the documentation should be verified before operational use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documentation describes JSON output, load averages, boot time, watch mode, alerts, compare mode, and cross-platform behavior, while the bundled script only reads /proc/uptime and prints a simple duration. <br>
Mitigation: Use the skill as a basic Linux uptime helper unless the broader options are separately implemented and tested. <br>
Risk: Security telemetry was still pending when the server evidence was generated. <br>
Mitigation: Review and scan the released artifact before deployment, especially before using it in automated monitoring workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dinghaibin/uptime-tool) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; bundled helper emits plain text uptime output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No credential access, network activity, or persistence was identified in the server security summary.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
