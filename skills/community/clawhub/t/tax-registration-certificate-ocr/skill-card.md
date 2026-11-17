## Description:

Supports OCR recognition for tax registration certificate documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scnet-sugon](https://clawhub.ai/user/scnet-sugon)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to submit tax registration certificate images, PDFs, or archives to the SCNET OCR API and receive structured extracted fields such as taxpayer name, certificate number, legal representative, address, business scope, and issue date.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tax registration certificate files and OCR results may contain sensitive business or personal data and are uploaded to SCNET for processing.

Mitigation: Only process documents the user is authorized to share, confirm SCNET data handling expectations, and avoid uploading secret or unauthorized documents.

Risk: The configurable SCNET_API_BASE setting can redirect uploaded files and the API token to another endpoint.

Mitigation: Keep the default endpoint unless the replacement service and transport security are fully trusted.

Risk: The SCNET API key can be exposed if pasted into chat or stored in an insecure configuration file.

Mitigation: Keep the key out of chat, store it in a locked-down config/.env file or protected environment, and restrict file permissions.

Risk: OCR output remains sensitive after processing.

Mitigation: Handle generated JSON as sensitive data and avoid unnecessary retention or disclosure.

## Reference(s):

- [Sugon-Scnet OCR API documentation summary](references/api-docs.md)
- [Tax registration certificate field summary](assets/templates/fields-summary.md)
- [SCNET website](https://www.scnet.cn)
- [SCNET OCR API endpoint](https://api.scnet.cn/api/llm/v1/ocr/recognize)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [Pretty-printed JSON on stdout with text error messages on failure]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns the API data array after removing per-item confidence fields; OCR output may contain sensitive business or personal information.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata; artifact frontmatter and skill.yaml declare 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
