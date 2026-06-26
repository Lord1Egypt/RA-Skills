## Description: <br>
Use study limitations drafter for academic writing workflows that need structured execution, explicit assumptions, and clear output boundaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Academic authors, researchers, and proposal teams use this skill to draft professional study limitation paragraphs from supplied study constraints while keeping assumptions, risks, and unresolved items explicit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local Python execution may read chosen input data and write generated output files. <br>
Mitigation: Run the script only inside a working project folder, review selected input and output paths, and keep outputs within the workspace. <br>
Risk: Sensitive study details may be included in generated limitation text or saved output files. <br>
Mitigation: Avoid sensitive datasets unless needed, review generated text before sharing, and remove confidential details from outputs. <br>
Risk: The documented path-safety checklist is guidance rather than a guaranteed sandbox. <br>
Mitigation: Validate paths before execution and do not rely on the skill documentation as a substitute for runtime sandboxing. <br>


## Reference(s): <br>
- [Audit Reference](references/audit-reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/study-limitations-drafter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown or plain text limitation paragraphs with optional shell commands for validation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write generated limitation text to a user-specified output file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
