## Description: <br>
Generates text-based radiology quiz cases from structured case descriptions for medical education and board exam preparation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Medical educators, students, and residents can use this skill to create bounded radiology quiz content from provided case data for study and board preparation. It is best suited for educational review workflows where assumptions, inputs, and limitations are stated explicitly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary says the advertised image-based radiology quiz capability does not match the shipped text-only script and missing documented code paths. <br>
Mitigation: Use the packaged scripts/main.py path for text-based quiz generation only, and review any additional referenced code before relying on image-based workflows. <br>
Risk: Radiology case content can include sensitive or identifying clinical details. <br>
Mitigation: Use de-identified educational case data only and confirm that inputs are appropriate for training or study use before generating quiz content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aipoch-ai/radiology-image-quiz) <br>
- [Audit reference](references/audit-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text or Markdown quiz content with optional shell commands for local validation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should identify inputs, assumptions, risks, unresolved items, and validation checks when relevant.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
