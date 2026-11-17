## Description:

Assists community clinic clinicians by drafting medication recommendations, checking interactions and contraindications, and suggesting dose adjustments from diagnosis and patient medication context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

External clinicians in community clinics and primary-care settings use this skill as prescription decision support. It produces medication options, interaction and contraindication checks, dosing considerations, monitoring suggestions, and patient education points for clinician review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process sensitive patient information through a remote model service.

Mitigation: Do not submit names, IDs, phone numbers, addresses, record numbers, or other identifiers unless the remote service and legal/privacy arrangements explicitly allow it.

Risk: Prescription recommendations may be incomplete, incorrect, or inappropriate for a specific patient.

Mitigation: Treat outputs as decision support only; a qualified clinician must review the recommendations and sign any final prescription.

Risk: Changing the model endpoint or using a broadly scoped AppKey could expose protected clinical data.

Mitigation: Use only an approved HTTPS endpoint, avoid overriding the base URL, and use a narrowly scoped AppKey that can be rotated.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-prescription-assist)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [JSON plus natural-language summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can print to stdout or write the same output to a file when an output path is supplied.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
