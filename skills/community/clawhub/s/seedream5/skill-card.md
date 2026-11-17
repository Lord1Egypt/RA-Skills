## Description:

Uses Volcengine Doubao Seedream 5.0 to generate or edit images from text prompts, reference images, grouped image generation, and optional web search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zealman2025](https://clawhub.ai/user/zealman2025)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to generate or edit images through Volcengine Seedream 5.0 from prompts, local or URL reference images, and optional web-search-enabled requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, reference images, and image URLs are sent to Volcengine for generation or editing.

Mitigation: Avoid sensitive or private content unless the target environment and Volcengine terms are appropriate for that data.

Risk: API keys can be exposed if passed directly on the command line.

Mitigation: Use the OpenClaw credential UI, openclaw.json, or protected environment variables for VOLC_API_KEY or ARK_API_KEY.

Risk: The requested output filename can overwrite an existing writable file.

Mitigation: Choose output filenames inside a safe working folder and use unique names such as timestamped filenames.

## Reference(s):

- [Volcengine Seedream API documentation](https://www.volcengine.com/docs/82379/1541523)
- [Volcengine image generation API endpoint](https://ark.cn-beijing.volces.com/api/v3/images/generations)
- [uv documentation](https://docs.astral.sh/uv/)
- [ClawHub Seedream5 skill page](https://clawhub.ai/zealman2025/skills/seedream5)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Code, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands and generated image file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv and a Volcengine API key; generated images are saved locally and reported with MEDIA paths.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
