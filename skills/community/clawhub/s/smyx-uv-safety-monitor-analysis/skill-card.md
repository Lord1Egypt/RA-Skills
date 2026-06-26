## Description: <br>
AI-powered UV disinfection safety monitor for pets that analyzes camera inputs for pet presence and UV lamp activity, then returns a safety-risk report with alerts, shutoff recommendations, and report history support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and facility operators use this skill to analyze smart-home or facility video for pet entry into UV disinfection zones and receive structured safety alerts, device-action recommendations, and cloud report links. It is intended for safety monitoring support, not medical advice or a guaranteed physical UV-lamp shutoff system. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Home, pet, or room videos may be processed by an external cloud service. <br>
Mitigation: Install and use only when users consent to external cloud processing of household video content. <br>
Risk: The skill may silently create or reuse an account identity and query account-linked report history. <br>
Mitigation: Confirm the publisher provides clear controls for consent, token deletion, and report data removal before deployment. <br>
Risk: The UV safety-monitor claims are broader than the code support and should not be treated as a complete real-time safety system. <br>
Mitigation: Use the output as safety-monitoring support only, and require independently verified physical UV-lamp controls for any automatic shutoff workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-uv-safety-monitor-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [API documentation](references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown safety reports with optional JSON details and report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May upload user-provided video or image inputs to an external cloud service and query account-linked report history.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
