## Description: <br>
WorkRally CLI is an AIGC comic/video creation workflow skill for AI agents, covering image and video generation, project, series, shot, asset, media, canvas, upload, and download operations through the workrally command line. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tencent-adm](https://clawhub.ai/user/tencent-adm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and AI agents use this skill to operate WorkRally CLI workflows for AI-generated images, AI-generated videos, storyboard and shot management, media uploads, asset organization, and collaborative canvas updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents through sensitive WorkRally project, asset, credential, media, and canvas actions. <br>
Mitigation: Install only for trusted WorkRally workflows, use least-privilege API keys, and keep the WorkRally config file private. <br>
Risk: Delete, recycle-bin, upload, download, canvas overwrite, and canvas clear operations can change or expose user work. <br>
Mitigation: Require explicit user confirmation before destructive, permanent, sensitive media, or broad canvas update operations. <br>
Risk: AI generation and media operations may fail or produce incorrect results if agents guess model IDs, URLs, or object identifiers. <br>
Mitigation: Use the documented CLI discovery commands, official WorkRally media URLs, and JSON output before submitting generation or asset operations. <br>


## Reference(s): <br>
- [WorkRally ClawHub page](https://clawhub.ai/tencent-adm/skills/workrally) <br>
- [WorkRally homepage](https://workrally.qq.com) <br>
- [WorkRally API key configuration](https://workrally.qq.com/open-api) <br>
- [AI generation guide](references/ai-generation-guide.md) <br>
- [Canvas guide](references/canvas-guide.md) <br>
- [Common pitfalls](references/common-pitfalls.md) <br>
- [Shot guide](references/shot-guide.md) <br>
- [Upload and assets guide](references/upload-and-assets-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, JSON] <br>
**Output Format:** [Markdown guidance with inline CLI commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents to use the workrally CLI with JSON output for automation-friendly operations.] <br>

## Skill Version(s): <br>
2.4.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
