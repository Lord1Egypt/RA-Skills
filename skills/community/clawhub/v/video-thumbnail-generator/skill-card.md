## Description:

Generate thumbnail candidates from video frames so creators, ecommerce teams, and operators can choose cleaner covers for social, storefronts, and internal sharing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leooooooow](https://clawhub.ai/user/leooooooow)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, ecommerce teams, operators, and other external users use this skill to extract and compare candidate still frames from a supplied video, then choose a clearer cover image for social, storefront, gallery, ad, or internal sharing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private or sensitive source videos may be processed in the agent workspace while candidate frames are extracted and evaluated.

Mitigation: Use only videos the user is comfortable having processed by the agent, and avoid private or sensitive video unless the workspace and retention practices are acceptable.

Risk: Low-quality, blurry, transitional, or awkward source footage may produce weak frame-based thumbnail candidates.

Mitigation: Tell the user when the video is weak for still-frame thumbnails, avoid overstating mediocre candidates, and recommend a custom static image when frame grabs are not suitable.

## Reference(s):

- [Video Thumbnail Generator Output Template](references/output-template.md)

## Skill Output:

**Output Type(s):** [files, markdown, guidance]

**Output Format:** [Markdown shortlist with candidate thumbnail frames, rationale, a best-choice recommendation, and risks or notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include extracted still-frame files when the agent has access to the source video and frame extraction tools.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
