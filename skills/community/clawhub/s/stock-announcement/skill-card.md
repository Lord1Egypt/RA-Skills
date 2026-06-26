## Description: <br>
Daily stock portfolio analysis with Gmail report delivery and Sonos voice announcement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and portfolio owners can use this skill to generate a daily stock portfolio summary, send it by Gmail, and announce the summary on a configured Sonos speaker. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package declares a runnable stock announcement script and configuration file, but the submitted artifact does not include them. <br>
Mitigation: Review before installing and do not run until the missing script and configuration are supplied and inspected. <br>
Risk: The skill requires Gmail OAuth access and recipient email configuration. <br>
Mitigation: Confirm the Gmail OAuth scope, token location, recipient address, and report contents before use. <br>
Risk: The skill can announce financial information through a Sonos speaker. <br>
Mitigation: Confirm the target speaker and avoid audible announcements of sensitive financial details in shared spaces. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/stock-announcement) <br>
- [Publisher profile](https://clawhub.ai/user/terrycarter1985) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Gmail OAuth credentials, recipient configuration, Python dependencies, and Sonos CLI access.] <br>

## Skill Version(s): <br>
99.99.99 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
