## Description: <br>
Privacy redaction toolkit for reading, masking, and replacing sensitive information in images, PDFs, Word documents, and PowerPoint presentations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[darknoah](https://clawhub.ai/user/darknoah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers can use this skill to extract text from supported file formats and redact or replace private information before sharing documents, presentations, PDFs, or images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unredacted sensitive text can be exposed or retained through normal logging, debug output, OCR processing, or temporary cache files. <br>
Mitigation: Review before installing, process only local files suitable for OCR and Office conversion, avoid debug modes for real PII, clear PPStructure/redact cache files after use, and treat terminal logs as sensitive. <br>


## Reference(s): <br>
- [ClawHub Redact skill page](https://clawhub.ai/darknoah/redact) <br>
- [uv documentation](https://docs.astral.sh/uv/) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, files, shell commands, configuration] <br>
**Output Format:** [Markdown instructions with command examples; script outputs include plain text, JSON, and redacted image or document files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3.10+ and OCR/document-processing dependencies.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
