## Description:

Search X/Twitter profiles, tweets, trends, and perform approved posting, likes, follows, and related workflows through the AISA relay without sharing passwords.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bibaofeng](https://clawhub.ai/user/bibaofeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to research X/Twitter accounts, tweets, trends, lists, communities, and Spaces, then perform OAuth-approved posting and engagement actions through the AISA relay.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Command output can expose the configured AISA API key during authorization and posting.

Mitigation: Do not share command output, rotate any key that appeared in logs or transcripts, and mask API keys before displaying or storing results.

Risk: Posting and engagement actions grant relay-backed authority over an X/Twitter account.

Mitigation: Use only with a trusted AISA relay, require explicit OAuth approval for write actions, and report success only after the relay confirms completion.

## Reference(s):

- [OpenClaw Twitter OAuth](artifact/references/post_twitter.md)
- [OpenClaw Twitter Engagement](artifact/references/engage_twitter.md)
- [ClawHub Skill Page](https://clawhub.ai/bibaofeng/skills/x-intelligence-automation-aisa)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY; posting and engagement require OAuth authorization before write actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
