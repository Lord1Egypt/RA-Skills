## Description: <br>
Extract text, metadata, pages, and basic transformations from local PDF files using pypdf. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Maverick-AI-Tech](https://clawhub.ai/user/Maverick-AI-Tech) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and document-workflow users use this skill to inspect local PDFs, extract text or selected pages, split or merge files, and rotate pages through deterministic CLI commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF text or metadata extracted by the tool may contain sensitive document content. <br>
Mitigation: Use the skill only on intended local PDFs and review extracted stdout or redirected files before sharing them. <br>
Risk: Commands that write PDFs can create directories or overwrite user-chosen output files. <br>
Mitigation: Choose input and output paths deliberately and inspect destination paths before running write operations. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; CLI stdout text and generated PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local file paths and 0-indexed page numbers; commands require python3 and the pypdf package.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
