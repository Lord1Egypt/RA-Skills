## Description:

Produces a compact, complete context dump of the current session directly in chat for reference, handoff, or session-state recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vyctorbrzezowski](https://clawhub.ai/user/vyctorbrzezowski)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent to summarize the active conversation into a concise Markdown session brief. It is useful for preserving goals, decisions, current state, important references, blockers, and next steps without creating files unless requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may recap sensitive details already present in the chat.

Mitigation: The skill instructs the agent to omit secrets, tokens, private credentials, and unnecessary personal data from the brief.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown block returned in chat]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No files are created unless the user explicitly requests one; the brief should omit secrets, tokens, private credentials, and unnecessary personal data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
