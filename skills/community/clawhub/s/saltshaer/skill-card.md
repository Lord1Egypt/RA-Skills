## Description: <br>
Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yueyongyue](https://clawhub.ai/user/yueyongyue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to set up and run gog commands for Google Workspace workflows across Gmail, Calendar, Drive, Contacts, Sheets, and Docs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on Google OAuth access for the external gog CLI. <br>
Mitigation: Use the narrowest Google account and service set needed, and review OAuth consent before use. <br>
Risk: Write-capable commands can send mail, create events, or change Workspace data such as Sheets and Docs. <br>
Mitigation: Require explicit confirmation before executing commands that mutate Google Workspace data. <br>


## Reference(s): <br>
- [gog CLI homepage](https://gogcli.sh) <br>
- [ClawHub skill page](https://clawhub.ai/yueyongyue/saltshaer) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and CLI examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the external gog CLI and Google OAuth setup; some commands can modify Workspace data.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
