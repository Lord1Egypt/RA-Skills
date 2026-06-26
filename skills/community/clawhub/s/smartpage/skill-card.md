## Description: <br>
Auto-fit Markdown to one A4 page. Binary search optimal font size, render with 10 themes, export PDF+PNG+MD. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fxjhello](https://clawhub.ai/user/fxjhello) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use SmartPage to format Markdown or converted document content into a single A4 page and export PDF, PNG, and Markdown outputs with selectable themes and layout options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may download and run an unpinned external npm project that was not included in the reviewed artifact. <br>
Mitigation: Review or pin the external project before use and install dependencies only in a trusted workspace. <br>
Risk: The workflow can write generated documents to broad user locations such as the desktop. <br>
Mitigation: Use a workspace-specific output directory for sensitive documents and inspect generated PDF, PNG, and Markdown files before sharing. <br>
Risk: The optional web editing workflow starts a local development server. <br>
Mitigation: Stop the local dev server after editing and avoid exposing it beyond the local machine. <br>


## Reference(s): <br>
- [SmartPage skill page](https://clawhub.ai/fxjhello/smartpage) <br>
- [fxjhello publisher profile](https://clawhub.ai/user/fxjhello) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and generated document files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce PDF, PNG, and Markdown files through an external npm project.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
