## Description: <br>
PDF 工具箱 helps agents run local PDF merge, split, rotate, compress, and text extraction workflows using bundled command-line scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[changeworldy-cyber](https://clawhub.ai/user/changeworldy-cyber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, office users, and document-processing agents use this skill to prepare shell commands for common local PDF operations such as combining files, extracting selected pages, rotating pages, compressing output, and exporting text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF operations write new files and may overwrite outputs when filenames are reused. <br>
Mitigation: Use explicit output filenames, keep backups of important PDFs, and review paths before running batch commands. <br>
Risk: The release advertises conversion, watermark, and encryption helpers that are not present in the supplied artifact. <br>
Mitigation: Treat missing helpers as unavailable or unreviewed unless they are supplied separately from a trusted source. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/changeworldy-cyber/simple-pdf-toolkit) <br>
- [Publisher profile](https://clawhub.ai/user/changeworldy-cyber) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Guidance, Files, Text] <br>
**Output Format:** [Markdown guidance with shell commands; bundled scripts return JSON status and may write PDF or text files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local file-processing workflows depend on pypdf and optionally Ghostscript for stronger compression.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
