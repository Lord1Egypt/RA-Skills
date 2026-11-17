## Description:

Generates chronic disease follow-up visit reminders, including follow-up date calculation, overdue status, reminder state, and suggested next actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

External healthcare application developers and care teams can use this skill to turn visit dates, follow-up intervals, and disease context into patient-facing follow-up reminders. It supports chronic disease management workflows that need overdue detection, reminder status, and preparation guidance without replacing clinician scheduling or medical judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process sensitive patient or medical data and send patient context to a remote medical model.

Mitigation: Review before use in real patient or regulated healthcare settings; use only non-sensitive test data unless provider terms, retention, consent, and data-minimization controls are approved.

Risk: Free-form notes or extracted document text can contain patient identifiers.

Mitigation: Prefer JSON-only inputs with minimized fields, avoid identifiers in notes, and redact unnecessary personal or clinical details before execution.

Risk: Saved prepared inputs can persist sensitive normalized patient data.

Mitigation: Avoid --save-prepared for real records and remove any generated prepared files when testing is complete.

Risk: The skill can fall back to external shared preprocessing code outside the bundled skill.

Mitigation: Remove or verify the external _shared preprocessing fallback before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-followup-reminder)
- [Simple app features](https://docs.simple.org/readme/simple-app-features)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [UTF-8 JSON containing structured reminder data and Markdown reminder text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes calculated follow-up date, overdue status, days overdue, reminder status, and generated follow-up preparation guidance.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
