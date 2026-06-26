## Description: <br>
Monitors and discovers popular skills across ClawHub, GitHub Actions, and npm with reports, usage flowcharts, and notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhdryanchang](https://clawhub.ai/user/zhdryanchang) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, teams, and skill creators use this agent to monitor tool trends across ClawHub, GitHub Actions, and npm, generate skill summaries and flowcharts, and send scheduled reports through configured notification channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A bundled SkillPay key appears in the release and should be treated as exposed. <br>
Mitigation: Replace it with an owner-controlled, rotated credential before use and do not reuse the bundled key. <br>
Risk: Notification, subscription, status, and payment callback endpoints are exposed without adequate caller or ownership scoping. <br>
Mitigation: Run the service only on localhost or behind authentication, and verify callers, payment webhooks, and destination ownership before exposing those endpoints. <br>


## Reference(s): <br>
- [Skill Discovery Monitor on ClawHub](https://clawhub.ai/zhdryanchang/skill-discovery-monitor) <br>
- [zhdryanchang ClawHub profile](https://clawhub.ai/user/zhdryanchang) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [JSON API responses, notification text, Mermaid markdown flowcharts, and setup commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results can include skill metadata, popularity metrics, feature summaries, usage flowcharts, and delivery status for Telegram, Discord, or email notifications.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, skill.json, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
