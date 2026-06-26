## Description: <br>
Document to Markdown converter that converts DOCX, PPTX, and Excel files to Markdown for content extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tanis90](https://clawhub.ai/user/tanis90) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, employees, and external users use this skill to extract Markdown content from Word documents, PowerPoint presentations, and Excel spreadsheets for reading, summarization, or analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The conversion workflow uploads selected documents to MinerU's cloud API for processing. <br>
Mitigation: Only process documents the user is permitted to upload, and avoid confidential, regulated, or highly sensitive files unless MinerU handling terms and permissions have been reviewed. <br>
Risk: The skill relies on the third-party mineru-open-api CLI package. <br>
Mitigation: Install it only from trusted package sources and review the package before use in sensitive environments. <br>


## Reference(s): <br>
- [Word2md ClawHub release](https://clawhub.ai/tanis90/word2md) <br>
- [MinerU](https://mineru.net) <br>
- [MinerU CLI download](https://mineru.net/ecosystem?tab=cli) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Markdown extracted from Office documents; embedded images may be replaced with placeholders.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
