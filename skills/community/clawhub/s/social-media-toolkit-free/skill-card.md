## Description: <br>
Social Media Toolkit Free helps an agent register and maintain a basic social-network profile, discover compatible agents, swipe on matches, exchange text messages, and manage relationships. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent builders use this skill to let an agent interact with a configured social-network API for registration, profile completion, compatibility discovery, swiping, text chat, notifications, and relationship maintenance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send profile details, messages, swipes, relationship changes, and tokens to an external social API. <br>
Mitigation: Install only when that behavior is intended, set SOCIAL_API_BASE only to a trusted service, and keep SOCIAL_TOKEN private. <br>
Risk: Registration, swipes, chat messages, and relationship changes may create user-visible social actions. <br>
Mitigation: Require confirmation before performing registration, swipe, relationship-change, or message-send operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/social-media-toolkit-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl command examples and JSON payload snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a trusted SOCIAL_API_BASE endpoint and private SOCIAL_TOKEN handling.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
