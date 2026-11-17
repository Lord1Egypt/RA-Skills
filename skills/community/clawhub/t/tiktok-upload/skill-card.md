## Description:

Helps agents publish or schedule TikTok videos and photo carousels through PostWire, with an owner-approved caption and privacy setting, and returns the post link.

This skill is ready for commercial/non-commercial use.

## Publisher:

[perufitlife](https://clawhub.ai/user/perufitlife)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and social media teams use this skill to publish or schedule TikTok videos and photo posts from an agent, with optional distribution to Instagram Reels and YouTube Shorts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting a social account or supplying an API key grants PostWire access to the posting workflow.

Mitigation: Confirm that you trust PostWire before connecting the account or providing the key; never expose the key in responses.

Risk: An incorrect caption, audience, platform list, or scheduled time can result in an unintended post.

Mitigation: Review the caption, privacy setting, destinations, and posting time with the account owner and obtain approval before publishing.

## Reference(s):

- [PostWire TikTok integration](https://postwire.io/mcp/tiktok/)
- [PostWire agent setup](https://postwire.io/SKILL.md)
- [PostWire error codes](https://postwire.io/docs/errors.md)
- [ClawHub skill listing](https://clawhub.ai/perufitlife/skills/tiktok-upload)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with a post link and status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Presents caption, privacy, and posting time for approval before publishing.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; skill frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
