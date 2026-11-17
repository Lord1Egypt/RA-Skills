## Description:

Create high-converting YouTube thumbnail concepts, overlay text, image prompts, and optional AI-generated cover images from raw titles, hooks, scripts, or marketing copy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luo-2q](https://clawhub.ai/user/luo-2q)

### License/Terms of Use:


## Use Case:

Creators, marketers, and agent users use this skill to turn video titles, hooks, scripts, or campaign copy into thumbnail angles, short overlay text, Nano Banana image prompts, and optional generated thumbnail assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Thumbnail copy and prompts may be sent to Google Gemini when the planning or image-generation scripts run.

Mitigation: Use only inputs approved for external processing and avoid sensitive unpublished material unless that data is allowed to leave the environment.

Risk: Gemini or Google API keys are required for live generation.

Mitigation: Keep API keys secret and provide them through environment variables rather than embedding them in prompts, files, or logs.

Risk: The workflow can write generated JSON, PNG, and metadata files locally.

Mitigation: Review output paths before execution and inspect generated artifacts before publishing or sharing them.

## Reference(s):

- [YouTube Thumbnail Patterns](artifact/references/youtube-thumbnail-patterns.md)
- [Publishing Contract](artifact/references/publishing-contract.md)
- [Google Generative Language API endpoint](https://generativelanguage.googleapis.com/v1beta/models/)
- [ClawHub skill page](https://clawhub.ai/luo-2q/skills/youtube-cover-nano-banana)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, files, guidance]

**Output Format:** [Markdown blocks with optional JSON result envelopes and PNG image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write a thumbnail plan JSON file, optional generated PNG, and image metadata JSON when Gemini credentials are configured.]

## Skill Version(s):

0.1.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
