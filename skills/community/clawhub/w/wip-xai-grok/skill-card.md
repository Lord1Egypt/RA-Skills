## Description: <br>
xAI Grok API. Search the web, search X, generate images, generate video. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parkertoddbrooks](https://clawhub.ai/user/parkertoddbrooks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to search current web and X content with xAI Grok and to generate or edit images and videos through CLI, module, or MCP tool interfaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Searches, prompts, image inputs, and video requests are sent to xAI. <br>
Mitigation: Use only with data approved for xAI processing, and avoid secrets, private media, or sensitive file paths in requests. <br>
Risk: The skill requires an xAI API key and can resolve it from either XAI_API_KEY or a 1Password lookup. <br>
Mitigation: Use a scoped or revocable key with spending limits, and set XAI_API_KEY directly if the 1Password lookup is not desired. <br>
Risk: Media generation and some API calls can incur usage costs, and generated media URLs may expire. <br>
Mitigation: Review generation parameters before execution, monitor spend, and download needed media promptly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/parkertoddbrooks/wip-xai-grok) <br>
- [Project homepage](https://github.com/wipcomputer/wip-xai-grok) <br>
- [xAI Web Search documentation](https://docs.x.ai/developers/tools/web-search) <br>
- [xAI X Search documentation](https://docs.x.ai/developers/tools/x-search) <br>
- [xAI Image Generation documentation](https://docs.x.ai/docs/guides/image-generations) <br>
- [xAI Video Generation documentation](https://docs.x.ai/docs/guides/video-generations) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files] <br>
**Output Format:** [MCP text responses, JSON objects, generated media URLs, and optional downloaded image or video files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires XAI_API_KEY; generated image and video URLs may be temporary.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata, SKILL.md frontmatter, package.json, CHANGELOG released 2026-03-16) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
