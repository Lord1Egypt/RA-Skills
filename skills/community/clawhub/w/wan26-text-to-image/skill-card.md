## Description:

Generates WeChat public account cover images, technical architecture diagrams, and article illustrations with Alibaba Cloud Wan 2.6.

This skill is ready for commercial/non-commercial use.

## Publisher:

[love254443233](https://clawhub.ai/user/love254443233)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, editors, and technical writers use this skill to generate WeChat cover images, architecture diagrams, and article illustrations from titles, summaries, component lists, or paragraph content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles API keys and may load shared environment files that contain other secrets.

Mitigation: Pass only the DashScope API key through the environment or --api-key, and review shared ~/.openclaw/.env or ~/.workbuddy/.env files before installing.

Risk: Setup helpers collect and save an API key locally, which can expose secrets during shared terminal sessions.

Mitigation: Avoid running setup helpers while screen sharing and confirm repository-local .env files remain excluded from version control.

Risk: Image generation is billed per generated image.

Mitigation: Review requested image counts and sizes before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/love254443233/skills/wan26-text-to-image)
- [Alibaba Cloud Wan image generation API reference](https://help.aliyun.com/zh/model-studio/wan-image-generation-api-reference)
- [Alibaba Cloud Model Studio API key guide](https://help.aliyun.com/zh/model-studio/get-api-key)

## Skill Output:

**Output Type(s):** [Files, JSON, Shell commands, Configuration instructions]

**Output Format:** [PNG image files with optional JSON status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Downloads generated images to a local output directory; generated image URLs may expire after 24 hours.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter states 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
