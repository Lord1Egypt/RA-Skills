## Description: <br>
Check X notifications, mentions, or reply threads and answer posts that still need a response from the user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dishant0406](https://clawhub.ai/user/dishant0406) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users with an X account use this skill to review notifications, mentions, or reply threads and post concise, first-person replies where the account has not already responded. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can like posts and publish replies from the user's X account. <br>
Mitigation: Review or require approval for each proposed reply before posting, and confirm the final report lists every reply and skip decision. <br>
Risk: The reply style guidance may encourage first-person feelings or experience claims that are not grounded in facts the user supplied. <br>
Mitigation: Keep replies thread-specific and avoid claims about personal experience, emotion, or prior use unless the user provided that context. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dishant0406/x-reply-unreplied) <br>
- [Human Voice](references/human-voice.md) <br>
- [Inbox Workflow](references/inbox-workflow.md) <br>
- [Reply Rules](references/reply-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Short plain-text replies plus a Markdown completion report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default cap of up to 5 suitable reply opportunities per run; replies are 1 or 2 short sentences unless the user asks for longer.] <br>

## Skill Version(s): <br>
1.1.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
