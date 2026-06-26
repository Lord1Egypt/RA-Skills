## Description: <br>
Interact with Tado smart thermostat. Use for reading temperature, setting heating with auto-revert, viewing energy usage, and controlling zones. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davek-dev](https://clawhub.ai/user/davek-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to authenticate with Tado, inspect thermostat zones, read temperatures and energy usage, and send zone overlay commands such as timed or schedule-bound heating changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tado access and refresh tokens can control the user's thermostat account if exposed. <br>
Mitigation: Store tokens only in trusted environment variables or secret storage, do not commit them, and revoke the Tado authorization when the skill is no longer needed. <br>
Risk: Temperature override commands can change real heating behavior for a home and zone. <br>
Mitigation: Confirm the home, zone, temperature, and duration before execution, and prefer timer or schedule-bound overrides over permanent manual overrides. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/davek-dev/tado-skill) <br>
- [Tado OAuth device authorization endpoint](https://login.tado.com/oauth2/device_authorize) <br>
- [Tado OAuth token endpoint](https://login.tado.com/oauth2/token) <br>
- [Tado account API endpoint](https://my.tado.com/api/v2/me) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands, Python examples, and JSON request and response snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that call Tado OAuth and thermostat APIs; users supply tokens, home IDs, and zone IDs.] <br>

## Skill Version(s): <br>
1.0.5 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
