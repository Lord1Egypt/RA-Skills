## Description: <br>
Analyzes living-room video to estimate whether an elderly person is seated on a sofa and watching TV, tracks continuous and daily viewing duration, and produces gentle activity reminders when configured sedentary thresholds are exceeded. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and elderly-care integrators use this skill to call a remote analysis service for home, nursing-home, or community-care video that tracks sofa-based TV watching duration and returns behavior statistics plus reminder text. It is intended for visual activity monitoring and friendly reminders, not medical diagnosis or treatment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive in-home video of an elderly person is sent to a remote health-analysis backend. <br>
Mitigation: Deploy only with informed consent from the monitored person or lawful guardian, and confirm the backend's storage, protection, deletion, and access-control practices before use. <br>
Risk: Reports are stored and retrieved by open-id, which may expose report history if identifiers are weak or shared. <br>
Mitigation: Use a non-secret, user-specific identifier for open-id, avoid using real API keys as identifiers, and restrict report access to authorized caregivers or operators. <br>
Risk: The skill produces health-adjacent behavior analysis that could be mistaken for medical advice. <br>
Mitigation: Present outputs as visual behavior statistics and friendly reminders only, and route medical concerns or symptoms to qualified healthcare professionals. <br>


## Reference(s): <br>
- [API interface documentation](references/api_doc.md) <br>
- [ClawHub release page](https://clawhub.ai/smyx-sunjinhui/smyx-elderly-tv-sedentary-reminder-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown tables or JSON reports with reminder text and status fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include continuous viewing duration, daily viewing totals, posture and face-orientation status, alert type, alert level, recommended action, and report links.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
