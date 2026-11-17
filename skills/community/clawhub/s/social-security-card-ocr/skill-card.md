## Description:

Recognizes social security card images only when explicitly requested and extracts core card fields such as name, social security number, and national ID number.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scnet-sugon](https://clawhub.ai/user/scnet-sugon)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to extract structured fields from an authorized social security card image through SCNet OCR. It is limited to social security card recognition and is not intended for general OCR or other identity documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive social security card images and extracted identity data are uploaded to a third-party OCR service.

Mitigation: Use only with explicit authorization from the card holder and only when privacy and compliance requirements permit third-party OCR processing.

Risk: A configurable SCNET_API_BASE can direct sensitive documents and the API key away from the declared SCNet endpoint.

Mitigation: Keep SCNET_API_BASE fixed to the documented SCNet HTTPS endpoint and review configuration before processing real documents.

Risk: SCNET_API_KEY exposure could allow unauthorized OCR requests.

Mitigation: Store the key outside chat, protect local configuration files, and rotate the key if exposure is suspected.

## Reference(s):

- [Sugon-Scnet OCR API documentation](references/api-docs.md)
- [Social security card field summary](assets/templates/fields-summary.md)
- [SCNet website](https://www.scnet.cn)
- [ClawHub skill page](https://clawhub.ai/scnet-sugon/skills/social-security-card-ocr)

## Skill Output:

**Output Type(s):** [JSON, API Calls]

**Output Format:** [Structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns OCR result records for social security card fields; confidence metadata is removed when present.]

## Skill Version(s):

1.0.6 (source: ClawHub release evidence; artifact frontmatter is 1.0.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
