## Description:

Enhances Telegram replies with context-aware dynamic CTA buttons that provide relevant, time-sensitive, task-oriented options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dendyadinirwana](https://clawhub.ai/user/dendyadinirwana)

### License/Terms of Use:


## Use Case:

External Telegram agent users use this skill to receive quick-action buttons that match the conversation context and time of day. Agent builders can use it to structure Telegram replies with button rows, callback actions, and a manual input fallback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may add Telegram CTA buttons more often than desired during Telegram conversations.

Mitigation: Review button text and callback actions before use, and limit button insertion to conversations where quick actions improve the user's workflow.

## Reference(s):

- [Time-Based Button Presets](artifact/references/time_logic.md)
- [ClawHub skill page](https://clawhub.ai/dendyadinirwana/skills/tg-smart-cta)

## Skill Output:

**Output Type(s):** [Markdown, Code, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline JavaScript examples and button configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Telegram button text and callback_data suggestions; no hidden code, persistence, credential access, or destructive behavior was identified by security evidence.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
