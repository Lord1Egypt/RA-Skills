## Description:

Reviews outpatient chronic disease claim materials for diabetes or hypertension from OCR-derived medical text and returns an audit decision with reasons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Healthcare claims and operations teams use this skill to review OCR text from outpatient chronic disease documents for diabetes or hypertension eligibility decisions. Developers can integrate the command-line scripts into document preprocessing and model-review workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OCR medical text may be sent unredacted to a configurable model endpoint.

Mitigation: Use only approved HTTPS endpoints and do not process real patient records unless the receiving endpoint is allowed by the applicable compliance process.

Risk: Review outputs may be saved locally in plaintext JSON and text files.

Mitigation: Route outputs to approved storage, limit local retention, and remove generated files after review when patient data is involved.

Risk: The skill documentation promises de-identification and no local persistence, while the security evidence reports behavior that does not match those promises.

Mitigation: Require the publisher to implement the promised protections or update documentation so operators understand the actual data handling behavior before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-chronic-disease)
- [Medical model API endpoint](https://maas-api.hivoice.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON review result plus natural-language text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save raw JSON and text outputs to caller-specified or default output paths.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
