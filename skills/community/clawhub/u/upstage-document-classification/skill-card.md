## Description: <br>
Classify documents into user-defined categories using the Upstage Document Classification API, with optional splitting for multi-document PDFs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[upstage-deployment](https://clawhub.ai/user/upstage-deployment) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document-processing teams use this skill to classify PDFs or document URLs into defined categories, inspect confidence scores, and optionally split mixed PDFs into separate document groups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documents or document URLs classified with the skill are sent to Upstage's hosted API. <br>
Mitigation: Use the skill only when the organization has approved Upstage's privacy, retention, billing, and compliance terms for the documents being processed. <br>
Risk: Regulated, confidential, or highly sensitive documents could be exposed through hosted processing or generated local outputs. <br>
Mitigation: Avoid those documents unless explicitly approved, restrict access to generated classified JSON and split-PDF outputs, and remove local outputs when they are no longer needed. <br>
Risk: The skill requires an Upstage API key. <br>
Mitigation: Provide the key through the UPSTAGE_API_KEY environment variable and do not hardcode it in prompts, scripts, or saved examples. <br>


## Reference(s): <br>
- [Upstage Document Classification API](https://console.upstage.ai/api/document-classification) <br>
- [Document Split - Multi-Document Separation](references/document-split.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/upstage-deployment/upstage-document-classification) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON, files] <br>
**Output Format:** [Markdown guidance with Python and curl snippets, JSON response examples, and resolved output file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses an Upstage API key from UPSTAGE_API_KEY and may produce classified JSON files or split PDF outputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
