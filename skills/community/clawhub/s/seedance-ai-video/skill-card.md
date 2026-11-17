## Description:

This skill helps an agent generate and download short AI videos through Atlas Cloud using ByteDance Seedance text-to-video and image-to-video models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xixihhhh](https://clawhub.ai/user/xixihhhh)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and content teams can use this skill to turn prompts or image URLs into short generated video clips and save the returned MP4 files. It is suited for drafts, social media reels, product demos, and cinematic clips where Atlas Cloud API use is acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an Atlas Cloud API key and sends prompts, image URLs, and potentially uploaded local media to Atlas Cloud.

Mitigation: Use the skill only with data that may be shared with Atlas Cloud, store the API key in ATLASCLOUD_API_KEY, and avoid submitting sensitive prompts or media.

Risk: The bundled script supports broader Atlas Cloud video generation and upload behavior than the Seedance-focused description highlights.

Mitigation: Review commands before execution, confirm model IDs and upload actions, and be cautious with upload --yes because it skips confirmation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xixihhhh/skills/seedance-ai-video)
- [Atlas Cloud](https://www.atlascloud.ai)
- [Atlas Cloud video generation API endpoint](https://api.atlascloud.ai/api/v1/model/generateVideo)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and Python script usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated media is retrieved from Atlas Cloud and saved as MP4 files when the bundled script is run.]

## Skill Version(s):

1.1.2 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
