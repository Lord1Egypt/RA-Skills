## Description:

Turns field voice notes into updated job records and draft estimate handoffs for field-service teams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluecolumnconsulting-lgtm](https://clawhub.ai/user/bluecolumnconsulting-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

Field-service workers capture site-visit details and changes; office staff recall job notes to draft estimate handoffs without losing measurements, materials, or open questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Job details and audio links are sent to a third-party service.

Mitigation: Confirm BlueColumn is approved for business data; minimize customer, property, employee, and confidential details, and review its privacy and retention terms.

Risk: The BlueColumn API key grants access to the service.

Mitigation: Keep the key in an environment variable rather than including it in job notes or shared output.

Risk: An estimate drafted before open questions are resolved may be inaccurate.

Mitigation: Check the recalled note against the site visit and hold the estimate until outstanding approvals or documents arrive.

## Reference(s):

- [BlueColumn API documentation](https://bluecolumn.ai/docs)
- [ClawHub skill listing](https://clawhub.ai/bluecolumnconsulting-lgtm/skills/voice-to-job-memory)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Job-note summaries and draft estimate handoffs based on recalled site-visit details.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
