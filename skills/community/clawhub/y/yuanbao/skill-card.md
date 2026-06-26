## Description: <br>
Yuanbao helps agents interact in Yuanbao groups by mentioning users, querying group and member information, and sending requested direct messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maliot100x](https://clawhub.ai/user/maliot100x) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to participate in Yuanbao group chats, look up exact members for mentions, query group information, and send requested direct messages or media. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can cause agent replies, @mentions, direct messages, or media to be sent to Yuanbao users. <br>
Mitigation: Install it only where agent replies are expected to be posted into Yuanbao chats, and review sensitive DM or media requests before sending. <br>
Risk: Wrong recipient selection could notify or message the wrong person in a group. <br>
Mitigation: Use member lookup before mentions and ask the user to clarify when multiple matching members are returned. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/maliot100x/yuanbao) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Guidance] <br>
**Output Format:** [Plain text replies with JSON-style tool calls when member lookup, group queries, direct messages, or media sending are needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may be delivered into Yuanbao chats as group replies, @mentions, or direct messages through the configured Yuanbao tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
