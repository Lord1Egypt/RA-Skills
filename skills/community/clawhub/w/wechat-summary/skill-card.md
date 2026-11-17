## Description:

Summarize WeChat conversations, triage unread messages, identify which items need a reply, and draft concise response suggestions while preserving privacy boundaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[benboby](https://clawhub.ai/user/benboby)

### License/Terms of Use:

MIT-0

## Use Case:

People who manage WeChat conversations use this skill to catch up on long chats, identify action items, decide what needs a reply, and draft concise responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private or sensitive chat content may be included in the context provided for summarization.

Mitigation: Share only the conversation content needed for the task and review summaries or reply drafts before using them.

Risk: Partial message coverage can lead to incomplete summaries or misplaced reply recommendations.

Mitigation: Provide the relevant conversation window when accuracy matters and treat low-confidence notes as a prompt to verify the thread.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Compact Markdown summaries, triage lists, and suggested replies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include confidence notes when message coverage is partial.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
