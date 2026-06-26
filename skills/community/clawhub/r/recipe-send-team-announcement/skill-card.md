## Description: <br>
Send a team announcement via both Gmail and a Google Chat space. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Teams or workspace operators use this recipe to send the same announcement through Gmail and Google Chat after confirming recipients, Chat space, subject, and message body. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the recipe can send real messages to the configured Gmail recipient and Google Chat space. <br>
Mitigation: Before execution, confirm the Google account, recipient address, Chat space, subject, and announcement body. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/recipe-send-team-announcement) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws CLI plus the gws-gmail and gws-chat skills; running the commands can send real Gmail and Google Chat messages.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
