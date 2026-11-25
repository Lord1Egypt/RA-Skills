## Description:

Checks whether submitted GitHub provenance fields appear in the stored public skill record by comparing the record with the submitted payload.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bucsaradu](https://clawhub.ai/user/bucsaradu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers can use this diagnostic to compare submitted GitHub provenance fields with a public skill record when assessing whether those fields are retained. Treat provenance as unavailable unless the server-resolved record confirms it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The diagnostic's stated conclusion treats missing fields in a stored record as proof that the publish schema strips them, which may overstate what the comparison establishes.

Mitigation: Confirm the result against server-resolved records and describe provenance as unavailable until server evidence supports a stronger conclusion.

## Reference(s):


## Skill Output:

**Output Type(s):** [Analysis, Guidance]

**Output Format:** [Text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
