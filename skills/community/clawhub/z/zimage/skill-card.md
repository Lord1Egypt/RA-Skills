## Description:

zimage helps agents generate images through the Z-Image text-to-image API by validating prompts, mapping aspect ratios to supported sizes, controlling request count, and returning structured result summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runninghcm](https://clawhub.ai/user/runninghcm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate posters, cover images, illustrations, product images, and other text-to-image outputs with explicit prompt, size or aspect-ratio, and count controls. It is not intended for image editing, OCR, video generation, or audio workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper scripts can store an API key locally and later load the local environment file as shell code.

Mitigation: Prefer an environment variable or managed secret store; only use a local ~/.config/z-image/.env file that you created and inspected, and keep it permission-restricted.

Risk: Prompts are sent to an external API and may expose sensitive or confidential content.

Mitigation: Do not include sensitive, confidential, regulated, or proprietary data in image-generation prompts.

## Reference(s):

- [z-image API Guide](references/api-guide.md)
- [Z-Image API endpoint](https://agent.mathmind.cn/minimalist/api/tywx/zImage)
- [ClawHub skill page](https://clawhub.ai/runninghcm/skills/zimage)
- [ClawHub publisher profile](https://clawhub.ai/user/runninghcm)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, API calls]

**Output Format:** [Markdown or plain text summaries with shell commands and JSON API payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call an external image-generation API using prompt, size, and count; requires an x-api-key.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
