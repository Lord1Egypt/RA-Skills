## Description: <br>
Uses the WebPrinter cloud printing service to upload documents, find printers, create roaming or direct print jobs, and update print settings such as duplex mode, color, copies, and paper size. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zimsoft](https://clawhub.ai/user/zimsoft) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, operators, and developers use this skill to submit user-selected local files or HTTPS document links to WebPrinter, choose a printer workflow, and adjust print task settings through guided shell commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documents or document links selected by the user are sent to WebPrinter's cloud service. <br>
Mitigation: Use the skill only when WebPrinter's handling of that data is acceptable, and avoid highly sensitive documents unless that risk has been reviewed. <br>
Risk: The skill requires a bearer token for WebPrinter API access. <br>
Mitigation: Store the token only in WEBPRINTER_ACCESS_TOKEN, keep it private, and rotate it if exposure is suspected. <br>
Risk: Incorrect file paths, URLs, printer identifiers, task IDs, or print settings can produce unintended print jobs. <br>
Mitigation: Confirm the file or URL, target printer, task ID, and print settings before executing commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zimsoft/webprinter) <br>
- [WebPrinter service](https://any.webprinter.cn) <br>
- [WebPrinter OAuth token page](https://any.webprinter.cn/get-ai-server-token) <br>
- [WebPrinter installation guide](https://liqdopokb8.feishu.cn/docx/A0audnVIaoolXqxWUHPcvl1UnFd) <br>
- [Cloud driver print reference](https://github.com/zimsoft/cloud-driver-print/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WEBPRINTER_ACCESS_TOKEN and sends selected documents or document links to WebPrinter.] <br>

## Skill Version(s): <br>
1.0.11 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
