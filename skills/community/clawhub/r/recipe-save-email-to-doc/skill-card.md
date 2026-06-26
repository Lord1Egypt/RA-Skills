## Description: <br>
Save a Gmail message body into a Google Doc for archival or reference. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and productivity-focused agents use this recipe to find a selected Gmail message, retrieve its content, and save the email body into a Google Doc for archival or reference. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The selected Gmail message may contain sensitive or regulated content. <br>
Mitigation: Confirm the email is the intended one and avoid copying unnecessary sensitive or regulated content into the document. <br>
Risk: The created Google Doc may expose retained email content through document permissions or retention settings. <br>
Mitigation: Review the created document's sharing permissions and retention expectations after writing the email body. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/recipe-save-email-to-doc) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/googleworkspace-bot) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown recipe with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires gws plus the gws-gmail and gws-docs skills; uses a selected Gmail message ID and Google Docs document ID.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata; artifact metadata version 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
