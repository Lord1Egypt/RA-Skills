## Description: <br>
Provides Zhipu AI MCP and HTTP helpers for image and video understanding, OCR, UI screenshot analysis, web search, web reading, GitHub repository lookup, CogView image generation, and CogVideoX video generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangalexhy](https://clawhub.ai/user/zhangalexhy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to access Zhipu/BigModel visual analysis, search, repository reading, image generation, and video generation tools from an agent workflow. It is intended for users who have configured a Zhipu API key and understand that prompts, media, URLs, and repository queries may be sent to remote services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads a saved Zhipu API key and sends selected content to remote Zhipu/BigModel services through MCP and HTTP calls. <br>
Mitigation: Install only if you trust Zhipu/BigModel and the npm tooling invoked by npx, use a limited API key where possible, and avoid sending confidential screenshots, videos, URLs, prompts, or private repository data. <br>
Risk: Generated image and video examples may consume account quota and download remote files to local paths. <br>
Mitigation: Review prompts, account limits, and output paths before running examples or one-shot scripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangalexhy/zhipu-coding-plan-mcp) <br>
- [Zhipu BigModel homepage](https://open.bigmodel.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and API/MCP invocation patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include remote service responses, extracted text, generated code, search results, image URLs, video URLs, and downloaded media depending on the selected tool.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
