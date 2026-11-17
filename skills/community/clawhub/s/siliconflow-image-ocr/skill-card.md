## Description:

Extracts text from screenshots, receipts, forms, and tables using SiliconFlow OCR, including mixed Chinese and English text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangziiiiii](https://clawhub.ai/user/wangziiiiii)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run OCR over local images or image URLs, especially for screenshots, receipts, forms, tables, and mixed Chinese/English document images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the skill can send the user's API key and document contents to an arbitrary caller-supplied endpoint.

Mitigation: Review before installing, use only documents acceptable to send to SiliconFlow, avoid sensitive IDs, financial records, credentials, and private business screenshots, and do not pass --base-url unless it is validated as the real SiliconFlow HTTPS endpoint.

Risk: The security evidence marks the release as suspicious pending endpoint validation.

Mitigation: Treat it as higher risk until the publisher removes or strictly validates custom endpoints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangziiiiii/skills/siliconflow-image-ocr)
- [SiliconFlow](https://siliconflow.cn)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; the OCR helper returns raw JSON from the API.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a SiliconFlow API key and network access to the configured API endpoint.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
