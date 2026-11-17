## Description:

Extracts structured resident health-record data from unstructured visit notes, exam reports, or questionnaire text and returns JSON plus a natural-language summary aligned to the National Basic Public Health Service Specification, Third Edition.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Community health service staff and public-health teams use this skill to convert de-identified resident health notes, physical exam reports, and health questionnaires into structured records for review and entry into formal health-management systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send full medical-record text to a configurable remote LLM endpoint.

Mitigation: Use only de-identified records, approved medical-data processing terms, and a trusted HTTPS endpoint before execution.

Risk: The runtime requires an API key for the remote LLM call.

Mitigation: Avoid long-lived keys and provide credentials only through controlled operational channels.

Risk: The output may influence health-record management decisions.

Mitigation: Require qualified public-health staff to review extracted records and summaries before entering them into formal systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-health-record-management)
- [Publisher profile](https://clawhub.ai/user/unisound-llm)
- [Unisound medical LLM API endpoint](https://maas-api.hivoice.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON health-record structure followed by a natural-language summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fields not supported by the input are expected to be null; BMI is calculated when height and weight are present.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
