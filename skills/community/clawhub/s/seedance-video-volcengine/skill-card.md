## Description:

Generate AI videos with ByteDance Seedance (豆包/火山方舟) via Ark API, supporting text-to-video and image-to-video with the doubao-seedance-1-5-pro-251215 model endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maddy-cc](https://clawhub.ai/user/maddy-cc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to guide agents through creating Seedance video-generation tasks, polling Ark task status, and retrieving generated MP4 URLs from text or image prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, image URLs, request metadata, and task data are sent to Volcengine Ark.

Mitigation: Use the skill only for inputs approved for sharing with that external service, and avoid confidential, personal, internal-only, or non-public image inputs.

Risk: The skill requires an Ark API key for authenticated API calls.

Mitigation: Keep ARK_API_KEY in an environment variable and do not paste it into prompts or shared files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/maddy-cc/skills/seedance-video-volcengine)
- [Volcengine Ark Console](https://console.volcengine.com/ark)
- [Volcengine Video Generation API Documentation](https://www.volcengine.com/docs/82379/1520757)
- [Seedance Video Skill Issues](https://github.com/maddy-cc/seedance-video-skill/issues)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls]

**Output Format:** [Markdown with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ARK_API_KEY and sends prompts, image URLs, request metadata, and task data to Volcengine Ark.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
