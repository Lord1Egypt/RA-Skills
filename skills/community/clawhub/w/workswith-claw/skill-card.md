## Description:

Workswith Claw is a local smart-home middleware service that uses the Home Assistant API for device control, semantic device understanding, habit learning, and proactive automation suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fanyur-wang](https://clawhub.ai/user/fanyur-wang)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and smart-home operators use this skill to run a local backend that connects OpenClaw-style user intents to Home Assistant device state, scenes, dashboards, and automation suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The service exposes home data and automation controls with insufficient authentication.

Mitigation: Run only on a trusted, firewalled host; require authentication before exposing any API or dashboard; and keep the dashboard and API off public networks.

Risk: Home Assistant tokens and other smart-home credentials may be handled unsafely.

Mitigation: Use HTTPS for Home Assistant, store tokens as local environment secrets, rotate any token entered into the dashboard, and avoid host networking unless necessary.

Risk: Automation creation can change real smart-home behavior.

Mitigation: Treat occupancy, device inventory, and automation creation as administrator-only capabilities and review generated automation YAML before enabling it.

## Reference(s):

- [Workswith Claw ClawHub page](https://clawhub.ai/fanyur-wang/skills/workswith-claw)
- [Home Assistant installation guide](https://www.home-assistant.io/installation/raspberry-pi)
- [Xiaomi Home Assistant integration](http://github.com/xiaomi/ha_xiaomi_home)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands, Python service code, YAML configuration, and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate or modify local Home Assistant automation YAML when configured and invoked by the running service.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
