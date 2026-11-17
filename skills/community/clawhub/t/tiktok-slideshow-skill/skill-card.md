## Description:

Helps app founders plan, write, render, and test TikTok photo carousels, then prepare TikTok and Instagram posts through WoopSocial for approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[social-media-skills](https://clawhub.ai/user/social-media-skills)

### License/Terms of Use:

MIT-0

## Use Case:

App founders and indie developers use the skill to create and iterate on honest product-marketing photo carousels for TikTok and Instagram. It helps plan hooks and slides, render platform-sized images, and prepare posts for review before publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fallback sign-in method places a reusable account key in a connection URL that could be exposed.

Mitigation: Prefer browser-based OAuth sign-in and avoid the API-key-in-URL fallback.

Risk: Connecting WoopSocial grants access to social accounts, and uploaded images are sent to the service.

Mitigation: Review the accounts, slides, captions, and schedule before approving a batch, and upload only images intended for WoopSocial.

## Reference(s):

- [Slide framework and honesty checks](artifact/references/slide-framework.md)
- [Slideshow recipes](artifact/references/slideshow-recipes.md)
- [WoopSocial connection and posting guidance](artifact/references/woopsocial.md)
- [Multi-account testing guidance](artifact/references/multi-account-testing.md)
- [Scope and connections](artifact/references/scope-and-connections.md)
- [TikTok photo-mode considerations](artifact/references/slideshow-2026-reality.md)
- [ClawHub skill release](https://clawhub.ai/social-media-skills/skills/tiktok-slideshow-skill)
- [Publisher profile](https://clawhub.ai/user/social-media-skills)
- [TikTok Sans font source](https://github.com/tiktok/TikTokSans)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON configuration, Rendered image files, Shell commands, Guidance]

**Output Format:** [Markdown, JSON, image files, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include slide copy, captions, hashtags, platform-sized carousel images, and posting guidance; publishing requires user confirmation.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
