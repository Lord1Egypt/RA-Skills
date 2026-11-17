## Description:

Generates short vertical product videos from source images using Runway Gen4 Turbo for ads, UGC-style demos, Reels, and YouTube Shorts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zero2ai-hub](https://clawhub.ai/user/zero2ai-hub)

### License/Terms of Use:

MIT

## Use Case:

Developers and content teams use this skill to turn a product image and motion prompt into a short MP4 suitable for TikTok ads, UGC-style product demos, Reels, and YouTube Shorts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The selected image and prompt are sent to Runway, and generated output can incur charges.

Mitigation: Use only images and prompts approved for Runway processing, confirm account billing expectations, and choose duration intentionally before running the command.

Risk: The skill can read credentials from RUNWAY_API_KEY or ~/tiktok-api.json.

Mitigation: Prefer RUNWAY_API_KEY or a dedicated config file, and avoid storing unrelated secrets in ~/tiktok-api.json.

Risk: The script depends on unpinned Python package installation through uv.

Mitigation: Pin dependencies before routine or commercial use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zero2ai-hub/skills/skill-runway-video-gen)
- [Runway image-to-video API endpoint](https://api.dev.runwayml.com/v1/image_to_video)
- [Runway task polling API endpoint](https://api.dev.runwayml.com/v1/tasks/{task_id})

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with bash command examples and a generated local MP4 file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv, Python 3.10 or later, a Runway API key, a source image path, an output MP4 path, and optional prompt, duration, and aspect-ratio arguments.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, artifact/_meta.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
