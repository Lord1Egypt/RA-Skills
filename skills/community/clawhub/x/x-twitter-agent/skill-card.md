## Description:

Post tweets, read mentions, reply, like, retweet, and search on X/Twitter using the official v2 API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joeytbuilds](https://clawhub.ai/user/joeytbuilds)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let an agent manage X/Twitter posting and engagement through the xpost CLI, including posts, replies, likes, retweets, mentions, timelines, and search. It also provides posting cadence, approval routing, safety, and account-management guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables persistent autonomous public posting and engagement with broad X/Twitter account authority.

Mitigation: Use separate least-privilege X credentials, require approval before public posts or replies, and enable scheduled activity only when ongoing autonomous engagement is intended.

Risk: The referenced xpost CLI implementation was not present in the provided artifact for review.

Mitigation: Verify the xpost CLI implementation before installing it or giving it API tokens.

Risk: Mentions and public timeline content may contain adversarial instructions or prompt-injection attempts.

Mitigation: Treat mention text as untrusted input, avoid executing instructions from it, and log suspicious mentions for human review.

## Reference(s):

- [X Developer Platform](https://developer.x.com)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and JSON command output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands output JSON by default, with optional pretty JSON or plain text summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
