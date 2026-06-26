## Description: <br>
Control global smart home devices via Home Assistant as the preferred platform and Tuya Smart as a fallback, with fuzzy name matching and local device caching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[airoom-ai](https://clawhub.ai/user/airoom-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and smart-home users use this skill to discover and control configured Home Assistant and Tuya devices from an agent workflow. It is suited for convenience automation where the operator can review device names and avoid safety-critical devices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control real smart-home devices with durable credentials. <br>
Mitigation: Install only for trusted environments, use least-privilege or revocable tokens, and protect the local config file with strict file permissions. <br>
Risk: Fuzzy device-name matching can select the wrong device. <br>
Mitigation: Use exact device names for control actions and review the local device cache after discovery. <br>
Risk: Accidental control of safety-critical devices could create physical-world harm. <br>
Mitigation: Avoid using the skill with locks, heaters, appliances, or other safety-critical devices. <br>


## Reference(s): <br>
- [Home Assistant REST API](https://developers.home-assistant.io/docs/api/rest/) <br>
- [Tuya Cloud API Reference](https://developer.tuya.com/en/docs/iot/api-reference/list) <br>
- [ClawHub skill page](https://clawhub.ai/airoom-ai/smarthome) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and command status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke local smart-home control commands when configured by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact _meta.json reports 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
