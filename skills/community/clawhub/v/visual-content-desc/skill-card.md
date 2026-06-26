## Description: <br>
Generates detailed descriptions, alt text, and figure text for medical images and charts from provided visual features. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, researchers, and developers use this skill to draft accessible descriptions, alt text, and figure text for medical visuals when the image type and key visual features are already known. It supports academic writing and documentation workflows, not diagnosis or independent medical image analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated text could be mistaken for medical image analysis or diagnosis. <br>
Mitigation: Use the skill as a drafting aid only and have qualified reviewers confirm any medical claims before publication or clinical use. <br>
Risk: Patient-related visual features could be exposed in generated descriptions or saved outputs. <br>
Mitigation: Provide only image features that are appropriate to include in generated text and review output destinations before sharing or writing files. <br>
Risk: Adapted local workflows may read from or write to unintended paths. <br>
Mitigation: Confirm input and output paths before execution and restrict any file writes to the intended workspace. <br>


## Reference(s): <br>
- [Visual Content Desc Guidelines](references/guidelines.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/visual-content-desc) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, guidance] <br>
**Output Format:** [JSON object with description, alt_text, and figure_text fields, with concise Markdown guidance when used interactively] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should state assumptions, constraints, risks, and unresolved items when they affect correctness.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
