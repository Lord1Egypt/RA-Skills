## Description:

火山引擎AI生成与理解API。让Agent能够调用火山引擎方舟的AI能力：图片生成(Seedream-5.0-lite)、视频生成(Seedance-1.5-pro)、图片理解、视频理解。使用前需配置API密钥(VOLCENGINE_API_KEY)。支持异步任务查询。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zzhimin](https://clawhub.ai/user/zzhimin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call Volcengine Ark APIs for image generation, video generation, image understanding, video understanding, and asynchronous task status checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes a concrete API key and suggests storing it in plaintext shell startup files.

Mitigation: Replace the embedded value with a user-owned scoped Volcengine API key and store secrets through an approved secret manager or ephemeral environment variable.

Risk: Prompts, image URLs, video URLs, personal data, or regulated content may be sent to Volcengine services.

Mitigation: Use the skill only after confirming an approved Volcengine data-sharing arrangement and avoid submitting confidential or regulated content without authorization.

## Reference(s):

- [Volcengine AI skill page](https://clawhub.ai/zzhimin/skills/volcengine-ai)
- [Volcengine Ark API endpoint](https://ark.cn-beijing.volces.com/api/v3/chat/completions)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs guide authenticated API calls and asynchronous task polling; generated media or analysis is returned by the external Volcengine service.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
