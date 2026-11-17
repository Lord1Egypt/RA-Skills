## Description:

Reviews whether documented medical-record evidence is sufficient to support specified surgeries or procedures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Healthcare coding, audit, and engineering teams use this skill to review structured records and candidate surgery or procedure codes for evidence sufficiency. It returns an assistive review result for insurance coding workflows and does not provide diagnosis or treatment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive medical record text and the supplied model credential may be sent to a caller-selected LLM endpoint.

Mitigation: Use a fixed trusted HTTPS endpoint, de-identify records before use, protect the appkey, and avoid passing a custom --base value from untrusted input.

Risk: Medical record text may be retained locally when prepared text is saved for debugging.

Mitigation: Avoid --save-prepared unless local retention of medical text is acceptable for the operating environment.

Risk: LLM-assisted review can produce incorrect or incomplete audit conclusions.

Mitigation: Treat outputs as insurance coding audit assistance, keep human review in the workflow, and use --no-llm for offline fallback review when external model use is not appropriate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-surgery-sufficiency-review)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs final_decision and concise reasoning; final_decision is one of: 依据充分, 依据不充分, 待人工复核.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
