## Description:

Creates completion-focused TikTok Photo Mode carousel plans and WoopSocial PHOTO publish configurations, including slide structure, overlay copy, caption guidance, privacy, comments, music, and truthful disclosure flags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[social-media-skills](https://clawhub.ai/user/social-media-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Social media teams, creators, and publishing agents use this skill to plan TikTok-native Photo Mode carousels and prepare WoopSocial PHOTO publish settings grounded in brand profile and goals/KPIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A TikTok PHOTO post could be published with unintended privacy, comment, music, or DIRECT_POST versus MEDIA_UPLOAD settings.

Mitigation: Review platform-input values and validate the WoopSocial PHOTO configuration before publishing.

Risk: Incorrect commercial-content disclosure flags could misrepresent whether the post promotes the user's brand or paid/gifted third-party content.

Mitigation: Set isYourBrand and isBrandedContent truthfully and review those values before publishing.

Risk: Photo Mode performance could be overstated or metrics could be fabricated.

Mitigation: Avoid virality or reach guarantees and use native analytics for reporting.

Risk: Users may assume the skill creates carousel images itself.

Mitigation: Route image creation to a human or image-generation skill before WoopSocial publishes the native PHOTO post.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/social-media-skills/skills/tiktok-photo-mode)
- [The SWIPE Framework](references/the-swipe-framework.md)
- [TikTok Photo Mode 2026 Reality](references/photo-mode-2026-reality.md)
- [Content Types, Publish Config, and Worked Examples](references/carousel-recipes-and-publish.md)
- [Scope, Distinctions, and Connections](references/scope-and-connections.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown with structured PHOTO publish configuration fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes slide plan, overlay copy, caption, and publish configuration; image creation and analytics collection remain outside the skill output.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
