## Description: <br>
Document to Markdown converter - convert DOCX, PPTX, Excel files to Markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tanis90](https://clawhub.ai/user/tanis90) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to extract content from Word, PowerPoint, and Excel files or document URLs and return Markdown for reading, summarization, or downstream analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected documents or document URLs are uploaded to MinerU cloud processing. <br>
Mitigation: Use only documents approved for third-party cloud processing; avoid confidential, regulated, internal, or personal files unless policy allows it. <br>
Risk: The skill depends on installing and running the MinerU CLI. <br>
Mitigation: Install the expected `mineru-open-api` CLI from the documented package source and review commands before execution. <br>
Risk: Standard extraction has file size and page limits, and embedded images may be returned as placeholders. <br>
Mitigation: Confirm the extracted Markdown before relying on it, and use MinerU's authenticated precision extraction path for larger or higher-fidelity documents when appropriate. <br>


## Reference(s): <br>
- [Word To Markdown ClawHub Page](https://clawhub.ai/tanis90/word-to-markdown) <br>
- [MinerU](https://mineru.net) <br>
- [MinerU CLI Download](https://mineru.net/ecosystem?tab=cli) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses MinerU Open API for document extraction; standard flash extraction is limited to 10MB or 20 pages per document, and embedded images may be replaced with placeholders.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
