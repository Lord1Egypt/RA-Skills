## Description:

Analyzes sales recordings and meeting notes to diagnose conversations, customer needs, stakeholder relationships, buying intent, and next-step coaching recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skychentian](https://clawhub.ai/user/skychentian)

### License/Terms of Use:


## Use Case:

Sales professionals and founders use this skill to review customer calls or meeting notes, identify gaps in discovery, value communication, objection handling, stakeholder coverage, and deal progression, then prepare a practical follow-up plan.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to search local customer-profile and meeting-note folders and read full customer or meeting transcripts that may contain sensitive business information.

Mitigation: Invoke it only for explicit customer-analysis tasks and limit available files to the relevant approved customer records or transcripts.

Risk: The skill can save detailed sales diagnosis reports locally, which may preserve confidential customer, investor, or internal operations material.

Mitigation: Review or disable report saving for confidential material and store any retained reports in access-controlled locations.

Risk: The skill infers stakeholder motives, relationship dynamics, decision styles, and unspoken expectations from meeting content, which may be incomplete or wrong.

Mitigation: Treat inferred relationship and intent findings as coaching hypotheses and verify them against transcript evidence before taking customer-facing action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/skychentian/skills/sales-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, analysis, guidance]

**Output Format:** [Markdown sales diagnosis report with tables, checklists, scored criteria, and action recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save a local Markdown report named by customer and date when the agent has filesystem access.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
