## Description: <br>
Control SwitchBot smart home devices (curtains, plugs, lights, locks, etc.) via SwitchBot Cloud API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daaab](https://clawhub.ai/user/daaab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People and agents managing SwitchBot-enabled spaces use this skill to set up API credentials, discover devices, control curtains, plugs, lights, locks, and humidifiers, and read device or sensor status through the SwitchBot Cloud API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform broad physical smart-home actions, including lock, unlock, plug, appliance, curtain, lighting, and humidifier control, using persistent credentials. <br>
Mitigation: Install only where ongoing SwitchBot device control from this machine is acceptable, limit available devices and commands to the intended use, and require explicit confirmation before lock, unlock, plug, appliance, or other safety-sensitive actions. <br>
Risk: The skill depends on a persistent SwitchBot token and secret stored for API access. <br>
Mitigation: Prefer a managed secret store when available; otherwise keep the credentials file owner-only, never display or log the token or secret, and rotate credentials if exposure is suspected. <br>
Risk: The raw command mode can send arbitrary SwitchBot commands beyond the typed helper flows. <br>
Mitigation: Restrict or remove raw command mode unless it is needed, and prefer the narrower list, status, curtain, and plug commands for routine operation. <br>


## Reference(s): <br>
- [SwitchBot Cloud API endpoint](https://api.switch-bot.com/v1.1) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and command-line text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided SwitchBot token and secret; command output can include device names, device IDs, status values, and API error messages.] <br>

## Skill Version(s): <br>
1.0.1 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
