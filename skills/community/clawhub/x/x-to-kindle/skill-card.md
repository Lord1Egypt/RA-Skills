## Description: <br>
Send X/Twitter posts and local files to Kindle for distraction-free reading. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brianlu365ai](https://clawhub.ai/user/brianlu365ai) <br>

### License/Terms of Use: <br>
ISC <br>


## Use Case: <br>
External users and developers use this skill to convert X/Twitter posts or local documents into Kindle-readable attachments and email them to a configured Kindle address. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stored SMTP app passwords may be exposed if placed in markdown configuration files. <br>
Mitigation: Keep SMTP credentials in protected environment secrets or a secret manager, and use a dedicated revocable app password for the sender account. <br>
Risk: The helper can email any local file available to the agent process. <br>
Mitigation: Only provide file paths for content explicitly intended for Kindle delivery, and review the file before invoking the helper. <br>


## Reference(s): <br>
- [X To Kindle ClawHub page](https://clawhub.ai/brianlu365ai/x-to-kindle) <br>
- [FxTwitter status API example](https://api.fxtwitter.com/status/1234567890) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with HTML and Python snippets, shell command invocation, and a helper-script email attachment workflow.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses SMTP credentials from environment variables and sends the selected local file as an email attachment to KINDLE_EMAIL.] <br>

## Skill Version(s): <br>
0.1.1 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
