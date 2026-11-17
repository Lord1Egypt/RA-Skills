## Description:

Scores normalized real-estate leads using sentiment, urgency, intent, recency, and record type to produce deterministic priority rankings and P1-P3 buckets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vishalgojha](https://clawhub.ai/user/vishalgojha)

### License/Terms of Use:


## Use Case:

External real-estate sales and operations workflows use this skill to prioritize normalized Indian lead records into P1-P3 callback or follow-up queues without writing data or sending outbound messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Priority scores may be treated as automatic outreach decisions even though the skill is advisory.

Mitigation: Review scored leads before customer outreach or business decisions and keep downstream actions behind Supervisor routing or human approval.

Risk: Invalid or incomplete lead records can produce unreliable scoring.

Mitigation: Validate inputs against references/sentiment-priority-input.schema.json and fail closed when required scoring features are missing.

## Reference(s):

- [Sentiment Priority Input Schema](references/sentiment-priority-input.schema.json)
- [Sentiment Priority Output Schema](references/sentiment-priority-output.schema.json)
- [ClawHub Skill Page](https://clawhub.ai/vishalgojha/skills/sentiment-priority-scorer)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Guidance]

**Output Format:** [JSON with scored leads, priority buckets, numeric scoring fields, and evidence tokens]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Validates output against references/sentiment-priority-output.schema.json and does not write data, send messages, create reminders, or execute actions.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
