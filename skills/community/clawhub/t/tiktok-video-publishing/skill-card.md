## Description:

Configures TikTok video publishing through WoopSocial by producing a search-optimized caption, cover direction, privacy and engagement settings, disclosure flags, and DIRECT_POST or MEDIA_UPLOAD guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[social-media-skills](https://clawhub.ai/user/social-media-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, social media operators, and brand teams use this skill to prepare a TikTok video post for publishing after the video file and campaign inputs already exist. It helps an agent produce the publish configuration, caption, cover guidance, validation checks, and scope boundaries needed before posting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect caption, privacy, cover, disclosure, or post mode settings could affect public brand content.

Mitigation: Review each caption, privacy level, disclosure flag, cover, and DIRECT_POST versus MEDIA_UPLOAD choice before publishing.

Risk: The skill can be misapplied to work outside its scope, such as filming or editing video, attaching licensed trending sounds through the API, pinning comments, editing already scheduled posts, or inventing metrics.

Mitigation: Require an existing video file, use MEDIA_UPLOAD or native TikTok steps for trending sounds and pinned comments, use delete and recreate for edits where allowed, and rely only on native analytics.

Risk: False branded-content disclosure or prohibited AI uses could create compliance and platform-policy risk.

Mitigation: Set isBrandedContent and isYourBrand truthfully, place ad disclosures up front when needed, reject fake endorsements or unlabeled deepfakes of real people, and do not make branded content private.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/social-media-skills/skills/tiktok-video-publishing)
- [Caption SEO, publish config + two worked examples](references/publish-config-and-recipes.md)
- [Scope, distinctions + connections](references/scope-and-connections.md)
- [The REACH framework](references/the-reach-framework.md)
- [TikTok video publishing 2026](references/video-publishing-2026-reality.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with publish configuration fields and caption text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill produces guidance and configuration for an existing video file; it does not film, edit, generate video, attach native trending sounds, pin comments, or fabricate metrics.]

## Skill Version(s):

1.0.0 (source: artifact frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
