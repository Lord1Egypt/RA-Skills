## Description:

Generates JSON schemas for structured document information extraction using Upstage's schema-generation API or a VLM-guided schema design workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upstage-deployment](https://clawhub.ai/user/upstage-deployment)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document AI practitioners use this skill to create extraction schemas for documents or folders before running structured information extraction. It supports fast API-based schema generation and more deliberate VLM-guided schema design.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default API mode can send document contents to Upstage using the user's UPSTAGE_API_KEY, including confidential, regulated, or customer documents.

Mitigation: Require explicit approval before upload, set file and page limits, and prefer a local/manual or carefully scoped VLM workflow for sensitive documents.

## Reference(s):

- [Schema Design Guidelines](references/schema-design.md)
- [VLM-Based Schema Generation Workflow](references/vlm-workflow.md)
- [Upstage Console](https://console.upstage.ai)
- [Upstage Schema Generation API Endpoint](https://api.upstage.ai/v1/information-extraction/schema-generation)

## Skill Output:

**Output Type(s):** [text, json, configuration, guidance]

**Output Format:** [JSON schema file with a concise Markdown response containing the resolved absolute path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes to a requested output path or a temporary schema path; default API mode requires UPSTAGE_API_KEY.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
