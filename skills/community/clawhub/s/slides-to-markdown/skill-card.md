## Description: <br>
Document to Markdown converter - convert DOCX, PPTX, Excel files to Markdown. Use when extracting content from Word documents, PowerPoint presentations, or Excel spreadsheets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tanis90](https://clawhub.ai/user/tanis90) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to extract readable Markdown from Word, PowerPoint, and Excel documents for review, summarization, or analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected documents are uploaded to MinerU's cloud API for processing. <br>
Mitigation: Use only with documents approved for cloud processing; avoid confidential, regulated, or highly sensitive files unless that processing has been approved. <br>
Risk: The workflow depends on the external mineru-open-api CLI package. <br>
Mitigation: Pin, verify, or approve the CLI package in managed environments before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tanis90/slides-to-markdown) <br>
- [MinerU homepage](https://mineru.net) <br>
- [MinerU CLI download page](https://mineru.net/ecosystem?tab=cli) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown text with optional shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Basic flash extraction accepts selected Office files or URLs and is documented with a 10MB or 20-page limit; larger or precision extraction requires authenticated CLI use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
