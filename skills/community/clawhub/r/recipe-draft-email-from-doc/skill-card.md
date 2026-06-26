## Description: <br>
Read content from a Google Doc and use it as the body of a Gmail message. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users working with Google Workspace use this recipe to read a Google Doc and use the document text as the body of a Gmail message. Review the document ID, recipient, subject, and body before sending. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is titled as a draft helper but its steps send a Gmail message containing document content. <br>
Mitigation: Verify the Google account, document ID, recipient, subject, and full message body, and require explicit confirmation before running the Gmail send command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/recipe-draft-email-from-doc) <br>
- [Publisher profile](https://clawhub.ai/user/googleworkspace-bot) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws command and the gws-docs and gws-gmail skills.] <br>

## Skill Version(s): <br>
1.0.12 (source: ClawHub release metadata); artifact metadata version 0.22.5 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
