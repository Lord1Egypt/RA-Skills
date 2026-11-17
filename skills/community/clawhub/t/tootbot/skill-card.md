## Description:

Publishes content to Mastodon when an agent needs to post a status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[behrangsa](https://clawhub.ai/user/behrangsa)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to post one or more Mastodon statuses, optionally with media attachments, visibility settings, language, quote policy, and scheduled time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish Mastodon posts using the user's account token, including public posts, media attachments, visibility settings, and scheduled times.

Mitigation: Review every status payload and media attachment before execution, and use a Mastodon access token with only the minimum posting permissions needed.

Risk: The README recommends unpinned bunx commands for remote package execution.

Mitigation: Pin and review the package version before running bunx, or run the bundled artifact script directly after inspection.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/behrangsa/skills/tootbot)
- [Clawdbot repository](https://github.com/anthropics/clawdbot)
- [Claude Code skills documentation](https://code.claude.com/docs/en/skills)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash commands and JSON status payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Bun plus MASTODON_URL and MASTODON_ACCESS_TOKEN environment variables.]

## Skill Version(s):

0.5.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
