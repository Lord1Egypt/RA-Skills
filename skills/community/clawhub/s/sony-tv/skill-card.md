## Description: <br>
Control Sony Bravia TV via IP Control protocol. Send IRCC remote commands, open URLs in TV browser, kill apps, and run diagnostics. Use when controlling a Sony TV on the local network. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yardfarmer](https://clawhub.ai/user/yardfarmer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and smart-home operators use this skill to control Sony Bravia TVs on a local network, generate IRCC and REST commands, open URLs in the TV browser, and run browser diagnostics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill publishes a TV control key and local network target values. <br>
Mitigation: Replace the hardcoded IP address and PSK with private configuration before use, then rotate the exposed PSK. <br>
Risk: The optional LAN diagnostic and control server is unauthenticated. <br>
Mitigation: Avoid running it on a shared LAN unless authentication is added or the service is bound to localhost. <br>
Risk: URL-opening, app-kill, and power commands can change the state of a real TV. <br>
Mitigation: Require explicit user intent before issuing these commands and use the skill only with TVs and networks the user controls. <br>


## Reference(s): <br>
- [Sony Tv ClawHub release](https://clawhub.ai/yardfarmer/sony-tv) <br>
- [Sony TV browser diagnostic report](artifact/docs/diag-report.md) <br>
- [Sony TV browser diagnostic results](artifact/docs/diag-results.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JavaScript snippets, and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce commands that control a local Sony TV when executed by an agent or user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
