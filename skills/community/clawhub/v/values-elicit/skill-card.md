## Description:

Run a Moral Graph Elicitation interview to help a user articulate a source of meaning and store it as a local values card for later agent consultation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[klingefjord](https://clawhub.ai/user/klingefjord)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to run a focused values interview, write a structured values card and transcript to a local values store, and rebuild VALUES.md for later agent consultation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive personal values and full interview transcripts are saved locally and may later be consulted by other agents.

Mitigation: Set a dedicated AGENT_VALUES_DIR, review generated cards, transcripts, and VALUES.md, and delete or edit content that is too private.

Risk: Broad activation triggers and limited upfront consent may start a values interview in situations where the user did not intend one.

Mitigation: Run the skill only on explicit invocation or when the user clearly signals openness; when uncertain, ask once before continuing.

## Reference(s):

- [Values skill page](https://clawhub.ai/klingefjord/skills/values-elicit)
- [Card format reference](references/cards.md)
- [Conversation flow reference](references/conversation.md)
- [User profile snippet](references/USER_MD_SNIPPET.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Concise chat text plus Markdown values cards, transcripts, and a generated VALUES.md file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local values store, defaults to ~/.openclaw/values unless AGENT_VALUES_DIR is set, and rebuilds VALUES.md with a Node helper.]

## Skill Version(s):

1.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
