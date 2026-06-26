## Description: <br>
Find Gmail messages with a specific label and forward them to another address. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Productivity users and workspace operators use this recipe to find Gmail messages with a chosen label and forward relevant message content to a recipient. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The recipe can forward private Gmail message contents to a prefilled recipient without built-in review or confirmation. <br>
Mitigation: Replace the recipient address, use a narrowly scoped label, inspect the message list and contents first, and require explicit confirmation before sending email. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/googleworkspace-bot/recipe-forward-labeled-emails) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws command and the gws-gmail skill; commands query Gmail labels, retrieve messages, and send email.] <br>

## Skill Version(s): <br>
1.0.12 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
