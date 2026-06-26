## Description: <br>
xAI Grok API. Search the web, search X, generate images, generate video. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parkertoddbrooks](https://clawhub.ai/user/parkertoddbrooks) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to access xAI Grok search, X search, image generation, image editing, and video generation through CLI, module, MCP, or skill interfaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent-exposed image editing can read local image paths without a containment or consent boundary. <br>
Mitigation: Review before installation, restrict MCP tool access, and do not allow untrusted prompts to choose local image paths or output paths. <br>
Risk: Prompts, private media, and generated requests are sent to the xAI API and may incur paid usage. <br>
Mitigation: Use a dedicated xAI API key with spending limits and avoid confidential prompts or private media. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/parkertoddbrooks/wip-grok) <br>
- [xAI API base](https://api.x.ai/v1) <br>
- [xAI Web Search documentation](https://docs.x.ai/developers/tools/web-search) <br>
- [xAI X Search documentation](https://docs.x.ai/developers/tools/x-search) <br>
- [xAI Image Generation documentation](https://docs.x.ai/docs/guides/image-generations) <br>
- [xAI Video Generation documentation](https://docs.x.ai/docs/guides/video-generations) <br>
- [ClawHub attribution source](https://clawhub.ai/castanley/grok) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown or JSON responses, with optional downloaded image or video files from CLI workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search outputs may include citations and raw response metadata; generated media URLs are temporary and should be downloaded promptly.] <br>

## Skill Version(s): <br>
1.0.2 (source: SKILL.md frontmatter, package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
