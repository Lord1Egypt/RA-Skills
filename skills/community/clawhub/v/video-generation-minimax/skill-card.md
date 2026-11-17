## Description:

Creates videos with the MiniMax video generation API from text prompts, image prompts, start and end frames, or subject reference images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xbos1314](https://clawhub.ai/user/xbos1314)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to invoke MiniMax video generation workflows from an agent workspace and save generated video files locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, image URLs, and face-reference images are sent to MiniMax for video generation.

Mitigation: Use only content that may be shared with MiniMax, avoid sensitive personal images unless consent is clear, and review MiniMax handling requirements before use.

Risk: The script accepts an output path and writes downloaded video content to disk.

Mitigation: Run the skill in a constrained workspace and use a dedicated output directory until output path validation and overwrite protection are enforced.

## Reference(s):

- [MiniMax API documentation](https://platform.minimaxi.com/docs/llms.txt)
- [ClawHub skill page](https://clawhub.ai/xbos1314/skills/video-generation-minimax)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with bash commands and generated video files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, the requests package, and MINIMAX_API_KEY; generated videos are downloaded as MP4 files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
