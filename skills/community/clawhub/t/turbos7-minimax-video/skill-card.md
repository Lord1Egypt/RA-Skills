## Description:

Generates videos with MiniMax from text prompts, image prompts, or paired first and last frames, and can query generation status and download completed videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[turbos7](https://clawhub.ai/user/turbos7)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create short videos through MiniMax models from text, a starting image, or first and last frame images. It also supports checking task status and saving completed MP4 files locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script can upload any readable local path supplied as a first or last image to MiniMax without file validation or an explicit confirmation step.

Mitigation: Use only trusted, non-sensitive image paths, and add file type and size validation plus explicit upload confirmation before shared or sensitive workspace use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/turbos7/skills/turbos7-minimax-video)
- [MiniMax video generation endpoint](https://api.minimaxi.com/v1/video_generation)
- [MiniMax video generation status endpoint](https://api.minimaxi.com/v1/query/video_generation?task_id={task_id})
- [MiniMax file retrieval endpoint](https://api.minimaxi.com/v1/files/retrieve?file_id={file_id})

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with Python and shell examples; the script produces CLI text output and MP4 video files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MINIMAX_API_KEY or an explicit API key; generated videos are saved to the configured local directory.]

## Skill Version(s):

1.1.0 (source: evidence release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
