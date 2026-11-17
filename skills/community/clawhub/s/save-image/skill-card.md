## Description:

Download images, GIFs, and media from web URLs using browser-like headers, Referer handling, CDN-aware scraping, gifgrep, yt-dlp, and download verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bstokes0971](https://clawhub.ai/user/bstokes0971)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill when they need reliable command guidance for saving images, GIFs, memes, thumbnails, or social media from URLs while handling common CDN and header-related failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide agents to fetch media from web URLs, including URLs the user did not intend to access.

Mitigation: Review URLs before fetching and avoid login-gated or private content unless explicitly intended.

Risk: Download commands can create or overwrite local files.

Mitigation: Choose output paths carefully and check for existing files before running generated commands.

Risk: Servers or CDNs can return HTML error pages or blocked responses instead of the requested media.

Mitigation: Verify HTTP status, file size, and file type after download as described by the skill.

## Reference(s):

- [Tool Reference](references/tools.md)
- [ClawHub Skill Page](https://clawhub.ai/bstokes0971/skills/save-image)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code]

**Output Format:** [Markdown guidance with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May suggest network fetches and local output paths; users should review URLs and paths before execution.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
