## Description:

Generates postoperative rehabilitation exercise guidance from exercise details, returning structured fields and Markdown text for patient-facing rendering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

External ClawHub users can use this skill to transform postoperative rehabilitation exercise entries into readable action guidance, frequency, duration, and precautions. It should be used with appropriate clinical review and not as a substitute for a clinician's rehabilitation plan.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may generate patient-facing rehabilitation guidance from incomplete exercise inputs.

Mitigation: Require clinical review before using outputs for real rehabilitation decisions, and treat generated frequency, duration, intensity, and precautions as draft guidance only.

Risk: Sensitive medical content may be sent to a remote API.

Mitigation: Do not submit identifiable medical records unless the API endpoint, authorization process, and data-handling controls have been approved.

Risk: The runtime may fall back to unaudited shared Python preprocessing code.

Mitigation: Review and approve the local preprocessing path and any shared-code fallback before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-exercise-guidance)
- [CareKit](https://github.com/carekit-apple/CareKit)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [UTF-8 JSON with structured data and Markdown text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes exercise name, rehabilitation phase, instruction, frequency, duration, precautions, status, and generated text.]

## Skill Version(s):

1.0.2 (source: server release evidence; artifact _meta.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
