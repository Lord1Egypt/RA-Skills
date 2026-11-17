## Description:

Use this skill when a nurse, charge nurse, or clinical educator needs to convert raw shift notes into a structured SBAR handoff packet for shift change, intra-facility transfer, or provider escalation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

External clinical users such as nurses, charge nurses, and clinical educators use this skill to turn de-identified raw shift notes into a draft SBAR handoff packet for shift change, transfer, provider escalation, or charge-nurse rounding. The output is intended for licensed-nurse review against the chart, patient, and facility policy before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Clinical handoff content can be incomplete, incorrect, or inconsistent with the patient chart.

Mitigation: Treat every output as a draft and require a licensed nurse to verify it against the chart, patient, and facility policy before handoff.

Risk: Patient identifiers or protected health information could be pasted into the agent conversation.

Mitigation: Remove patient identifiers before use; the skill includes a de-identification gate and stops when identifiers are present.

Risk: The draft could be mistaken for clinical advice or a replacement for nursing judgment.

Mitigation: Use the skill only to restate and organize supplied facts, with no medication dosing, titration, diagnosis, lab interpretation, charting, transmission, or storage.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown SBAR handoff draft with checklists and unresolved-information sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires de-identified input and labels all generated handoffs as drafts requiring nurse review.]

## Skill Version(s):

0.1.2 (source: server release evidence and changelog, released 2026-05-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
