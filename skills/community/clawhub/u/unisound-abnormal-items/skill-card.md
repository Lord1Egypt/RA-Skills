## Description:

Interprets abnormal health exam indicators one by one, explaining what each item means, why it may be abnormal, potential health impact, suggested interventions, and cross-indicator correlations in accessible language.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Health management staff, physical examination centers, and developers use this skill to turn abnormal exam report items into structured JSON and Chinese patient-facing explanations. It supports health education workflows by summarizing possible causes, health impact, lifestyle and medical follow-up suggestions, urgency, and correlations such as metabolic syndrome patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive medical reports may be sent to a remote API without code-enforced de-identification.

Mitigation: Pre-redact patient identifiers and unnecessary details before use, and review data handling requirements before submitting real patient data.

Risk: A custom base URL can redirect reports and the app key to an endpoint outside the expected service.

Mitigation: Use only a verified trusted API endpoint and restrict app key handling to approved environments.

Risk: Generated medical explanations may be incomplete or incorrect for clinical decision-making.

Mitigation: Treat outputs as health education material and require clinician review for diagnosis, treatment, or urgent-care decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-abnormal-items)
- [Publisher profile](https://clawhub.ai/user/unisound-llm)
- [Unisound MaaS chat completions endpoint](https://maas-api.hivoice.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON object followed by Chinese explanatory text headed with 【专项解读】]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May print to stdout or write to a user-specified output file; generated content is health education guidance and not a substitute for medical diagnosis.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
