## Description:

This skill analyzes audio and video from fixed cameras with microphones in shared family spaces to detect conflict events, wait for a calm window, and provide neutral aftercare suggestions or safety-resource escalation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to analyze household shared-space audio/video for conflict signals, generate structured reports, and recommend calm-window aftercare actions. It is intended for public household areas such as living rooms, kitchens, and dining rooms, with safety-resource escalation for redline events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes private household audio and video through cloud services.

Mitigation: Use only with explicit consent from affected household members and confirm where media and reports are stored, retained, and deleted.

Risk: Unsafe HTTP defaults could expose sensitive media, reports, or tokens.

Mitigation: Require HTTPS production endpoints before deployment.

Risk: Silent identity storage can cause reports to be associated with the wrong person on shared devices.

Mitigation: Review identity handling before installation and avoid shared-device identity reuse.

Risk: The skill may identify serious household safety events but is not an emergency-response system.

Mitigation: Do not rely on the skill for emergency response; route redline events to appropriate safety resources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-family-conflict-aftercare-suggest-analysis)
- [Skill demo](https://lifeemergence.com/sample.html)
- [API documentation](references/api_doc.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Structured analysis report with conflict signals, aftercare recommendations, safety-resource guidance, and report links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May output historical report lists and optional saved result files.]

## Skill Version(s):

1.0.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
