## Description:

This skill helps an agent respond to emotionally expressive or casual conversation by selecting a context-appropriate sticker keyword, querying a third-party sticker API, and returning one sticker with accompanying text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chensanle](https://clawhub.ai/user/chensanle)

### License/Terms of Use:


## Use Case:

External users and agent operators use this skill to add casual, emotion-aware sticker responses in chat. It is intended for conversational moments such as greetings, thanks, celebration, encouragement, jokes, complaints, and other emotionally colored exchanges.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is always on and may contact a third-party sticker API during ordinary emotional or casual messages.

Mitigation: Use the skill only where automatic sticker lookup is expected, and prefer releases that require explicit sticker requests or user consent before external lookups.

Risk: Conversation-derived sticker keywords may be sent to a third-party service.

Mitigation: Avoid enabling the skill in sensitive conversations or environments where message-derived search terms should not leave the agent runtime.

Risk: The third-party API returns media URLs that the security evidence describes as unvalidated.

Mitigation: Validate or proxy returned media URLs before display, and restrict rendering to trusted media schemes and hosts when deploying.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chensanle/skills/sticker)
- [Third-party sticker API endpoint](https://api.tangdouz.com/a/biaoq.php?return=json&nr=关键词)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API Calls, guidance]

**Output Format:** [Markdown text with a MEDIA image token and optional inline shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [At most one sticker per response; sticker selection depends on conversation context and third-party API results.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
