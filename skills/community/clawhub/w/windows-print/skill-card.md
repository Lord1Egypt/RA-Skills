## Description: <br>
Print files from inbound attachments or local paths on Windows only after a clear user print request, with support for printer selection, multiple copies, and optional waiting for the spawned print process. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sqfcyily](https://clawhub.ai/user/sqfcyily) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to convert explicit user print requests for attachments or local files into Windows PowerShell print jobs. It is intended for workflows where the agent must confirm the target file or batch before printing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A failed named-printer job may fall back to the default printer, which can expose confidential documents to the wrong device. <br>
Mitigation: Verify the exact file and printer before printing, avoid broad wildcard patterns, and use this skill cautiously with shared office printers or confidential documents. <br>
Risk: Printing is a real-world action that may disclose file contents or consume physical resources if triggered on the wrong target. <br>
Mitigation: Require an explicit print instruction and a clear file or batch selection for each print action; do not print based on file arrival, filenames, or document contents. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline PowerShell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run bundled PowerShell scripts to list printers or submit print jobs when the user explicitly approves printing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
