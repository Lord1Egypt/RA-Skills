## Description: <br>
Smart Home Hub is a cross-platform smart-home control skill for managing devices, scenes, security monitoring, energy usage, automation rules, and device diagnostics across Home Assistant, Apple HomeKit, Google Home, Amazon Alexa, and Xiaomi Mi Home. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-gaoqian](https://clawhub.ai/user/ai-gaoqian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to control and monitor smart-home devices through natural language, coordinate multi-device scenes, manage automation rules, inspect energy usage, and diagnose offline or misconfigured devices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Smart-home platform access can affect safety-sensitive devices such as locks, alarms, cameras, and automation rules. <br>
Mitigation: Use least-privilege platform tokens and require explicit user confirmation before lock, alarm, camera, or automation-edit actions. <br>
Risk: Scene and automation backups may contain sensitive home configuration details. <br>
Mitigation: Review where backups are stored and restrict access to users and systems that need the data. <br>


## Reference(s): <br>
- [Smart Home Hub on ClawHub](https://clawhub.ai/ai-gaoqian/smart-home-hub) <br>
- [ai-gaoqian publisher profile](https://clawhub.ai/user/ai-gaoqian) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown smart-home operation reports with status summaries, device details, scene previews, diagnostics, and confirmation prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include per-device execution results, partial-success or failure details, troubleshooting recommendations, and backup or confirmation notes for scene and security changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
