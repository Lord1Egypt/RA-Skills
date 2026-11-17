## Description:

Generates personalized vaccination reminder lists from resident age, vaccination history, and special health conditions, returning JSON and a natural-language summary based on China's national immunization plan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Community health service staff and township clinic public health workers use this skill to identify overdue vaccinations, upcoming vaccinations, non-mandatory recommendations, contraindication prompts, and pre-visit precautions for residents. The generated reminder is advisory and should be reviewed by a vaccination clinician before action.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Resident vaccination and health information, together with an API key, may be sent to a configurable remote service.

Mitigation: Use de-identified inputs, keep the trusted HTTPS API endpoint unless operating a controlled replacement, and review before running with real resident data.

Risk: Saved outputs may contain sensitive medical information.

Mitigation: Treat saved output as sensitive health data and avoid writing production records unless storage controls are in place.

Risk: Vaccination recommendations can vary by region, records completeness, and patient-specific contraindications.

Mitigation: Use the reminder as a public-health workflow aid and require clinician review before final vaccination decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-vaccination-reminder)
- [Configured medical model API endpoint](https://maas-api.hivoice.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [JSON, text, guidance]

**Output Format:** [JSON object followed by a natural-language summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can print to stdout or save to a file; consumes UTF-8 text or JSON resident vaccination input.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
