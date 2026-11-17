## Description:

Analyzes children's behavior videos to identify and summarize repetitive behaviors such as spinning, hand flapping, and body rocking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Rehabilitation professionals and parents can use the skill to record observed repetitive behaviors, review their frequency and duration over time, and support care planning. It can also retrieve historical reports; its results are not a diagnosis or treatment plan.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Children's footage is processed in the cloud during ordinary use, and the no-analysis option is ineffective; account credential and shared identity handling also create privacy risks.

Mitigation: Wait for fixes to the no-analysis option and credential handling before using children's footage. Confirm the provider's retention policy, obtain guardian consent, and use a separate workspace for each user.

Risk: Observed behavior counts could be mistaken for an autism diagnosis or a prescribed intervention.

Mitigation: Treat results as observational support only; have a qualified clinician or rehabilitation professional review them and determine any diagnosis or intervention.

## Reference(s):

- [API documentation](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Guidance]

**Output Format:** [Structured behavior reports and Markdown summaries with event counts, durations, and report links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Visual observations for professional and caregiver review; not a diagnosis or treatment plan.]

## Skill Version(s):

1.0.14 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
