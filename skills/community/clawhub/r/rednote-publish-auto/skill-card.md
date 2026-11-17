## Description:

Creates Xiaohongshu/RedNote post copy from a user topic or source material, renders Markdown image cards, and publishes the post after explicit user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hhua007](https://clawhub.ai/user/hhua007)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and social media operators use this skill to draft Xiaohongshu/RedNote posts, turn Markdown into 3:4 image cards, and publish only after the user approves the preview.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles full Xiaohongshu account cookies that can authorize account actions.

Mitigation: Use a dedicated Xiaohongshu account, keep cookies out of shared project directories, and rotate or revoke any cookie that may have been exposed.

Risk: API publishing mode can send the account cookie to an API service.

Mitigation: Use API mode only with a local or otherwise trusted API URL, and avoid remote or untrusted API endpoints.

Risk: Rendering untrusted Markdown can expose the user to unsafe HTML or network-loading behavior.

Mitigation: Render only trusted Markdown until HTML sanitization and network restrictions are added.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/hhua007/skills/rednote-publish-auto)
- [Xiaohongshu](https://www.xiaohongshu.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown drafts, rendered PNG image-card files, shell commands, and concise publishing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user confirmation before publishing and depends on a valid Xiaohongshu session cookie.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
