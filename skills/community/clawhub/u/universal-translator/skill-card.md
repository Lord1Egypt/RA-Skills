## Description: <br>
Universal Translator helps agents handle translation requests for Word, PDF, Excel, PowerPoint, HTML, Markdown, and text files, including batch workflows and format-preservation goals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobewin](https://clawhub.ai/user/tobewin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent to translate supported document files or batches of files while preserving common document structure where possible. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security review reports that the skill's shown translation behavior may label original text instead of actually translating it. <br>
Mitigation: Test translated outputs on non-sensitive sample files and verify the implementation before using it for business, legal, compliance, or confidential documents. <br>
Risk: Translation quality and data handling depend on the configured OpenClaw model environment. <br>
Mitigation: Confirm the OpenClaw model configuration and data path before processing confidential or regulated documents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tobewin/universal-translator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Files, Guidance] <br>
**Output Format:** [Markdown guidance, Python code snippets, and translated document or text outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3; optional document libraries are listed for DOCX, XLSX, PPTX, PDF, and HTML handling.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence; artifact frontmatter says 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
