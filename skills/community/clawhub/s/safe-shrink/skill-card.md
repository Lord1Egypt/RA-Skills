## Description: <br>
Safe Shrink helps agents route document optimization tasks to SafeShrink for compression, sanitization, SSD conversion, OCR, and batch file-processing workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinwatech](https://clawhub.ai/user/jinwatech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they want an agent to prepare documents for downstream analysis by compressing files, masking sensitive information, converting documents to Markdown-like .ssd output, or generating SafeShrink CLI commands for single-file and batch workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to download and run a cached Windows executable from GitHub. <br>
Mitigation: Install only after verifying the release source and integrity, and limit execution to environments where running the SafeShrink EXE is acceptable. <br>
Risk: Compression, OCR, sanitization, and SSD conversion can alter or remove document content. <br>
Mitigation: Run the tool on copies of source documents and review outputs before relying on or sharing them. <br>
Risk: The release makes broad offline and safety claims around a bundled executable. <br>
Mitigation: Treat those claims as publisher assertions, avoid blanket antivirus exclusions, and apply normal endpoint security review. <br>


## Reference(s): <br>
- [ClawHub Safe Shrink release page](https://clawhub.ai/jinwatech/safe-shrink) <br>
- [SafeShrink project repository](https://github.com/JinwaTech/safeshrink) <br>
- [SafeShrink latest releases](https://github.com/JinwaTech/safeshrink/releases/latest) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline SafeShrink CLI commands and file-handling recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce command examples and suggested output filenames such as .ssd, _slim, or sanitized document variants.] <br>

## Skill Version(s): <br>
1.2.15 (source: server evidence release.version and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
