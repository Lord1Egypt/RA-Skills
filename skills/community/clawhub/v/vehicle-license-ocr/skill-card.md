## Description: <br>
Recognizes main-page and secondary-page vehicle license information, including plate number, owner, brand/model, VIN, engine number, archive number, approved passenger count, total mass, and inspection records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scnet-sugon](https://clawhub.ai/user/scnet-sugon) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to submit vehicle-license document images to Scnet's OCR API and receive structured JSON for main-page and secondary-page fields. It is useful when an agent needs to extract vehicle registration details from local image or PDF files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Vehicle-license images and extracted personal or vehicle details are sent to Scnet's OCR API. <br>
Mitigation: Use the skill only for documents you are authorized to process and review Scnet's privacy and data-retention terms before uploading sensitive documents. <br>
Risk: The skill requires an API key that could be exposed through chats, shared logs, or insecure configuration files. <br>
Mitigation: Keep SCNET_API_KEY out of chat transcripts and shared logs, store it in a restricted environment or config file, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [Sugon-Scnet OCR API docs](references/api-docs.md) <br>
- [Vehicle license OCR field summary](assets/templates/fields-summary.md) <br>
- [Vehicle License Ocr on ClawHub](https://clawhub.ai/scnet-sugon/vehicle-license-ocr) <br>
- [Scnet website](https://www.scnet.cn) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, API Calls, Shell commands, Configuration] <br>
**Output Format:** [Structured JSON printed to standard output, with errors printed as text messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SCNET_API_KEY and optionally SCNET_API_BASE; uploads local document files to Scnet's OCR API and removes the top-level result confidence field before printing.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, skill.yaml, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
