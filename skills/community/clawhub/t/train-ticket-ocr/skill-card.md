## Description: <br>
Train Ticket Ocr extracts structured fields from train ticket images or PDFs, including stations, train number, seat details, fare, travel date, ID number, and sales information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scnet-sugon](https://clawhub.ai/user/scnet-sugon) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to submit train ticket files to Scnet OCR and receive structured ticket fields for expense, reconciliation, or document processing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Train ticket images or PDFs are sent to Scnet for OCR processing and may contain personal or business data. <br>
Mitigation: Process only tickets approved for third-party OCR, verify the configured endpoint, and avoid submitting sensitive tickets when external processing is not acceptable. <br>
Risk: The skill requires a sensitive SCNET_API_KEY. <br>
Mitigation: Use a dedicated revocable key, store it in a restricted environment or config file, avoid pasting it into chat or logs, and rotate it if exposure is suspected. <br>
Risk: Rapid repeated OCR calls can trigger the documented API rate limit. <br>
Mitigation: Run calls serially when possible and respect retry or backoff behavior after 429 responses. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/scnet-sugon/train-ticket-ocr) <br>
- [Sugon-Scnet OCR API Documentation](references/api-docs.md) <br>
- [Train Ticket Field Summary](assets/templates/fields-summary.md) <br>
- [Scnet Website](https://www.scnet.cn) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text] <br>
**Output Format:** [Structured JSON on stdout, with plain-text error messages on failure.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SCNET_API_KEY and sends the selected ticket file to Scnet OCR for processing.] <br>

## Skill Version(s): <br>
1.0.3 (source: evidence release and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
