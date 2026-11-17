## Description:

Generates a structured marketing audit report from aggregated marketing data using a single GPT-4.1-mini API call with six predefined sections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adarshvmore](https://clawhub.ai/user/adarshvmore)

### License/Terms of Use:


## Use Case:

Developers and marketing operations teams use this skill to convert aggregated audit data into a concise, structured marketing report while limiting generation to one model call.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the full audit payload to OpenAI for report generation.

Mitigation: Confirm organizational approval for external AI processing and remove regulated, confidential, or unnecessary fields before use.

Risk: Missing credentials or API failures can prevent model-generated report output.

Mitigation: Configure OPENAI_API_KEY before use and review the fallback report when an API error occurs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adarshvmore/skills/report-generator-adarsh)

## Skill Output:

**Output Type(s):** [Markdown, Code, Guidance]

**Output Format:** [Markdown report with structured section data and raw audit data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses one GPT-4.1-mini API call with a documented fallback report path on API failure or missing credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
