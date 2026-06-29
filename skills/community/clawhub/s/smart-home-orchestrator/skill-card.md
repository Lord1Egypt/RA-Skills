## Description: <br>
Smart Home Orchestrator helps an agent coordinate cross-brand smart-home devices and routines across Mi Home, HomeKit, Alexa, Google Home, MQTT, and Zigbee2MQTT environments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-gaoqian](https://clawhub.ai/user/ai-gaoqian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and smart-home operators use this skill to describe scenes, device checks, and automation rules in natural language, then have an agent translate those requests into coordinated smart-home actions or configuration guidance. It is intended for homes with mixed device ecosystems and gateway-based control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Centralized smart-home control can affect household safety, privacy, and physical devices if an action is wrong or unauthorized. <br>
Mitigation: Use least-privilege gateway tokens and require explicit user confirmation for locks, cameras, alarms, presence-based routines, and bulk actions. <br>
Risk: Gateway credentials or account passwords may expose broad device access if shared with the agent unnecessarily. <br>
Mitigation: Prefer scoped long-lived tokens, avoid password sharing where token-based access is available, and rotate credentials after testing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ai-gaoqian/smart-home-orchestrator) <br>
- [Publisher profile](https://clawhub.ai/user/ai-gaoqian) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown with YAML configuration snippets and natural-language device or scene instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include smart-home gateway configuration, scene plans, automation rules, device status guidance, and confirmation-oriented previews for sensitive actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
