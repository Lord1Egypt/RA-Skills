## Description:

Drafts Uptimely incident postmortems from incident timelines, monitor history, and alerts, and summarizes incidents over a selected period.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devino](https://clawhub.ai/user/devino)

### License/Terms of Use:

MIT-0

## Use Case:

Uptimely users draft evidence-based incident reviews for approval and save approved postmortems to incidents. They can also request read-only summaries of incidents over a period.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incident records may not support a claimed root cause or action item.

Mitigation: Use only supported details, leave gaps clearly marked, and ask the user to fill them.

Risk: Saving an inaccurate postmortem could mislead incident reviewers.

Mitigation: Review the full draft and obtain explicit approval of the exact text before saving.

Risk: The Uptimely connection may grant access to incident data and postmortem writes.

Mitigation: Confirm OAuth scopes match the required read tools and postmortem-save operation.

## Reference(s):

- [Writing Postmortems on ClawHub](https://clawhub.ai/devino/skills/uptimely-writing-postmortems)

## Skill Output:

**Output Type(s):** [Markdown, Text]

**Output Format:** [Markdown postmortem drafts or text incident summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Postmortems are saved to Uptimely only after approval of the exact draft; period summaries are read-only.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
