## Description:

Use PoYo AI Veo 3.1 for frame-conditioned video generation through the `https://api.poyo.ai/api/generate/submit` endpoint, including fast and quality modes, start-frame and end-frame guidance, up to 4K resolution, and reference-image video generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative automation users use this skill to prepare PoYo Veo 3.1 video-generation payloads, submit jobs with a PoYo API key, and track returned task IDs for polling or webhook follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, referenced image URLs, callback URLs, and related parameters are sent to PoYo for generation.

Mitigation: Submit only content appropriate for PoYo processing, and avoid private media, secrets, or sensitive information in prompts and URLs.

Risk: The PoYo API key can be exposed through command-line arguments, shell history, or process logs.

Mitigation: Set POYO_API_KEY in the environment where possible, avoid passing keys directly on the command line, and rotate the key if exposure is suspected.

## Reference(s):

- [PoYo VEO 3 1 API Reference](references/api.md)
- [PoYo Veo 3.1 model page](https://poyo.ai/models/veo-3-1)
- [PoYo Veo 3.1 API documentation](https://docs.poyo.ai/api-manual/video-series/veo-3-1)
- [PoYo Veo 3.1 OpenAPI JSON](https://docs.poyo.ai/api-manual/video-series/veo-3-1.json)
- [PoYo task status documentation](https://docs.poyo.ai/api-manual/task-management/status)
- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/veo-3-1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON payloads and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include selected model ID, request parameters, reference-image usage, returned task ID, and the next polling or webhook step.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
