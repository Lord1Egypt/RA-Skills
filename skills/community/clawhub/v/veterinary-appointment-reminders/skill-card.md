## Description:

Drafts clear US veterinary appointment reminders with prep instructions, location, and policy notes without medical advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

External veterinary clinic staff use the skill to prepare appointment reminders from clinic-provided scheduling, location, preparation, and policy details. The messages are intended for pet owners and should avoid medical advice.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The bundled script checks required fields and length limits but does not produce the promised appointment reminder.

Mitigation: Draft the reminder separately and reconcile each field against the clinic-provided details.

Risk: The script does not enforce the skill's medical-content restrictions.

Mitigation: Review the final reminder to remove medical advice and direct clinical questions to the clinic.

Risk: The optional Windows app is outside this workflow and needs separate review.

Mitigation: Do not download or run the optional app as part of this workflow unless it has been independently reviewed.

## Reference(s):

- [US veterinary appointment communication](references/vet-reminders.md)
- [Publisher homepage](https://github.com/rapidworker1)
- [ClawHub skill page](https://clawhub.ai/rapidworker1/skills/veterinary-appointment-reminders)

## Skill Output:

**Output Type(s):** [Text, Markdown, YAML configuration, Guidance]

**Output Format:** [Reminder text, a Markdown field-check report, and a YAML starter template]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script reports missing or over-limit fields; it does not generate the reminder, which must be drafted separately.]

## Skill Version(s):

1.0.7 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
