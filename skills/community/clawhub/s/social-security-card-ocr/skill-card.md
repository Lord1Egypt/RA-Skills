## Description: <br>
Extracts text and structured social security card fields from local image or PDF files by sending them to the Scnet OCR API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scnet-sugon](https://clawhub.ai/user/scnet-sugon) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, developers, and operations teams can use this skill to OCR social security card images and receive structured JSON fields such as name, social security number, card number, bank card number, and issuing institution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads social security card images and extracted identity or financial fields to a remote OCR service. <br>
Mitigation: Use only with explicit user consent and after privacy, retention, and compliance requirements for the Scnet OCR API have been reviewed. <br>
Risk: The skill requires an API key for a third-party OCR service. <br>
Mitigation: Store SCNET_API_KEY outside chat, restrict file permissions for local configuration, and rotate the key if it is exposed or no longer needed. <br>
Risk: The OCR endpoint and base URL can be configured, which may send sensitive files to an unintended service if misconfigured. <br>
Mitigation: Verify SCNET_API_BASE before use and keep it pointed at the expected Scnet API endpoint. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/scnet-sugon/social-security-card-ocr) <br>
- [scnet-sugon Publisher Profile](https://clawhub.ai/user/scnet-sugon) <br>
- [Sugon-Scnet OCR API Documentation Summary](artifact/references/api-docs.md) <br>
- [Social Security Card Field Summary](artifact/assets/templates/fields-summary.md) <br>
- [Scnet Website](https://www.scnet.cn) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Structured JSON written to stdout, with setup and error guidance in text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SCNET_API_KEY and sends the provided file to the configured Scnet OCR API endpoint.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata, SKILL.md frontmatter, skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
