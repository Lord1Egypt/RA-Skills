## Description: <br>
Control Xiaomi/Mi Home devices via Home Assistant REST API for lights, switches, sensors, AC, fans, media players, and scenes using natural language. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huangqiulong](https://clawhub.ai/user/huangqiulong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Home Assistant users and smart-home operators use this skill to let an agent query device state and control Xiaomi/Mi Home devices through the Home Assistant REST API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad Home Assistant authority over real smart-home devices. <br>
Mitigation: Install only when this level of device control is acceptable, use the least-privileged Home Assistant account available, and require explicit confirmation for scenes, scripts, automations, climate changes, switches, and bulk actions. <br>
Risk: A long-lived Home Assistant token can expose device control if it is pasted into chat or stored insecurely. <br>
Mitigation: Configure HA_TOKEN through a secure local channel, do not paste it into chat, and rotate any token that may already have been shared. <br>


## Reference(s): <br>
- [Home Assistant REST API](https://www.home-assistant.io/integrations/rest/) <br>
- [ClawHub skill page](https://clawhub.ai/huangqiulong/xiaomi-homne-ha) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires HA_URL and HA_TOKEN environment configuration plus curl and jq.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
