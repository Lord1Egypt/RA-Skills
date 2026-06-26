## Description: <br>
Helps pharmaceutical R&D teams structure clinical trial design inputs and receive protocol-design review suggestions for indications, interventions, phases, populations, endpoints, and visit schedules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Pharmaceutical R&D and clinical development users use this skill to prepare structured clinical trial design inputs and receive protocol-design review suggestions. It supports design work only and does not replace medical, statistical, ethics, or regulatory review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive clinical trial design details may be sent to an external LLM provider. <br>
Mitigation: Require explicit disclosure and approval before use; redact proprietary or patient-adjacent material or route inference through an approved private endpoint. <br>
Risk: Complex document parsers and OCR may process untrusted clinical documents. <br>
Mitigation: Run document conversion in a sandboxed, low-privilege environment and restrict accepted files to trusted sources. <br>
Risk: Generated trial-design guidance may be incomplete, incorrect, or unsuitable for a specific study. <br>
Mitigation: Require review by clinical, statistical, ethics, and regulatory experts before using outputs in a protocol or decision process. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/unisound-llm/unisound-clinical-trial-design) <br>
- [Clinical Trial Protocol Skill reference](https://agent-skills.md/skills/anthropics/healthcare/clinical-trial-protocol-skill) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Markdown, Guidance] <br>
**Output Format:** [UTF-8 JSON with structured trial-design fields and a Markdown natural-language review field] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires caller-provided API credentials for external medical LLM inference.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
