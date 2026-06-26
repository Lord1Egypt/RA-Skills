## Description: <br>
Scnet Ocr sends user-selected images, PDFs, or archives to the Scnet OCR API to extract text and structured fields from general text, identity documents, cards, certificates, invoices, receipts, stamps, and financial documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scnet-sugon](https://clawhub.ai/user/scnet-sugon) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Agents and users use this skill when they need OCR for local document files and want structured JSON results for downstream review or extraction workflows. It is most relevant for documents such as IDs, bank cards, invoices, payment records, certificates, stamps, and other forms supported by Scnet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads selected document files to Scnet's OCR service, and supported document types may contain sensitive personal, financial, or medical data. <br>
Mitigation: Use it only with clear permission and a deliberate file path, and avoid processing IDs, bank cards, payment records, birth records, or medical invoices unless the provider's privacy and retention terms are acceptable. <br>
Risk: The skill requires a Scnet API key and can read it from a config/.env file. <br>
Mitigation: Prefer protected environment variables or a config/.env file with restrictive permissions such as chmod 600, and do not paste API keys into chat. <br>
Risk: OCR requests may be rate limited by the Scnet service. <br>
Mitigation: Run OCR calls serially and rely on the built-in retry behavior for 429 responses rather than launching concurrent requests. <br>


## Reference(s): <br>
- [Scnet OCR API documentation](references/api-docs.md) <br>
- [OCR field summary](assets/templates/fields-summary.md) <br>
- [Scnet website](https://www.scnet.cn) <br>
- [ClawHub skill page](https://clawhub.ai/scnet-sugon/scnet-ocr) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON OCR results with setup guidance and command-line usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SCNET_API_KEY and a local file path; output fields vary by ocrType and may include elements and stamps.] <br>

## Skill Version(s): <br>
1.0.6 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
