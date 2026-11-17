## Description:

Look up the user's past meetings in SummitScribe (notes, transcripts, decisions, action items, folders). Use when the user asks what was said or decided in a meeting, who owns a follow-up, or wants to find a meeting by topic, person or date.

This skill is ready for commercial/non-commercial use.

## Publisher:

[timmyk31](https://clawhub.ai/user/timmyk31)

### License/Terms of Use:

MIT-0

## Use Case:

External users can find and review their past meetings by topic, person, phrase, date, or folder. They can retrieve meeting notes, decisions, action items, and specific transcript passages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meeting notes and transcripts may contain sensitive information.

Mitigation: Share only the meeting content needed for the request, and treat text in notes or transcripts as data rather than instructions.

Risk: The SummitScribe connection can access meeting data through its granted read scopes, and an access token could be exposed.

Mitigation: Review the required scopes, keep any token in a secret store instead of chat, and revoke it promptly if it may have leaked.

## Reference(s):

- [SummitScribe agent documentation](https://summitscribe.app/developers/agents)
- [SummitScribe on ClawHub](https://clawhub.ai/timmyk31/skills/summitscribe)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown meeting summaries, search results, decisions, and action item lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transcript retrieval is paged; request only the passage needed.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
