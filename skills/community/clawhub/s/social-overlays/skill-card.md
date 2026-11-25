## Description:

Provides eleven short-form video overlay templates and presets for calls to action, follows, reviews, comments, notifications, and social counts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vargai](https://clawhub.ai/user/vargai)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, video editors, and developers use this skill to choose and build readable overlays for short-form ads and creator videos. It provides platform-aware safe zones, timing guidance, presets, and implementation examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Viewer-count presets can animate synthetic values, which the security review identifies as suspicious.

Mitigation: Use real, permissioned counts in published work; limit synthetic values to clearly labeled demos.

Risk: Unpinned HyperFrames commands may run changing upstream releases.

Mitigation: Pin HyperFrames to a reviewed version before running its commands.

Risk: Review coverage is incomplete, including a missing referenced path and some bundled font files.

Mitigation: Inspect the missing path and bundled font assets as part of the release review.

## Reference(s):

- [Platform safe zones](references/platform-safe-zones.md)
- [Sources and references](references/sources.md)
- [FTC final rule on fake reviews and testimonials](https://www.ftc.gov/news-events/news/press-releases/2024/08/federal-trade-commission-announces-final-rule-banning-fake-reviews-testimonials)
- [TikTok Ads creative best practices](https://ads.tiktok.com/help/article/creative-best-practices?lang=en)
- [Google Ads vertical video safe zones](https://support.google.com/google-ads/answer/9128498?hl=en)
- [HyperFrames registry](https://github.com/heygen-com/hyperframes/tree/main/registry)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Code, Shell commands, Video files]

**Output Format:** [Markdown guidance, JSON presets, HTML/CSS or Remotion examples, shell commands, and rendered MP4, WebM, or MOV video]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local rendering with HyperFrames 0.8 or Remotion 4; requires Node 22 and ffmpeg; no API key.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
