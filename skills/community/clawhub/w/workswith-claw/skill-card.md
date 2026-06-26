## Description: <br>
Workswith Claw is an independent smart-home middleware service that integrates with Home Assistant APIs for semantic device understanding, habit learning, and anticipatory automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Fanyur-Wang](https://clawhub.ai/user/Fanyur-Wang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External smart-home users and developers use this skill to run a local middleware service that connects to Home Assistant, interprets natural-language home intents, learns usage habits, and proposes or applies home automation behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Default deployment can expose Home Assistant data and control without adequate authentication or scoping. <br>
Mitigation: Install only in a tightly trusted local environment, use a non-empty API key or real authentication, and bind the service to localhost or protect it with firewall rules. <br>
Risk: Home Assistant tokens can grant meaningful control over household devices. <br>
Mitigation: Rotate and protect the Home Assistant token, avoid storing it in the dashboard, and prefer HTTPS or an isolated trusted link to Home Assistant. <br>
Risk: Generated automation YAML can create persistent smart-home behavior. <br>
Mitigation: Review generated automation YAML before enabling it. <br>
Risk: LLM or OpenClaw integrations may introduce separate privacy exposure. <br>
Mitigation: Treat any LLM or OpenClaw integration as an explicit opt-in privacy decision. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Fanyur-Wang/workswith-claw) <br>
- [Home Assistant installation documentation](https://www.home-assistant.io/installation/raspberry-pi) <br>
- [Xiaomi Home Assistant integration](http://github.com/xiaomi/ha_xiaomi_home) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, environment configuration, API behavior, and YAML automation examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate Home Assistant automation YAML and local service configuration that should be reviewed before use.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
