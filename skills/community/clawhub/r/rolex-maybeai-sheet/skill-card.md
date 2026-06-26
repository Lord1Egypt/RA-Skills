## Description: <br>
MaybeAI Sheet skill for full Excel/spreadsheet lifecycle management. Upload, read, edit, and analyze Excel files via the MaybeAI platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ojbkxiongdei](https://clawhub.ai/user/ojbkxiongdei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and spreadsheet operators use this skill to guide token-authenticated MaybeAI workflows for uploading, reading, editing, formatting, charting, exporting, and managing Excel workbooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives broad token-authorized examples for reading, uploading, editing, exporting, and deleting spreadsheet data. <br>
Mitigation: Review commands before execution, keep the bearer token private, and run examples only against intended workbooks. <br>
Risk: Example workflows can modify or remove workbook data through delete, clear, rename, append, update, import, and export operations. <br>
Mitigation: Use copies or test files first, especially when adapting examples for production or sensitive spreadsheets. <br>
Risk: Using this skill may send spreadsheet contents to MaybeAI services. <br>
Mitigation: Use it only when that data flow is acceptable for the workbook contents and organization policy. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ojbkxiongdei/rolex-maybeai-sheet) <br>
- [Publisher profile](https://clawhub.ai/user/ojbkxiongdei) <br>
- [MaybeAI Sheet homepage](https://github.com/OmniMCP-AI/maybeai-uni) <br>
- [MaybeAI](https://maybe.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a MaybeAI bearer token and the curl and jq command-line tools for the bundled shell examples.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
