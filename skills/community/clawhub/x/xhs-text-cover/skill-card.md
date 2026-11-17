## Description:

Xhs helps agents draft Xiaohongshu titles and post copy, generate simple cover images, and guide publishing, search, and engagement actions through a local Xiaohongshu MCP service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luckychay](https://clawhub.ai/user/luckychay)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and operators use this skill to create Xiaohongshu-ready titles, post copy, cover images, and guided account actions such as publishing, search, comments, likes, and favorites.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A third-party Xiaohongshu MCP binary can control an authenticated account from the user's machine.

Mitigation: Use only pinned and checksum-verified releases, run the service as an unprivileged user or inside a container, and avoid installing it as a root-level system service.

Risk: Stored Xiaohongshu session cookies can act like passwords if exposed.

Mitigation: Avoid pasting raw browser cookies when possible, restrict file access to cookie storage, and rotate or delete cookies after use.

Risk: Publishing, commenting, liking, and favoriting actions can affect a real social account.

Mitigation: Require user confirmation and payload review before each account action, especially public posts and engagement actions.

## Reference(s):

- [Content Guide](references/content-guide.md)
- [Cover Guide](references/cover-guide.md)
- [Title Guide](references/title-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/luckychay/skills/xhs-text-cover)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands, generated post text, and optional local image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Cover images are generated as local 1080x1440 image files when ImageMagick is available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
