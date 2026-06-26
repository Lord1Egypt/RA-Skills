## Description: <br>
Rocket.Chat team messaging - channels, messages, users, integrations via REST API <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zenjabba](https://clawhub.ai/user/zenjabba) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, workspace administrators, and team operations users use this skill to work with Rocket.Chat rooms, messages, users, integrations, and server statistics through REST API examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses user-provided Rocket.Chat credentials for expected chat, channel, user, and integration actions. <br>
Mitigation: Install with a limited bot or service account token when possible, and avoid broad admin tokens for routine messaging. <br>
Risk: Some examples can post, edit, delete, archive channels, manage users, or use webhooks. <br>
Mitigation: Review each requested Rocket.Chat action before allowing the agent to run it, especially actions that change messages, users, channels, or integrations. <br>


## Reference(s): <br>
- [Rocket.Chat REST API documentation](https://developer.rocket.chat/reference/api/rest-api) <br>
- [Rocket.Chat API documentation](https://developer.rocket.chat/reference/api) <br>
- [ClawHub skill page](https://clawhub.ai/zenjabba/rocketchat) <br>
- [Publisher profile](https://clawhub.ai/user/zenjabba) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline bash and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses user-provided Rocket.Chat URL, token, and user ID environment variables; examples may read, post, edit, delete, archive, or manage Rocket.Chat resources depending on requested action.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
