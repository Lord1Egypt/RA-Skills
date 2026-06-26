## Description: <br>
Control and monitor Tesla vehicles through the Tessie API for battery, range, location, climate, charging, drive history, and vehicle-state tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baanish](https://clawhub.ai/user/baanish) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users with Tessie-linked Tesla accounts use this skill through an agent to retrieve vehicle status, location, drive history, and charging details, and to issue remote vehicle commands such as climate and charging actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Tessie API key can expose sensitive vehicle data and enable remote vehicle commands if mishandled. <br>
Mitigation: Store the key as a secret or environment variable, avoid sharing logs or screenshots that may include vehicle data, and rotate the key if it is exposed. <br>
Risk: Vehicle location and drive history are sensitive personal data. <br>
Mitigation: Return location or trip details only when the user asks for them and keep those outputs within trusted conversations. <br>
Risk: Remote actions such as climate and charging commands can change the vehicle state. <br>
Mitigation: Review the requested action and target vehicle context before allowing an agent to run control commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/baanish/tessie) <br>
- [Tessie developer credentials](https://tessie.com/developers) <br>
- [Tessie developer documentation](https://developer.tessie.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text command output with concise Markdown setup and usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Tessie API key and a Tesla account linked to Tessie.] <br>

## Skill Version(s): <br>
2.0.3 (source: server release metadata, created 2026-01-14) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
