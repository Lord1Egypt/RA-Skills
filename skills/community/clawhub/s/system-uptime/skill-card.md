## Description: <br>
Get the current system uptime using the native 'uptime' command. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alamby](https://clawhub.ai/user/alamby) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, operators, and agents use this skill to answer local system uptime and basic status questions on Unix-like systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can reveal basic local system status, including uptime, load average, and logged-in user count. <br>
Mitigation: Install only in environments where exposing this local status information is acceptable, and review use before deployment. <br>
Risk: The skill depends on the native uptime binary being available on the host. <br>
Mitigation: Confirm the target environment provides the uptime command before relying on the skill. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands] <br>
**Output Format:** [Plain text uptime output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs the local uptime command and returns its stdout.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
