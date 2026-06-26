## Description: <br>
Convert Markdown reports to professionally formatted PDF documents using pdfkit, with Chinese font support, A4 layout, automatic headers and footers, and page numbers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaocaixia888](https://clawhub.ai/user/zhaocaixia888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert structured Markdown reports, trade journals, weekly reviews, and investment memos into print-ready A4 PDF files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill loads a local pdfkit dependency, so an untrusted package path could affect generated output or runtime behavior. <br>
Mitigation: Install or point PDFKIT_PATH only to a trusted pdfkit package before running the generator. <br>
Risk: The generator writes to the output path supplied by the user or agent. <br>
Mitigation: Choose output paths intentionally and avoid paths that could overwrite important files. <br>
Risk: Chinese text may render incorrectly if no suitable CJK TrueType or TrueType Collection font is available. <br>
Mitigation: Provide a trusted CJK font in the skill assets directory or configure a known local system font. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zhaocaixia888/zcx-pdf-report-generator) <br>
- [Publisher Profile](https://clawhub.ai/user/zhaocaixia888) <br>
- [Noto Sans SC](https://fonts.google.com/noto/specimen/Noto+Sans+SC) <br>


## Skill Output: <br>
**Output Type(s):** [files, shell commands, configuration, guidance] <br>
**Output Format:** [PDF file output with Markdown and shell-command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and a local pdfkit dependency; Chinese text rendering requires an available CJK font.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
