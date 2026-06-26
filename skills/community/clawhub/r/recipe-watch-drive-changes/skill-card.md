## Description: <br>
Subscribe to change notifications on a Google Drive file or folder. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this recipe to create, list, and renew Google Workspace Events subscriptions for Google Drive file or folder changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A subscription can be created against the wrong Google account, Drive resource, Google Cloud project, or Pub/Sub topic. <br>
Mitigation: Confirm the intended Google identity, Drive resource, project, and topic before running the subscription command. <br>
Risk: Pub/Sub notifications or included resource payloads can expose Drive change data to unintended recipients. <br>
Mitigation: Restrict Pub/Sub IAM access and only enable includeResource payloads when the workflow requires them. <br>
Risk: Unneeded subscriptions can continue sending Drive change notifications. <br>
Mitigation: Delete or stop renewing subscriptions when monitoring is no longer required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/recipe-watch-drive-changes) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON command arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws command-line tool and the gws-events skill.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
