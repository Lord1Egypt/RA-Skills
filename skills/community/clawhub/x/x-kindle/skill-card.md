## Description: <br>
Send X/Twitter posts to Kindle for distraction-free reading. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brianlu365ai](https://clawhub.ai/user/brianlu365ai) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to convert shared X/Twitter post links into Kindle-readable email content and send them to a configured Kindle address. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to store an email app password in a plain TOOLS.md file. <br>
Mitigation: Use a dedicated email account or protected secret storage instead of placing a Gmail app password in TOOLS.md. <br>
Risk: Tweet information is fetched through fxtwitter and emailed through the user's SMTP provider. <br>
Mitigation: Review the content before sending and avoid using the workflow for sensitive or private material. <br>
Risk: The workflow can send email to a configured Kindle recipient. <br>
Mitigation: Confirm the Kindle recipient address before sending. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with formatted HTML email content and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches tweet data through fxtwitter and sends formatted content through the user's SMTP provider.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
