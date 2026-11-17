## Description:

Create locally rendered 1080×1920 kinetic-text shorts from sourced material, with a cover and review sheet, and optionally publish them to TikTok, Instagram Reels, or YouTube Shorts through WoopSocial after confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[social-media-skills](https://clawhub.ai/user/social-media-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and social media teams use this skill to turn sourced facts, articles, data, launches, or lists into short vertical videos, review them, and optionally publish them to TikTok, Instagram Reels, or YouTube Shorts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API-key-in-URL connection option can expose a social-posting key through shared links, logs, or configuration exports.

Mitigation: Prefer local-only rendering or OAuth sign-in, avoid the API-key-in-URL option, and rotate any exposed key.

Risk: Publishing can affect connected social accounts and audiences.

Mitigation: Review the account, privacy setting, schedule, and post content before approving publication.

## Reference(s):

- [Project homepage](https://github.com/social-media-skills/remotion-shorts-skill)
- [Short JSON format](artifact/references/short-json.md)
- [Writing shorts](artifact/references/writing-shorts.md)
- [Platform specifications](artifact/references/platform-specs.md)
- [WoopSocial posting guide](artifact/references/woopsocial.md)
- [WoopSocial tool reference](https://docs.woopsocial.com/mcp/tools-reference)

## Skill Output:

**Output Type(s):** [Video files, Image files, JSON, Guidance]

**Output Format:** [MP4 short video, JPG review sheet and cover, and a JSON scene script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Vertical 1080×1920 video at 30 fps. Posting is optional and requires user confirmation.]

## Skill Version(s):

1.0.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
