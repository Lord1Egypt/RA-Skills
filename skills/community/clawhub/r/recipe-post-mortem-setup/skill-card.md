## Description: <br>
Create a Google Docs post-mortem, schedule a Google Calendar review, and notify via Chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Engineering teams use this skill to start an incident post-mortem workflow by creating the review document, scheduling the follow-up meeting, and sending a Chat notification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make live Google Workspace changes, including creating documents, calendar events, and Chat notifications. <br>
Mitigation: Review the document sharing settings, attendee list, meeting time, and Chat space or recipients before executing the commands. <br>
Risk: Incident details may be sent to the wrong audience or disclosed through an incorrectly shared document or Chat message. <br>
Mitigation: Substitute placeholders deliberately and verify the target team, space, and document permissions before sending notifications. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/googleworkspace-bot/recipe-post-mortem-setup) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws CLI and the gws-docs, gws-calendar, and gws-chat skills; commands may create documents, calendar events, and Chat messages.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata); source skill metadata version 0.22.5 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
