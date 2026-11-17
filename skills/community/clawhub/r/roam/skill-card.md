## Description:

Interact with Roam HQ via REST API to search meetings, get transcripts, prompt transcripts with AI, send messages, and manage groups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robfig](https://clawhub.ai/user/robfig)

### License/Terms of Use:

MIT-0

## Use Case:

Roam HQ users can ask an agent to find meetings, summarize transcripts, analyze transcript content, review group chat history, and draft or send follow-up messages through Roam.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use a Roam API token to read meeting transcripts, summaries, group lists, and chat history.

Mitigation: Install it only when that access is intended and use a least-privileged Roam token if available.

Risk: The skill can post messages to Roam chats.

Mitigation: Review any drafted chat message before allowing it to be sent.

Risk: Roam API requests may be rate limited.

Mitigation: Respect the documented burst, sustained rate, and Retry-After behavior when making API calls.

## Reference(s):

- [Roam API Documentation](https://developer.ro.am)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with REST request details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use ROAM_API_KEY to read transcripts, summaries, group lists, chat history, and post messages through the Roam API.]

## Skill Version(s):

1.0.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
