## Description:

Document to Markdown converter - convert DOCX, PPTX, Excel files to Markdown. Use when extracting content from Word documents, PowerPoint presentations, or Excel spreadsheets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tanis90](https://clawhub.ai/user/tanis90)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to extract readable Markdown from Word documents, PowerPoint presentations, and Excel spreadsheets provided as local files or URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send selected office documents or document URLs to MinerU's cloud API for processing.

Mitigation: Confirm user intent before upload and avoid confidential, regulated, or enterprise documents unless external processing is approved.

## Reference(s):

- [MinerU](https://mineru.net)
- [MinerU CLI download](https://mineru.net/ecosystem?tab=cli)
- [mineru-open-api npm package](https://www.npmjs.com/package/mineru-open-api)
- [MinerU Open API Go install path](https://github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs Markdown extracted from DOCX, PPTX, XLS, or XLSX inputs; embedded images may be replaced with placeholders.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
