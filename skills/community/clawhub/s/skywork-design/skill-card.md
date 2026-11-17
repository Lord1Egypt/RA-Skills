## Description:

Skywork Design generates or edits images through the Skywork Image API for image creation, poster design, logo design, visual asset generation, and image modification requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gxcun17](https://clawhub.ai/user/gxcun17)

### License/Terms of Use:

MIT-0

## Use Case:

Designers, marketers, developers, and agents use this skill to generate or edit visual assets such as posters, logos, brand materials, social media images, storyboards, brochures, infographics, and e-commerce product images. It is useful when a workflow needs guided prompt construction, aspect ratio and resolution choices, or image-to-image edits using local reference images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid Skywork credentials could be exposed or misused if SKYWORK_API_KEY is stored or printed insecurely.

Mitigation: Store SKYWORK_API_KEY in a secret manager or tightly permissioned runtime configuration, avoid printing credential-bearing config, and rotate the key if it is exposed.

Risk: Sensitive prompts or private reference images may be processed by Skywork and returned through an externally hosted URL.

Mitigation: Review prompts and input images before use, avoid sending sensitive material unless approved for the Skywork service, and treat hosted result URLs as externally accessible artifacts.

## Reference(s):

- [Skywork Design ClawHub listing](https://clawhub.ai/gxcun17/skills/skywork-design)
- [Skywork publisher profile](https://clawhub.ai/user/gxcun17)
- [Skywork website](https://skywork.ai)
- [API key setup guide](references/apikey-fetch.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated image file paths or hosted image URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local image files and externally hosted OSS URLs after calling the Skywork API.]

## Skill Version(s):

1.0.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
