## Description: <br>
Provides bidirectional English-Chinese translation for text, documents, code comments, email, and batch Markdown or text workflows while preserving formatting where possible. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jeffrey-Zou](https://clawhub.ai/user/Jeffrey-Zou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and writers use this skill to translate between English and Chinese for plain text, Markdown documents, code comments, technical documentation, business emails, and conversational content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Batch file helpers can write to caller-specified output paths and may overwrite files when an existing filename is supplied. <br>
Mitigation: Only point the helpers at files intended for translation, choose output paths deliberately, and avoid existing filenames unless overwriting is intended. <br>
Risk: The included translation scripts appear basic, so important translations may be inaccurate or incomplete. <br>
Mitigation: Manually review important translations before relying on or publishing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Jeffrey-Zou/translate-en-zh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance, files] <br>
**Output Format:** [Plain text or Markdown, with optional shell command examples for batch file helpers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Batch helpers read user-selected UTF-8 files and write translated text or Markdown outputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
