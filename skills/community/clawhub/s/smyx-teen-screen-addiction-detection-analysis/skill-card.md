## Description: <br>
Analyzes fixed-camera video to estimate adolescent screen-use posture and duration, classify phone or game screen behavior, and produce structured reminders and reports for guardians. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze home, study-room, or school camera video for teen screen-looking posture, cumulative duration, threshold-based alerts, and guardian-facing daily summaries. The outputs are behavioral observations and reminders, not medical diagnoses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive teen-monitoring video, identifiers, account, history, and health-analysis behavior may be sent to a remote service with under-disclosed handling. <br>
Mitigation: Confirm the remote API operator, transmitted data, storage location, retention and deletion process, account behavior, and guardian plus adolescent consent before installation or use. <br>
Risk: Behavioral outputs could be mistaken for a medical or psychiatric diagnosis. <br>
Mitigation: Use outputs only as visual behavior statistics and family reminders; route suspected behavioral addiction concerns to qualified professionals. <br>
Risk: The artifact declares an invalid `yaml` dependency that may prevent installation or create dependency confusion. <br>
Mitigation: Replace `yaml` with the intended maintained package before installation. <br>


## Reference(s): <br>
- [API 接口文档](references/api_doc.md) <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/smyx-teen-screen-addiction-detection-analysis) <br>
- [Publisher profile](https://clawhub.ai/user/smyx-sunjinhui) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown summaries with structured JSON analysis fields and optional report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include posture classifications, screen-time durations, alert levels, friendly reminders, parent summaries, recommended actions, and history tables.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
