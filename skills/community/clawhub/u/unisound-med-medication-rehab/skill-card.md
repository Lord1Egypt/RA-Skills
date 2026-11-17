## Description:

Provides clinical medication consultation, personalized medication education, and rehabilitation guidance Q&A with task-specific prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and clinical workflow integrators use this skill to route medication consultation, medication education, or rehabilitation questions to a medical LLM and return structured assistant output. The output is model-assisted information and is not a substitute for formal clinical diagnosis, prescribing, or treatment decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive medical questions and API credentials may be sent to an external or caller-supplied API endpoint.

Mitigation: Use only a trusted HTTPS endpoint, avoid overriding --api-url unless the destination is controlled, protect the API key, and de-identify patient details before submission.

Risk: Generated output may be mistaken for clinical diagnosis, prescribing, or treatment decisions.

Mitigation: Review responses through qualified clinical workflows and treat outputs as model-assisted information only.

Risk: Files written with --output may contain sensitive medical records or identifiers.

Mitigation: Store output files only in approved locations, restrict access, and handle them as sensitive records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-med-medication-rehab)
- [Default medical model API endpoint](https://maas-api.hivoice.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [JSON by default, plain answer text with --text-only, or NDJSON for batch output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write UTF-8 JSON or NDJSON files when --output is provided.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
