## Description:

Provides real-time sales coaching during live meetings, transcript reviews, and meeting preparation by detecting objections, buying signals, and deal-stage cues and returning concise actions and suggested phrases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shawnshenopeninterx](https://clawhub.ai/user/shawnshenopeninterx)

### License/Terms of Use:

MIT-0

## Use Case:

Sales professionals use this skill during live sales meetings, transcript reviews, and meeting prep to identify coaching moments and produce concise objection-handling, discovery, closing, and negotiation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use sales-related CRM records, email threads, and meeting notes without clear privacy limits or user confirmation.

Mitigation: Invoke it explicitly for each meeting, limit retrieved records to the relevant deal and participants, and avoid displaying raw confidential customer or internal content in shared meeting contexts.

Risk: Live coaching suggestions may be incomplete or inappropriate for a specific customer conversation or negotiation.

Mitigation: Treat coaching cards as decision support and require the salesperson to use judgment before repeating suggested phrases or making commitments.

## Reference(s):

- [Sales Methodologies Reference](references/methodologies.md)
- [Real-Time Coaching Cards](references/coaching-cards.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Concise Markdown coaching cards with a detected signal, recommended action, and suggested phrase.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May rely on live transcript chunks, deal-stage context, CRM records, email threads, and prior meeting notes when available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
