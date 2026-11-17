## Description:

Converts human reminder requests in Vietnamese or English into structured JSON reminder data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anhducna](https://clawhub.ai/user/anhducna)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn reminder requests into a raw JSON object with title, datetime, recurrence, priority, and optional note fields. It also supports user-specified output field names and delegates lunar-date conversion to a separate lunar-convert skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate on broad scheduling language and produce reminder JSON when the user's intent is ambiguous.

Mitigation: Review the generated JSON before passing it to a downstream reminder or scheduling system.

Risk: Lunar-calendar reminder requests depend on a separate lunar-convert skill and may be wrong if that skill is unavailable or unreviewed.

Mitigation: Install and review the lunar-convert skill separately before using lunar-date reminders.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/anhducna/skills/reminder-agent)
- [Publisher Profile](https://clawhub.ai/user/anhducna)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Raw JSON object, or one concise clarification question when required fields are missing]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default schema contains title, datetime, recurrence, priority, and note; custom output preserves requested field names.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
