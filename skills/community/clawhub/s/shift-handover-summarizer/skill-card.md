## Description:

Generate structured shift handover summaries from EHR records, highlighting critical events, vital sign changes, and pending tasks for incoming clinical staff.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Clinical staff and support agents use this skill to turn structured EHR shift records into handover summaries that prioritize patients, call out key events, summarize vitals and medications, and list pending tasks. It is intended for handover support and requires qualified clinical review before decisions are made.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The implementation does not enforce the documented shift, department, or timezone boundaries for sensitive clinical records.

Mitigation: Pre-filter records to the intended shift, department, and timezone before running the skill, and have clinical staff verify the generated handover against source records.

Risk: The skill processes EHR data and may produce incomplete or misleading handover summaries if input records are incomplete or out of scope.

Mitigation: Use it only for structured handover support, keep patient data handling compliant with applicable privacy requirements, and do not use outputs as a substitute for direct clinical handover, real-time assessment, emergency triage, diagnosis, or treatment decisions.

Risk: The provided requirements list includes unnecessary standard-library modules as installable packages.

Mitigation: Review and remove or lock dependencies through a trusted process before installing requirements in modern Python environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/shift-handover-summarizer)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Structured Markdown guidance and optional JSON summary output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries include patient priority ranking, key events, vitals and medication summaries, pending tasks, assumptions, risks, and manual checks.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
