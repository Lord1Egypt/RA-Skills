## Description:

Run Twitter/X likes, follows, replies, and OAuth-gated posting through AIsa for users who already know which account, tweet, or campaign to act on and need explicit engagement workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bibaofeng](https://clawhub.ai/user/bibaofeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to research Twitter/X context, publish approved posts, replies, and quotes, and perform explicit likes, follows, and unfollows through AIsa-backed workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Command output can expose the AIsa API key.

Mitigation: Avoid logging command output, redact or fix API-key fields before use, and rotate any key that may have been exposed.

Risk: The skill can take public Twitter/X actions such as posting, replying, liking, following, unfollowing, and uploading media.

Mitigation: Require explicit user approval for the target account, content, action, and media path, and confirm success only from the returned API result.

Risk: Local media files passed to the posting workflow are uploaded through the remote AIsa service.

Mitigation: Pass only media paths the user intentionally provided for upload and review files before sending them.

## Reference(s):

- [AIsa Twitter OAuth](references/post_twitter.md)
- [AIsa Twitter Engagement](references/engage_twitter.md)
- [AIsa homepage](https://aisa.one)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY; actions depend on remote AIsa and Twitter/X responses.]

## Skill Version(s):

1.0.3 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
