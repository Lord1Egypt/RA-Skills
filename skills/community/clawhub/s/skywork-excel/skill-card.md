## Description: <br>
Skywork Excel generates Excel and CSV files, analyzes spreadsheets and uploaded files, builds charts and reports, fetches live web data, and converts supported document or image inputs through the Skywork Excel backend service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gxcun17](https://clawhub.ai/user/gxcun17) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill to create spreadsheet deliverables, analyze tabular or uploaded business data, generate dashboards and HTML reports, and convert documents or images into tables. It is intended for tasks where prompts and files may be processed by Skywork's cloud service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and uploaded files may be sent to the Skywork cloud service for processing. <br>
Mitigation: Use the skill only with prompts and files that are approved to share with Skywork, especially when handling financial, business, personal, or client data. <br>
Risk: API key setup or troubleshooting commands can expose the full SKYWORK_API_KEY or configuration contents. <br>
Mitigation: Use masked or set/not-set checks instead of printing secrets, and rotate the key if it has already been exposed. <br>
Risk: Generated spreadsheet, analysis, or report outputs can contain incorrect or misleading results. <br>
Mitigation: Review generated files and analysis before relying on them or sharing them externally. <br>


## Reference(s): <br>
- [Skywork API Key Setup Guide](references/apikey-fetch.md) <br>
- [Skywork](https://skywork.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/gxcun17/skywork-excel) <br>
- [Publisher Profile](https://clawhub.ai/user/gxcun17) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown status messages with shell commands, download links, local file paths, and generated spreadsheet or report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs asynchronous Skywork Excel backend tasks, polls progress logs, can upload user-provided Excel, CSV, PDF, or image files, and may return OSS download URLs plus local output paths.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
