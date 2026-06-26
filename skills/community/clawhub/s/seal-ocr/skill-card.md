## Description: <br>
Seal OCR recognizes seals in user-selected files and returns structured details such as seal coordinates, shape, color, type, text, and confidence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scnet-sugon](https://clawhub.ai/user/scnet-sugon) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to call SCNet's seal OCR service for images, PDFs, or archives and return structured seal recognition results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images, PDFs, or archives are uploaded to SCNet for OCR processing. <br>
Mitigation: Use only files you are authorized to share; avoid identity documents, contracts, invoices, or confidential seals unless permission and SCNet data-handling terms have been reviewed. <br>
Risk: The skill requires an SCNet API key. <br>
Mitigation: Store SCNET_API_KEY in a local environment variable or config/.env file with restricted permissions, and do not paste the key into chats or logs. <br>
Risk: SCNet may rate-limit OCR requests. <br>
Mitigation: Run requests serially where possible and back off before retrying if 429 responses occur. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/scnet-sugon/seal-ocr) <br>
- [Sugon-Scnet OCR API Documentation](references/api-docs.md) <br>
- [Seal OCR Field Summary](assets/templates/fields-summary.md) <br>
- [SCNet Website](https://www.scnet.cn) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, text, shell commands, configuration, guidance] <br>
**Output Format:** [Structured JSON recognition results with text error messages and command-line usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SCNET_API_KEY and uploads selected files to SCNet for recognition.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and changelog, released 2025-05-29) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
