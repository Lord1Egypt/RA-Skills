## Description: <br>
Apply Gmail labels to matching messages and archive them to keep your inbox clean. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People who manage Gmail use this recipe to search matching messages, apply Gmail labels, and remove the messages from the inbox without deleting them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The recipe can change Gmail labels and remove messages from the inbox. <br>
Mitigation: Before running modify commands, confirm the Google account, search results, message ID, and label ID; archiving removes messages from the inbox but does not delete them. <br>


## Reference(s): <br>
- [Recipe Label And Archive Emails on ClawHub](https://clawhub.ai/googleworkspace-bot/recipe-label-and-archive-emails) <br>
- [googleworkspace-bot publisher profile](https://clawhub.ai/user/googleworkspace-bot) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires gws and the gws-gmail skill; commands can modify Gmail labels and inbox visibility.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata; embedded skill metadata version 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
