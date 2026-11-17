## Description:

Generates UGC-style fashion and activewear product videos for TikTok and Instagram Reels from a single outfit image, including talking-head and voiceover variants.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dai-shuo](https://clawhub.ai/user/dai-shuo)

### License/Terms of Use:

MIT-0

## Use Case:

External fashion, activewear, ecommerce, DTC, and social commerce teams use this skill to turn outfit images into short-form product video concepts and generation commands for TikTok, Instagram Reels, and related vertical video channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outfit images are uploaded to a third-party IMA Studio service during normal use.

Mitigation: Use only non-sensitive images that the user is comfortable sending to IMA Studio.

Risk: The skill requires the IMA_API_KEY credential.

Mitigation: Store IMA_API_KEY in a secret-safe environment variable and avoid placing it in prompts, logs, or source files.

Risk: Untrusted file paths, URLs, brand names, or prompt text could be unsafe if passed through shell interpolation.

Mitigation: Invoke the CLI with structured arguments or carefully quoted parameters rather than interpolating untrusted text into a shell command.

Risk: The package dependency is declared as a version range.

Mitigation: Prefer a pinned imastudio-cli dependency and lockfile before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dai-shuo/skills/ugc-fashion-activewear-product-video-generator)
- [IMA Studio](https://imastudio.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with media URLs, generated prompts, narration scripts, and CLI command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses IMA_API_KEY and imastudio-cli to upload images, create image-to-video tasks, and generate text-to-speech narration.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
