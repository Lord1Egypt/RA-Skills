## Description: <br>
火山引擎AI生成与理解API。让Agent能够调用火山引擎方舟的AI能力：图片生成(Seedream-5.0-lite)、视频生成(Seedance-1.5-pro)、图片理解、视频理解。使用前需配置API密钥(VOLCENGINE_API_KEY)。支持异步任务查询。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zzhimin](https://clawhub.ai/user/zzhimin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to prepare Volcengine Ark API calls for image generation, video generation, image understanding, video understanding, and asynchronous task status checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact includes a real-looking Volcengine API-key-like value and shows shell startup-file persistence for credentials. <br>
Mitigation: Do not use the embedded value; create a fresh Volcengine key, store it securely, and avoid placing long-lived secrets in shared or backed-up shell startup files. <br>
Risk: Prompts, images, videos, and URLs may be transmitted to Volcengine Ark services when the generated API commands are used. <br>
Mitigation: Only send content that is approved for transmission to Volcengine and review data-handling requirements before use. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, API Calls, Guidance] <br>
**Output Format:** [Markdown with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided VOLCENGINE_API_KEY and may submit prompts, images, videos, or URLs to Volcengine Ark endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
