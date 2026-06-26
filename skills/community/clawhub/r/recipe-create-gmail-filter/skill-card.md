## Description: <br>
Create a Gmail filter to automatically label, star, or categorize incoming messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users managing Gmail with the Google Workspace CLI use this recipe to create a label, create a Gmail filter, and verify that incoming messages are labeled or removed from the inbox as intended. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands run against the Gmail account currently authenticated in gws. <br>
Mitigation: Confirm gws is signed into the intended Gmail account before executing the recipe. <br>
Risk: Using the sample sender, LABEL_ID, or inbox-removal action unchanged could mislabel or archive matching messages. <br>
Mitigation: Replace sample values and confirm that removing matching messages from the inbox is the desired behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/recipe-create-gmail-filter) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown instructions with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires gws and the gws-gmail skill; sample sender and LABEL_ID values must be replaced before use.] <br>

## Skill Version(s): <br>
1.0.12 (source: ClawHub release evidence; artifact metadata version 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
