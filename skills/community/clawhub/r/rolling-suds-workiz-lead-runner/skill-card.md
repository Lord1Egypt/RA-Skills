## Description:

A read-only workflow for reviewing Rolling Suds Workiz leads and associated client data, validating required fields, and producing lead summaries, cleaned intake, estimates when possible, Workiz-ready notes, and manual-review flags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mwdearing](https://clawhub.ai/user/mwdearing)

### License/Terms of Use:

MIT-0

## Use Case:

Rolling Suds operators or agents use this skill to process current-day, specified-day, pasted, or exported Workiz lead and client data in a read-only review flow. It helps preserve the Workiz Lead #, identify missing required address data, and prepare downstream intake, estimate, note, and manual-review outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may expose Workiz lead and connected client details to the agent and downstream Rolling Suds skills.

Mitigation: Install and use it only in contexts where sharing those lead and client details with the agent workflow is approved.

Risk: Future Workiz API use could exceed the reviewed read-only posture if write access is added later.

Mitigation: Keep API activity read-only unless a later skill version is explicitly updated and reviewed for write access.

## Reference(s):

- [Default design](references/default-design.md)
- [Iteration notes](references/iteration-notes.md)
- [Version history](references/version-history.md)
- [Workiz developer documentation](https://developer.workiz.com)
- [ClawHub skill page](https://clawhub.ai/mwdearing/skills/rolling-suds-workiz-lead-runner)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with structured lead-by-lead sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves provided Workiz Lead # values and stops estimate generation when required address data is missing.]

## Skill Version(s):

0.1.6 (source: server release evidence and artifact version history)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
