## Description:

Approval-first social media publishing with the ReplyNodes scheduler for cross-posting and auto-posting in OpenClaw, using browser OAuth for LinkedIn and X/Twitter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[replynodes-ai](https://clawhub.ai/user/replynodes-ai)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to connect OpenClaw to ReplyNodes, prepare social posts for connected LinkedIn and X/Twitter channels, preview the channel-specific output, and publish or schedule only after explicitly confirming a named run.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish or schedule public social posts after approval.

Mitigation: Review the channel preview and confirm only a named run that should be published or scheduled.

Risk: Unpinned installation can make it harder to verify the reviewed package.

Mitigation: Install from a reviewed immutable tag or commit.

Risk: A stored ReplyNodes session can retain access until it expires or is revoked.

Mitigation: Revoke the ReplyNodes session when uninstalling or when access is no longer needed.

## Reference(s):

- [ReplyNodes OpenClaw homepage](https://replynodes.com/openclaw)
- [README](README.md)
- [Security guidance](SECURITY.md)
- [Release notes](RELEASE.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Configuration guidance]

**Output Format:** [Markdown with structured JSON examples, confirmation prompts, channel previews, and per-channel receipts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires browser authorization, channel capability checks, and fresh explicit confirmation before publish or schedule side effects.]

## Skill Version(s):

1.0.3 (source: evidence release, artifact VERSION)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
