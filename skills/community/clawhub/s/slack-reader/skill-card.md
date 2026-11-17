## Description:

Read and summarize Slack channel history and thread conversations when given Slack links, channel IDs, or requests to inspect channel, thread, or reply conversations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[epikoding](https://clawhub.ai/user/epikoding)

### License/Terms of Use:


## Use Case:

Agents and developers use this skill to retrieve Slack channel history, full threads, or individual replies and turn them into concise conversation context for review or summarization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can retrieve Slack conversations that may contain sensitive or confidential information.

Mitigation: Use it only for channels and threads the requester is authorized to review, and avoid summarizing confidential conversations unless authorized.

Risk: The skill uses a local OpenClaw Slack bot token to access channels and threads available to that bot.

Mitigation: Install only when this local token access is acceptable, and treat the token and retrieved conversation text as sensitive.

Risk: Broad channel history requests may retrieve more conversation data than needed.

Mitigation: Use date and limit options for broad channels, and explicitly decide whether thread replies should be included.

Risk: Slack user identity mappings are cached locally for up to 24 hours.

Mitigation: Account for the local cache when handling user identity data or cleaning up sensitive workspace artifacts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/epikoding/skills/slack-reader)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text conversation transcripts with Markdown usage examples and shell command invocations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Messages are formatted one per line with timestamps, sender names, participants, reactions, attachment references, and optional inline thread replies.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
