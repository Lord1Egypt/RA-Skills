## Description: <br>
Removes watermarks from PDF files, supporting single-file and batch workflows with environment checks, dependency-install confirmation, watermark detection, and user confirmation before removal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TechhnicistSmallWhite](https://clawhub.ai/user/TechhnicistSmallWhite) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and document-processing agents use this skill to inspect PDFs for watermarks, generate preview evidence, and create new PDF copies with detected watermark patterns removed after explicit approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unauthorized modification of protected or third-party PDFs. <br>
Mitigation: Use the skill only on PDFs the user is authorized to modify and require explicit confirmation before watermark removal. <br>
Risk: Unexpected preview images or output PDFs may be written to disk. <br>
Mitigation: Review output directories before execution, keep originals backed up, and prefer an explicit output path for generated files. <br>
Risk: Dependency installation can alter the active Python environment. <br>
Mitigation: Approve package installation only in a trusted Python environment after reviewing the required packages. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TechhnicistSmallWhite/watermark-remover) <br>
- [Publisher profile](https://clawhub.ai/user/TechhnicistSmallWhite) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, files, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON script output, generated preview images, and output PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates preview images and new PDF outputs; defaults to naming outputs with a _no_watermark suffix when no output path is supplied.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
