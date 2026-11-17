## Description:

Analyzes video of a pregnant person for prolonged standing and frequent bending, and provides fatigue-risk reminders and reports for health reference rather than diagnosis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Expecting parents and care teams can analyze home-camera video for prolonged standing and frequent bending, review rest reminders, and retrieve past reports. Results are for health reference, not medical diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive pregnancy videos and reports are sent to configured cloud services.

Mitigation: Obtain the pregnant person's clear consent and confirm the destination and handling of videos and reports before use.

Risk: Shared or automatically created identities and cached tokens can expose reports across users.

Mitigation: Use only in a single-user workspace until identity handling is fixed; protect local tokens and report access.

Risk: Posture detection can misclassify bending or standing, and fatigue reminders are not medical assessments.

Mitigation: Review results in context and seek clinical advice for health concerns rather than relying on alerts for diagnosis.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/smyx-sunjinhui/skills/smyx-pregnant-posture-fatigue-detection-analysis)
- [Skill API documentation](references/api_doc.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [JSON analysis reports or Markdown history tables with report links and rest reminders]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on clear, full-body video and do not provide a medical diagnosis.]

## Skill Version(s):

1.0.11 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
