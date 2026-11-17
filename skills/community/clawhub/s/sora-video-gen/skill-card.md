## Description:

Generate videos using OpenAI's Sora API from text prompts or reference images, with support for image-to-video generation and automatic image resizing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pauldelavallaz](https://clawhub.ai/user/pauldelavallaz)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to create Sora videos from prompts or reference images and save the generated result as an MP4 file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Video prompts and reference images are sent to OpenAI for processing.

Mitigation: Use only content that is appropriate to send to OpenAI and avoid sensitive prompts or images unless that use is approved.

Risk: API keys can be exposed when passed directly on the command line.

Mitigation: Prefer OPENAI_API_KEY from a protected environment or secret manager instead of the --api-key flag.

Risk: The script writes an MP4 file to the requested output path.

Mitigation: Choose output paths deliberately and review file locations and permissions before running the skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pauldelavallaz/skills/sora-video-gen)
- [OpenAI Videos API Endpoint](https://api.openai.com/v1/videos)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Files]

**Output Format:** [Markdown guidance with bash commands and generated MP4 files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated videos are saved to the requested output path; reference images may be resized before API submission.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
