## Description: <br>
Generates structured academic medical affairs draft materials for pharmaceutical use cases from a topic, audience, key messages, evidence points, and references. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Medical affairs teams and developers use this skill to create academic medical draft materials that can be reviewed by medical, compliance, and subject-matter experts before use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive medical or pharmaceutical documents may be sent to the documented remote medical AI API. <br>
Mitigation: Use only documents permitted for that provider, redact patient-identifying and confidential business details where possible, and verify the provider's privacy and retention terms. <br>
Risk: Local document conversion and OCR can process complex files before generation. <br>
Mitigation: Run conversion in a sandbox with patched, pinned tools and resource limits; prefer structured JSON input when possible. <br>
Risk: AI-generated medical affairs drafts may be mistaken for clinical advice, promotional claims, or regulatory submission material. <br>
Mitigation: Require medical, compliance, and subject-matter expert review before use and keep outputs within academic draft boundaries. <br>
Risk: The appkey is a sensitive credential required for generation. <br>
Mitigation: Pass the appkey through the execution environment or secret handling path and avoid storing it in input files, output files, prepared artifacts, or logs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/unisound-llm/unisound-academic-material-generation) <br>
- [Scientific Writing source skill](https://agent-skills.md/skills/ovachiever/droid-tings/scientific-writing) <br>
- [Remote medical LLM API endpoint](https://maas-api.hivoice.cn/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [UTF-8 JSON with structured data and Markdown text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an appkey for remote medical LLM generation; supports JSON, CSV, Excel, text, PDF, Word, and image inputs through preprocessing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
