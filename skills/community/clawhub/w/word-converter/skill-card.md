## Description: <br>
Word Converter helps agents convert .docx and .doc files to Markdown, HTML, LaTeX, DOCX, or JSON using the mineru-open-api CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[veeicwgy](https://clawhub.ai/user/veeicwgy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical writers, researchers, and content migration teams use this skill to prepare Word-document conversion commands and select the right MinerU mode for single-file or batch conversions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Document contents may be processed through MinerU or mineru-open-api. <br>
Mitigation: Use the skill only for documents approved for third-party processing; avoid confidential, regulated, client, legal, or personal documents unless that processing is approved. <br>
Risk: The workflow depends on the mineru-open-api npm package and MinerU service terms. <br>
Mitigation: Review the npm package source and MinerU data-handling terms before installation or production use. <br>
Risk: Conversion mode limitations can affect fidelity, such as flash-extract not supporting tables. <br>
Mitigation: Choose extract mode for tables or multi-format output and review converted documents before relying on them. <br>


## Reference(s): <br>
- [ClawHub Word Converter release](https://clawhub.ai/veeicwgy/word-converter) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; converted document outputs may be Markdown, HTML, LaTeX, DOCX, or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses mineru-open-api; extract mode may require a token and batch mode requires an output directory.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
