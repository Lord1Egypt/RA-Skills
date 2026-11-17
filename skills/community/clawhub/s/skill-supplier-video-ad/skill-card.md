## Description:

Build polished 1080x1920 TikTok/Instagram Reels product ads from supplier or CJ Dropshipping source videos using clean-zone detection, slow-motion cuts, Pillow-rendered text overlays, branded CTA end cards, and audio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zero2ai-hub](https://clawhub.ai/user/zero2ai-hub)

### License/Terms of Use:


## Use Case:

Developers and ecommerce operators use this skill to turn raw supplier or CJ Dropshipping footage into short-form product ads for TikTok and Instagram Reels. It helps identify text-free clips, define a JSON product configuration, and assemble a portrait MP4 with overlays, music, and a branded CTA card.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A product configuration can influence the temporary output path that the pipeline later deletes during cleanup.

Mitigation: Run only trusted configs, keep output_name to a plain filename with no slashes or .. segments, and use a dedicated working directory or container until cleanup handling is hardened.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zero2ai-hub/skills/skill-supplier-video-ad)
- [ClawHub publisher profile](https://clawhub.ai/user/zero2ai-hub)
- [SKILL.md](artifact/SKILL.md)
- [Example product config](artifact/example/product-config.json)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with bash commands and JSON configuration examples; pipeline output is an MP4 file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces 1080x1920, 30 FPS H.264/AAC portrait video when required local media assets, ffmpeg, ffprobe, Pillow, and a TTF font are available.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
