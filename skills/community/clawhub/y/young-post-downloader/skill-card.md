## Description: <br>
Young Post Downloader helps an agent fetch Young Post Club Spark articles, assemble them into HTML and PDF files, and optionally upload the PDF to Feishu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cgxxxxxxxxxxxx](https://clawhub.ai/user/cgxxxxxxxxxxxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users or agents use this skill to collect Young Post Club Spark articles, generate study-material HTML/PDF bundles, and send the PDF to Feishu when that upload is intended. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF conversion uses a shell command, which can be unsafe when paths contain shell metacharacters. <br>
Mitigation: Use a trusted workspace path, review generated paths before conversion, and prefer a patched version that invokes Chrome with argument-based subprocess execution. <br>
Risk: Feishu upload is part of the normal workflow and may transfer generated files before the user has reviewed them. <br>
Mitigation: Ask for explicit confirmation before any Feishu upload and review the generated PDF and target destination first. <br>


## Reference(s): <br>
- [Young Post Downloader on ClawHub](https://clawhub.ai/cgxxxxxxxxxxxx/young-post-downloader) <br>
- [Young Post Club Spark](https://www.youngpostclub.com/spark) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with Python and shell command snippets, plus generated HTML and PDF file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local HTML/PDF files and upload the generated PDF to Feishu when enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
