## Description:

Log and track vital signs including blood pressure, blood sugar, weight, heart rate, and temperature. Use when users record health measurements or want to review their vitals history and trends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiwenbing](https://clawhub.ai/user/jiwenbing)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to record vitals with timestamps and units, review recent history, identify trends, and receive non-diagnostic prompts to consult a doctor for consistently abnormal readings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may handle sensitive health readings and vitals history.

Mitigation: Record only the details needed for tracking, avoid storing unnecessary context, and ask how to delete past readings.

Risk: Users could mistake range checks or trend summaries for medical diagnosis or emergency guidance.

Mitigation: Use outputs for logging and general context only; consult a clinician for abnormal readings and seek emergency help when appropriate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiwenbing/skills/vitals-log)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or plain text health log entries, trend summaries, range notes, and consultation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include timestamps, metric type, units, recent trend direction, and non-diagnostic notes for abnormal readings.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
