## Description:

Draft, publish, and manage posts on X (Twitter), inspect timelines, manage profiles, and automate social media workflows via the X API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an X account through ClawLink, inspect timelines and profiles, search posts, and prepare or perform account actions such as posts, follows, bookmarks, media uploads, and direct messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables high-impact actions on a real X account, including public posts, follows, blocks, bookmarks, media, and direct messages.

Mitigation: Review requested actions before execution, use tool previews for writes, and require explicit user confirmation before posting, deleting, following, blocking, bookmarking, uploading media, or sending direct messages.

Risk: The skill asks users to install and allowlist an external ClawLink plugin that remains enabled in OpenClaw.

Mitigation: Proceed only after verifying the ClawLink plugin source and OAuth permissions, and keep the plugin enabled only when its account access is needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hith3sh/skills/twitter-posts)
- [ClawLink](https://claw-link.dev)
- [ClawLink OpenClaw Docs](https://docs.claw-link.dev/openclaw)
- [X API Documentation](https://developer.x.com/en/docs)
- [X API Reference](https://developer.x.com/en/docs/api-reference)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a connected X account through ClawLink; write actions should be previewed and explicitly confirmed.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
