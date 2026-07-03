## Description: <br>
Smart Home IoT Control helps agents manage and automate smart-home devices across Home Assistant, Mi Home, Tuya Smart, SmartThings, HomeKit, and common IoT protocols. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-gaoqian](https://clawhub.ai/user/ai-gaoqian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent discover, monitor, and control smart-home devices through natural language. It can help create scenes, schedules, status checks, and energy-management recommendations across supported platforms. <br>

### Deployment Geography for Use: <br>
Global, with Mi Home support noted for China/Asia. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give agents broad control over locks, security systems, thermostats, and appliances. <br>
Mitigation: Use it only with accounts and devices the operator is willing to let an agent control, and require explicit confirmation for safety-sensitive actions. <br>
Risk: OAuth tokens and sensitive smart-home credentials could grant wider access than intended. <br>
Mitigation: Prefer limited-role credentials, narrow automation scopes, and audit logs for agent-controlled actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ai-gaoqian/smart-home-iot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Configuration, Guidance] <br>
**Output Format:** [Markdown with YAML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include device actions, scene definitions, schedules, status summaries, and warnings for safety-sensitive devices.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
