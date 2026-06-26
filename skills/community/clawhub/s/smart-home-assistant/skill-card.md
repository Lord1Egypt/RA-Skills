## Description: <br>
Monitor and analyze Home Assistant energy consumption, including power usage by room or area and draft Home Assistant automations based on power thresholds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liverock](https://clawhub.ai/user/liverock) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and smart-home operators use this skill to analyze Home Assistant power telemetry, identify high consumers by device or area, and draft threshold-based automations for manual review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Home Assistant long-lived token and reads entity, device, and area data. <br>
Mitigation: Install only if you are comfortable granting that access, and keep the token in environment-backed configuration. <br>
Risk: Generated automations can contain turn_on or turn_off actions for derived target entities if a user applies them. <br>
Mitigation: Review every generated automation, target entity, and action before use; avoid applying rules to critical appliances, safety systems, networking gear, or medical-adjacent devices. <br>


## Reference(s): <br>
- [Smart Home Assistant ClawHub release](https://clawhub.ai/liverock/smart-home-assistant) <br>
- [Skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Plain text summaries, Markdown tables, and Home Assistant automation JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only Home Assistant analysis; generated automations are drafts for manual review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
