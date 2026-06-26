## Description: <br>
Monitor Outlook and other common webmail inboxes in a persistent Edge profile, process new messages as a detached local background task, capture complete message screenshots, download attachments to the desktop, and write structured Excel rows with deterministic Python logic. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jizhidemu52](https://clawhub.ai/user/jizhidemu52) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to start, stop, check, or modify a Windows webmail monitoring workflow that processes inbox messages into local workbooks, screenshots, attachments, and logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The monitor can keep using a logged-in mailbox and save email contents, screenshots, and attachments to disk. <br>
Mitigation: Run it only for an intended mailbox, preferably with a dedicated browser profile, and confirm where workbook data, screenshots, logs, and attachments are stored before starting. <br>
Risk: The release evidence flags the skill for review because its behavior is broad and automatic. <br>
Mitigation: Review the required scripts and command surface before execution, verify how to stop the monitor, and delete retained email artifacts when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jizhidemu52/webmail-email-monitor-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with inline PowerShell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct a local monitor to produce an Excel workbook, message screenshots, downloaded attachments, and runtime logs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
