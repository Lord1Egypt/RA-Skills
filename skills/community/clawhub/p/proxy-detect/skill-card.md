## Description: <br>
Detects active system proxy settings on Windows and macOS, tests proxy availability, and returns results in JSON format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[noah-smith-max](https://clawhub.ai/user/noah-smith-max) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to check whether a machine has an active proxy configuration and to capture the detected proxy address and activity status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can reveal whether a machine uses an active proxy and what address or local port it uses. <br>
Mitigation: Install and run it only where exposing proxy configuration to the agent is acceptable. <br>
Risk: Release provenance is unavailable, limiting supply-chain assurance. <br>
Mitigation: Review the disclosed script before use in environments that require strong provenance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/noah-smith-max/proxy-detect) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, JSON] <br>
**Output Format:** [Markdown guidance with shell commands; runtime output includes JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The reported JSON contains a proxy address and an active-status boolean.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
