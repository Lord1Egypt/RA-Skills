## Description:

Reviews medical claim materials to classify the relationship between other diagnoses and the primary diagnosis, then returns a reimbursement recommendation in the requested fixed-line format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Claims reviewers and developers use this skill to send de-identified medical claim text to an internal medical model and receive an auxiliary pre-existing-condition relationship assessment and reimbursement recommendation. The output does not replace policy terms or final human claims decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive claim text and a bearer API key can be sent to a user-configurable network endpoint.

Mitigation: Use the documented internal HTTPS API endpoint, avoid overriding the API URL in production, provide a narrowly scoped key, and de-identify claim materials before submission.

Risk: Outputs may contain sensitive medical or claims information.

Mitigation: Treat stdout and output files as sensitive claims data and apply the same storage, access-control, and retention rules used for source claim materials.

Risk: The model response is an auxiliary review opinion rather than a final benefits determination.

Mitigation: Require human claims review against policy terms before making legal, coverage, or payment decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-pre-existing-review)
- [Publisher profile](https://clawhub.ai/user/unisound-llm)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [JSON by default, or plain text when text-only output is requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns the model answer, original question, model name, input mode, record index, and optional metadata; batch input can produce NDJSON.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
