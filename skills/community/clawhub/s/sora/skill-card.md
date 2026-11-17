## Description:

Generate videos from text prompts or reference images using OpenAI Sora.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pauldelavallaz](https://clawhub.ai/user/pauldelavallaz)

### License/Terms of Use:


## Use Case:

Developers and creators use this skill to ask an agent to generate text-to-video or image-to-video MP4 assets with configurable model, duration, and resolution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and optional reference images are sent to OpenAI for video generation.

Mitigation: Use the skill only with content approved for transfer to OpenAI under the user's applicable data handling requirements.

Risk: Supplying an API key on the command line can expose credentials through shell history or process inspection.

Mitigation: Set OPENAI_API_KEY through the environment or a secret manager instead of passing --api-key when possible.

Risk: Dependencies are declared with lower bounds rather than locked versions.

Mitigation: Pin and review dependency versions before deploying the skill in sensitive or controlled environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pauldelavallaz/skills/sora)
- [OpenAI Videos API endpoint](https://api.openai.com/v1/videos)
- [OpenAI video content endpoint](https://api.openai.com/v1/videos/{video_id}/content)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with bash commands and generated MP4 video files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an OpenAI API key, Python 3.10 or later, and network access to OpenAI APIs.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
