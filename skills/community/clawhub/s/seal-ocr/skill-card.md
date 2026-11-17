## Description:

Precisely identifies seal information in images and returns seal coordinates, shape, color, type, and inner text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scnet-sugon](https://clawhub.ai/user/scnet-sugon)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users use this skill to submit an image, PDF, or archive to Scnet OCR and receive structured seal-recognition results for document processing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected images, PDFs, or archives are uploaded to Scnet's OCR service for processing.

Mitigation: Use the skill only with documents appropriate for that provider and confirm data-handling terms before processing confidential or regulated content.

Risk: The API key and document uploads can be sent to a configurable API base.

Mitigation: Keep SCNET_API_KEY out of chat, protect config/.env, and change SCNET_API_BASE only to a fully trusted endpoint.

Risk: Rapid repeated calls can hit the OCR service rate limit.

Mitigation: Call the skill serially where possible and rely on the built-in retry/backoff behavior when 429 responses occur.

## Reference(s):

- [Sugon-Scnet OCR API documentation](references/api-docs.md)
- [Seal recognition fields summary](assets/templates/fields-summary.md)
- [Scnet website](https://www.scnet.cn)
- [Scnet OCR API base](https://api.scnet.cn/api/llm/v1)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [JSON OCR results emitted to standard output, with Markdown guidance in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The JSON data contains seal recognition fields such as position, confidence, shape, color, type, and text.]

## Skill Version(s):

1.0.0 (source: frontmatter, skill.yaml, changelog, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
